import ctypes
import time
from threading import Thread
import os
import sys
import subprocess
import datetime


SERVER_BASE_PATH = r"D:\..main"


def full_ssd_backup():
    directories_all = os.walk(SERVER_BASE_PATH)

    directory_list = []
    files_all = []
    server_data = []
    for directory in directories_all:
        directory_list.append(os.path.join(SERVER_BASE_PATH, directory[0]))

    for folder in directory_list:
        entities_in_folder = os.listdir(folder)

        for entity in entities_in_folder:
            entity = os.path.join(folder, entity)
            print(entity)
            if os.path.isfile(entity):
                files_all.append(entity)

    for file in files_all:
        size = os.path.getsize(file)
        server_data.append((file, size))

    print(server_data)




full_ssd_backup()


def full_ssd_backup_check():
    time_now = datetime.datetime.now()
    weekday = time_now.weekday()

    if weekday == 6:
        if time_now.hour == datetime.datetime(year=1, month=1, day=1, hour=23).hour:
            pass

