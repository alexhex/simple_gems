# -*-coding:utf-8-*-

# Alexhex 12-29-2021


import sqlite3

from files import *


class SqlTable():

    def __init__(self):
        db_file_path = make_here('db.sqlite')
        self.conn = sqlite3.connect(db_file_path)
        self.cc = self.conn.cursor()
        # self.c_cmmd = 'jREATE TABLE {tn}'

    def create_assy_table(self):
        self.cc.execute("CREATE TABLE {tn} ({nf} {ft} auto_increment)".format(
            tn='assemblies', nf='id', ft='INTEGER'))

    def read_assy_table(self):
        pass

    def update_assy_table(self, lod):
        pass

    def delete_assy_table(self):
        pass


my_sql = SqlTable()
my_sql.create_assy_table()
