import requests
from .credentials import get_prop, _get_password, _get_from_user


def get_credentials():  # pragma: no cover

    configurable_props = ["NSO_HOST", "NSO_USERNAME", "NSO_PASSWORD"]
    config = dict()

    for p in configurable_props:
        val = get_prop(p)
        if val:
            config[p] = val

    if not config.get("NSO_HOST"):
        config["NSO_HOST"] = _get_from_user("Enter NSO IP/Hostname: ")

    if not config.get("NSO_USERNAME"):
        config["NSO_USERNAME"] = _get_from_user("Enter NSO username: ")

    if not config.get("NSO_PASSWORD"):
        config["NSO_PASSWORD"] = _get_password("Enter NSO password: ")

    return (config["NSO_HOST"], config["NSO_USERNAME"], config["NSO_PASSWORD"])


def check_for_rfc8040(nso_host, nso_username, nso_password):
    url = "http://{}:8080/.well-known/host-meta".format(nso_host)
    headers = {"Accept": "application/json"}

    try:
        response = requests.request("GET", url, auth=(nso_username, nso_password), headers=headers)
        response.raise_for_status()
    except Exception:
        return False
    else:
        json = response.json()
        if "links" in json and "restconf" in json["links"]:
            for u in json["links"]["restconf"]:
                if u["href"] == "/restconf":
                    return True

    return False


def perform_sync_from():
    nso_host, nso_username, nso_password = get_credentials()
    url = "http://{}:8080".format(nso_host)
    headers = dict()

    if not check_for_rfc8040(nso_host, nso_username, nso_password):
        url += "/api/running/devices/_operations/sync-from"
        headers = {"Content-Type": "application/vnd.yang.operation+json", "Accept": "application/vnd.yang.operation+json"}
    else:
        url += "/restconf/operations/tailf-ncs:devices/tailf-ncs:sync-from"
        headers = {"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}

    response = requests.request("POST", url, auth=(nso_username, nso_password), headers=headers)
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
    url = "http://{}:8080".format(nso_host)
    headers = dict()

    if not check_for_rfc8040(nso_host, nso_username, nso_password):
        url += "/api/config/devices/"
        headers = {"Content-Type": "application/vnd.yang.data+xml"}
    else:
        url += "/restconf/data/tailf-ncs:devices"
        headers = {"Content-Type": "application/yang-data+xml"}

    response = requests.request("PATCH", url, auth=(nso_username, nso_password), data=xml_payload, headers=headers)

    return response
