"""
OAuth2-based client for more advanced applications.

Single-user CLI
---------------

This method is suitable for testing or where indefinite authentication is
required, for example a long-running service.
In general, regular single-user applications should instead take the user's
personal API key and use the simple client.

.. code:: python

    # Initialise client with basic defaults
    from srf_client import *
    srf = SRFDataOAuth(client_id='...', client_secret='...')

    # Start a browser login session
    import webbrowser
    webbrowser.open_new_tab(srf.start_login())

    # Receive auth code
    code = input('Enter authorization code: ')
    srf.login_with_code(code)

    # Test connection
    srf.ping()

Multi-user webapp
-----------------

Each user must use their own separate authenticated session.
This can be achieved with multiple client instances, or by switching the token
of a single instance before each request.

This is a basic flask example. A robust app will need more state and error
handling.

.. code:: python

    from flask import Flask, jsonify, redirect, request, session
    from srf_client.oauth import *

    app = Flask(__name__)
    srf_config = {'client_id': '...',
                  'client_secret': '...',
                  'redirect_uri': 'https://example.com/oauth_callback'}

    def save_oauth_token(token):
        session['oauth_token'] = token

    def get_client():
        srf_client = SRFDataOAuth(save_token=save_oauth_token, **srf_config)
        if 'oauth_token' in session:
            srf_client.login_with_token(session['oauth_token'])
        return srf_client

    @app.route('/login')
    def login():
        return redirect(get_client().start_login())

    @app.route('/oauth_callback')
    def callback():
        get_client().login_with_callback(request.url)
        return redirect('/')

    @app.route('/logout')
    def logout():
        get_client().logout()
        session.pop('oauth_token')
        return redirect('/')

    @app.route('/')
    def index():
        return jsonify(get_client().ping())

Client-only access
------------------
.. versionadded:: 1.1

Some APIs provide access to shared data and do not require user authorization.
If your app only uses these then configure a single scope of :code:`CLIENT`.
Saving the token is not necessary, as a new one will be fetched whenever
needed.

.. code:: python

    from srf_client import *

    srf = SRFDataOAuth(client_id='...', client_secret='...', scope=('CLIENT',))
    srf.login_with_client()
    srf.ping()

"""

from oauthlib.oauth2 import BackendApplicationClient, OAuth2Error, \
    WebApplicationClient
from requests import RequestException
from requests_oauthlib import OAuth2Session
from typing import Callable, Mapping, Sequence
from urllib.parse import urljoin

from .client import SRFData

__all__ = ['SRFDataOAuth']


def make_urls(server_root):
    """
    Build keyword arguments for a non-standard server root.

    Useful for testing:

    .. code:: python

        srf = SRFDataOAuth(client_id='TEST', client_secret='TEST',
                           **make_urls('https://localhost:8443')

    """
    return {'root': urljoin(server_root, 'api'),
            'redirect_uri': urljoin(server_root, 'oauth/callback'),
            'auth_endpoint': urljoin(server_root, 'oauth/authorize'),
            'token_endpoint': urljoin(server_root, 'oauth/token'),
            'revoke_endpoint': urljoin(server_root, 'oauth/revoke')}


