import sys
import os
script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', 'src')
sys.path.append( mymodule_dir )

from excelbdd.behavior import get_example_list
from parameterized import parameterized
import pytest

excelBDDFile = "../BDDExcel/ExcelBDD.xlsx"

@pytest.mark.parametrize("HeaderName,ExcelFileName, SheetName, HeaderMatcher, HeaderUnmatcher, Header1Name, FirstGridValue, LastGridValue, \
                         ParamName1InSet2Value, ParamName2InSet2Value, ParamName3Value, MaxBlankThreshold, ParameterCount, TestDataSetCount", 
                         get_example_list(excelBDDFile,"SmartBDD","V1.1", "Expected"))
def test_example_list_SBT(HeaderName,ExcelFileName, SheetName, HeaderMatcher, HeaderUnmatcher, Header1Name, FirstGridValue, LastGridValue, 
                      ParamName1InSet2Value, ParamName2InSet2Value, ParamName3Value, MaxBlankThreshold, ParameterCount, TestDataSetCount):
    testcaseSetList = get_example_list("../BDDExcel/" + ExcelFileName, SheetName, HeaderMatcher,HeaderUnmatcher)
    assert len(testcaseSetList) == TestDataSetCount
    assert testcaseSetList[0][1] == FirstGridValue
    assert testcaseSetList[1][1] == "V1.2"
    assert testcaseSetList[2][1] == "V1.3"
    assert testcaseSetList[3][1] == "V1.4"
    
    assert len(testcaseSetList[0]) ==  13
    assert testcaseSetList[0][4] == "V2.1"
    assert testcaseSetList[1][4] == "V2.2"
    assert testcaseSetList[2][4] == "V2.3"
    assert testcaseSetList[3][4] == "V2.4"
    
    assert testcaseSetList[0][7] ==  None
    assert testcaseSetList[1][7] ==  None
    assert testcaseSetList[2][7] ==  None
    assert testcaseSetList[3][7] ==  None

    assert testcaseSetList[0][10] ==  "2021/4/30"
    assert testcaseSetList[1][10] ==  False
    assert testcaseSetList[2][10] ==  True
    assert testcaseSetList[3][10] ==  LastGridValue


@pytest.mark.parametrize("HeaderName,ExcelFileName, SheetName, HeaderMatcher, HeaderUnmatcher, Header1Name, FirstGridValue, LastGridValue, \
                         ParamName1InSet2Value, ParamName2InSet2Value, ParamName3Value, MaxBlankThreshold, ParameterCount, TestDataSetCount", 
                         get_example_list(excelBDDFile,"SmartBDD","Expected"))
def test_example_list_Expected(HeaderName,ExcelFileName, SheetName, HeaderMatcher, HeaderUnmatcher, Header1Name, FirstGridValue, LastGridValue, 
                      ParamName1InSet2Value, ParamName2InSet2Value, ParamName3Value, MaxBlankThreshold, ParameterCount, TestDataSetCount):
    testcaseSetList = get_example_list("../BDDExcel/" + ExcelFileName, SheetName, HeaderMatcher,HeaderUnmatcher)
    assert len(testcaseSetList) == TestDataSetCount
    assert testcaseSetList[0][1] == FirstGridValue
    assert testcaseSetList[1][1] == "V1.2"
    assert testcaseSetList[2][1] == "V1.3"
    assert testcaseSetList[3][1] == "V1.4"
    
    assert len(testcaseSetList[0]) ==  9
    assert testcaseSetList[0][3] == "V2.1"
    assert testcaseSetList[1][3] == "V2.2"
    assert testcaseSetList[2][3] == "V2.3"
    assert testcaseSetList[3][3] == "V2.4"
    
    assert testcaseSetList[0][5] ==  None
    assert testcaseSetList[1][5] ==  None
    assert testcaseSetList[2][5] ==  None
    assert testcaseSetList[3][5] ==  None

    assert testcaseSetList[0][7] ==  "2021/4/30"
    assert testcaseSetList[1][7] ==  False
    assert testcaseSetList[2][7] ==  True
    assert testcaseSetList[3][7] ==  LastGridValue