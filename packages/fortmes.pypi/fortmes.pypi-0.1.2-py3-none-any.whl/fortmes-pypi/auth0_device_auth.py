import httpx
import asyncio

class Auth0DeviceAuth:
    def __init__(self, client_id, auth0_domain):
        self.client_id = client_id
        self.auth0_domain = auth0_domain

    async def initiate_device_flow(self):
        async with httpx.AsyncClient() as client:
            data = {
                'client_id': self.client_id,
                'scope': 'openid profile email',  # Adjust the scopes as needed
            }
            response = await client.post(f'https://{self.auth0_domain}/oauth/device/code', data=data)

            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                raise Exception('Failed to initiate device flow')

    async def poll_for_tokens(self, device_code):
        async with httpx.AsyncClient() as client:
            while True:
                await asyncio.sleep(5)  # Poll every 5 seconds (you can adjust this)
                data = {
                    'client_id': self.client_id,
                    'device_code': device_code,
                    'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                }
                response = await client.post(f'https://{self.auth0_domain}/oauth/token', data=data)

                if response.status_code == 200:
                    response_data = response.json()
                    return response_data
                elif response.status_code == 400 and response.json().get('error') == 'authorization_pending':
                    continue
                else:
                    raise Exception('Failed to get tokens')

    async def authenticate(self):
        device_flow_data = await self.initiate_device_flow()
        device_code = device_flow_data['device_code']

        print(f"Open the following URL in your browser: {device_flow_data['verification_uri_complete']}")
        print("Then enter the code displayed on your device.")

        tokens = await self.poll_for_tokens(device_code)
        return tokens
