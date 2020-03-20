from Common.FileProcess.AbstractClass import FileProcess
from Common.FileProcess.TXTFile import TXTFile
import sys
import os
class Folder(FileProcess):
    def __init__(self, path):
        self.path = path
        self.content = []


    def bulid(self, path):
        folder = os.path.exists(path)
        if not folder: os.makedirs(path)
        else: print("folder existed")

    def delete(self, path):
        folder = os.path.exists(path)
        if folder: os.removedirs(path)
        else: print("folder not existed")


    def read(self, type, Reader):
        folder = os.path.isdir(self.path)
        if folder:
            paths = os.listdir(self.path)
            for path in paths:
                path = self.path + '\\' + path
                for item in Folder(path).read(type, Reader):
                    self.content.append(item)
        elif os.path.isfile(self.path) and str(self.path).endswith(type):
                reader = Reader(self.path)
                self.content.append(reader.read())
        return self.content


    def operation(self):
        pass

if __name__ == '__main__':
    folder = Folder(r'C:\Users\Horn\Desktop\Python语音合成')
    answer = folder.read('txt', TXTFile)
    print(answer)
