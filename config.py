from requests import post


response = post(
    'https://www.olx.uz/api/open/oauth/token/',
    json={
        "device_id": "c8d47d63-79e7-4c0d-9437-5cc074fbcea6",
        "device_token": "eyJpZCI6ImM4ZDQ3ZDYzLTc5ZTctNGMwZC05NDM3LTVjYzA3NGZiY2VhNiJ9.4b76cf6994d7f9d7a82f617223945c11f6045c54",
        "grant_type": "device",
        "client_id": "100309",
        "client_secret": "QVnzW1SoFUt0JoNJmiBvMsKWkFvG9NUKZCdrjegVlZYCc8FR"
    }
)


TOKEN = response.json()['access_token']
