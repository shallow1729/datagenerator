import copy
from datetime import datetime
import json
import os
import random
import sys
MAX_COLLISION_COUNT = 10


# gen_random_set return one value from candidates
def gen_set(candidates: list, rest: int):
    target = random.randrange(rest)
    result = candidates[target]
    return target, result


def check_jd(jd, required: list):
    for v in required:
        if v not in jd:
            raise Exception("".join([v, " is required\n", json.dumps(jd)]))


def select_data(candidates, length: int, dupf: bool, ordered):
    rest = len(candidates)
    results = []

    if dupf:
        for i in range(length):
            _, result = gen_set(candidates, rest)
            results.append(result)
    else:
        if length > len(candidates):
            raise Exception("".join(["number of candidates is smaller than length\n", json.dumps(jd)]))
        for i in range(length):
            target, result = gen_set(candidates, rest - i)
            results.append(result)
            candidates[target] = candidates[rest - i - 1]

    if ordered is not None:
        if ordered == 'asc':
            results.sort()
        elif ordered == 'desc':
            results.sort(reverse=1)
        else:
            raise Exception("ordered need to be asc or desc\n")
    return results


def execute(func, jd, length: int, dupf: bool, ordered):
    results = []
    d = {}
    counter = 0
    while len(results) < length:
        result = func(jd)
        if result not in d:
            results.append(result)
            if not dupf:
                d[result] = 1
                counter = 0
        else:
            counter += 1
            if counter == MAX_COLLISION_COUNT:
                raise Exception("".join(["duplicated value frequently occur\n", json.dumps(jd)]))

    if ordered is not None:
        if ordered == 'asc':
            results.sort()
        elif ordered == 'desc':
            results.sort(reverse=1)
        else:
            raise Exception("ordered need to be asc or desc\n")

    if len(results) == 1:
        return results[0]
    else:
        return results


def gen_and_merge_list(jd):
    dupf = jd['duplicate'] if 'duplicate' in jd else True
    ordered = jd['ordered'] if 'ordered' in jd else None
    result = gen_data(jd['values'], length=jd['length'], dupf=dupf, ordered=ordered)
    return jd['separator'].join(result)


def gen_and_merge_sequence(jd):
    result = []
    for symbol in jd['symbols']:
        check_jd(jd, [symbol])
        result.append(gen_data(jd[symbol]))
    return jd['separator'].join(result)


def gen_and_merge_table(jd):
    symbols = jd['symbols']
    sep = jd['separator']
    csep = jd['symbolSeparator']
    # parse UniqueKey
    uniqueKeys = []
    if 'uniqueKeys' in jd:
        uniqueKey_defs = jd['uniqueKeys']
        # if uniqueKey is single column, convert to duplicate flag.
        for uniqueKey_def in uniqueKey_defs:
            if len(uniqueKey_def) == 1:
                jd[uniqueKey_def[0]]['duplicate'] = False
        for uniqueKey_def in uniqueKey_defs:
            if len(uniqueKey_def) <= 1:
                continue
            # if unique key is included, the key is unique
            # add only if all part of unique key can duplicate
            if all([jd[symbol]['duplicate'] for symbol in uniqueKey_def]):
                uniqueKeys.append(uniqueKey_def)

    d = {}
    for symbol in symbols:
        check_jd(jd, [symbol])
        check_jd(jd[symbol], ['values'])
        dupf = jd[symbol]['duplicate'] if 'duplicate' in jd[symbol] else True
        ordered = jd[symbol]['ordered'] if 'ordered' in jd[symbol] else None
        d[symbol] = gen_data(jd[symbol]['values'], length=jd['length'], dupf=dupf, ordered=ordered)
    results = []
    uniq_memo = [{} for _ in range(len(uniqueKeys))]
    for i in range(jd['length']):
        # unique key check and regenerate if collide

        # counter count number of collide
        counter = 0
        while True:
            keys = []
            for j in range(len(uniqueKeys)):
                tmp = tuple(d[symbol][i] for symbol in uniqueKeys[j])
                if tmp not in uniq_memo[j]:
                    keys.append(tmp)
                else:
                    # if collide, just regenerate.
                    # unique check is not necessary because each symbol value can duplicate.
                    for symbol in uniqueKeys[j]:
                        d[symbol][i] = gen_data(jd[symbol]['values'], length=1)
                    counter += 1
                    if counter == MAX_COLLISION_COUNT:
                        raise Exception("".join(["duplicated value frequently occur\n", json.dumps(jd)]))
                    break

            if len(keys) == len(uniqueKeys):
                for j in range(len(uniqueKeys)):
                    uniq_memo[j][keys[j]] = 1
                counter = 0
                break

        rec = []
        for symbol in symbols:
            rec.append(d[symbol][i])
        results.append(csep.join(rec))
    return sep.join(results)


def gen_data(jd, length: int = 1, dupf: bool = True, ordered=None):
    check_jd(jd, ['type'])
    t = jd['type']
    if t == 'set':
        check_jd(jd, ['candidates'])
        # use copy to avoid side effect.
        results = select_data(copy.copy(jd['candidates']), length, dupf, ordered)
        if length == 1:
            return results[0]
        else:
            return results

    elif t == 'int':
        candidates = None
        if 'candidates' in jd:
            candidates = jd['candidates']
        else:
            check_jd(jd, ['min', 'max'])
            candidates = [i for i in range(jd['min'], jd['max'] + 1)]
        if length > len(candidates) and not dupf:
            raise Exception("".join(["number of candidates is smaller than length\n", json.dumps(jd)]))
        results = select_data(candidates, length, dupf, ordered)

        if 'digits' in jd:
            results = ['{:02}'.format(i) for i in results]
        else:
            results = [str(i) for i in results]

        if length == 1:
            return results[0]
        else:
            return results

    elif t == 'char':
        candidates = [chr(i) for i in range(ord(jd['min']), ord(jd['max']) + 1)]
        if length > len(candidates) and not dupf:
            raise Exception("".join(["number of candidates is smaller than length\n", json.dumps(jd)]))
        results = select_data(candidates, length, dupf, ordered)

        if length == 1:
            return results[0]
        else:
            return results

    elif t == 'list':
        check_jd(jd, ['length', 'separator', 'values'])
        if 'ordered' in jd and jd['ordered'] not in ['asc', 'desc']:
            raise Exception("".join(["ordered need to be asc or desc\n", json.dumps(jd)]))
        return execute(gen_and_merge_list, jd, length, dupf, ordered)

    elif t == 'sequence':
        check_jd(jd, ['symbols', 'separator'])
        return execute(gen_and_merge_sequence, jd, length, dupf, ordered)

    elif t == 'table':
        check_jd(jd, ['symbols', 'length', 'separator', 'symbolSeparator'])
        return execute(gen_and_merge_table, jd, length, dupf, ordered)


if __name__ == "__main__":
    usage = "".join(["usage: ", sys.argv[0], " ./path/to/target.json"])
    cwd = os.getcwd()
    if len(sys.argv) < 2 or (not sys.argv[1].endswith(".json")):
        raise Exception(("".join(["invalid input.\n", usage])))
    target = sys.argv[1]
    if not os.path.exists(target):
        raise Exception("".join(["target not found.\n", usage]))
    with open(target) as f:
        d = json.load(f)
        print(gen_data(d))
