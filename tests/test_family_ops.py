import unittest
from pyhbasecli import HBaseCli


URL = ""
headers = {"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"}


class FamilyOpsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cli = HBaseCli(
            url=URL,
            headers=headers)
        self.cli.open()
        print("section start")

    def tearDown(self) -> None:
        self.cli.close()
        print("section end")

    def test_family_ops(self) -> None:
        print("测试列簇相关")
        namespace = "recommend_hsz_test_family"
        tablename = "test_family"
        family = "testfamily"
        tablefullname = f"{namespace}:{tablename}"
        nss = self.cli.show_namespaces()
        if namespace in [i["name"] for i in nss]:
            print(f"已创建命名空间: {namespace}")
        else:
            self.cli.create_namespace(namespace)
        try:
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
                print("开始测试列簇")
                families = self.cli.show_families(tablefullname)
                assert "info" in [i["name"] for i in families]
                print("测试创建列簇")
                self.cli.create_family(family, tablefullname)
                families = self.cli.show_families(tablefullname)
                assert family in [i["name"] for i in families]
                target_family = [i for i in families if i["name"] == family][0]
                assert target_family["timeToLive"] != 120
                print("测试修改列簇")
                self.cli.modify_family(family, tablefullname, timeToLive=120)
                families = self.cli.show_families(tablefullname)
                target_family = [i for i in families if i["name"] == family][0]
                assert target_family["timeToLive"] == 120
                # print("测试删除列簇")
                # self.cli.delete_family(family, tablefullname)
                # families = self.cli.show_families(tablefullname)
                # assert family not in [i["name"] for i in families]
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
