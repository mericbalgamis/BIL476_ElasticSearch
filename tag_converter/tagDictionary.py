import csv
import json
class DcmTagDictionary:
    def __init__(self):
        self.tagDict = {}
        self.hexTagDict = {}
        self.txtTagDict = {}
        with open('./app/utilities/dcm_tags_tab_sep.txt', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                tagHex = row[0].strip().replace('(','').replace(')','').replace(',','')
                tagTxt = row[1].strip().replace(' ','_')
                if tagHex in self.tagDict:
                    print('Duplicate key:' + tagHex)
                else:
                    self.tagDict[tagHex] = tagTxt

                if tagHex in self.hexTagDict:
                    print('Duplicate key:' + tagHex)
                else:
                    self.hexTagDict[tagHex] = tagTxt

                if tagTxt in self.tagDict:
                    print('Duplicate key:' + tagTxt)
                else:
                    self.tagDict[tagTxt] = tagHex

                if tagTxt in self.txtTagDict:
                    print('Duplicate key:' + tagTxt)
                else:
                    self.txtTagDict[tagTxt] = tagHex

    def convert(self,txt):
        if txt in self.tagDict:
            return self.tagDict[txt]
        else:
            return None

    def convertJsonToTxtTag(self,input_path,output_path):
        with open(input_path, 'r') as inputF:
            json_str = inputF.read()
            for key in self.hexTagDict.keys():
                json_str = json_str.replace('\"'+key+'\":','\"'+self.hexTagDict[key]+'\":')
            with open(output_path, 'w') as outputF:
                outputF.write(json_str)
            del json_str