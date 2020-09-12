import requests
from .credentials import get_prop, _get_password, _get_from_user
from jinja2 import Environment


class NSO(object):
    __rfc8040 = False
    __nso_username = None
    __nso_password = None
    __nso_host = None

    def __init__(self):
        self.__get_credentials()
        self.__check_for_rfc8040()

    def __get_credentials(self):  # pragma: no cover

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

        self.__nso_host = config["NSO_HOST"]
        self.__nso_username = config["NSO_USERNAME"]
        self.__nso_password = config["NSO_PASSWORD"]

    def __check_for_rfc8040(self):
        url = "http://{}:8080/.well-known/host-meta".format(self.__nso_host)
        headers = {"Accept": "application/json"}
        rfc8040 = False

        try:
            response = requests.request("GET", url, auth=(self.__nso_username, self.__nso_password), headers=headers)
            response.raise_for_status()
        except Exception:
            pass
        else:
            json = response.json()
            if "links" in json and "restconf" in json["links"]:
                for u in json["links"]["restconf"]:
                    if u["href"] == "/restconf":
                        rfc8040 = True

        self.__rfc8040 = rfc8040

    def __build_ned_vars(self):
        url = "http://{}:8080".format(self.__nso_host)
        headers = dict()
        nurl = ""
        murl = ""

        if not self.__rfc8040:
            nurl = url + "/api/config/devices/ned-ids/ned-id"
            murl = url + "/api/config/modules-state/module"  # XXX: Is this correct for pre-RFC8040 NSO?
            headers = {"Content-Type": "application/vnd.yang.operation+json", "Accept": "application/vnd.yang.operation+json"}
        else:
            nurl = url + "/restconf/data/tailf-ncs:devices/ned-ids/ned-id"
            murl = url + "/restconf/data/ietf-yang-library:modules-state/module"
            headers = {"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}

        response = requests.request("GET", nurl, auth=(self.__nso_username, self.__nso_password), headers=headers)
        neds = response.json()
        ned_patterns = {
            "cisco-ios-": "IOS",
            "cisco-iosxr-": "XR",
            "cisco-nx-": "NX",
            "cisco-asa-": "ASA",
        }
        # Set some "sane" defaults.  These are at least the same as what the older
        # virlutils had.
        ned_vars = {
            "NX_PREFIX": "cisco-nx-id",
            "NX_NED_ID": "cisco-nx",
            "NX_NAMESPACE": "http://tail-f.com/ned/cisco-nx-id",
            "XR_PREFIX": "cisco-ios-xr-id",
            "XR_NED_ID": "cisco-ios-xr",
            "XR_NAMESPACE": "http://tail-f.com/ned/cisco-ios-xr-id",
            "IOS_PREFIX": "ios-id",
            "IOS_NED_ID": "cisco-ios",
            "IOS_NAMESPACE": "urn:ios-id",
            "ASA_PREFIX": "asa-id",
            "ASA_NED_ID": "cisco-asa",
            "ASA_NAMESPACE": "http://cisco.com/ned/asa-id",
        }

        response = requests.request("GET", murl, auth=(self.__nso_username, self.__nso_password), headers=headers)
        modules = response.json()

        for ned in neds["tailf-ncs:ned-id"]:
            (prefix, nid) = ned["id"].split(":")
            for pattern, platform in ned_patterns.items():
                # FIXME: This only uses the first encountered matching NED ID.
                # If one has multiple NEDs, the desirned NED may not be ideal.
                if nid.startswith(pattern):
                    ned_vars["{}_PREFIX".format(platform)] = prefix
                    ned_vars["{}_NED_ID".format(platform)] = nid
                    for module in modules["ietf-yang-library:module"]:
                        if module["name"] == nid:
                            ned_vars["{}_NAMESPACE".format(platform)] = module["namespace"]
                            break
                    break

        return ned_vars

    def perform_sync_from(self):
        url = "http://{}:8080".format(self.__nso_host)
        headers = dict()

        if not self.__rfc8040:
            url += "/api/running/devices/_operations/sync-from"
            headers = {"Content-Type": "application/vnd.yang.operation+json", "Accept": "application/vnd.yang.operation+json"}
        else:
            url += "/restconf/operations/tailf-ncs:devices/tailf-ncs:sync-from"
            headers = {"Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json"}

        response = requests.request("POST", url, auth=(self.__nso_username, self.__nso_password), headers=headers)
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

    def update_devices(self, xml_payload):
        url = "http://{}:8080".format(self.__nso_host)
        headers = dict()

        if not self.__rfc8040:
            url += "/api/config/devices/"
            headers = {"Content-Type": "application/vnd.yang.data+xml"}
        else:
            url += "/restconf/data/tailf-ncs:devices"
            headers = {"Content-Type": "application/yang-data+xml"}

        ned_vars = self.__build_ned_vars()
        env = Environment()
        template = env.from_string(source=xml_payload, globals=ned_vars)

        response = requests.request("PATCH", url, auth=(self.__nso_username, self.__nso_password), data=template.render(), headers=headers)

        return response
