from abc import abstractmethod, ABCMeta
import sys
import os

class FileProcess(metaclass=ABCMeta):
    @abstractmethod
    def bulid(self, path): pass

    @abstractmethod
    def delete(self, path): pass

    @abstractmethod
    def read(self): pass

    @abstractmethod
    def operation(self): pass



if __name__ == '__main__':
    print(os.getcwd())
    print(sys.argv[0])