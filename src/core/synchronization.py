import httpx
from utils.config import settings

class CloudServiceClient:
    def __init__(self): #base_url: str = None, cert: tuple = None, verify: str = None):
        self.auth_url = settings.AUTH_URL
        self.cc_url = settings.CATALOGUE_URL
        self.cert = settings.APP_CERTIFICATE_PATH
        self.verify = True
        self.realm = settings.AUTH_REALM
        self.access_token = None
        self.payload = {
                "grant_type": "client_credentials",
                "client_id": settings.CLIENT_ID
            }

# Calls keycloak to get token (mTLS)
    async def get_token(self) -> dict:
        async with httpx.AsyncClient(cert=self.cert, verify=self.verify) as client:
            response = await client.post(f"{self.auth_url}/realms/{self.realm}/protocol/openid-connect/token", data=self.payload)
            response.raise_for_status()
            return response.json()

# Calls collab manager to login and publish node DCAT description (Send token with BEARER header)
    async def handshake(self) -> dict:
        async with httpx.AsyncClient(verify=self.verify) as client:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            response = await client.get(f"{self.cc_url}/api/node/handshake", headers=headers)
            response.raise_for_status()
            return response.json()

    @staticmethod
    def login():
        settings.APP_ONLINE = True
        return

    @staticmethod
    def logout():
        settings.APP_ONLINE = False
        return
    
    @staticmethod
    def is_online() -> bool:
        return settings.APP_ONLINE