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
    uQue = dict()  # Uniqueness of keys
    fundList = []
    isProg = filter=="."
    if isProg:
        outFile.write("dict_ISO4217={\n")
    else:
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
        entity, aName, ccy, sNumber, unts = elem["CtryNm"], elem["CcyNm"], elem["Ccy"], elem["CcyNbr"], elem["CcyMnrUnts"]
        if  type(aName)==str:
            nm = aName
            isFund = False
        else:
            nm = aName["#text"]
            isOk = aName["@IsFund"]=="true"
            assert isOk
            isFund = isOk
        number = int( sNumber )
        if entity[ 1: ]=="ALAND ISLANDS"[ 1: ]:
            entity = "ALAND ISLANDS"
        elif number==418:
            entity = "LAOS"
        elif number==408:
            entity = "NORTH KOREA"
        elif entity.endswith( "IVOIRE" ):
            entity = "COTE D'IVOIRE"
        elif entity.startswith( "CURA" ):
            entity = "CURACAO"
        elif entity.startswith( "SAINT BART" ):
            entity = "SAINT BARTHELEMY"
        elif entity[0]=="R" and entity.endswith( "UNION" ):
            entity = "REUNION"
        elif entity=='SISTEMA UNITARIO DE COMPENSACION REGIONAL DE PAGOS "SUCRE"':
            entity = entity[ :entity.find('"') ].strip()
        s = "{3}; {0}; {1}; {2}; {4}\n".format( entity, nm, ccy, number, unts )
        prog = " "*4 + '("{0}",\t"{1}", "{2}", "{3}", "{4}"),\n'.format( entity, nm, ccy, number, unts )
        ignore = entity.startswith("ZZ")
        isOk = (ignore and not isFund) or not ignore
        assert isOk
        # Check uniqueness
        if entity=="UNITED STATES MINOR OUTLYING ISLANDS (THE)":
            uq = "USMOI-USD"
        elif entity=="VIRGIN ISLANDS (BRITISH)":
            uq = "VIGB-USD"
        else:
            uq = "{}{}".format( "_".join(entity.split(" ")[:2]), ccy if ccy=="" else "-"+ccy )
        isOk = uq not in uQue
        if not isOk:
            errFile.write("Non unique key ({}), first seen here: {}==> {}\n".format( uq, uQue[uq], s ))
        assert isOk
        uQue[ uq ] = s
        #print("Debug:", xCharMap.simpler_ascii( uq ))
        if ignore: continue
        bogus = False
        try:
            outFile.write(prog if isProg else s)
        except:
            bogus = True
        if bogus:
            latins += 1
            keep[ idx ] = s
        assert int( number )>=0
        assert entity!=""
        if isFund:
            fundList.append(number)
    if "q" not in filter:
        pub = cont["@Pblshd"]
        errFile.write("Published: '{}'\n".format( pub ))
    if latins>0:
        errFile.write("Output skipped for {} Latin-1 lines.\n".format( latins ))
        for k, val in keep.items():
            s = xCharMap.simpler_ascii( val )
            print("Index:", k, ";", s)
    """
	(***) We avoid having properties such as the following:

	#984; BOLIVIA (PLURINATIONAL STATE OF); OrderedDict([('@IsFund', 'true'), ('#text', 'Mvdol')]); BOV; 2
	...caused by:
		<CcyNm IsFund="true">Mvdol</CcyNm>
	Note the regular bolivian coin is:
	# 68; BOLIVIA (PLURINATIONAL STATE OF); Boliviano; BOB; 2
	#	(here 'ccy' is "BOB")
    """
    if isProg:
        outFile.write(" "*4+"}\n\n")
        outFile.write("dict_ISO4217_fundList={}\n\n".format( tuple(fundList) ))
    else:
        print("Fund list:", tuple( fundList ))
    return True


#
# Test suite
#
if __name__ == "__main__":
    import sys
    code = run_tests( sys.stdout, sys.stderr, sys.argv[ 1: ] )
    sys.exit( code )
