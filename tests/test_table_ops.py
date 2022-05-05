import unittest
from pathlib import Path

from pyhbasecli import HBaseCli

URL = ""
headers = {"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"}


class TableOpsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cli = HBaseCli(
            url=URL,
            headers=headers)
        self.cli.open()
        print("section start")

    def tearDown(self) -> None:
        self.cli.close()
        print("section end")

    def test_table_ops(self) -> None:
        print("测试表相关")
        namespace = "recommend_hsz_test_table"
        tablename = "test_table"
        tablefullname = f"{namespace}:{tablename}"
        nss = self.cli.show_namespaces()
        if namespace in [i["name"] for i in nss]:
            print(f"已创建命名空间: {namespace}")
        else:
            self.cli.create_namespace(namespace)
        try:
            print(f"测试表开始")
            if self.cli.table_exists(tablefullname):
                print(f"测试表已存在,先删除")
                if not self.cli.is_table_disabled(tablefullname):
                    print(f"测试表不是disable状态,先设为disable状态")
                    self.cli.disable_table(tablefullname)
                self.cli.delete_table(tablename, ns=namespace)
            print(f"创建测试表")
            self.cli.create_table(tablefullname, [{"name": "info"}])
            try:
                print(f"测试测试表成功创建")
                assert self.cli.table_exists(tablename, ns=namespace)
                print(f"测试表信息测试")
                print(self.cli.show_tables(namespace))
                print(self.cli.desc_table(tablefullname))
                print(self.cli.show_families(tablefullname))
                print(f"测试表状态测试")
                assert not self.cli.is_table_disabled(tablefullname)
                assert self.cli.is_table_enabled(tablefullname)
                assert self.cli.is_table_available(tablefullname)
                print(f"测试表切换状态")
                self.cli.disable_table(tablefullname)
                assert self.cli.is_table_disabled(tablefullname)
                assert not self.cli.is_table_enabled(tablefullname)

            finally:
                if not self.cli.is_table_disabled(tablefullname):
                    self.cli.disable_table(tablefullname)
                print(f"删除表{tablefullname}")
                self.cli.delete_table(tablefullname)

        finally:
            print(f"删除命名空间{namespace}")
            self.cli.delete_namespace(namespace)

    # def test_namespace_show(self) -> None:
    #     print("测试命名空间相关")
    #     namespace = "recommend_hsz_test"
    #     nss = self.cli.show_namespaces()
    #     print(nss)
    #     if namespace in [i["name"] for i in nss]:
    #         print(f"已创建命名空间: {namespace}")
    #     else:
    #         print(f"命名空间{namespace}未创建,创建...")
    #         cli.create_namespace(namespace)
    #         print(f"命名空间{namespace}创建完成")
    #     try:
    #         nsinfo = cli.desc_namespace(namespace)
    #         print(f"命名空间{namespace}描述如下:")
    #         print(nsinfo)

    #         print("测试表相关")
    #     finally:
    #         print(f"删除命名空间{namespace}")
    #         cli.delete_namespace(namespace)
