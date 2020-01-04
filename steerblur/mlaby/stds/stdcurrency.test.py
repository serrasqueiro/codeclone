# stdcurrency.test.py  (c)2020  Henrique Moreira (part of 'mlaby/stds')

"""
  stdcurrency module tests.

  Compatibility: python 3.
"""

from redito import xCharMap
from stdcurrency import *
import xmltodict


#
# run_tests()
#
def run_tests (outFile, errFile, inArgs):
    code = 0
    enc = "UTF-8"
    args = inArgs
    op = {"xml-in": args[ 0 ],
          "filter": "." if len(args)<=1 else args[1],
          }
    fileListOneXML = op["xml-in"]
    filter = op["filter"]
    with open(fileListOneXML, "r", encoding=enc) as fd:
        data = fd.read()
        assert data.startswith("<?xml version=")
        isOk = workout( outFile, errFile, data, filter )
    assert isOk
    return code


def workout (outFile, errFile, data, filter, debug=0):
    # Should import ISO 4217:2015
    #	https://www.currency-iso.org/en/home/tables/table-a1.html
    #
    # https://www.currency-iso.org/dam/downloads/lists/list_one.xml

    latins = 0
    fixesCurrency = {
        "TONGA": "Pa'anga",
        928: "Bolivar Soberano",
        }
    keep = dict()
    print("Filter:", filter)
    d = xmltodict.parse( data )
    cont = d["ISO_4217"]
    currencyTable = cont["CcyTbl"]
    entities = currencyTable["CcyNtry"]
    # Fix TONGA "Pa'anga"
    for name, newCurrencyName in fixesCurrency.items():
        for x in entities:
            newName = None
            entityName = x["CtryNm"]
            if entityName==name:
                newName = newCurrencyName
            elif "CcyNbr" in x:
                number = int( x["CcyNbr"] )
                if number in fixesCurrency:
                    newName = fixesCurrency[ number ]
            if newName is not None:
                x["CcyNm"] = newName
            """
            y = dict(x)
            try:
                print( x["CcyNbr"], entityName, xCharMap.simpler_ascii( y ) )
            except:
                pass
            """
    idx = 0
    for country in entities:
        idx += 1
        elem = country
        fields = ("CtryNm", "CcyNm", "Ccy", "CcyNbr", "CcyMnrUnts")
        slim_dict( elem, fields, {"CcyNbr":0} )
        entity, nm, ccy, sNumber, unts = elem["CtryNm"], elem["CcyNm"], elem["Ccy"], elem["CcyNbr"], elem["CcyMnrUnts"]
        number = int( sNumber )
        if number==978:
            entity = "ALAND ISLANDS"
        elif number==418:
            entity = "LAOS"
        elif number==408:
            entity = "NORTH KOREA"
        elif number==952:
            entity = "COTE D'IVOIRE"
        elif number==532:
            entity = "CURACAO"
        s = "{3}; {0}; {1}; {2}; {4}\n".format( entity, nm, ccy, number, unts )
        ignore = entity.startswith("ZZ")
        if ignore: continue
        bogus = False
        try:
            outFile.write(s)
        except:
            bogus = True
        if bogus:
            latins += 1
            keep[ idx ] = s
        assert int( number )>=0
        assert entity!=""
    if "q" not in filter:
        pub = cont["@Pblshd"]
        errFile.write("Published: '{}'\n".format( pub ))
    if latins>0:
        errFile.write("Output skipped for {} Latin-1 lines.\n".format( latins ))
        for k, val in keep.items():
            s = xCharMap.simpler_ascii( val )
            print("Index:", k, ";", s)
    return True


#
# Test suite
#
if __name__ == "__main__":
    import sys
    code = run_tests( sys.stdout, sys.stderr, sys.argv[ 1: ] )
    sys.exit( code )
