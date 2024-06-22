from click.testing import CliRunner

from . import BaseCMLTest


class TestCMLGroups(BaseCMLTest):
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
    post_groups = {
        "id": "48c9c605-552f-4666-bd23-5b68cf4de665",
        "created": "2024-02-29T21:44:13+00:00",
        "modified": "2024-02-29T21:45:04+00:00",
        "name": "group",
        "description": "",
        "members": ["00000000-0000-4000-a000-000000000000"],
        "labs": [
            {"id": "88119b68-9d08-40c4-90f5-6dc533fd0254", "permission": "read_write"},
        ],
    }

    patch_groups = post_groups

    get_groups = [
        {
            "id": "48c9c605-552f-4666-bd23-5b68cf4de665",
            "created": "2024-02-29T21:44:13+00:00",
            "modified": "2024-02-29T21:45:04+00:00",
            "name": "group",
            "description": "",
            "members": ["00000000-0000-4000-a000-000000000000"],
            "labs": [
                {"id": "88119b68-9d08-40c4-90f5-6dc533fd0254", "permission": "read_write"},
            ],
        },
    ]

    def test_cml_groups_ls(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("get", m, "groups", json=self.get_groups)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["groups", "ls"])
            self.assertEqual(0, result.exit_code)

    def test_cml_groups_ls_verbose(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("get", m, "groups", json=self.get_groups)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["groups", "ls", "--verbose"])
            self.assertEqual(0, result.exit_code)

    def test_cml_groups_create_group(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("post", m, "groups", json=self.post_groups)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["groups", "create", "group"])
            self.assertEqual(0, result.exit_code)

    def test_cml_groups_create_group_fail(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["groups", "create", "group"])
            self.assertEqual(1, result.exit_code)

    def test_cml_groups_update_group(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("get", m, "groups", json=self.get_groups)
            self.setup_func("patch", m, "groups/48c9c605-552f-4666-bd23-5b68cf4de665", json=self.patch_groups)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["groups", "update", "group"])
            self.assertEqual(0, result.exit_code)

    def test_cml_groups_update_group_fail(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "users", json=self.get_users)
            self.setup_func("get", m, "groups", json=self.get_groups)
            self.setup_func("patch", m, "groups/48c9c605-552f-4666-bd23-5b68cf4de665", json=self.patch_groups)
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["groups", "update", "nonexistent_group"])
            self.assertEqual(1, result.exit_code)

    def test_cml_groups_delete_group(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "groups", json=self.get_groups)
            self.setup_func("delete", m, "groups/48c9c605-552f-4666-bd23-5b68cf4de665")
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["groups", "delete", "group"])
            self.assertEqual(0, result.exit_code)

    def test_cml_groups_delete_group_fail(self):
        with self.get_context() as m:
            self.setup_mocks(m)
            self.setup_func("get", m, "groups", json=self.get_groups)
            self.setup_func("delete", m, "groups/48c9c605-552f-4666-bd23-5b68cf4de665")
            virl = self.get_virl()
            runner = CliRunner()
            result = runner.invoke(virl, ["groups", "delete", "nonexistent_group"])
            self.assertEqual(1, result.exit_code)
