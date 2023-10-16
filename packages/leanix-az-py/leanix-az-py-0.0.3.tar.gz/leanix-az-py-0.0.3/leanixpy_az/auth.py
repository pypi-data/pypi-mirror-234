import requests


#authorization with the base url and the api token. returns the bearer token
def getBearerToken(base_url, api_token):
    access_token = None
    api_token = api_token
    auth_url = base_url+'/services/mtm/v1/oauth2/token'

    try:
        response = requests.post(auth_url, auth=('apitoken', api_token),
                             data={'grant_type': 'client_credentials'})
        response.raise_for_status()
        access_token = response.json()['access_token']
        auth_header = 'Bearer ' + access_token
        header = {'Authorization': auth_header}
        return header
    except Exception as ex:
        raise
