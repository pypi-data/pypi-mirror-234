import requests

def upload_file(file_name, signed_url):
    with open(file_name, 'rb') as f:
        # to add progress here
        requests.post(signed_url['url'], data=signed_url['fields'], files=f)

