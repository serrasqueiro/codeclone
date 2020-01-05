# stdcurrency.test.py  (c)2020  Henrique Moreira (part of 'mlaby/stds')

"""
  stdcurrency module tests.

  Compatibility: python 3.
"""

from redito import xCharMap
from stdcurrency import *
from stdorder import *
import xmltodict


#
# run_tests()
#
def run_tests (outFile, errFile, inArgs):
    code = 0
    enc = "UTF-8"
    args = inArgs if inArgs!=[] else ["."]
    op = {"xml-in": args[ 0 ],
          "filter": "." if len(args)<=1 else args[1],
          }
    fileListOneXML = op["xml-in"]
    filter = op["filter"]
    if fileListOneXML==".":
        code = test_stdorder(outFile, errFile, filter)
        assert code==0
        return 0
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


def test_stdorder (outFile, errFile, filter, debug=0):
    verbose = 1
    opts = {"-v": verbose,
            "filter": filter,
            }
    iCurrency = SCurrency()
    basic_dump(outFile, errFile, iCurrency, opts, debug)
    return 0


#
# basic_dump()
#
def basic_dump (outFile, errFile, iCurrency, opts, debug=0):
    verbose = opts[ "-v" ]
    verbose += int(debug)
    aDict = dict()
    nickDict = dict()
    content = dict_ISO4217
    content_2 = dict_ISO4217_fundList
    for row in content:
        assert len(row) == 5
        country, currency, nick, number, units = row
        if number in aDict:
            aDict[number].append(row)
        else:
            aDict[number] = [row]
        sNick = "---" if nick == "" else nick
        s = "{:>3} {:<3} {} '{}'".format(number, sNick, country, currency.replace(" ", "_"))
        if verbose >= 2:
            outFile.write("{}\n".format(s))
        vNumber = int( number )
        if sNick not in nickDict:
            nickDict[sNick] = [vNumber, currency, 1]
        else:
            assert nickDict[sNick][:2]==[vNumber, currency]
            nickDict[sNick][2] += 1
    nicks = SDict( nickDict )
    for x in nicks.byName:
        print("nick:", x, "is:", nicks.get( x ))
    for nick in iCurrency.currencies.byName:
        number, currency, units = iCurrency.currencies.get( nick )
        if verbose>=2 and number>0:
            print("INFO: {} = {:3} '{}' (Minor units: {})".format( nick, number, currency, units ))
    xd = nicks.histog( 3, True )
    # Now show first the mostly used currencies:
    if verbose>0:
        print("\n...")
        highCount = xd.byName[0]
        assert highCount>=1
        h = [0] * (highCount+1)  # we only need e.g. 35+1 elements if the mostly used currency occurs 35 times
        occIter = [i for i in range(highCount, 0, -1)]  # e.g. 35 down to 1
        for n in occIter:
            z = xd.get( n )
            if z: h[n] = z
        for n in occIter:
            z = h[n]
            if z>0:
                for x in nicks.byName:
                    tup = nicks.ori[ x ]
                    y = tup[ 2 ]
                    if y==n:
                        number, currency = tup[:2]
                        xtra = " [***fund***]" if number in content_2 else ""
                        print("Histog.: {:>3} ({}) {} (appears {}){}".format( number, iCurrency.by_number(number), currency, "once" if n<=1 else str(n)+"*", xtra ))
                        assert iCurrency.by_abbrev( iCurrency.by_number(number) )==number
                        for row in content:
                            country1, currency1, nick1, number1, units1 = row
                            vNumber = int( number1 )
                            if number==vNumber:
                                print("\tat: {}".format( country1 ))
                        print("")
    return 0


#
# Test suite
#
if __name__ == "__main__":
    import sys
    """ stdcurrency.test.py dotOrXML [...]

dotOrXML is either a dot ('.'), or an xml file containing
	https://www.currency-iso.org/dam/downloads/lists/list_one.xml
or alike.
This will then generate the tuples which can be copied down to stdcurrency.py, e.g.
    ("AFGHANISTAN",	"Afghani", "AFN", "971", "2"), ...

If you enter nothing, or a dot, this script will simply dump the histogram of coins.
    """
    code = run_tests( sys.stdout, sys.stderr, sys.argv[ 1: ] )
    sys.exit( code )
