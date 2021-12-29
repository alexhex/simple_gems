# -*-coding:utf-8-*-
# 19-Dec-2021, XNiu2

import re
import csv
# import collections


assy_level = 2
cmpnt_level = 3

features = ['Drawing', 'Material', 'QCP', 'Coating', 'NDE', 'CIS']


class RawTable:
    'RawTable reads the file and discard the lines out of the table'

    def __init__(self):
        self.table = []

    # The original csv file is exported from GeMS, make_table will discard the file head.
    def make_table(self, path):
        with open(path, 'r', newline='', errors='ignore') as header:
            head = header.readlines()
            for i in range(len(head)):
                if re.match(r'Level,', head[i]):
                    break
            self.table = head[i:]
            # print (self.table)

    def return_table(self):
        return self.table if self.table else None


class ValConverter:
    'ValConverter is to convert the string values into the correct type of variables.'

    def convert(self, typ, *args):
        func_name = 'convert_' + '_'.join(typ.lower().split(' '))
        method = getattr(self, func_name, None)
        if hasattr(method, '__call__'):
            return method(*args)
        else:
            return self.convert_none(*args)

    def convert_none(self, val):
        return val

    def convert_qty(self, val):
        return float(re.sub(r'[=\"\']', '', val)) if val else 0

    def convert_item_number(self, val):
        # print (val)
        return int(re.sub(r'\D', '', val)) if val else 0

    def convert_level(self, val):
        return int(re.sub(r'\D', '', val)) if val else 0

    # def convert_usage(self, val):

    def short_description(self, val):

        short_desc_list = []
        # assy = re.compile(r'(\d-?')
        component_1 = r'([\w ]*?,[ ]*[\w\- ]*?),[ ]*\d'
        component_2 = r'([\w ]*?),[ ]*\d'
        component_3 = r'([\w ]*?),'
        oring = r'(O-RING).*#(\d\d\d)'
        bur = r'(BACK-UP).*#(\d\d\d)'
        shear_screw = r'.*SCREW.*SHEAR.*'
        screw = r'.*SCREW.*'
        short_desc = ''
        # return val

        fetch_object = re.search(bur, val)
        if fetch_object:
            str_2 = fetch_object.group(2)
            short_desc = f'BUR #{str_2}'
            return short_desc

        fetch_object = re.search(oring, val)
        if fetch_object:
            str_2 = fetch_object.group(2)
            short_desc = f'O-RING #{str_2}'
            return short_desc

        fetch_object = re.search(shear_screw, val)
        if fetch_object:
            short_desc = 'SHEAR SCREW'
            return short_desc

        fetch_object = re.search(screw, val)
        if fetch_object:
            short_desc = 'SCREW'
            return short_desc

        short_desc_list = re.findall(component_1, val)
        if not short_desc_list:
            short_desc_list = re.findall(component_2, val)
        if not short_desc_list:
            short_desc_list = re.findall(component_3, val)
        if not short_desc_list:
            short_desc = val
        else:
            short_desc_list = short_desc_list[0].split(', ')
            short_desc_list.reverse()
            short_desc_list = list(map(lambda i: i.strip(), short_desc_list))
            try:
                short_desc = ' '.join(short_desc_list)
            except:
                short_desc = short_desc_list[0]

        return short_desc


