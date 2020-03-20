from abc import abstractmethod, ABCMeta
import sys
import os

class DatabaseProcess(metaclass=ABCMeta):
    @abstractmethod
    def connect(self, path): pass

    #下方为数据库级别操作，表的添加与删除
    @abstractmethod
    def drop(self): pass

    @abstractmethod
    def add(self): pass
    #下方为表级操作 增删改查
    @abstractmethod
    def delete(self, path): pass

    @abstractmethod
    def search(self): pass

    @abstractmethod
    def update(self): pass

    @abstractmethod
    def insert(self): pass
