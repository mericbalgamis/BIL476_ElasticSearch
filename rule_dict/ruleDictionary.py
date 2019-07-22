import json
class RuleDictionary:

    def __init__(self,rule_path):
        with open(rule_path, 'r') as json_file:
            rule = json.load(json_file)
            self.indList = rule["individual_rules"]
            self.pkgList = rule["bulk_rules"]

    def findInInd(self,subset_id,rule_id):
        for i in self.indList:
            if i["rule_subset"]["subset_id"] == subset_id:
                for ii in i["rules"]:
                    if ii["rule_id"] == rule_id:
                        return ii
        return {"rule_id": "NotExists","rule_name": "NotExists","rule": "NotExists"}

    def findInPkg(self,subset_id,rule_id,type):
        for i in self.pkgList:
            if i["rule_subset"]["subset_id"] == subset_id:
                for ii in i[type]:
                    if ii["rule_id"] == rule_id:
                        return ii
        return {"rule_id": "NotExists","rule_name": "NotExists","rule": "NotExists"}
