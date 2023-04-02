# -*-coding:utf-8-*-


# Alexhex 12-29-2021

from csv import DictWriter
import os
import re
import shutil

crrt_folder_path = os.path.dirname(os.path.abspath(__file__))


def make_full_path_here(filename):
    filepath = os.path.join(crrt_folder_path, filename)
    return filepath


class FileFinder():

    def __init__(self):
        self.folder = ''
        self.files = []
        self.log = ''
        self.errorlog = ''

    def reset(self):
        self.folder = ''
        self.files = []
        self.log = ''
        self.errorlog = ''

    def get_fldr(self, fldr):
        # self.dest_folder = input("请输入准备寄送的文件夹： "
        self.folder = fldr

    # def get_rsc_fldr(self, fldr):
        # self.res_folder = input("请输入含有所需文件的文件夹：")
        # self.res_folder = fldr

    # 3. Go thru the 2 folders and get a list of the files in each folder;
    def list_files(self, folder, pttrn):
        file_lst = []
        for rootpath, dirs, files in os.walk(folder):
            for name in files:
                # match_obj = re.search(pttrn, name)
                # Case Insensitive
                match_obj = re.search(pttrn, name, re.I)
                if match_obj:
                    # print(os.path.join(rootpath, name))
                    # name = re.sub(r"_Smith", '', name)
                    file_lst.append(
                        os.path.join(rootpath, name))
        return file_lst

    # def get_files_ready(self):
    #     self.pdf_files_to_be_rpl = self.list_pdf_files(
    #         self.dest_folder, r'_Smith.pdf$')
    #     self.pdf_files_resource = self.list_pdf_files(
    #         self.res_folder, r'.pdf$')

    # 4. Go thru the list and search for the replacement file in the B folder;

        # for file_a in self.pdf_files_to_be_rpl:
        #     for file_b in self.pdf_files_resource:
        #         # if the filename without '_smith' is the same with the filename in resource pool, set up a pair
        #         if os.path.basename(re.sub(r'_Smith', '', file_a)).lower() == os.path.basename(file_b).lower():
        #             self.file_pair[file_a] = file_b

    # 5. List the changes to the user and ask for confirmation;

    # def generate_log(self):
    #     for lmnt in self.pdf_files_to_be_rpl:
    #         if lmnt in self.file_pair.keys():
    #             self.log += f'{os.path.basename(lmnt)} would be replaced;\r\n'
    #         else:
    #             self.log += f'{os.path.basename(lmnt)} is NOT found;\r\n'
    #     return (self.log)


# 6. If confirmed, start copying and replacing the files;

    def replace_files(self):
        for key in self.file_pair.keys():
            # Instead of covering the original files, we delete the "Smith" files and make copies of
            # the original files. This would be a hint to the user.
            # shutil.copy(file_pair[key], key)
            shutil.copy(self.file_pair[key], os.path.dirname(key))
            try:
                os.remove(key)
            except OSError as e:
                self.errorlog += f'Error: {key} : {e.strerror}'


class TablaWriter():
    'write a list of dict into a csv file'

    def __init__(self, filepath, lst_dict):

        self.filepath = filepath
        self.lst_dict = lst_dict

    def write_table(self):
        keys = self.lst_dict[0].keys()
        with open(self.filepath, 'w', newline='') as write_handle:
            dict_ww = DictWriter(write_handle, keys)
            dict_ww.writeheader()
            dict_ww.writerows(self.lst_dict)


class LineReader():
    'a generator to read files'

    def __init__(self):
        self.filepath = ''

    def get_fldr(self, filepath):
        self.filepath = filepath

    def read_file(self):
        with open(self.filepath, 'r', newline='') as rd_handle:
            while True:
                line = rd_handle.readline()
                if not line:
                    break
                yield line
