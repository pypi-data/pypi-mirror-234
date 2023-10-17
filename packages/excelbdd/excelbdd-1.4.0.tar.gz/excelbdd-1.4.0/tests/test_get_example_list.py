import sys
import os
script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'src')
sys.path.append( mymodule_dir )

from excelbdd.behavior import get_example_list
from parameterized import parameterized
import pytest

excelBDDFile = "../BDDExcel/ExcelBDD.xlsx"

#@parameterized.expand(get_example_list(excelBDDFile,"Sheet1","Scenario"))
@pytest.mark.parametrize("HeaderName, ParamName1, ParamName2, ParamName3, ParamName4", get_example_list(excelBDDFile,"Sheet1","Scenario"))
def test_loaddata_from_Sheet1(HeaderName, ParamName1, ParamName2, ParamName3, ParamName4):
    print(HeaderName, ParamName1, ParamName2, ParamName3, ParamName4)

def test_loaddata_from_Sheet2():
    testcaseSetList = get_example_list(excelBDDFile,"Sheet2","Scenario")
    print(testcaseSetList)
    assert len(testcaseSetList) == 4
    assert testcaseSetList[0][1] == "V1.1"
    assert testcaseSetList[1][1] == "V1.2"
    assert testcaseSetList[2][1] == "V1.3"
    assert testcaseSetList[3][1] == "V1.4"
    
    assert testcaseSetList[0][2] == "V2.1"
    assert testcaseSetList[1][2] == "V2.2"
    assert testcaseSetList[2][2] == "V2.3"
    assert testcaseSetList[3][2] == "V2.4"
    
    assert testcaseSetList[0][3] ==  None
    assert testcaseSetList[1][3] ==  None
    assert testcaseSetList[2][3] ==  None
    assert testcaseSetList[3][3] ==  None

    assert testcaseSetList[0][4] ==  "2021/4/30"
    assert testcaseSetList[1][4] ==  False
    assert testcaseSetList[2][4] ==  True
    assert testcaseSetList[3][4] ==  4.4


@pytest.mark.parametrize("HeaderName, ParamName1, ParamName2, ParamName3, ParamName4", get_example_list(excelBDDFile,"Sheet3"))
def test_loaddata_from_Sheet3(HeaderName, ParamName1, ParamName2, ParamName3, ParamName4):
    print(HeaderName, ParamName1, ParamName2, ParamName3, ParamName4)

 
# @parameterized.expand(get_example_list(excelBDDFile,"SmartBDD",None,"V1.1"))
@pytest.mark.parametrize("HeaderName,ExcelFileName, SheetName, HeaderMatcher, HeaderUnmatcher, Header1Name, FirstGridValue, LastGridValue, \
                         ParamName1InSet2Value, ParamName2InSet2Value, ParamName3Value, MaxBlankThreshold, ParameterCount, TestDataSetCount", 
                         get_example_list(excelBDDFile,"SmartBDD"))
def test_example_list(HeaderName,ExcelFileName, SheetName, HeaderMatcher, HeaderUnmatcher, Header1Name, FirstGridValue, LastGridValue, 
                      ParamName1InSet2Value, ParamName2InSet2Value, ParamName3Value, MaxBlankThreshold, ParameterCount, TestDataSetCount):
    testcaseSetList = get_example_list("../BDDExcel/" + ExcelFileName, SheetName, HeaderMatcher,HeaderUnmatcher)
    assert len(testcaseSetList) == TestDataSetCount
    paramLen = len(testcaseSetList[0])
    step = (paramLen-1)/4

    assert testcaseSetList[0][1] == FirstGridValue
    assert testcaseSetList[1][1] == "V1.2"
    assert testcaseSetList[2][1] == "V1.3"
    assert testcaseSetList[3][1] == "V1.4"
    
    assert testcaseSetList[0][int(1+step)] == "V2.1"
    assert testcaseSetList[1][int(1+step)] == "V2.2"
    assert testcaseSetList[2][int(1+step)] == "V2.3"
    assert testcaseSetList[3][int(1+step)] == "V2.4"
    
    assert testcaseSetList[0][int(1+step*2)] ==  None
    assert testcaseSetList[1][int(1+step*2)] ==  None
    assert testcaseSetList[2][int(1+step*2)] ==  None
    assert testcaseSetList[3][int(1+step*2)] ==  None

    assert testcaseSetList[0][int(1+step*3)] ==  "2021/4/30"
    assert testcaseSetList[1][int(1+step*3)] ==  False
    assert testcaseSetList[2][int(1+step*3)] ==  True
    assert testcaseSetList[3][int(1+step*3)] ==  LastGridValue

# @parameterized.expand(get_example_list(excelBDDFile,"Exception"))
@pytest.mark.parametrize("HeaderName, ExcelFileName, SheetName, Message", 
                         get_example_list(excelBDDFile,"Exception"))
def test_excelbdd_exception(HeaderName, ExcelFileName, SheetName, Message):
    print(HeaderName, ExcelFileName, SheetName, Message)    
    with pytest.raises(Exception) as ex:
        testcaseSetList = get_example_list("../BDDExcel/" + ExcelFileName, SheetName)

    assert Message in str(ex.value)   

def test_excelbdd_no_sheetName():
    testcaseSetList = get_example_list("../BDDExcel/ExcelBDDSampleA.xlsx")
    assert len(testcaseSetList) == 5

