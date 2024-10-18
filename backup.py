import ctypes
import time
from threading import Thread
import os
import sys
import subprocess
import datetime
import shutil


# SERVER_BASE_PATH = r"C:\..Server"
# SERVER_BACKUP_PATH = r"C:\..Server backup"  # change that to point to D: disc


def get_files_from_directory(directory: str) -> list[tuple[str, int]]:
    """
    Returns the list of all files in chosen directory and its subdirectories.
    :return:
    :param directory:
    :return:
    """
    directories_all = os.walk(directory)

    sub_directory_list = []
    files_all = []
    data = []
    for sub_dir in directories_all:
        sub_directory_list.append(os.path.join(directory, sub_dir[0]))

    for folder in sub_directory_list:
        entities_in_folder = os.listdir(folder)

        for entity in entities_in_folder:
            entity = os.path.join(folder, entity)
            if os.path.isfile(entity):
                files_all.append(entity)

    for file in files_all:
        size = os.path.getsize(file)
        data.append((file, size))
    return data


def backup_directories(server_base_path: str, backup_base_path: str, delete_directories: bool = False,
                       force_delete: bool = False):
    """
    Clones the directories from server to back-up.\n
    This function will always add new directories from server to back-up, but it needs an parameter to delete any
    directories from back-up.\n
    force_delete enables the function to delete the directory with its subdirectories and files.
    :param server_base_path:
    :param backup_base_path:
    :param delete_directories:
    :param force_delete:
    :return:
    """
    if not os.path.isdir(backup_base_path):
        os.makedirs(backup_base_path)

    data_server = os.walk(server_base_path)
    data_backup = os.walk(backup_base_path)
    dirs_server = []
    dirs_backup = []
    dirs_backup_to_delete = []

    for iteration in data_server:
        bases_of_dirs_to_add_to_backup = iteration[0].replace(server_base_path, backup_base_path)

        for dir_name_on_server in iteration[1]:
            dirs_server.append(os.path.join(bases_of_dirs_to_add_to_backup, dir_name_on_server))

    for dir_to_add_to_backup in dirs_server:
        if not os.path.isdir(dir_to_add_to_backup):
            os.makedirs(dir_to_add_to_backup)

    if delete_directories:
        for iteration in data_backup:
            bases_of_dirs_backup = iteration[0]

            for dir_name_backup in iteration[1]:
                dirs_backup.append(os.path.join(bases_of_dirs_backup, dir_name_backup))

        for dir_backup in dirs_backup:
            try:
                dirs_server.remove(dir_backup)
            except ValueError:
                dirs_backup_to_delete.append(dir_backup)

        if force_delete:
            for dir_to_delete in dirs_backup_to_delete:
                shutil.rmtree(dir_to_delete)
            return

        for dir_to_delete in dirs_backup_to_delete:
            try:
                os.rmdir(dir_to_delete)
            except OSError:
                pass
        return


def backup_files(server_base_path: str, backup_base_path: str, delete_files: bool = False):
    data_server = os.walk(server_base_path)
    data_backup = os.walk(backup_base_path)
    files_spared = []
    files_delete = []

    # where 1st str is a path to the file on the server
    #       2nd str is a path to the back-up, where the file is expected to be
    files_to_backup: [tuple[str, str]] = []

    for iteration in data_server:
        base_dir_server = iteration[0]
        base_dir_backup = iteration[0].replace(server_base_path, backup_base_path)

        for file_name in iteration[2]:
            files_to_backup.append((os.path.join(base_dir_server, file_name), os.path.join(base_dir_backup, file_name)))
    print(f'files to backup: {files_to_backup}')

    for file in files_to_backup:
        print(file[1])
        if os.path.exists(file[1]):
            if not os.path.getsize(file[0]) == os.path.getsize(file[1]):
                os.remove(file[1])
                shutil.copyfile(file[0], file[1])
                print(f'Copied\n{file[0]}\nto\n{file[1]}\n')
        else:
            shutil.copyfile(file[0], file[1])

    if delete_files:

        for file in files_to_backup:
            files_spared.append(file[1])

        for iteration in data_backup:
            for file_name in iteration[2]:
                files_delete.append(os.path.join(iteration[0], file_name))

        print(f'delete initial: {files_delete}')
        for file in files_spared:
            try:
                files_delete.remove(file)
            except ValueError:
                pass

        print(f'spared: {files_spared}')
        print(f'delete final: {files_delete}')

















class BackupCommands:
    def __init__(self, server_path: str, backup_path: str):
        self.SERVER_BASE_PATH = server_path
        self.SERVER_BACKUP_PATH = backup_path

    def general_hdd_backup(self):
        if not os.path.isdir(self.SERVER_BACKUP_PATH):
            os.makedirs(self.SERVER_BACKUP_PATH)

        weekday_now = datetime.datetime.now().weekday() + 1
        hour_now = datetime.datetime.now().hour + 1

        # if (weekday_now == 7) and (hour_now == 23):    # !* replace logic after testing
        if ((weekday_now == 7) and (hour_now == 23)) or True:


            data_server = get_files_from_directory(self.SERVER_BASE_PATH)
            data_backup = get_files_from_directory(self.SERVER_BACKUP_PATH)

            backup_files_relative = [file[0].replace(f'{self.SERVER_BACKUP_PATH}\\', '') for file in data_backup]
            server_files_relative = [file[0].replace(f'{self.SERVER_BASE_PATH}\\', '') for file in data_server]

            for index_server, file in server_files_relative:
                if file in backup_files_relative:
                    index_backup = backup_files_relative.index(file)
                    file_size_backup = data_backup[index_backup][1]
                    file_size_server = data_server[index_server][1]

                    if not file_size_backup == file_size_server:
                        os.remove(data_backup[index_backup][0])
            return














if __name__ == '__main__':
    backup = BackupCommands(server_path=r"C:\..Server", backup_path=r"C:\..Server backup")
    # backup.general_hdd_backup()
    backup_directories(server_base_path=r"C:\..Server", backup_base_path=r"C:\..Server backup", delete_directories=True,
                       force_delete=True)
    backup_files(server_base_path=r"C:\..Server", backup_base_path=r"C:\..Server backup", delete_files=True)
