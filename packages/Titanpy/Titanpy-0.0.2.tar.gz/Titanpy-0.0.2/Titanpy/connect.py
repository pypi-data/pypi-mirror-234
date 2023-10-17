def load_credentials(cred_path):

    import requests
    from json import load

    # opens and stores json in creds_data variable
    try:
        creds_json = open(cred_path)
        creds_data = load(creds_json)
        creds_json.close()
    except Exception as e:
        print("There was an error with the requested credential path.")
        print(e)

    # set up variables
    auth_url = 'https://auth.servicetitan.io/connect/token'
    form = {
        "grant_type": "client_credentials",
        "client_id": creds_data["CLIENT_ID"],
        "client_secret": creds_data["CLIENT_SECRET"]
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    # make request to return access_token
    try:
        request = requests.post(auth_url,data=form, headers=headers)
        if request.status_code == 200:
            creds_data["ACCESS_TOKEN"] = request.json()["access_token"]
            print(f"Access token successfully retrieved for Tenant {creds_data['TENANT_ID']}")
            return creds_data
        else:
            print(f"There was an error when requesting access token. Status returned: {request.status_code}")
    except Exception as e:
        print("There was an unknown error when requesting access token.")
        print(e)
