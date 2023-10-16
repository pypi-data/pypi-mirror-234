Use Excel file as BDD feature file, get example data from excel files, support automation tests

```
#pip install excelbdd
import pytest
from excelbdd.behavior import get_example_list
import FizzBuzz

excelBDDFile = "path of excel file" 
@pytest.mark.parametrize("HeaderName, Number1, Output1, Number2, Output2, Number3, Output3, Number4, Output4",
                        get_example_list(excelBDDFile,"FizzBuzz"))
def test_FizzBuzz(HeaderName, Number1, Output1, Number2, Output2, Number3, Output3, Number4, Output4):
    assert FizzBuzz.handle(Number1) == Output1
    assert FizzBuzz.handle(Number2) == Output2
    assert FizzBuzz.handle(Number3) == Output3
    assert FizzBuzz.handle(Number4) == Output4
```    

more information at [ExcelBDD Guideline by Python](https://dev.azure.com/simplopen/ExcelBDD/_wiki/wikis/ExcelBDD.wiki/80/ExcelBDD-Guideline-by-Python)