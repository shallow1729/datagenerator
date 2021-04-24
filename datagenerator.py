from datetime import datetime
import json
import os
import random
import sys


# gen_random_set return one value from candidates
def gen_set(candidates: list, rest: int):
    target = random.randrange(rest)
    result = candidates[target]
    return target, result


def check_jd(jd, required: list):
    for v in required:
        if v not in jd:
            raise Exception("".join([v, " is required\n", json.dumps(jd)]))


def gen_data(jd, length=1, dupf: bool = True, ordered=None):
    check_jd(jd, ['type'])
    t = jd['type']
    results = []
    if t == 'set':
        check_jd(jd, ['candidates'])
        candidates = jd['candidates']
        rest = len(candidates)

        if dupf:
            for i in range(length):
                _, result = gen_set(candidates, rest)
                results.append(result)
        else:
            if length > len(candidates):
                raise Exception("".join(["number of candidates is smaller than length\n", json.dump(jd)]))
            for i in range(length):
                target, result = gen_set(candidates, rest - i)
                results.append(result)
                candidates[target] = candidates[rest - i - 1]

        if ordered is not None:
            l = [int(i) for i in results]
            if ordered == 'asc':
                l.sort()
            elif ordered == 'desc':
                l.sort(reverse=1)
            else:
                raise Exception("ordered need to be asc or desc\n")
            results = [str(i) for i in l]
        if length == 1:
            return results[0]
        else:
            return results

    elif t == 'int':
        check_jd(jd, ['min', 'max'])
        if 'digits' in jd:
            candidates = ['{:02}'.format(i) for i in range(jd['min'], jd['max'] + 1)]
        else:
            candidates = [str(i) for i in range(jd['min'], jd['max'] + 1)]
        if length > len(candidates):
            raise Exception("".join(["number of candidates is smaller than length\n", json.dump(jd)]))
        return gen_data({'type': 'set', 'candidates': candidates}, length=length, dupf=dupf, ordered=ordered)

    elif t == 'char':
        candidates = [chr(i) for i in range(ord(jd['min']), ord(jd['max']) + 1)]
        if length > len(candidates):
            raise Exception("".join(["number of candidates is smaller than length\n", json.dump(jd)]))
        return gen_data({'type': 'set', 'candidates': candidates}, length=length, dupf=dupf, ordered=ordered)

    elif t == 'list':
        check_jd(jd, ['length', 'separator', 'values'])
        if 'ordered' in jd and jd['ordered'] not in ['asc', 'desc']:
            raise Exception("".join(["ordered need to be asc or desc\n", json.dump(jd)]))
        sep = jd['separator']
        dupf = jd['duplicate'] if 'duplicate' in jd else True
        ordered = jd['ordered'] if 'ordered' in jd else None
        results = []
        for i in range(length):
            result = gen_data(jd['values'], length=jd['length'], dupf=dupf, ordered=ordered)
            if isinstance(result, list):
                results.append(sep.join(result))
            else:
                results.append(sep.join(result))
        if len(results) == 1:
            return results[0]
        else:
            return results

    elif t == 'sequence':
        check_jd(jd, ['symbols', 'separator'])
        symbols = jd['symbols']
        results = []
        for i in range(length):
            result = []
            for symbol in symbols:
                check_jd(jd, [symbol])
                result.append(gen_data(jd[symbol]))
            results.append(jd['separator'].join(result))
        if len(results) == 1:
            return results[0]
        else:
            return results

    elif t == 'table':
        check_jd(jd, ['symbols', 'length', 'separator', 'columnSeparator'])
        symbols = jd['symbols']
        sep = jd['separator']
        csep = jd['columnSeparator']
        d = {}
        for symbol in symbols:
            check_jd(jd, [symbol])
            dupf = jd[symbol]['duplicate'] if 'duplicate' in jd[symbol] else True
            ordered = jd[symbol]['ordered'] if 'ordered' in jd[symbol] else None
            d[symbol] = gen_data(jd[symbol], length=jd['length'], dupf=dupf, ordered=ordered)
        results = []
        for i in range(jd['length']):
            rec = []
            for symbol in symbols:
                rec.append(d[symbol][i])
            results.append(csep.join(rec))
        return sep.join(results)


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
