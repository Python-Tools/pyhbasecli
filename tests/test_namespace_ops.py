import unittest
from pyhbasecli import HBaseCli

URL = ""
headers = {"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"}


class NamespaceOpsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cli = HBaseCli(
            url=URL,
            headers=headers)
        self.cli.open()
        print("section start")

    def tearDown(self) -> None:
        self.cli.close()
        print("section end")

    def test_namespace_ops(self) -> None:
        print("测试命名空间相关")
        namespace = "recommend_hsz_test_ns"
        nss = self.cli.show_namespaces()
        print(nss)
        if namespace in [i["name"] for i in nss]:
            print(f"已创建命名空间: {namespace}")
            print(f"删除命名空间{namespace}")
            self.cli.delete_namespace(namespace)

        print(f"创建命名空间{namespace}未创建")
        self.cli.create_namespace(namespace)
        print(f"命名空间{namespace}创建完成")
        try:
            nsinfo = self.cli.desc_namespace(namespace)
            print(f"命名空间{namespace}描述如下:")
            print(nsinfo)
            assert nsinfo["name"] == namespace

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
