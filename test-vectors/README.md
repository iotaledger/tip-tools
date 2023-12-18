# Serialization example of IOTA 2.0 data structures

This tool prints the json structure, yaml structure, serialized bytes and the ID of the IOTA 2.0 data structures.

To list the supported objects:
```bash
$ go run . [-h | -help | --help | help]

# outputs:
#     Usage: go run main.go "[object name]" [yaml flag]
#     Supported object:
#         - Protocol Parameters
#         - Commitment
#         - Transaction
#         - Transaction Basic Block
#         - TaggedData Basic Block
#         - Validation Block
```    

The following command prints the json structure, serialized bytes and the ID of the Protocol Parameters object:
```
$ go run . "Protocol Parameters"
```

## Print yaml structure
Yaml flag is optional and defaults to `false`. To print the yaml structure, pass the second argument as `true` or `1` or `T`:
```
$ go run . "Protocol Parameters" true
```
or
```
$ go run . "Protocol Parameters" 1
```