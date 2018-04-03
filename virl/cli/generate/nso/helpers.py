import os
import requests
import six
import getpass


def update_devices(xml_payload):
    try:
        input = raw_input
    except NameError:
        pass

    nso_host = os.getenv('NSO_HOST', input('Enter NSO IP/Hostname: '))
    nso_username = os.getenv('NSO_USERNAME', input('Enter NSO username: '))
    nso_password = os.getenv('NSO_PASSWORD',
                             getpass.getpass('Enter NSO password: '))

    url = "http://{}:8080/api/config/devices/".format(nso_host)

    headers = {
        'Content-Type': "application/vnd.yang.data+xml",
        }

    response = requests.request("PATCH",
                                url,
                                auth=(nso_username, nso_password),
                                data=xml_payload, headers=headers)


    return response
