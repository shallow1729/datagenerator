import unittest
import datagenerator
import json
from collections import defaultdict


class Datagenerator(unittest.TestCase):
    def test_testset(self):
        with open('test_json/testset.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            self.assertEqual(s, "abc", "exact output")

    def test_testrandomset(self):
        with open('test_json/testrandomset.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            d = defaultdict(int)
            for i in range(10):
                s = datagenerator.gen_data(jd)
                d[s] += 1
            candidates = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1}
            for key in d.keys():
                self.assertTrue(key in candidates)
                d[key] < 10

    def test_testchar(self):
        with open('test_json/testchar.json') as f:
            jd = json.load(f)
            candidates = {'a': 1, 'b': 1, 'c': 1, 'd': 1}
            for i in range(5):
                s = datagenerator.gen_data(jd)
                self.assertEqual(candidates[s], 1, "result is possible charactor")

    def test_testint(self):
        with open('test_json/testint.json') as f:
            jd = json.load(f)
            for i in range(5):
                s = datagenerator.gen_data(jd)
                s = int(s)
                self.assertTrue(s <= 5 and 1 <= s, "result is possible integer")

    def test_testrandomsetlist1(self):
        with open('test_json/testrandomsetlist1.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            candidates = {'a': 1, 'b': 1, 'c': 1}
            for i in range(len(s)):
                self.assertTrue(s[i] in candidates)
                if s[i] == 'b':
                    self.assertEqual(s[i + 1], 'c')

    def test_testrandomsetlist2(self):
        with open('test_json/testrandomsetlist2.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            candidates = {'a.bc': 1, 'bc.a': 1}
            for i in range(3):
                self.assertTrue(s in candidates)

    def test_testintlist(self):
        with open('test_json/testintlist.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            vs = [int(i) for i in s.split(',')]
            d = {}
            for v in vs:
                self.assertTrue(0 <= v and v <= 1000)
                self.assertFalse(v in d)
                d[v] = 1
            self.assertEqual(len(d.keys()), 100)

    def test_testintcandidatelist(self):
        with open('test_json/testintcandidatelist.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            ans = [1, 3, 5, 11, 23, 111, 211]
            result = [int(i) for i in s.split(' ')]
            self.assertEqual(len(result), 7)
            for i in range(7):
                self.assertEqual(ans[i], result[i])

    def test_testrandomorderedlist(self):
        with open('test_json/testrandomorderedlist.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            vs = [int(i) for i in s.split(' ')]
            c = 0
            for v in vs:
                self.assertTrue(0 <= v and v <= 1000)
                self.assertTrue(c <= v)
                c = v
            self.assertEqual(len(vs), 100)

    def test_testrandomorderedlistdesc(self):
        with open('test_json/testrandomorderedlistdesc.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            vs = [int(i) for i in s.split(' ')]
            c = 21
            for v in vs:
                self.assertTrue(0 <= v and v <= 1000)
                self.assertTrue(c > v)
                c = v
            self.assertEqual(len(vs), 20)

    def test_testinput1(self):
        with open('test_json/testinput1.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            results = s.split('\n')
            self.assertEqual(results[0], "5")
            vs = [int(i) for i in results[1].split()]
            for i in range(5):
                v = int(vs[i])
                self.assertTrue(1 <= v and v <= 1000)

    def test_testtable1(self):
        with open('test_json/testtable1.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            results = s.split('\n')
            self.assertEqual(results[0], "20 1000")
            for i in range(1, 21):
                v, p = [int(j) for j in results[i].split()]
                self.assertTrue(1 <= v and v <= 1000)
                self.assertTrue(0 <= p and p <= 100)

    def test_testtable2(self):
        with open('test_json/testtable2.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            results = s.split('\n')
            for i in range(20):
                v, p = [int(j) for j in results[i].split()]
                self.assertTrue(0 <= v and v <= 20)
                self.assertTrue(21 <= p and p <= 40)

    def test_testdate1(self):
        with open('test_json/testdate1.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            results = s.split('\n')
            self.assertTrue(len(results), 5)
            for i in range(5):
                v, datev = [j for j in results[i].split(',')]
                self.assertTrue(1 <= int(v) and int(v) <= 5)
                y, m, d = [p for p in datev.split('-')]
                self.assertTrue(2018 <= int(y) and int(y) <= 2020)
                self.assertTrue(1 <= int(m) and int(m) <= 5)
                self.assertTrue(len(m), 2)
                self.assertTrue(1 <= int(d) and int(d) <= 15)
                self.assertTrue(len(d), 2)

    def test_nestedlist(self):
        with open('test_json/testnestedlist.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            results = s.split('\n')
            self.assertTrue(len(results), 5)
            d = defaultdict(int)
            for i in range(5):
                self.assertTrue(len(results[i]), 5)
                for j in range(5):
                    d[results[i][j]] += 1
            self.assertTrue('#' in d)
            self.assertTrue('.' in d)
            self.assertTrue(len(d.keys()), 2)

    def test_nestedtable(self):
        with open('test_json/testnestedtable.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            results = s.split('\n')
            self.assertTrue(len(results), 5)
            d = {}
            for i in range(5):
                rec = results[i].split(' ')
                self.assertTrue(len(rec), 3)
                for j in range(3):
                    ch, integ = rec[j].split('-')
                    d[ch] = 1
                    self.assertTrue(1 <= int(integ) and int(integ) <= 8)
                self.assertEqual(len(d.keys()), 3)
                for ch in ['A', 'B', 'C']:
                    self.assertTrue(ch in d)

    def test_nestedlist2(self):
        with open('test_json/testnestedlist2.json') as f:
            jd = json.load(f)
            s = datagenerator.gen_data(jd)
            results = s.split('\n')
            self.assertTrue(len(results), 5)
            d = {}
            for i in range(5):
                d[results[i]] = 1
            self.assertEqual(len(d.keys()), 5)


if __name__ == '__main__':
    unittest.main()
