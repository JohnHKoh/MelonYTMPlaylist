from difflib import SequenceMatcher
import json

SIMILARITY_THREADSHOLD = 0.9

class Util:
    def similar(a, b):
        try:
            return SequenceMatcher(None, a.lower(), b.lower()).ratio() > SIMILARITY_THREADSHOLD
        except:
            return False

    def log(string, level = 1):
        dash_prefix = "--" * (level - 1)
        separator = "" if level == 1 else " "
        print("{}{}{}".format(dash_prefix, separator, string))

    def get_config():
        f = open('../config.json')
        return json.load(f)

    def get_manual_fixes():
        f = open('../data/manual_fixes.json', 'r', encoding='utf-8')
        return json.load(f)
