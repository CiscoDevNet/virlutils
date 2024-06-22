from click.testing import CliRunner

from . import BaseCMLTest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestCMLUsers(BaseCMLTest):
    get_users = [
        {
            "id": "00000000-0000-4000-a000-000000000000",
            "created": "2022-09-30T10:03:53+00:00",
            "modified": "2024-06-21T15:16:42+00:00",
            "username": "admin",
            "fullname": "",
            "email": "",
            "description": "",
            "admin": True,
            "directory_dn": "",
            "groups": [],
            "labs": [],
            "opt_in": True,
            "resource_pool": None,
            "tour_version": "2.6.1+build.11",
            "pubkey_info": "",
        },
        {
            "id": "9e4e75b4-aaab-47af-9edb-9364460a81ae",
            "created": "2024-06-19T20:29:02+00:00",
            "modified": "2024-06-21T10:42:20+00:00",
            "username": "user",
            "fullname": "",
            "email": "",
            "description": "",
            "admin": False,
            "directory_dn": "",
            "groups": ["48c9c605-552f-4666-bd23-5b68cf4de665"],
            "labs": [],
            "opt_in": True,
            "resource_pool": None,
            "tour_version": "",
            "pubkey_info": "",
        },
    ]
    post_users = {
        "id": "9e4e75b4-aaab-47af-9edb-9364460a81ae",
        "created": "2024-06-19T20:29:02+00:00",
        "modified": "2024-06-21T10:42:20+00:00",
        "username": "user",
        "fullname": "",
        "email": "",
        "description": "",
        "admin": False,
        "directory_dn": "",
        "groups": ["48c9c605-552f-4666-bd23-5b68cf4de665"],
        "labs": [],
        "opt_in": True,
        "resource_pool": None,
        "tour_version": "",
        "pubkey_info": "",
    }
    patch_users = post_users

    get_groups = [
        {
            "id": "48c9c605-552f-4666-bd23-5b68cf4de665",
            "created": "2024-02-29T21:44:13+00:00",
            "modified": "2024-02-29T21:45:04+00:00",
            "name": "admin",
            "description": "",
            "members": ["00000000-0000-4000-a000-000000000000"],
            "labs": [
                {"id": "88119b68-9d08-40c4-90f5-6dc533fd0254", "permission": "read_write"},
            ],
        },
    ]

    def test_cml_users_ls(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("get", m, "groups", json=self.get_groups)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["users", "ls"])
            self.assertEqual(0, result.exit_code)

    def test_cml_users_ls_verbose(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("get", m, "groups", json=self.get_groups)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["users", "ls", "--verbose"])
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.users.create.commands.confirm_password")
    def test_cml_users_create_user(self, mock_confirm_password):
        with self.get_context() as m:
            mock_confirm_password.return_value = "password"
            self.setup_mocks(m)
            self.setup_func("post", m, "users", json=self.post_users)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["users", "create", "user"])
            self.assertEqual(0, result.exit_code)

    @patch("virl.cli.users.create.commands.confirm_password")
    def test_cml_users_create_user_fail(self, mock_confirm_password):
        with self.get_context() as m:
            mock_confirm_password.side_effect = Exception
            self.setup_mocks(m)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["users", "create", "user"])
            self.assertEqual(1, result.exit_code)

    def test_cml_users_update_user(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("get", m, "groups", json=self.get_groups)
            self.setup_func("patch", m, "users/9e4e75b4-aaab-47af-9edb-9364460a81ae", json=self.patch_users)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["users", "update", "user"])
            self.assertEqual(0, result.exit_code)

    def test_cml_users_update_user_fail(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("get", m, "groups", json=self.get_groups)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["users", "update", "nonexistent_user"])
            self.assertEqual(1, result.exit_code)

    def test_cml_users_delete_user(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("delete", m, "users/9e4e75b4-aaab-47af-9edb-9364460a81ae")
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["users", "delete", "user"])
            self.assertEqual(0, result.exit_code)

    def test_cml_users_delete_user_fail(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("delete", m, "users/9e4e75b4-aaab-47af-9edb-9364460a81ae")
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["users", "delete", "nonexistent_user"])
            self.assertEqual(1, result.exit_code)
