import sys
from lib.gcp.auth.gcp_auth import authenticate_implicit_with_adc
from lib.gcp.gcp_upload import upload_blob
from lib.extract_metadata import extract_metadata

def auth_and_init():
    try:
        authenticate_implicit_with_adc(project_id=os.getenv("GCP_PROJECT_ID"))
    except Exception as e:
        print("Error authenticating:", e)
        sys.exit(1)
    
if __name__ == "__main__":
    auth_and_init()   
    
        

        




    