import psutil
import json
import argparse
import os
import time


def get_stats(fp, second):
    fp = os.path.normpath(fp)
    pid_file = psutil.Popen(fp, shell=True).pid
    p = psutil.Process(pid_file)
    backslash = '\\'
    file_name = fr"{time.time()}_{fp.split(backslash)[-1].split('.')[0]}.json"
    exp = []
    while True:
        dict_exp = {}
        with p.oneshot():
            try:
                fa = open(file=file_name, mode='w')
                json.dump(exp, fa, sort_keys=False, indent=4)
                fa.close()

                fo = open(file=file_name, mode='r')
                exp = json.load(fo)
                fo.close()
            except FileNotFoundError:
                fw = open(file=file_name, mode='w')
                fw.close()

            time.sleep(second)
            cpu_percent = p.cpu_percent()
            dict_exp.update({'cpu_percent': cpu_percent})
            working_set = p.memory_info()[4]
            dict_exp.update({'working_set': working_set})
            private_bytes = p.memory_info()[-1]
            dict_exp.update({'private_bytes': private_bytes})
            count_handles = p.num_handles()
            dict_exp.update({'count_handles': count_handles})
            exp.append(dict_exp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Collecting statistics')
    parser.add_argument('-fp')
    parser.add_argument('-interval', type=int)
    args = parser.parse_args()
    get_stats(fp=args.fp, second=args.interval)
