# -*- coding: iso-8859-1 -*-
"""
Module for bank names

(c)2020  Henrique Moreira (part of 'mintracker')
"""

### alternative: -*- coding: utf-8 -*-

# pylint: disable=missing-docstring


BANK_NAMES = {
    "PT500035": "CAIXA GERAL DE DEPOSITOS",
    }

_ORIGINAL_NAMES = {
    "PT500035": "Caixa Geral de Depósitos",
    }


def get_original_name(num, orig=None):
    """ Return the original bank name, if exists.
    """
    if orig is None:
        dct_orig = _ORIGINAL_NAMES
    else:
        dct_orig = orig
    assert isinstance(dct_orig, dict)
    astr = dct_orig.get(num)
    if astr is not None:
        return astr
    return BANK_NAMES[num]


if __name__ == "__main__":
    print("Module, no run!")
