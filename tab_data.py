# -*-coding:utf-8-*-

# Alexhex 12-29-2021

import re


class Tab_Data():

    def __init__(self):
        self.rawdata = ''
        self.data = []
        self.tab_data = {}

    def get_rawdata(self, data):
        self.rawdata = data

    def sort_tab_data(self):
        if not self.rawdata:
            return None
        else:
            self.data = self.rawdata.split('|')
            for line in self.data:
                vals = line.split('=')
                if len(vals) != 2:
                    return None
                else:
                    [attr, val] = [x.strip() for x in vals]
                    self.tab_data[attr] = val

    def filter_tab_data(self, pttrn):
        # new_dict = {}
        # for (key, value) in self.tab_data.items():
        #     if re.search(pttrn.upper(), key):
        #         new_dict[key] = value
        # return new_dict

        # the above codes are equal to the line below:

        return dict(filter(lambda elem: re.search(pttrn.upper(), elem[0]), self.tab_data.items()))


def sort_tab_data(data, pttrns):
    lines = data.split('\r\n')
    results = []

    for attribute in lines:
        for pattern in pttrns:
            if re.search(pattern, attribute):
                vals = attribute.split('=')
                vals = [x.strip() for x in vals]
                results.append(vals)

    return results


test_str = "ACTIVE FLOW WETTED MATERIAL - YIELD STRENGTH (KSI) = 41XX[80]			|APPROXIMATE WEIGHT (LBS) = 2000			|EXTERNAL WORKING PRESSURE (PSI) - AT SPECIFIED TEMP (F) = 5000[350]			|I.D. - DRIFT (IN) = 6.151			|I.D. - MIN. (IN) = 6.187			|I.D. (IN) = 6.200			|INTERNAL WORKING PRESSURE (PSI) - AT SPECIFIED TEMP (F) = 5000[350]			|LOWER THREAD CONNECTING - SIZE (IN), WT (PPF), TYPE, CONFIG = NA			|MAKE-UP LENGTH (IN) = 711.6			|MATERIAL/VEE PACKING = PTFE, PEEK			|MATERIAL/O-RING(S) = VITON			|MAX. WORKING TEMPERATURE (DEG.F) = 350			|MIN. WORKING TEMPERATURE (DEG.F) = 100			|O.D. - MAX. (IN) = 8.400			|OVERALL LENGTH (IN) = 711.6|LATCH SEAL SIZE (IN) = 7.75|LOWER STINGER SEAL SIZE (IN) = 7.00			|QUALITY CONTROL PLAN - QCP = SLB STANDARD			|RETRIEVAL METHOD = STRAIGHT PULL			|SERVICE NACE (YES/NO) = YES			|TENSILE STRENGTH (LBS) - AT SPECIFIED TEMP (F) = 300000[350]|COMPRESSION  STRENGTH (LBS) - AT SPECIFIED TEMP (F) = 120000[350]			|TORQUE CAPACITY - (FT-LBS) = 5500[350]			|UPPER THREAD CONNECTING - SIZE (IN), WT (PPF), TYPE, CONFIG = NA"


my_tb = Tab_Data()
my_tb.get_rawdata(test_str)
my_tb.sort_tab_data()
print(my_tb.filter_tab_data(r'min'))
