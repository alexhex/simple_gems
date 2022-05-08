# -*-coding:utf-8-*-

from bom_cl import *
from files import *

my_file_checker = FileFinder()
file_path = make_here('out.csv')

# my_file_checker.get_fldr(folderpath)
files_lst = my_file_checker.list_files(crrt_folder_path, r'.csv$')

for csvfile in files_lst:
    # my_raw_table = RawTable()
    # my_raw_table.make_table(csvfile)

    my_converter = ValConverter()
    my_checker = Checker()

    my_bom = Ebom(my_converter)
    my_bom.make_ebom(csvfile)
    # my_bom.make_ebom()

    phantom_kits_list = ['103235257', '103235214', '100029390',
                         '103235261', '103235212', '103235208', '103235216', '103235250']
    my_bom.phantom_item(phantom_kits_list)

my_attributer = Attributer(my_bom, my_checker)
my_attributer.attribute()

new_bom = my_bom.filter_ebom(3, '', 'Uses')

my_writer = TablaWriter(file_path, new_bom)
my_writer.write_table()