class Ebom:
    'Ebom is to convert the RawTable to a true BOM structure'

    def __init__(self, table, converter):
        self.ebom = []
        self.ebom_depth = 0
        self.rawtable = table.return_table()
        self.converter = converter
        self.assy_level = 0
        self.cmpnt_level = 0

    def make_ebom(self):
        # self.ebom would be a list of OrderedDict.
        self.ebom = list(csv.DictReader(self.rawtable))
        for row in self.ebom:
            for typ in row.keys():
                try:
                    row[typ] = self.converter.convert(typ, row[typ])
                except KeyError:
                    pass

        # Below is to add a column called "Parent Name" to record the parent_id
        # The lowerest ebom level in file is 1 not 0.
        # This can only be done after value conversion as level is an integer and was a text.
        self.ebom_depth = max([row['Level'] for row in self.ebom])
        id_group = [0] * self.ebom_depth
        for row in self.ebom:
            id_group[row['Level'] - 1] = row['Name']
            try:
                row['Parent Name'] = id_group[row['Level'] - 2]
            except:
                row['Parent Name'] = 'NA'
        # print (self.ebom_depth)

    def filter_ebom(self, level, parent='', usage=''):
        # return [(row['Name'], row['Qty']) for row in self.ebom if row['Level'] == level]
        if (not usage) and (not parent):
            return [row for row in self.ebom if (row['Level'] == level)]
        elif (usage and not parent):
            return [row for row in self.ebom if (row['Level'] == level and row['Usage'] == usage)]
        elif (parent and not usage):
            return [row for row in self.ebom if (row['Level'] == level and row['Parent Name'] == parent)]
        else:
            return [row for row in self.ebom if (row['Level'] == level and row['Parent Name'] == parent and row['Usage'] == usage)]

    def phantom_item(self, pn):

        for part_number in pn:

            phantom_flag = False
            current_level = self.ebom_depth
            current_parent = [0] * self.ebom_depth
            # current_parent = []

            for item in self.ebom:
                if phantom_flag == False:
                    if item['Name'] == part_number:
                        current_level = item['Level']
                        current_parent[0] = item['Parent Name']
                        self.ebom.remove(item)
                        # item['Phantom Flag'] = True
                        phantom_flag = True
                        # break
                else:
                    if item['Level'] > current_level:
                        level_diff = item['Level'] - current_level
                        item['Level'] = item['Level'] - 1
                        item['Parent Name'] = current_parent[level_diff-1]
                        current_parent[level_diff] = item['Name']

                    else:
                        phantom_flag = False
                        break

    def return_ebom(self):
        return self.ebom if self.ebom_depth else None


class Checker:
    'to check if the object is some type of document'

    def is_object(self, typ, *args):
        func_name = 'is_part_' + typ.lower()
        method = getattr(self, func_name, None)
        if hasattr(method, '__call__'):
            return method(*args)
        else:
            return self.is_none(*args)

    def is_none(self, line):
        return None

    def is_part_drawing(self, line):
        typ = r'(ProE Drawing|CAD Drawing)'
        # if line['Usage'] == 'Described By' and re.match(typ, line['Type']):
        if line['Document Usage'] == 'Described By' and re.match(typ, line['Type']):
            return True
        return False

    def is_part_material(self, line):
        typ = r'(Material Specification List|Metal Material Specification|Metallic Material Specifications)'
        if re.match(typ, line['Type']) or re.match('MDS', line['Name']):
            return True
        return False

    def is_part_nde(self, line):
        typ = r'NDE'
        if re.match(typ, line['Name']):
            return True
        return False

    def is_part_cis(self, line):
        typ = r'CIS'
        if re.match(typ, line['Name']):
            return True
        return False

    def is_part_coating(self, line):
        typ = r'CSP'
        if re.match(typ, line['Name']):
            return True
        return False

    def is_part_qcp(self, line):
        typ = r'Quality Control Plan'
        if re.match(typ, line['Type']):
            return True
        return False


class Attributer:
    'to assign the attributes to one specific column to specify if it is specific type of doc'

    def __init__(self, ebom, val_checker):
        self.ebom = ebom
        self.checker = val_checker

    def attribute(self):
        # Give attributes to each component
        parts = self.ebom.filter_ebom(cmpnt_level, '', 'Uses')

        for part in parts:
            lines = self.ebom.filter_ebom(cmpnt_level + 1, part['Name'])
            for attr in features:
                part[attr] = set()
                for line in lines:
                    if self.checker.is_object(attr, line):
                        part[attr].add(line['Name'])


