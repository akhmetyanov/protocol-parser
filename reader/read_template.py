from datetime import datetime
import os, json, codecs

def read_template(lab: str, name: str) -> json:
    dir_name = os.path.dirname(__file__)
    path = dir_name + '/templates/' + lab + r'//' + name + '.JSON'
    teamplte = json.load(codecs.open(path, 'r', 'utf-8-sig'))
    return teamplte

def template_to_mask(word: str):
    word = word.replace('0', 'X')
    word = word.replace('1', 'X')
    word = word.replace('2', 'X')
    word = word.replace('3', 'X')
    word = word.replace('4', 'X')
    word = word.replace('5', 'X')
    word = word.replace('6', 'X')
    word = word.replace('7', 'X')
    word = word.replace('8', 'X')
    word = word.replace('9', 'X')
    return word


def str_to_date(s_date: str):
    if (s_date == None): return None
    if '/' in s_date:
        try:
            _date = datetime.strptime(s_date, '%d/%m/%Y')
        except:
            _date = datetime.strptime(s_date, '%m/%d/%Y')
    if '.' in s_date: _date = datetime.strptime(s_date, '%d.%m.%Y')
    return _date