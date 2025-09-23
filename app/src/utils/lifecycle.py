import asyncio
from .config import settings
from core.synchronization import CloudServiceClient
from core.trust import parse_certificate

async def initialize():
    print("##############################################")
    print("""
    ▄▖▄▖▄▖▄▖▖▖▖         ▖ ▖   ▌  
    ▌ ▐ ▙▘▌ ▌▌▌ █▌▛▘▛▘  ▛▖▌▛▌▛▌█▌
    ▙▖▟▖▌▌▙▖▙▌▙▖▙▖▄▌▄▌  ▌▝▌▙▌▙▌▙▖                        
    """)
    print("Welcome to CIRCULess node app")
    print(f"Running on version {settings.APP_VERSION} ... ")
    if not settings.APP_CERTIFICATE_PATH:
        settings.APP_ENV = "DEV"
        settings.APP_MODE = "PRIVATE"
        print(f"Running in {settings.APP_ENV} environment")
    else:
        try:
            # Load certificate & set client_id
            settings.APP_CERTIFICATE = await parse_pem_cert_file_async(settings.APP_CERTIFICATE_PATH)
            settings.CLIENT_ID = settings.APP_CERTIFICATE["subject"]["CN"]
            # Sync with the cloud (After client_id is initialized)
            client = CloudServiceClient()
            kc_response = await client.get_token()    
            client.access_token = kc_response["access_token"]
            cc_response = await client.handshake()
            organization = cc_response["claims"]["organization"]
            CloudServiceClient.login()
            print(f"Running in {settings.APP_ENV} environment")
            print(f"Node with client id: {settings.CLIENT_ID}")
            print(f"Node is managed by {list(organization.keys())}")
        except:
            settings.APP_ENV = "DEV"
            settings.APP_MODE = "PRIVATE"
            print(f"Running in {settings.APP_ENV} environment")
            print(f"Node with client id: UNKNOWN")
    print(f"Node runs {settings.APP_MODE} mode")
    print("Initialization ended")
    print("##############################################")
    return
    
def shutdown():
    return

async def parse_pem_cert_file_async(cert_file_path: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, parse_certificate, cert_file_path)


