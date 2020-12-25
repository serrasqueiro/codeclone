#-*- coding: iso-8859-1 -*-
# ibanpt.py  (c)2020  Henrique Moreira

""" Module for IBAN, and NIB (pt)
"""

# pylint: disable=missing-docstring

# Format:
#	NIB: 21 digits
#	BIC/SWIFT: e.g. 'CGDIPTPL'
#	'PSP Name': ...

_BANKS = (("0035 AAAA CCCCCCCCCCC XX", "CGDIPTPL", "CAIXA GERAL DE DEPOSITOS"),
          )


def bank_accounts() -> list:
    """ Returns a list with the splitted strings for each bank.
    """
    # https://www.bancosdeportugal.info/codigos-iban-nib-bancos/
    base = """
NIB: 0018 AAAA CCCCCCCCCCC XX
IBAN: PT50 0018 AAAA CCCCCCCCCCC XX
BIC/SWIFT: TOTAPTPLXXX
Nome PSP: BANCO SANTANDER TOTTA, SA

Millennium BCP
NIB: 0033 AAAA CCCCCCCCCCC XX
IBAN: PT50 0033 AAAA CCCCCCCCCCC XX
BIC/SWIFT: BCOMPTPLXXX
Nome PSP: BANCO COMERCIAL PORTUGUÊS, SA

Novo Banco
NIB: 0007 AAAA CCCCCCCCCCC XX
IBAN: PT50 0007 AAAA CCCCCCCCCCC XX
BIC/SWIFT: BESCPTPLXXX
Nome PSP: NOVO BANCO, SA

Bankinter
NIB: 0269 AAAA CCCCCCCCCCC XX
IBAN: PT50 0269 AAAA CCCCCCCCCCC XX
BIC/SWIFT: BKBKPTPLXXX
Nome PSP: BANKINTER, SA. SUCURSAL EM PORTUGAL

EuroBIC
NIB: 0079 AAAA CCCCCCCCCCC XX
IBAN: PT50 0079 AAAA CCCCCCCCCCC XX
BIC/SWIFT: BPNPPTPLXXX
Nome PSP: BANCO BIC PORTUGUÊS, SA

Popular
NIB: 0046 AAAA CCCCCCCCCCC XX
IBAN: PT50 0046 AAAA CCCCCCCCCCC XX
BIC/SWIFT: CRBNPTPLXXX
Nome PSP: BANCO POPULAR PORTUGAL, SA

NIB: 0036 AAAA CCCCCCCCCCC XX
IBAN: PT50 0036 AAAA CCCCCCCCCCC XX
BIC/SWIFT: MPIOPTPLXXX
Nome PSP: CAIXA ECONÓMICA MONTEPIO GERAL

Banco CTT
NIB: 0193 AAAA CCCCCCCCCCC XX
IBAN: PT50 0193 AAAA CCCCCCCCCCC XX
BIC/SWIFT: CTTVPTPLXXX
Nome PSP: BANCO CTT, SA
"""
    res = base.strip('\n').split("\n\n")
    return res


def iban_list() -> list:
    """ Returns a raw IBAN list from a string source.
    """
    # pylint: disable=line-too-long

    # listaiban.xls:
    #	https%3A%2F%2Fwww.bportugal.pt%2Fsites%2Fdefault%2Ffiles%2Flistaiban.xls
    #
    # IBAN (english):
    #	www.bportugal.pt/sites/default/files/anexos/documentos-relacionados/international_bank_account_number_en.pdf
    res = list()
    # ToDo
    return res


# Main script
if __name__ == "__main__":
    print("Module, no run!")
