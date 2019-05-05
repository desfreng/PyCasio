#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Utils import Devices


class AbstractNode():
    def __init__(self, name, directory=None):
        self._dir = None
        self._name = None

        self.name = name
        self.parent = directory

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._dir is None:
            self._name = name
        elif name not in self.parent:
            self._name = name

    @property
    def parent(self):
        return self._dir

    @parent.setter
    def parent(self, directory):
        if directory is None:
            self._dir = None
        elif self not in directory:
            directory.add(self)


class DirectoryNode(AbstractNode):
    def __init__(self, dir_name, parent=None):
        super().__init__(dir_name, parent)

        self._child = []
        self._ro = False

    def __iter__(self):
        return iter(self._child)

    @property
    def read_only(self):
        return self._ro

    def _set_ro(self, value):
        self._ro = value

        for a in self:
            if isinstance(a, DirectoryNode):
                a._ro = value

    @property
    def files(self):
        value_return = []

        for a in self:
            if isinstance(a, FileNode):
                value_return.append(a)

        return tuple(value_return)

    @property
    def file_number(self):
        return len(self.files)

    @property
    def directories(self):
        value_return = []

        for a in self:
            if isinstance(a, DirectoryNode):
                value_return.append(a)

        return tuple(value_return)

    @property
    def directories_number(self):
        return len(self.directories)

    def __repr__(self):
        return "DirectoryNode : {}".format(self.name)

    def __len__(self):
        return len(self._child)

    def __contains__(self, item):
        if isinstance(item, str):
            for a in self:
                if a.name == item:
                    return True
            return False
        else:
            for a in self:
                if a.name == item.name:
                    return True
            return False

    def exist(self, file):
        return file in self

    def find_by_name(self, name):
        for a in self:
            if a.name == name:
                return a
        return None

    def add(self, file):
        if self._ro:
            raise Exception("Directory in Read Only mode !")

        if not isinstance(file, AbstractNode):
            raise TypeError

        if isinstance(file, DirectoryNode) and self.parent is not None:
            raise Exception("This Directory is not Root directory. Can add directory to child")

        if file not in self:
            self._child.append(file)
            file._dir = self

    def remove(self, file):
        if self._ro:
            raise Exception("Directory in Read Only mode !")

        if file in self:
            if isinstance(file, str):
                remove = self.find_by_name(file)
            elif isinstance(file, AbstractNode):
                remove = file
            else:
                raise TypeError

            remove._dir = None
            self._child.remove(remove)
        else:
            raise KeyError

    def __iadd__(self, other):
        self.add(other)
        return self

    def __isub__(self, other):
        self.remove(other)
        return self

    def __getattr__(self, item):
        return self.find_by_name(item)

    def __delattr__(self, item):
        self.remove(item)

    def __getitem__(self, item):
        if item in self:
            return self.find_by_name(item)
        else:
            raise KeyError

    def __delitem__(self, key):
        self.remove(key)


class FileNode(AbstractNode):
    def __init__(self, device, filename, directory=None, filesize=0, data_type=b"00", group_name=""):
        super().__init__(filename, directory)

        self._device = None
        self.device = device

        self._data_type = None
        self._group_name = None

        if self.device == Devices.MCS:
            self.data_type = data_type
            self.group_name = group_name

        self.size = filesize

    @property
    def data_type(self):
        if self.device == Devices.MCS:
            return self._data_type
        else:
            raise Exception("MCS Files don't have data_type field")

    @data_type.setter
    def data_type(self, data):
        if self.device == Devices.MCS:
            if len(data) < 2:
                raise ValueError
            else:
                self._data_type = data[0:2]
        else:
            raise Exception("MCS Files don't have data_type field")

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device):
        self._device = device

    def __repr__(self):
        if self.device == Devices.MCS:
            return "[Device : MCSStorage] File : {} (Data Type : {}), Size : {}, Parent : {}" \
                .format(self.name, self.data_type, self.size, self.parent.name)
        else:
            return "[Device : {}] File : {}, Size : {}, Parent : {}" \
                .format(self.device.name, self.name, self.size, self.parent.name)

    @property
    def group_name(self):
        if self.device == Devices.MCS:
            return self._group_name
        else:
            raise Exception("MCS Files don't have data_type field")

    @group_name.setter
    def group_name(self, data):
        if self.device == Devices.MCS:
            self._group_name = data
        else:
            raise Exception("MCS Files don't have group_name field")
