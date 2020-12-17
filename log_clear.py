#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
1. 一个文件夹内日志文件的日期开头只应该存在一种, 如"~20201212..."或"20201212.."
2. 日志文件开头都是日期,如20201212.txt，或者~20201212.txt
3. 非文件名开头连续8位数字非有效日期,或者日期大于当天,排除在外
4. 软件每次启动时运行一次

"""
import os
import re
import json
import datetime
class ClearLog(object):
    def __init__(self, cnf_path=None):
        self._dir_list = []
        self._file_class = []
        self._limit = 0 # unit is day
        self._compile_obj = re.compile("^~*(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<tail>.*)")
        if not cnf_path:
            cnf_path = self._gen_default_path()
        self._read_cnf(cnf_path)
        self.main_path = self._gen_default_target_path()
        self._today = datetime.date.today()

    def _gen_default_path(self):
        default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        return default_path
    
    def _gen_default_target_path(self):
        splits = os.path.abspath(__file__).split(os.path.sep)
        return os.path.sep.join(splits[:-3])

    def relative2abs(self, relative):
        ret = os.path.join(self.main_path, relative)
        if not os.path.exists(ret):
            os.makedirs(ret)
        return ret

    def _read_cnf(self, cnf_path):
        # TODO move config to xyz_app
        # distinguish absdir with relevant dir
        with open(cnf_path) as f_obj:
            cnf_dict = json.load(f_obj)
        self._dir_list = cnf_dict["dir_path"]
        self._file_class = cnf_dict["file_class"]
        self._limit = cnf_dict["limit"]

    def _is_target(self, match_obj):
        if not match_obj:
            return False
 
        if match_obj.group("tail").split('.')[-1] not in self._file_class:
            return False
        #print("file type pass")
        try:
            year = int(match_obj.group("year"))
            month = int(match_obj.group("month"))
            day = int(match_obj.group("day"))
            date_obj = datetime.date(year=year, month=month, day=day)
        except:
            return False
        #print("valid date pass")
        if date_obj>self._today:
            return False
        #print("pass or current date pass")
        return True

    def _collect_all_log(self, dir_path):
        # dir_path is abspath
        ret = {}
        if not os.path.exists(dir_path):
            print("dir path to clear log dosen't exist")
            return ret
        for element in os.listdir(dir_path):
            abs_path = os.path.join(dir_path, element)
            # TODO a dir may exist more than one type log, such as ~20201212.txt and 20201212.txt
            if os.path.isfile(abs_path):
                match_obj = self._compile_obj.search(element)
                if self._is_target(match_obj):
                    key = "{year}{month}{day}".format(year=match_obj.group("year"), month=match_obj.group("month"), day=match_obj.group("day"))
                    ret.setdefault(key,[]).append(element)
                    #print("updated: %s" %str(ret))
        return ret
    
    def _delete_file(self, dir_path, date_dict):
        day_class = list(date_dict.keys())
        day_class.sort(reverse=True) #descent
        delete_days = day_class[self._limit:]
        #print("%s"%str(delete_days))
        for date_str in delete_days:
            for file_path in date_dict[date_str]:
                abs_file_dir = os.path.join(dir_path, file_path)
                try:
                    os.remove(abs_file_dir)
                    print("remove: %s" % abs_file_dir)
                except:
                    print("fail to remove %s" %abs_file_dir)

    def run(self):
        # TODO is it neccessary to traverse all sub dir path? 
        for dir_path in self._dir_list:
            if os.path.isabs(dir_path):
                abs_dir_path = dir_path
            else:
                abs_dir_path = os.path.join(self.main_path, dir_path)
            date_dict = self._collect_all_log(abs_dir_path)
            self._delete_file(abs_dir_path, date_dict)
    
        


def get_today_str(fmt="%Y%m%d"):
    return datetime.date.today().strftime(fmt)

if __name__ == "__main__":
    # print(get_today_str())
    lc = ClearLog()
    s = "~20201212.txt"
    match_obj = lc._compile_obj.search(s)
    print("match_obj: %s" % match_obj.group())
    print(lc._is_target(match_obj))