from . import BaseCMLTest
from click.testing import CliRunner
import requests_mock
import textwrap
import os
import traceback


class CMLDefinitionsTest(BaseCMLTest):
    def test_cml_image_definitions_import(self):
        with requests_mock.Mocker() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            m.post(self.get_api_path("image_definitions/"), json=True)  # virl2_client 2.2.1 uses URI that ends in slashes
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(
                virl,
                [
                    "definitions",
                    "images",
                    "import",
                    "definition",
                    "-f",
                    os.path.join(os.path.dirname(__file__), "static/fake_image_definitions.yaml"),
                ],
            )
            self.assertEqual(0, result.exit_code, result.stdout)

    def test_node_definitions_list(self):
        with requests_mock.Mocker() as m:
            with open(os.path.join(os.path.dirname(__file__), "static/response_get_node_defs.json"), "rb") as fh_node_defs:
                # Mock the request to return what we expect from the API.
                self.setup_mocks(m)
                m.get(
                    self.get_api_path("node_definitions/"), body=fh_node_defs, headers={"content-type": "application/json; charset=utf-8"}
                )
                virl = self.get_virl()
                runner = CliRunner()
                result = runner.invoke(virl, ["definitions", "nodes", "ls"])
                if result.exception:
                    traceback.print_exception(*result.exc_info)
                    raise result.exception
                with open(os.path.join(os.path.dirname(__file__), "static/node_defs_list_output.txt")) as fh_node_defs:
                    output_text = fh_node_defs.read()
                    self.assertEquals(output_text, result.output)

    def test_node_definitions_list_one(self):
        with requests_mock.Mocker() as m:
            with open(os.path.join(os.path.dirname(__file__), "static/response_get_node_defs.json"), "rb") as fh_node_defs:
                # Mock the request to return what we expect from the API.
                self.setup_mocks(m)
                m.get(
                    self.get_api_path("node_definitions/"), body=fh_node_defs, headers={"content-type": "application/json; charset=utf-8"}
                )
                virl = self.get_virl()
                runner = CliRunner()
                result = runner.invoke(virl, ["definitions", "nodes", "ls", "--node", "nxosv9000"])
                if result.exception:
                    traceback.print_exception(*result.exc_info)
                    raise result.exception
                expected = textwrap.dedent(
                    """\
                    ╒═══════════╤════════════╤══════════════════════════╤══════════════════════╤════════╤════════╤══════════════════╕
                    │ ID        │ Label      │ Description              │   Max No. Interfaces │ RAM    │   CPUs │ Boot Disk Size   │
                    ╞═══════════╪════════════╪══════════════════════════╪══════════════════════╪════════╪════════╪══════════════════╡
                    │ nxosv9000 │ NX-OS 9000 │ Cisco Nexus 9000v Switch │                   65 │ 8.0 GB │      2 │ N/A              │
                    ╘═══════════╧════════════╧══════════════════════════╧══════════════════════╧════════╧════════╧══════════════════╛
                    """
                )
                self.assertEquals(expected, result.output)

    def test_node_definitions_list_legacy(self):
        """
        Check that we can still handle data in the legacy format that was
        returned by the API before CML 2.3.
        """
        with requests_mock.Mocker() as m:
            with open(os.path.join(os.path.dirname(__file__), "static/response_get_node_defs_cml22.json"), "rb") as fh_node_defs:
                # Mock the request to return what we expect from the API.
                self.setup_mocks(m)
                m.get(
                    self.get_api_path("node_definitions/"), body=fh_node_defs, headers={"content-type": "application/json; charset=utf-8"}
                )
                virl = self.get_virl()
                runner = CliRunner()
                result = runner.invoke(virl, ["definitions", "nodes", "ls"])
                if result.exception:
                    traceback.print_exception(*result.exc_info)
                    raise result.exception
                with open(os.path.join(os.path.dirname(__file__), "static/node_defs_list_output_cml22.txt")) as fh_node_defs:
                    output_text = fh_node_defs.read()
                    self.assertEquals(output_text, result.output)
