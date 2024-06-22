from click.testing import CliRunner

from . import BaseCMLTest


class TestCMLLs(BaseCMLTest):
    def test_cml_ls_all(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["ls", "--all"])
            self.assertEqual(0, result.exit_code)

    def test_cml_ls(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["ls"])
            self.assertEqual(0, result.exit_code)
