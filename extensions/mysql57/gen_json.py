import json
from typing import Text
from argparse import ArgumentParser


# read query result
def get_input():
    inputs = []
    while True:
        try:
            inputs.append(input())
        except EOFError:
            return inputs


# parse query result to dict
def parse_columns(lines):
    columns = None
    defs = [None for i in range(len(lines) - 1)]
    # get column definitions
    columns = lines[0].split('\t')
    for i in range(1, len(lines)):
        attrs = lines[i].split('\t')
        d = {}
        for i in range(len(attrs)):
            d[columns[i]] = attrs[i]
        # order by ORDINAL_POSITION
        defs[int(d['ORDINAL_POSITION']) - 1] = d
    return defs


# ex) int(10) -> int, 10
def parse_col_type(v):
    kind = None
    length = 0
    if v == 'text' or v == 'blob':
        kind = 'varchar'
        length = 100
        return kind, length
    elif v == 'datetime':
        kind = 'datetime'
        length = 1
        return kind, length
    else:
        kind, length = v.split('(')
        return kind, int(length.rstrip(')'))


def date_def():
    return {
        "type": "sequence",
        "symbols": ["Y", "M", "D"],
        "separator": "-",
        "Y": {
            "type": "int",
            "min": 1990,
            "max": 2030
        },
        "M": {
            "type": "int",
            "min": 1,
            "max": 12,
            "digits": 2
        },
        "D": {
            "type": "int",
            "min": 1,
            "max": 28,
            "digits": 2
        }
    }


def datetime_def():
    return {
        "type": "sequence",
        "symbols": ["date", "T", "time"],
        "separator": "",
        "date": {
            "type": "sequence",
            "symbols": ["Y", "M", "D"],
            "separator": "-",
            "Y": {
                "type": "int",
                "min": 1990,
                "max": 2030
            },
            "M": {
                "type": "int",
                "min": 1,
                "max": 12,
                "digits": 2
            },
            "D": {
                "type": "int",
                "min": 1,
                "max": 28,
                "digits": 2
            }
        },
        "T": {
            "type": "set",
            "candidates": ["T"]
        },
        "time": {
            "type": "sequence",
            "separator": ":",
            "symbols": ["h", "m", "s"],
            "h": {
                "type": "int",
                "min": 0,
                "max": 23,
                "digits": 2
            },
            "m": {
                "type": "int",
                "min": 0,
                "max": 59,
                "digits": 2
            },
            "s": {
                "type": "int",
                "min": 0,
                "max": 59,
                "digits": 2
            }
        }
    }

def decimal_def():
    pass

def gen_dg_input(kind, length, nullable, key):
    d = {}

    if kind == 'int' or kind == 'bigint':
        d['type'] = 'int'
        d['max'] = 10**6
        d['min'] = 0
    elif kind == 'tinyint':
        d['type'] = 'int'
        d['max'] = 1
        d['min'] = 0
    elif kind == 'varchar':
        d['type'] = 'list'
        d['length'] = length
        d['separator'] = ''
        values = {}
        values['type'] = 'char'
        values['min'] = 'a'
        values['max'] = 'z'
        d['values'] = values
    elif kind == 'datetime':
        d = datetime_def()
    elif kind == 'date':
        d = date_def()
    elif kind == 'decimal':
        d = decimal_def()
    return d


def gen_dg_input_from_def(col_def):
    kind, length = parse_col_type(col_def['COLUMN_TYPE'])
    length = length
    nullable = True if col_def['IS_NULLABLE'] == 'YES' else False
    key = col_def['COLUMN_KEY']
    return gen_dg_input(kind, length, nullable, key)


def gen_json(lines, length):
    col_defs = parse_columns(lines)
    d = {'type': 'table', 'length': length, 'separator': '\n', 'symbolSeparator': ','}
    d['symbols'] = [col_def['COLUMN_NAME'] for col_def in col_defs]
    for col_def in col_defs:
        d[col_def['COLUMN_NAME']] = {}
        d[col_def['COLUMN_NAME']]['values'] = gen_dg_input_from_def(col_def)
    uniq_keys = {}
    for col_def in col_defs:
        if col_def['UNIQ_KEYS'] != 'NULL':
            key_names = col_def['UNIQ_KEYS'].split(',')
            for key_name in key_names:
                if key_name not in uniq_keys:
                    uniq_keys[key_name] = [col_def['COLUMN_NAME']]
                else:
                    uniq_keys[key_name].append(col_def['COLUMN_NAME'])
    d['uniqueKeys'] = [uniq_keys[key] for key in uniq_keys]
    print(json.dumps(d))


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument('-l', '--length', type=int, default=100, help='Specify record length')
    args = argparser.parse_args()
    gen_json(get_input(), args.length)