class Comparer:
    def __init__(self, base, ref, resultpath):
        self.base = base
        self.ref = ref
        self.resultpath = resultpath

        self.base_parts = self.base.filter_ebom(cmpnt_level, '', 'Uses')
        self.ref_parts = self.ref.filter_ebom(cmpnt_level, '', 'Uses')

        self.result = []
        self.head = ['Item Number', 'New Packer',
                     'Ref Packer', 'Short Description', 'Comments']

        with open(self.resultpath, 'w', newline='') as resulthandle:
            resultwriter = csv.DictWriter(resulthandle, self.head)
            resultwriter.writeheader()

    def compare(self):
        # The comparison logic is:
        # 1. Try finding the the same part number;
        # 2. If not, try finding the part with the same drawing;
        # 3. If not, try finding the part with the same item number;
        # 4. If not
        for base_part in self.base_parts:
            found_mark = False
            for ref_part in self.ref_parts:
                if base_part['Name'] == ref_part['Name']:
                    self.add_note(base_part, ref_part)
                    found_mark = True
                    break
                elif (base_part['Drawing'] == ref_part['Drawing'] and base_part['Drawing'] != set()):
                    self.add_note(base_part, ref_part, True)
                    found_mark = True
                    break

            if not found_mark:
                for ref_part in self.ref_parts:
                    if base_part['Item Number'] == ref_part['Item Number']:
                        found_mark = True
                        self.add_note(base_part, ref_part, True)
                        break

            if not found_mark:
                self.add_note(base_part)

        with open(self.resultpath, 'w', newline='') as resulthandle:
            resultwriter = csv.DictWriter(resulthandle, self.head)
            resultwriter.writerows(self.result)

    # This is to compare the component to component.

    def add_note(self, base_part, ref_part=None, typ=False):
        line = {
            'Item Number': base_part['Item Number'],
            'New Packer': base_part['Name'],
            'Short Description': self.base.converter.short_description(base_part['Description']),
            'Comments': ''
        }

        # When no corresponding part is found, a note will be directly marked "not found"
        if ref_part is None:
            line['Ref Packer'] = 'NA'
            line['Comments'] = 'No corresponding part'
            self.result.append(line)
            return True
        else:
            line['Ref Packer'] = ref_part['Name']

        base_val, ref_val = ['', '']
        if not typ:
            if base_part['Qty'] == ref_part['Qty']:
                line['Comments'] = 'Perfect'
                self.result.append(line)
                return True
            else:
                base_val, ref_val = [base_part['Qty'], ref_part['Qty']]
                line['Comments'] = f'Qty changed from {ref_val} to {base_val}\n'
                self.result.append(line)
                return True

        for attr in features:
            if base_part[attr] != ref_part[attr]:
                base_val = ' and '.join(list(base_part[attr]))
                if base_val == '':
                    base_val = 'None'
                ref_val = ' and '.join(list(ref_part[attr]))
                if ref_val == '':
                    ref_val = 'None'
                new_comment = f'{attr} changed from {ref_val} to {base_val}\n'
                line['Comments'] += new_comment

        self.result.append(line)
        return True


# table_1 = RawTable()
# table_2 = RawTable()

# folderpath = os.path.dirname(os.path.abspath(__file__))
# fullpath_1 = os.path.join(folderpath, 'base.csv')
# fullpath_2 = os.path.join(folderpath, 'ref.csv')
# fullpath_3 = os.path.join(folderpath, 'common.csv')

# table_1.make_table(fullpath_1)
# table_2.make_table(fullpath_2)

# my_converter = ValConverter()
# my_checker = Checker()


# base_ebom = Ebom(table_1, my_converter)
# base_ebom.make_ebom()

# base_assigner = Attributer(base_ebom, my_checker)
# base_assigner.attribute()

# ref_ebom = Ebom(table_2, my_converter)
# ref_ebom.make_ebom()

# ref_assigner = Attributer(ref_ebom, my_checker)
# ref_assigner.attribute()

# my_comparer = Comparer(base_ebom, ref_ebom, fullpath_3)
# my_comparer.compare()