class SRFDataOAuth(SRFData):
    """SRF Data client. Provides OAuth2-based access to the REST API."""

    def __init__(self, client_id: str, client_secret: str,
                 scope: Sequence[str] = ('USER',),
                 redirect_uri='https://data.csrf.ac.uk/oauth/callback',
                 save_token: Callable[[Mapping], None] = None,
                 auth_endpoint='https://data.csrf.ac.uk/oauth/authorize',
                 token_endpoint='https://data.csrf.ac.uk/oauth/token',
                 revoke_endpoint='https://data.csrf.ac.uk/oauth/revoke',
                 **kwargs):
        """
        Initialise a new instance.

        :param client_id: Registered client ID
        :param client_secret: Registered client secret
        :param scope: (optional) Request additional authorisation
        :param redirect_uri: (optional) Callback URL to receive auth result
        :param save_token: (optional) Callback function to save token state
            e.g. in a web session
        :param root: (optional) API root URL
        :param auth_endpoint: (optional) Override OAuth URL
        :param token_endpoint: (optional) Override OAuth URL
        :param revoke_endpoint: (optional) Override OAuth URL
        """
        super().__init__(client_id=client_id,
                         scope=scope,
                         redirect_uri=redirect_uri,
                         token_endpoint=token_endpoint,
                         **kwargs)
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = tuple(scope)
        self._redirect_uri = redirect_uri
        self._auth_endpoint = auth_endpoint
        self._token_endpoint = token_endpoint
        self._revoke_endpoint = revoke_endpoint
        self._save_token = save_token

    def _make_session(self, **kwargs):
        # the client class determines the grant_type
        if tuple(kwargs['scope']) == ('CLIENT',):
            # client_credentials
            client = BackendApplicationClient(kwargs['client_id'],
                                              scope=kwargs['scope'])
        else:
            # authorization_code
            client = WebApplicationClient(kwargs['client_id'],
                                          scope=kwargs['scope'],
                                          redirect_url=kwargs['redirect_uri'])

        session = OAuth2Session(
            client=client,
            scope=kwargs['scope'],
            redirect_uri=kwargs['redirect_uri'],
            auto_refresh_url=kwargs['token_endpoint'],
            token_updater=self._update_token
        )
        session.request = self._wrap_request(session.request)
        session.refresh_token = self._wrap_refresh(session.refresh_token)
        self._session = session

    def _update_token(self, token):
        self._session.token = token
        if self._save_token is not None:
            self._save_token(token)

    def _wrap_request(self, func):
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                if response.status_code == 401:
                    self._clear_token()
                return response
            except OAuth2Error as exc:
                self._clear_token()
                raise RequestException(exc.error) from exc
        return wrapper

    def _wrap_refresh(self, func):
        # https://github.com/requests/requests-oauthlib/issues/264
        def wrapper(*args, **kwargs):
            if self._scope == ('CLIENT',):
                self.login_with_client()
                return self._session.token
            else:
                kwargs['auth'] = (self._client_id, self._client_secret)
                kwargs.pop('allow_redirects', None)
                return func(*args, **kwargs)
        return wrapper

    def _clear_token(self):
        self._session.token = {}
        self._session.access_token = None

    @property
    def logged_in(self) -> bool:
        """
        Whether the client is currently authenticated.

        Does not make a remote call to check for e.g. expiration.
        Use ``ping()`` for an active check.
        """
        return self._session.authorized

    def start_login(self) -> str:
        """
        Begin an interactive login session.

        Complete with either ``login_with_callback`` or ``login_with_code``.

        :return: The URL that the user should visit.
        """
        return self._session.authorization_url(self._auth_endpoint)[0]

    def login_with_callback(self, response_callback: str) -> None:
        """
        Complete a login session using a received callback URL.

        :param response_callback: Full callback URL
        """
        self._session.fetch_token(
            token_url=self._token_endpoint,
            client_secret=self._client_secret,
            authorization_response=response_callback
        )
        if self._save_token is not None:
            self._save_token(self._session.token)

    def login_with_code(self, authorization_code: str) -> None:
        """
        Complete a login session using a hand-entered code.

        :param authorization_code: User's auth code
        """
        self._session.fetch_token(
            token_url=self._token_endpoint,
            client_secret=self._client_secret,
            code=authorization_code
        )
        if self._save_token is not None:
            self._save_token(self._session.token)

    def login_with_client(self) -> None:
        """
        Login as a non-user client.

        .. versionadded:: 1.1

        """
        self._session.fetch_token(
            token_url=self._token_endpoint,
            client_secret=self._client_secret
        )
        if self._save_token is not None:
            self._save_token(self._session.token)

    def login_with_token(self, token: Mapping) -> None:
        """
        Restore auth state from a saved token.

        :param token: object previously received via ``save_token``
        """
        self._session.token = token

    def logout(self) -> None:
        """
        Invalidate the current auth state.

        Saved tokens will not be reusable.
        """
        token = self._session.token
        if token:
            oauth_client = self._session._client  # noqa
            url, headers, body = oauth_client.prepare_token_revocation_request(
                self._revoke_endpoint,
                token.get('refresh_token', token.get('access_token')),
                token_type_hint=None)
            self._session.post(url, headers=headers, data=body,
                               auth=(self._client_id, self._client_secret))
        self._clear_token()
