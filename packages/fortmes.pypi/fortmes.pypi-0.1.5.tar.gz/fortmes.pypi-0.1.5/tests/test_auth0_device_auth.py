import unittest
import asyncio
from unittest.mock import patch
from your_package.auth0_device_auth import Auth0DeviceAuth

class TestAuth0DeviceAuth(unittest.TestCase):
    @patch('your_package.auth0_device_auth.httpx.AsyncClient')
    @patch('your_package.auth0_device_auth.asyncio.sleep')
    async def test_authenticate(self, mock_sleep, mock_async_client):
        # Mock responses from the Auth0 server
        mock_device_response = {
            'device_code': 'test_device_code',
            'verification_uri_complete': 'https://auth0.com/verify',
        }
        mock_token_response = {
            'access_token': 'test_access_token',
            'token_type': 'Bearer',
        }

        # Create an instance of Auth0DeviceAuth
        auth = Auth0DeviceAuth('test_client_id', 'test_auth0_domain')

        # Mock async client's post method
        async def mock_post(url, data):
            if 'device/code' in url:
                return mock_device_response
            elif 'oauth/token' in url:
                return mock_token_response

        mock_async_client.return_value.post.side_effect = mock_post

        # Mock asyncio.sleep to avoid waiting in tests
        mock_sleep.side_effect = None

        # Perform the authentication
        tokens = await auth.authenticate()

        # Assertions
        self.assertEqual(tokens['access_token'], 'test_access_token')
        mock_async_client.return_value.post.assert_called_with(
            'https://test_auth0_domain/oauth/device/code',
            data={'client_id': 'test_client_id', 'scope': 'openid profile email'}
        )

if __name__ == '__main__':
    unittest.main()
