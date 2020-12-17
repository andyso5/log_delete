#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
1. 一个文件只应该有一种命名方式的文件
2. 搜索所有日志文件
3. 日志文件开头都是日期,如20201212.txt，或者~20201212.txt
4. 软件每次启动时运行一次

"""
import os
import re
import json
import time
class ClearLog(object):
    def __init__(self, cnf_path=None):
        self._dir_list = []
        self._file_class = []
        self._limit = 0 # unit is day
        self._compile_obj = re.compile("^~*(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})")
        if not cnf_path:
            cnf_path = self._gen_default_path()
        self._read_cnf(cnf_path)
        self._today_time_tuple = time.localtime()

    def _gen_default_path(self):
        default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        return default_path

    def _read_cnf(self, cnf_path):
        with open(cnf_path) as f_obj:
            cnf_dict = json.load(f_obj)
        self._dir_list = cnf_dict["dir_path"]
        self._file_class = cnf_dict["file_class"]
        self._limit = cnf_dict["limit"]

    def _is_target(self, file_name):
        if file_name.split('.')[-1] not in self._file_class:
            return False
        match_obj = self._compile_obj.search(file_name)
        if not match_obj:
            return False
        if int(match_obj.group("year")) > self._today_time_tuple:
            return False
        if int(match_obj.group("month")) > 12:
            return False
        if int(match_obj.group("month")) > 31:
            return False
        # TODO if a file's name is 20200230, it can't judge
        return True

    def _collect_all_log(self, dir_path):
        # dir_path is abspath
        #chosen_file = []
        day_class = set()

        if not os.path.exists(dir_path):
            print("dir path to clear log dosen't exist")
            return day_class#chosen_file, day_class
        for element in os.listdir(dir_path):
            abs_path = os.path.join(dir_path, element)
            # TODO a dir may exist more than one type log, such as ~20201212.txt and 20201212.txt
            if os.path.isfile(abs_path) and self._is_target(element):
                #chosen_file.append(abs_path)
                print("element: %s" % element)
                day_class.add(element)
                print("updated: %s" %str(day_class))
        return day_class#chosen_file, day_class
    
    def _delete_file(self, day_class):
        day_class = list(day_class)
        day_class.sort(reverse=True) #descent
        delete_days = day_class[self._limit:]
        print("%s"%str(delete_days))
        for file_path in delete_days:
            try:
                os.remove(file_path)
            except:
                print("fail to remove %s" %file_path)

    def run(self):
        # TODO is it neccessary to traverse all sub dir path? 
        for dir_path in self._dir_list:
            day_class = self._collect_all_log(dir_path)
            self._delete_file(day_class)
    
        


