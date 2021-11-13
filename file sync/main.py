import os
import shutil
import logging
import argparse
from time import sleep


class SyncDir:

    def __init__(self, source, replica):
        self.source = os.path.normpath(source)
        self.root_source = source
        self.replica = os.path.normpath(replica)
        self.root_replica = replica
        self.logger = logging.getLogger('Directory synchronization')
        self.logger.setLevel(logging.INFO)
        self.fh = logging.FileHandler(filename=f'{__file__}.log'.replace('.py', ''), encoding='utf8')
        self.fh.setLevel(logging.INFO)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.ch.setFormatter(self.formatter)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)
        self.sync_dir()

    def sync_dir(self):
        list_dir_replica = [j.name for j in os.scandir(self.replica) if j.is_dir()]
        list_dir_source = [j.name for j in os.scandir(self.source) if j.is_dir()]

        list_files_replica = [j.name for j in os.scandir(self.replica) if j.is_file()]
        list_files_source = [j.name for j in os.scandir(self.source) if j.is_file()]

        for j in set(list_dir_replica).difference(list_dir_source):
            shutil.rmtree(os.path.join(self.replica, j))
            self.logger.info(fr'Удалил папку {os.path.join(self.replica, j)}')

        for j in set(list_files_replica).difference(list_files_source):
            os.remove(os.path.join(self.replica, j))
            self.logger.info(fr'Удалил Файл {os.path.join(self.replica, j)}')

        for i in os.scandir(self.source):
            new_path = os.path.join(self.root_replica, i.path.replace(f'{self.root_source}\\', ''))
            if i.is_dir():
                path_for_list_dir = os.path.join(self.root_replica, i.path.replace(f'{self.root_source}\\', '').replace(i.name, ''))
                list_dir = [j.name for j in
                            os.scandir(path_for_list_dir)]

                new_path = os.path.join(self.root_replica, i.path.replace(f'{self.root_source}\\', ''))

                if i.name not in list_dir:
                    new_path = os.path.join(self.root_replica, i.path.replace(f'{self.root_source}\\', ''))
                    os.mkdir(new_path)
                    self.logger.info(fr'Создал папку {new_path}')
                    self.replica = new_path

                self.replica = new_path
                self.source = i.path
                self.sync_dir()

            elif i.is_file():
                path_file_replica = new_path

                if os.path.isfile(path_file_replica):
                    stat_source_file = [os.stat(i).st_mtime, os.stat(i).st_size,
                                        os.stat(i).st_dev, os.stat(i).st_mode]
                    stat_replica_file = [os.stat(path_file_replica).st_mtime,
                                         os.stat(path_file_replica).st_size,
                                         os.stat(path_file_replica).st_dev,
                                         os.stat(path_file_replica).st_mode]
                    if stat_source_file != stat_replica_file:
                        shutil.copy2(i, i.path.replace(f'{self.root_source}', f'{self.root_replica}'))
                        self.logger.info(fr'Скопировал файл {i.path.replace(f"{self.root_source}", f"{self.root_replica}")}')
                else:
                    shutil.copy2(i, i.path.replace(f'{self.root_source}', f'{self.root_replica}'))
                    self.logger.info(fr'Скопировал файл {i.path.replace(f"{self.root_source}", f"{self.root_replica}")}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Directory synchronization')
    parser.add_argument('-source')
    parser.add_argument('-replica')
    parser.add_argument('-interval', type=int, default=20)
    args = parser.parse_args()
    while True:
        SyncDir(source=args.source, replica=args.replica)
        sleep(args.interval)
