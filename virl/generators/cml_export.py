from requests.exceptions import HTTPError
import logging


def export_generator(lab, extract=True):
    if extract:
        print("Extracting configurations...")
        # The client library prints "API Error" warnings when a node doesn't support extraction.  Quiet these.
        logger = logging.getLogger("virl2_client.models.authentication")
        level = logger.getEffectiveLevel()
        logger.setLevel(logging.CRITICAL)
        for node in lab.nodes():
            if node.is_booted():
                try:
                    node.extract_configuration()
                except HTTPError as he:
                    if he.response.status_code != 400:
                        # Ignore 400 as that typically means the node doesn't support config extraction.
                        print("WARNING: Failed to extract configuration from node {}: {}".format(node.label, he))
                except Exception as e:
                    print("WARNING: Failed to extract configuration from node {}: {}".format(node.label, e))

        logger.setLevel(level)

    return lab.download()
