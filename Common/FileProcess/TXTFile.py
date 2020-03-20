from Common.FileProcess.AbstractClass import FileProcess
import sys
import os
class TXTFile(FileProcess):

    def __init__(self, path):
        self.path = path


    def bulid(self, content):
        if os.path.exists(self.path):
            print("文件已经存在无需创建,请调用rewrite()函数复写")
            return
        with open(self.path, 'w', errors='ignore') as file:
            file.write(content)

    def rewrite(self, content):
        if os.path.exists(self.path):
            with open(self.path, 'w', errors='ignore') as file:
                file.write(content)

    def delete(self):
        if os.path.exists(self.path):
            os.remove(self.path)
            print(self.path + "删除成功")
        else: print("文件不存在， 无法删除")

    def read(self):
        if not os.path.exists(self.path): return "文件不存在"
        with open(self.path, 'r', errors='ignore', encoding='utf-8') as file:  # 文档中编码有些问题，所有用errors过滤错误
            content = file.read()
            return content

    def operation(self):
        pass