import os
from random import randint
from datetime import date

def run(days, prefix="", year=2020):
    start_ordinal = date.today().replace(day=1,month=1, year=year).toordinal()
    end_ordinal = date.today().replace(day=30,month=12, year=year).toordinal()
    cnt = 0
    res = []
    while cnt<days:
        day = randint(start_ordinal, end_ordinal)
        file_name = prefix + date.fromordinal(day).strftime("%Y%m%d") + ".txt"
        if file_name in res:
            continue
        with open(file_name, "w") as f_obj:
            f_obj.write("log")
        res.append(file_name)
        cnt+=1

if __name__ == "__main__":
    run(10,"")




