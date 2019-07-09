import csv
class DcmTagDictionary:
    def __init__(self):
        self.tagDict = {}
        with open('./app/utilities/dcm_tags_tab_sep.txt', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                tagHex = row[0].strip().replace('(','').replace(')','').replace(',','')
                tagTxt = row[1].strip().replace(' ','_')
                if tagHex in self.tagDict:
                    print('Duplicate key:' + tagHex)
                else:
                    self.tagDict[tagHex] = tagTxt
                if tagTxt in self.tagDict:
                    print('Duplicate key:' + tagTxt)
                else:
                    self.tagDict[tagTxt] = tagHex
    def convert(self,txt):
        if txt in self.tagDict:
            return self.tagDict[txt]
        else:
            return None
