## datagenerator
`datagenerator` can generate random data defined with json.
It can also control output format like csv and blank separated data, which is often used for programming contest.

## json format
Example json inputs are in `sample/`
### set
```
{
    "type": "set",
    "candidates": [
        "a",
        "b"
    ]
}
```
`set` select one value from candidates.

### int
```
{
    "type": "int",
    "min": 1,
    "max": 5
}
```
`int` select one integer the value of which is `min <= value <= max`.

### char
```
{
  "type": "char",
  "min": "a",
  "max": "d"
}
```
`char` select one charactor the value of which is `min <= value <= max` in an integer representing of the Unicode character.

### list
```
{
    "type": "list",
    "values": {
        "type": "set",
        "candidates": [
            "a",
            "b"
        ]
    },
    "duplicate": true,
    "length": 10,
    "separator": " "
}
```
`list` randomly select `values` from candidates for `length` times and then joins with `separator`.  
This example will output like `a b a a a b b a b b`.  
`duplicate` flag can controll if select same value multiple times.(default value is True)  
`ordered` flag can controll if result have to be sorted. you can control the direction with `asc` or `desc`. If not defined, result will not be sorted.

### sequence
```
{
  "type": "sequence",
  "symbols": [
    "V",
    "W"
  ],
  "separator": "\n",
  "V": {
    "type": "set",
    "candidates": [
      "5"
    ]
  },
  "W": {
    "type": "list",
    "length": 5,
    "duplicate": false,
    "separator": " ",
    "values": {
      "type": "int",
      "min": 1,
      "max": 20
    }
  }
}
```
`sequence` output symbols in order joined by separator.
Possible result of this input is as below. 
```
5
4 7 15 2 11
```

### table
```
{
    "type": "table",
    "symbols": [
        "V",
        "P"
    ],
    "symbolSeparator": " ",
    "length": 5,
    "separator": "\n",
    "V": {
        "type": "int",
        "min": 1,
        "max": 5,
        "duplicate": false
    },
    "P": {
        "type": "int",
        "min": 6,
        "max": 10,
        "duplicate": false
    }
}
```
`table` generate symbol values and the join them with `symbolSeparator` and then join each line with `separator`.
Possible result of this example is as below.
```
4 6
5 9
3 7
2 8
1 10
```