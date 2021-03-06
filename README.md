# datagenerator
`datagenerator` is simple but powerful random data generator.

## License
MIT

## Usage
`python3 datagenerator.py sample/sampletable1.json`

## Example
### input
```
{
    "type": "list",
    "values": {
        "type": "int",
        "min": 1,
        "max": 100
    },
    "duplicate": false,
    "length": 5,
    "separator": ","
}
```
### output
```
31,78,23,63,64
```

### input
```
{
    "type": "list",
    "length": 5,
    "separator": "\n",
    "values": {
        "type": "table",
        "symbols": [
            "A",
            "B"
        ],
        "length": 3,
        "symbolSeparator": "-",
        "separator": " ",
        "A": {
            "values": {
                "type": "set",
                "candidates": [
                    "A",
                    "B",
                    "C"
                ]
            },
            "duplicate": false
        },
        "B": {
            "values": {
                "type": "int",
                "min": 1,
                "max": 8
            }
        }
    }
}
```
### output
```
C-5 B-1 A-3
B-4 C-6 A-4
B-8 C-7 A-2
B-2 C-2 A-8
A-2 B-2 C-1
```
Other example json inputs are in `sample/`

## json format
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
`set` select one value from `candidates`.

### int
```
{
    "type": "int",
    "min": 1,
    "max": 5
    "digits": 2
}
```
`int` select one integer the value of which is `min <= value <= max`. 
if `digits` is defined, 0 padding will be done. the result of this input is like `02`.  
You can also use `candidates` instead of `min` and `max`.

### char
```
{
  "type": "char",
  "min": "a",
  "max": "d"
}
```
`char` select one character the value of which is `min <= value <= max` in an integer representing of the Unicode character.

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
`duplicate` flag can control if select same value multiple times.(default value is True)  
`ordered` flag can control if result have to be sorted. you can control the direction with `asc` or `desc`. If not defined, result will not be sorted.

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
`sequence` output symbols in order joined by `separator`.
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
        "values": {
            "type": "int",
            "min": 1,
            "max": 5
        },
        "duplicate": false
    },
    "P": {
        "values": {
            "type": "int",
            "min": 6,
            "max": 10
        },
        "duplicate": false
    }
}
```
`table` generate symbol values and then join them with `symbolSeparator` and then join each line with `separator`.
Possible result of this example is as below.
```
4 6
5 9
3 7
2 8
1 10
```