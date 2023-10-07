Module oqtant.util.auth
=======================

Functions
---------


`generate_challenge(verifier: str) ‑> str`
:


`generate_random(length: int) ‑> str`
:


`get_authentication_url(auth_server_port: int)`
:


`get_token(verifier: str, code: str, auth_server_port: int)`
:


`get_user_token(auth_server_port: int = 8080) ‑> str`
:   A utility function required for getting Oqtant authenticated with your Oqtant account.
       Starts up a server to handle the Auth0 authentication process and acquire a token.
    Args:
        auth_server_port (int): optional port to run the authentication server on
    Returns:
        str: Auth0 user token


`login(request: starlette.requests.Request)`
:


`main(request: starlette.requests.Request, code)`
:
