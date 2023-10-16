import requests
import json
import base64


#for running a graphql query with the auth header
#json_data has to be given with json.dumps(data)
def runGraphql(headerdict, json_data):
    header = headerdict["Authorization"]
    encoded_payload = header.split(".")[1]

    # fix missing padding for this base64 encoded string.
    # If number of bytes is not dividable by 4, append '=' until it is.
    missing_padding = len(encoded_payload) % 4
    if missing_padding != 0:
        encoded_payload += '='* (4 - missing_padding)
    payload = json.loads(base64.b64decode(encoded_payload))
    base_url = payload["instanceUrl"]


    request_url = base_url+'/services/pathfinder/v1/graphql'
    try:
        response = requests.post(url=request_url, headers=header, data=json_data)
        response.raise_for_status()
    except Exception as ex:
        raise
    return response
