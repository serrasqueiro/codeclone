#-*- coding: iso-8859-1 -*-
# ibanimporter.py  (c)2020  Henrique Moreira

""" Importer module for IBANs; used in PT IBANs.
"""

# pylint: disable=missing-docstring

import sys
from waxpage.redit import char_map


def main():
    myprog = __file__
    args = sys.argv[1:]
    code = runner(args)
    if code is None:
        print(f"""Usage:

{myprog} cat-text [textual-iban-list.txt]
""")
    sys.exit(code if code else 0)


def runner(args):
    code = None
    fname = "../docs/listaiban_text.txt"
    if not args:
        return None
    cmd = args[0]
    param = args[1:]
    if cmd in ("cat-text",):
        if param:
            fname = param[0]
            del param[0]
        code = cat_text(fname, param)
        return code
    return code


def cat_text(fname, param) -> int:
    read_enc = "ISO-8859-1"
    data = open(fname, "r", encoding=read_enc).read()
    lines = data.splitlines()
    payload = [dig_throu(astr) for astr in lines if astr and astr[0] != "#"]
    if param:
        for tup in payload:
            show = param == ["."] or find_bank_etc(tup, param)
            if show:
                print(tup)
        return 0
    dump_from_payload(payload)
    return 0


def dump_from_payload(payload, debug=0) -> int:
    """ Dump IBAN and IBAN groups """
    ibans, banks = dict(), dict()
    inames, pairs = dict(), dict()
    multiples = list()
    for triplet in payload:
        iban, bank_id, name = triplet
        assert name
        is_ok = bank_id not in banks
        if "ex-BANCO POPULAR PORTUGAL" in name:
            assert not is_ok
            continue
        #print("Processing:", bank_id, ":", name, "OK?", is_ok)
        banks[bank_id] = name
        pairs[f"{iban}.{bank_id}"] = name
        if iban in ibans:
            ibans[iban].append(bank_id)
        else:
            ibans[iban] = [bank_id]
    for iban in sorted(ibans.keys()):
        alen = len(ibans[iban])
        bank_id = ibans[iban][0]
        if alen > 1:
            multiples.append(iban)
            hint = f" multiple bank_id(s), #{alen}"
            assert int(bank_id) <= 0
            inames[iban] = pairs[f"{iban}.{bank_id}"]
        else:
            hint = ""
            inames[iban] = banks[bank_id]
        if debug > 0:
            print(f"IBAN {iban}:{hint}")
            for elem in ibans[iban]:
                shown = banks[elem]
                print(f"  - {elem} = {shown}")
            print()
    for iban in sorted(inames.keys()):
        print(iban, inames[iban])
    return 0


def find_bank_etc(tup, afilter) -> list:
    assert afilter
    matches = list()
    name = tup[2]
    for what in afilter:
        if what.upper() in name:
            matches.append(what)
    return matches


def dig_throu(astr) -> tuple:
    basic = char_map.simpler_ascii(astr)
    iban, bank_id, inst_name, type_of = basic.split('\t')
    check = int(bank_id)
    assert check >= 0
    check = int(iban)
    kind = " ".join(type_of.split(' '))
    assert kind == type_of
    tup = (iban, bank_id, inst_name)
    return tup


# Main script
if __name__ == "__main__":
    main()
