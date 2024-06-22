from click.testing import CliRunner

from . import BaseCMLTest


class Tests(BaseCMLTest):
    def test_virl_generate_pyats(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "pyats"])
            self.assertEqual(0, result.exit_code)

    def test_virl_generate_pyats_topology(self):
        with self.get_context() as m:
            # Mock the request to return what we expect from the API.
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["generate", "pyats", "-o", "topology.yaml"])
            self.assertEqual(0, result.exit_code)
