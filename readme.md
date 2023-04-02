## Module Class List

```python
# bom_cl.py

class ValConverter
# to convert text into the correct value type \
	def convert_xxx(val)
    
class Checker
# to check if a document is ....
	def is_part_xxx(line)

class Ebom
# to add relationship to line of records
    def __init__(self, val_converter)
    def make_ebom()
    	add column ['Parent Name', 'Used in Assy', 'Children', 'AC Level']
    def phantom_item(pn)
    def filter_ebom(level, parent, usage)
    # Rewrite this one as level is not needed...
    def return_ebom()
	
class Attributer()
	def __init__(self, ebom, checker)
	def attribute()
    	
	

class Comparer(base, ref,)

# parts.py

class Part

class Assy(Part)
class TopAssy(Assy)
class SubAssy(Assy)
class Cmpnt(Part)


# db.py
# !TBD



# files.py
def make_full_path_here(filename)
class FileFinder()
class TableWriter()
class LineReader()



```

Assy_Table

| Assy Name | Rev  | Family | Children | Description | Assy Drawing |
| --------- | ---- | ------ | -------- | ----------- | ------------ |
|           |      |        |          |             |              |



Cmpnt_Table

| Cmpnt Name | Rev  | Family | Used in Assy | Description |  Features    |
| --------- | ---- | ------ | -------- | ----------- | ---- |
|           |      |        |          |             |      |

BOM_Table

| ID   | Assy | Cmpnt | Qty  | Item Number |      |
| ---- | ---- | ----- | ---- | ----------- | ---- |
|      |      |       |      |             |      |
