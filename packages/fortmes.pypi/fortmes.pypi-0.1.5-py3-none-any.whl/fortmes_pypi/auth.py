import aiohttp
import asyncio

class Auth0Client:
    def __init__(self, auth0_domain, client_id):
        self.auth0_domain = auth0_domain
        self.client_id = client_id

    async def device_authorization(self):
        # Step 1: Request device code and user code
        device_authorization_url = f'https://{self.auth0_domain}/oauth/device/code'
        data = {
            'client_id': self.client_id,
            'scope': 'openid profile',  # Define required scopes
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(device_authorization_url, json=data) as response:
                response_data = await response.json()

        device_code = response_data['device_code']
        user_code = response_data['user_code']
        verification_uri = response_data['verification_uri']

        print(f"Please visit {verification_uri} and enter code: {user_code} to authenticate.")

        # Step 2: Poll for user authentication
        authorization_endpoint = f'https://{self.auth0_domain}/authorize'
        data = {
            'client_id': self.client_id,
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        }

        while True:
            async with aiohttp.ClientSession() as session:
                async with session.post(authorization_endpoint, json=data) as response:
                    if response.status == 200:
                        auth_response = await response.json()
                        return auth_response['access_token']
                    elif response.status == 400:
                        error_data = await response.json()
                        if error_data['error'] == 'authorization_pending':
                            await asyncio.sleep(5)  # Wait and retry
                        else:
                            raise Exception(f"Authorization error: {error_data['error_description']}")
                    else:
                        raise Exception(f"Unexpected response: {response.status} - {await response.text()}")
