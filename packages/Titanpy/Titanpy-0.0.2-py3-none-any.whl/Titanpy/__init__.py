# visit my page! happy to help: https://github.com/pabboat 
# I recommend using "from titanpy import Titanpy as tp"

# imports


# Titan Class Doc
class Titanpy:

    # Variable Initialization
    def __init__(self, credentials=None, client_id=None, client_secret=None, app_id=None, app_key=None, tenant_id=None, access_token=None):
        
        # credential variables
        self.credentials = credentials
        self.client_id = client_id
        self.client_secret = client_secret
        self.app_id = app_id
        self.app_key = app_key
        self.tenant_id = tenant_id
        self.access_token = access_token

    # Connect method takes credentials and creates a connection token in order to request from other API sources
    def Connect(self, cred_path):

        from connect import load_credentials

        credentials = load_credentials(cred_path)

        self.client_id = credentials["CLIENT_ID"]
        self.client_secret = credentials["CLIENT_SECRET"]
        self.app_id = credentials["APP_ID"]
        self.app_key = credentials["APP_KEY"]
        self.tenant_id = credentials["TENANT_ID"]
        self.timezone = credentials["TIMEZONE"]
        self.access_token = credentials["ACCESS_TOKEN"]
        self.credentials = credentials

    # Returns data from a source.
    # Use Connect() before using API methods.
    def Get(self, endpoint=None, query = None, id=None, category=None, url=None, *args, **kwargs):

        if self.access_token == None:
            print("No proper connection. Please ensure Connect method has been run successfully.")
        elif endpoint !=None:
            from get import get
            print(f"Endpoint received. Requesting for endpoint ({endpoint})")
            return get(credentials = self.credentials, endpoint = endpoint, query = query, id=id, category=category)
        elif url !=None:
            from get import get_request
            print(f"Url received. Requesting from url ({url}).")
            return get_request(credentials = self.credentials, query=query, url=url)
        else:
            print("No endpoint or url has been entered. Please enter an endpoint or a url.")

    def Post(self):

        if self.access_token == None:
            print("No proper connection. Please ensure Connect method has been run successfully.")

        else:
            print("This method has not been coded yet. See https://github.com/pabboat/Titanpy for more information.")

    def Del(self):

        if self.access_token == None:
            print("No proper connection. Please ensure Connect method has been run successfully.")

        else:
            print("This method has not been coded yet. See https://github.com/pabboat/Titanpy for more information.")

    def Put(self):

        if self.access_token == None:
            print("No proper connection. Please ensure Connect method has been run successfully.")

        else:
            print("This method has not been coded yet. See https://github.com/pabboat/Titanpy for more information.")

    def Patch(self):

        if self.access_token == None:
            print("No proper connection. Please ensure Connect method has been run successfully.")

        else:
            print("This method has not been coded yet. See https://github.com/pabboat/Titanpy for more information.")


if __name__ == "__main__":
    b = Titanpy()

    b.Connect(cred_path="./credentials/servicetitan_credentials.json")

    print(b.Get(endpoint = 'forms'))
