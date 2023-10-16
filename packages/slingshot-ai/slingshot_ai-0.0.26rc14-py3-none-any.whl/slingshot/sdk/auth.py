import time

import requests
import typer

from slingshot.cli.shared.settings import settings
from slingshot.sdk.errors import SlingshotException
from slingshot.sdk.utils import console

GRANT_TYPE = 'urn:ietf:params:oauth:grant-type:device_code'


def login_auth0(auth0_domain: str, auth0_cli_client_id: str) -> str:
    """
    Triggers the login flow for Auth0.
    Returns the ID token from Auth0 if successful.
    Otherwise, raises typer.Exit(code=1) and prints the error.
    """
    # TODO: Move this
    device_code_payload = {'client_id': auth0_cli_client_id, 'scope': 'openid email profile'}
    device_code_response = requests.post(
        f'https://{auth0_domain}/oauth/device/code', data=device_code_payload, timeout=30
    )
    if device_code_response.status_code != 200:
        raise SlingshotException('Error logging in, please try again')

    device_code_data = device_code_response.json()
    console.print(f"Verification code: {device_code_data['user_code']}")

    verification_url = device_code_data['verification_uri_complete']
    console.print(f'On your computer or mobile device navigate to: {verification_url}')
    typer.launch(verification_url)

    token_payload = {
        'grant_type': GRANT_TYPE,
        'device_code': device_code_data['device_code'],
        'client_id': auth0_cli_client_id,
    }

    elapsed_sec = 0
    while elapsed_sec < settings.auth0_timeout_sec:
        # TODO: Use a Slingshot URL that redirects to Auth0
        token_response = requests.post(f'https://{auth0_domain}/oauth/token', data=token_payload, timeout=30)
        token_data = token_response.json()

        if token_response.status_code == 200:
            console.print('Successfully authenticated with browser', style='green')
            return token_data['id_token']
        elif token_data['error'] not in ('authorization_pending', 'slow_down'):
            console.print(f"Error authenticating: {token_data['error_description']}", style='red')
            raise typer.Exit(code=1)

        time.sleep(device_code_data['interval'])
        elapsed_sec += device_code_data['interval']

    console.print('Timed out waiting for authentication', style='red')
    raise typer.Exit(code=1)
