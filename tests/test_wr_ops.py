from cgitb import reset
from typing import Any, Dict, Union, DefaultDict, Callable, Optional
import unittest
from collections import defaultdict
from pyhbasecli import HBaseCli, ColumnsValue

URL = ""
headers = {"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"}


class WROpsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cli = HBaseCli(
            url=URL,
            headers=headers)
        self.cli.open()
        print("section start")

    def tearDown(self) -> None:
        self.cli.close()
        print("section end")

    def test_wr_ops_same_decoder(self) -> None:
        print("测试相同编码解码器读写相关")
        namespace = "recommend_hsz_test_wr_samedecoder"
        tablename = "test_same_decoder"
        family = "info"
        row = "1"
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
            self.cli.create_table(tablefullname, [{"name": family}])
            try:
                families = self.cli.show_families(tablefullname)
                assert family in [i["name"] for i in families]
                print(f"测试测试表成功创建")
                print("开始测试读写")
                print("测试写操作")
                pr = self.cli.put(
                    tablefullname,
                    row,
                    [
                        ColumnsValue.from_value(family, "test1", 1, encoder=lambda x, y:str(x).encode("utf-8")),
                        ColumnsValue.from_value(family, "test2", 2, encoder=lambda x, y:str(x).encode("utf-8"))
                    ]
                )
                assert pr
                print("测试读操作")
                assert self.cli.exists(tablefullname, row)
                rowcolumns = self.cli.get(tablefullname, "notin", columns_decoder=defaultdict(lambda: lambda x, y: int(x.decode("utf-8"))))
                assert rowcolumns is None
                rowcolumns = self.cli.get(tablefullname, row, columns_decoder=defaultdict(lambda: lambda x, y: int(x.decode("utf-8"))))
                assert rowcolumns is not None
                print([rowcolumn.values() for rowcolumn in rowcolumns])
                print("测试append")
                appres = self.cli.append(
                    tablefullname,
                    row,
                    [
                        ColumnsValue.from_value(family, "test3", 3, encoder=lambda x, y:str(x).encode("utf-8")),
                    ],
                )
                assert appres is None
                appres = self.cli.append(
                    tablefullname,
                    row,
                    [
                        ColumnsValue.from_value(family, "test3", 2, encoder=lambda x, y:str(x).encode("utf-8")),
                    ],
                    returnResults=True,
                    columns_decoder=defaultdict(lambda: lambda x, y: x.decode("utf-8"))
                )
                assert appres is not None
                print([rowcolumn.values() for rowcolumn in appres])
                print("测试incr")
                incrres = self.cli.increment(
                    tablefullname,
                    row,
                    {f"{family}:test4": 2}
                )
                assert incrres is not None
                print("@@@@@@@@@@@@@@@@@@")
                print(incrres)
                print("@@@@@@@@@@@@@@@@@@")

                print("测试删除")
                assert self.cli.delete(tablefullname, row)
                assert not self.cli.exists(tablefullname, row)
            finally:
                if not self.cli.is_table_disabled(tablefullname):
                    self.cli.disable_table(tablefullname)
                print(f"删除表{tablefullname}")
                self.cli.delete_table(tablefullname)

        finally:
            print(f"删除命名空间{namespace}")
            self.cli.delete_namespace(namespace)

    def test_wr_ops_diff_decoder(self) -> None:
        print("测试不同编码器读写相关")
        namespace = "recommend_hsz_test_wr_diff_decoder"
        tablename = "test_diff_decoder"
        family = "info"
        row = "1"
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
            self.cli.create_table(tablefullname, [{"name": family}])
            try:
                families = self.cli.show_families(tablefullname)
                assert family in [i["name"] for i in families]
                print(f"测试测试表成功创建")
                print("开始测试读写")
                print("测试写操作")
                self.cli.put(
                    tablefullname,
                    row,
                    [
                        ColumnsValue.from_value(family, "test1", 1, encoder=lambda x, y:str(x).encode("utf-8")),
                        ColumnsValue.from_value(family, "test2", "test", encoder=lambda x, y:x.encode("utf-8"))
                    ])

                print("测试读操作")
                columns_decoder: Union[DefaultDict[str, Callable[[bytes, Optional[bytes]], Any]], Dict[str, Callable[[bytes, Optional[bytes]], Any]]] = defaultdict(lambda: lambda x, y: int(x.decode("utf-8")))
                columns_decoder.update({'info:test2': lambda x, y: x.decode("utf-8")})
                rowcolumns = self.cli.get(tablefullname, row, columns_decoder=columns_decoder)
                assert rowcolumns is not None
                print([rowcolumn.values() for rowcolumn in rowcolumns])

            finally:
                if not self.cli.is_table_disabled(tablefullname):
                    self.cli.disable_table(tablefullname)
                print(f"删除表{tablefullname}")
                self.cli.delete_table(tablefullname)

        finally:
            print(f"删除命名空间{namespace}")
            self.cli.delete_namespace(namespace)

    def test_wr_ops_batch(self) -> None:
        print("测试批量读写相关")
        namespace = "recommend_hsz_test_wr_diff_decoder"
        tablename = "test_diff_decoder"
        family = "info"
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
            self.cli.create_table(tablefullname, [{"name": family}])
            try:
                families = self.cli.show_families(tablefullname)
                assert family in [i["name"] for i in families]
                print(f"测试测试表成功创建")
                print("开始测试读写")
                print("测试写操作")
                self.cli.batch_put(
                    tablefullname,
                    rkvs={
                        "comic:1": [
                            ColumnsValue.from_value(family, "test1", 1, encoder=lambda x, y:str(x).encode("utf-8")),
                            ColumnsValue.from_value(family, "test2", "test1", encoder=lambda x, y:x.encode("utf-8"))
                        ],
                        "game:2": [
                            ColumnsValue.from_value(family, "test1", 2, encoder=lambda x, y:str(x).encode("utf-8")),
                            ColumnsValue.from_value(family, "test2", "test2", encoder=lambda x, y:x.encode("utf-8"))
                        ]}
                )

                print("测试批量读操作")
                columns_decoder: Union[DefaultDict[str, Callable[[bytes, Optional[bytes]], Any]], Dict[str, Callable[[bytes, Optional[bytes]], Any]]] = defaultdict(lambda: lambda x, y: int(x.decode("utf-8")))
                columns_decoder.update({'info:test2': lambda x, y: x.decode("utf-8")})
                rowscolumns = self.cli.batch_get(tablefullname, rows=["comic:1", "game:2"], columns_decoder=columns_decoder)
                for row, rowcolumns in rowscolumns.items():
                    print(f"get row {row}:")
                    print([rowcolumn.values() for rowcolumn in rowcolumns])

                print("测试搜索")
                rowscolumns = self.cli.scan(tablefullname, filterString="PrefixFilter('comic:')", columns_decoder=columns_decoder)
                for row, rowcolumns in rowscolumns.items():
                    print(f"get row {row}:")
                    print([rowcolumn.values() for rowcolumn in rowcolumns])

                print("测试批量删除")
                self.cli.batch_delete(tablefullname, rows=["comic:1", "game:2"])
                assert not self.cli.exists(tablefullname, "comic:1")
                assert not self.cli.exists(tablefullname, "game:2")

            finally:
                if not self.cli.is_table_disabled(tablefullname):
                    self.cli.disable_table(tablefullname)
                print(f"删除表{tablefullname}")
                self.cli.delete_table(tablefullname)

        finally:
            print(f"删除命名空间{namespace}")
            self.cli.delete_namespace(namespace)
