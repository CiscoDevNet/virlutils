import os
import requests
import getpass


def get_input(prompt):  # pragma: no cover
    try:
        inp = raw_input
    except NameError:
        pass
    try:
        inp = input
    except NameError:
        pass
    return inp(prompt)


def get_credentials():  # pragma: no cover

    nso_host = os.getenv('NSO_HOST', None)
    if not nso_host:
        nso_host = get_input('Enter NSO IP/Hostname: ')

    nso_username = os.getenv('NSO_USERNAME', None)
    if not nso_username:
        nso_username = get_input('Enter NSO username: ')

    nso_password = os.getenv('NSO_PASSWORD', None)
    if not nso_password:
        nso_password = getpass.getpass('Enter NSO password: ')

    return(nso_host, nso_username, nso_password)


def perform_sync_from():
    nso_host, nso_username, nso_password = get_credentials()
    url = "http://{}:8080".format(nso_host)
    url = url + "/api/running/devices/_operations/sync-from".format(nso_host)
    headers = {'Content-Type': "application/vnd.yang.operation+json",
               'Accept': "application/vnd.yang.operation+json"}

    response = requests.request("POST",
                                url,
                                auth=(nso_username, nso_password),
                                headers=headers)
    return response


# def perform_sync_to():
#     nso_host, nso_username, nso_password = get_credentials()
#     url = "http://{}:8080".format(nso_host)
#     url = url + "/api/running/devices/_operations/sync-to".format(nso_host)
#     headers = {'Content-Type': "application/vnd.yang.operation+json",
#                'Accept': "application/vnd.yang.operation+json"}
#
#     response = requests.request("POST",
#                                 url,
#                                 auth=(nso_username, nso_password),
#                                 headers=headers)
#     return response


def update_devices(xml_payload):

    nso_host, nso_username, nso_password = get_credentials()
    url = "http://{}:8080/api/config/devices/".format(nso_host)

    headers = {'Content-Type': "application/vnd.yang.data+xml"}

    response = requests.request("PATCH",
                                url,
                                auth=(nso_username, nso_password),
                                data=xml_payload, headers=headers)

    return response
