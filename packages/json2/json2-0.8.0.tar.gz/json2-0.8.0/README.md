# Json2

## Purpose
Python package which just wraps the default python json but with.
Additonally it can hanlde numpy arrays and torch tensors without throwing an exception.
```json2.load_file``` and ```json2.save_file```

## Installation

```pip install json2```

## Usage

```
import json2

a = json2.load_file(r'/home/user/myjson.json')
json2.dump_file(r'/home/user/myjson.json', a)
```
