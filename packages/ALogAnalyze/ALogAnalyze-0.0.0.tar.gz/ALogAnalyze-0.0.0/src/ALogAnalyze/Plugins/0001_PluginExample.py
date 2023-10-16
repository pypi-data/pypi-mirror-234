#!/usr/bin/env python3

class PluginExample:
    """
    PluginExample类是一个编写LogTools插件的示例

    @id(123456): 唯一码
    @name(zengjf): 唯一码别名
    """

    def __init__(self, kwargs):
        print(">>> in plugin init method")

        self.id = kwargs["id"]
        self.name = kwargs["name"]

        print("实例输出：id: " + kwargs["id"] + ", name: " + kwargs["name"])

        print("<<< out plugin init method")

if __name__ == "__main__" :
    PluginExample({"id": "123456", "name": "zengjf"})
