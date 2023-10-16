# -*- coding: utf-8 -*-
# @Time: 2023-03-31 14:43
# Description: Info基类

from datetime import datetime
from bson import ObjectId


class InfoBase(object):
    """
    Info类的基类，为其子类提供一些特性
    """
    def __init__(self):
        super(InfoBase, self).__setattr__('raw_info', None)
        super(InfoBase, self).__setattr__('attr_list', [])

    def pop(self, key, default=None):
        """
        删除一个属性。

        :param key: str. 属性名
        :param default: any. 调用pop函数的返回值(原理同dict.pop())
        :return:
        """
        if hasattr(self, key):
            delattr(self, key)
            if key != 'raw_info':
                self.attr_list.remove(key)

        return default

    def get(self, key, default=None):
        """
        获取属性的值。

        :param key: str. 属性名
        :param default: any. 当属性不存在时，返回default。
        :return:
        """
        if hasattr(self, key):
            return getattr(self, key)

        return default

    def keys(self):
        """获取info对象的属性列表"""
        return self.attr_list

    def to_dict(self):
        """
        将Info对象格式转为字典(dict)，用于给前端返回使用
        """
        temp_dict = {}

        for key in self.attr_list:
            # 由于一些类型不可被序列化，所以在返回给前端之前需要对这些类型的数据转为字符串
            if isinstance(self.get(key), datetime) or isinstance(self.get(key), ObjectId):
                value_str = str(self.get(key))
            else:
                value_str = self.get(key)
            temp_dict[key] = value_str

        return temp_dict

    def dict(self):
        '''
        Info对象格式转为字典，并删除value为None的key
        '''
        temp_dict = {}

        for key in self.attr_list:
            # 由于一些类型不可被序列化，所以在返回给前端之前需要对这些类型的数据转为字符串
            if isinstance(self.get(key), datetime) or isinstance(self.get(key), ObjectId):
                value_str = str(self.get(key))
            else:
                value_str = self.get(key)
            if value_str is not None:
                temp_dict[key] = value_str

        return temp_dict

    def to_db(self):
        """
        用于写入数据库时使用。
        和to_dict的主要区别在_id字段，程序中都是str类型，在这一步统一转为ObjectId类型
        :return:
        """
        temp_dict = {key: self.get(key) for key in self.attr_list}

        if temp_dict.get('_id'):
            obj_id = temp_dict['_id']
            # 如果_id有值，且值为ObjectId类型，无需处理。
            # 如果值为非ObjectId类型，需要转化成ObjectId类型
            if isinstance(obj_id, ObjectId):
                pass
            else:
                temp_id = temp_dict.get('_id')
                if ObjectId.is_valid(temp_id):
                    temp_dict['_id'] = ObjectId(temp_id)
                else:
                    temp_dict['_id'] = ObjectId()
        else:
            # 如果_id存在，但是值为空，去掉_id属性
            # 目的是在插入info时，让数据库自动生成ObjectId作为_id
            if '_id' in temp_dict:
                temp_dict.pop('_id')

        return temp_dict

    def update(self, update_data):
        """
        批量更新

        注意，只能更新已存在属性的数据，不能新增属性。

        :param update_data: dict. 更新数据
        :return:
        """
        if not isinstance(update_data, dict):
            raise TypeError("update_data参数类型错误，必须是dict类型")

        for k, v in update_data.item():
            if k in self.attr_list:
                setattr(self, k, v)

    def __setitem__(self, key, value):
        setattr(self, key, value)
        # super().__setitem__(key, value)
        if key != 'raw_info' and key not in self.attr_list:
            self.attr_list.append(key)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)

        return None

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key != 'raw_info' and key not in self.attr_list:
            self.attr_list.append(key)

    def __contains__(self, key):
        if hasattr(self, key):
            return True
        else:
            return False

    def __str__(self):
        # 将属性列表中的各个属性的值都打印出来
        attr_value_dict = {attr_name: getattr(self, attr_name) for attr_name in self.attr_list}
        attr_description = ",\n".join([f"{attr_name}: {attr_value}" for attr_name, attr_value in attr_value_dict.items()])

        return f"""<{self.__class__.__name__} Object: {attr_description}>"""


class UpdateResult:
    """
    更新结果类为分片仿pymongo返回结果
    """
    def __init__(self):
        self.matched_count = 0
        self.modified_count = 0