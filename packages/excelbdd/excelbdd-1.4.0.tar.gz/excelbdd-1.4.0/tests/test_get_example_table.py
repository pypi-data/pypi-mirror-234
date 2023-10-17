import pytest
import sys
import os
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '..', 'src')
sys.path.append(mymodule_dir)

from excelbdd.behavior import get_example_table
from excelbdd.behavior import get_example_list

excelBDDFile = "../BDDExcel/DataTableBDD.xlsx"


@pytest.mark.parametrize("HeaderName, ExcelFileName, SheetName, HeaderRow, StartColumn, TestSetCount, FirstGridValue, LastGridValue, ColumnCount, Header03InThirdSet",
                         get_example_list(excelBDDFile, "DataTableBDD"))
def test_get_example_tableA(HeaderName, ExcelFileName, SheetName, HeaderRow, StartColumn, TestSetCount, FirstGridValue, LastGridValue, ColumnCount, Header03InThirdSet):
    print(HeaderName, ExcelFileName, SheetName, HeaderRow, StartColumn,
          TestSetCount, FirstGridValue, LastGridValue, ColumnCount, Header03InThirdSet)
    testcaseSetList = get_example_table(
        excelBDDFile, SheetName, HeaderRow, StartColumn)
    
    assert len(testcaseSetList) == TestSetCount
    assert len(testcaseSetList[0]) == ColumnCount
    assert testcaseSetList[0][0] == FirstGridValue
    assert testcaseSetList[5][7] == LastGridValue
    assert testcaseSetList[2][2] == Header03InThirdSet

@pytest.mark.parametrize("Header01, Header02, Header03, Header04, Header05, Header06, Header07, Header08",
                         get_example_table(excelBDDFile, "DataTable4"))
def test_get_example_tableB(Header01, Header02, Header03, Header04, Header05, Header06, Header07, Header08):
    print(Header01, Header02, Header03, Header04, Header05, Header06, Header07, Header08)


def test_get_example_table_exceptions():
    with pytest.raises(Exception) as ex:
        testcaseSetList = get_example_table(excelBDDFile, "DataTable4",1,'a')
    assert "Start Column must in A~Z" in str(ex.value)  

    with pytest.raises(Exception) as ex:
        testcaseSetList = get_example_table(excelBDDFile, "DataTable4",1,'1')
    assert "Start Column must in A~Z" in str(ex.value) 

    with pytest.raises(Exception) as ex:
        testcaseSetList = get_example_table(excelBDDFile, "DataTable4",1,'AA')
    assert "Start Column must in A~Z" in str(ex.value)

    with pytest.raises(Exception) as ex:
        testcaseSetList = get_example_table(excelBDDFile, "DataTable4NotExist",1,'a')
    assert "sheet does not exist" in str(ex.value)  

@pytest.mark.parametrize("HeaderName, ExcelFileName, SheetName, HeaderRow, StartColumn, Message",
                         get_example_list(excelBDDFile, "Exception"))
def test_get_example_table_exceptionsB(HeaderName, ExcelFileName, SheetName, HeaderRow, StartColumn, Message): 
    with pytest.raises(Exception) as ex:
        testcaseSetList = get_example_table("../BDDExcel/" + ExcelFileName, SheetName, HeaderRow, StartColumn)
    assert Message in str(ex.value)  