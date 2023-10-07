<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>

# Hunahpu  
Colav Similairy

# Description
Package with customized colav similarity algorithm.

# Installation

## Package
`pip install hunahpu`

# Usage
This is a library package, so you can use it in your code as follows:

```python
from hunahpu.ColavSimilarity import ColavSimilarity

paper1 = {}
paper1['title'] = 'My title one'
paper1["journal"] = "Journal one"
paper1["year"] = 2016

paper2 = {}
paper2['title'] = 'My title two'
paper2["journal"] = "Jornal two"
paper2["year"] = 2016

if ColavSimilarity(paper1, paper2):
    print("The papers are similar")
else:
    print("The papers are not similar")
```


it also allows several options for tunning such as:
```
ratio_thold: int
    threshold for  ratio matric
partial_thold: int
    threshold for partial ratio
low_thold: int
    low threshold for ratios
use_translation : str
    enable translation support
use_parsing: boolean
    use parsing to remove unneeded characters 
```
example:
```python
from hunahpu.ColavSimilarity import ColavSimilarity

paper1 = {}
paper1['title'] = 'My title one'
paper1["journal"] = "Journal one"
paper1["year"] = 2016

paper2 = {}
paper2['title'] = 'My title two'
paper2["journal"] = "Jornal two"
paper2["year"] = 2016

if ColavSimilarity(paper1, paper2, ratio_thold=90, partial_thold=92, low_thold=92, use_translation=True, use_parsing=True):
    print("The papers are similar")
else:
    print("The papers are not similar")
```

NOTE: translation does not work in all cases, so it is not recommended to use it.

# License
BSD-3-Clause License 

# Links
http://colav.udea.edu.co/



