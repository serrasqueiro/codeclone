# malias.py  (c)2020  Henrique Moreira

"""
  Basic mail alias (or other text alias)

  Compatibility: python 3.
"""

# pylint: disable=missing-docstring, invalid-name, line-too-long


import sys
import re
from texables.bdebug import cprint


MAIL_REGEX = '^([A-Za-z0-9]+[A-Za-z0-9._-]*)@([a-z0-9]+[a-z0-9_-]*[.][a-z0-9][a-z0-9._-]*)$'

strict_TLD = list()	# Example: ['.com', '.net', '.us']


def main():
    """ Main script """
    args = sys.argv[1:]
    code = test_malias(args)
    if code is None:
        print("""malias COMMAND [options]

Commands are:
  help
          This help.

  check
          Check alias file.

  test
          Test alias file.
""")
    elif code > 0:
        print("Bogus, error-code:", code)
    sys.exit(code if code else 0)


def test_malias (args):
    """Main function"""
    verbose = 0   # use 1, or... 9 for more verbose content!
    #verbose = 9
    if args == []:
        return None
    cmd = args[0]
    param = args[1:]
    if cmd == "help":
        return None
    if cmd == "check":
        return run_test(param, verbose)
    if cmd == "test":
        return run_test(param, verbose=9)
    print("Invalid command: {}\n".format(cmd))
    return None


def run_test(param, verbose, doSort=True):
    """Run simple 'test'
    """
    listed = []
    code = read_malias(param[0], param[1:], listed, verbose)
    for ma in listed:
        print("Mailbox:", ma.mainMail)
        these = sorted(ma.alias) if doSort else ma.alias
        for m in these:
            print(f"\t{m}")
        print(end = "" if len(listed) <= 1 else "\n")
    return code


def read_malias (inFile, mailBoxes, listed, debug=0):
    """read mail alias
    """
    numberOfM = len(mailBoxes)
    cprint(debug, "Reading", inFile, "; n# mailBoxes: {}".format(numberOfM))
    isOk = mails_ok(mailBoxes)
    if not isOk:
        return 3
    try:
        q = open(inFile, "rb")
    except PermissionError:
        return 13
    cont = q.read()
    # Make sure there is no '\r'
    if cont.find("\r".encode()) >= 0:
        return 6
    with open(inFile, "r") as p:
        cont = p.read().splitlines()
    for a in cont:
        s = a.strip(" \t\r")
        if a != s:
            cprint(debug, "(ERROR: unstripped line) " + s)
            return 5
    code, mas = process_malias(cont, debug)
    for ma in mas:
        if numberOfM > 0 and ma.mainMail not in mailBoxes:
            continue
        listed.append(ma)
        if debug > 0:
            dump_mail_alias(ma)
    return code


def dump_mail_alias(ma):
    print("")
    print("MailAlias({}), alias #{}".format(ma, len(ma.alias)))
    idx = 0
    for a in ma.alias:
        idx += 1
        print("alias({:02d}): {}".format(idx, a))


def process_malias (cont, debug=0):
    """process mail alias
    """
    assert isinstance(cont, list)
    assert isinstance(debug, int)
    code = 0
    mas = []
    listed = []
    ma = MailAlias("")
    n = cont.count("Mailbox Alias:")
    cprint(debug, "process_malias(),",
           "#{} line(s), 'Mailbox Alias:' {}".format(len(cont), n))
    i, line = 0, 0
    isAlias = True
    mbox = None
    mboxStr = ""
    last = None
    alias = []
    beforeLast = None
    for a in cont:
        line += 1
        if a.startswith("#"):
            continue
        if a == "Mailbox Alias:":
            if mboxStr == "":
                code = 103
                break
            isAlias = False
            mboxStr = ""
        elif isAlias:
            if mbox is not None:
                isOk = mbox.add_alias(alias)
                if not isOk:
                    cprint(debug, "Invalid mail(s):", alias)
                    code = 104
                    break
                listed.append(mbox)
                alias = []
            isOk = ma.valid_mail(a) != ""
            if isOk:
                posAt = a.find("@")
                assert posAt > 0  # e.g. w@yourdomain.com --> ownDomain is 'yourdomain.com'
                ownDomain = a[posAt+1:]
                mbox = MailAlias(a, ownDomain)
                mboxStr = a
                i += 1
                cprint(debug, "Mailbox#{}:".format(i), mbox)
            else:
                cprint(debug, f"Line {line}: Invalid mailbox: {a}")
                code = 101
                break
        elif a == "":
            if last == "":
                if beforeLast == "":
                    code = 102
                    break
                isAlias = True
        else:
            isOk = ma.valid_mail(a) != ""
            if isOk:
                alias.append(a)
            else:
                cprint(debug, "Wrongly formed mail:", a)
                code = 105
                break
        beforeLast = last
        last = a
    assert mbox
    if code != 0:
        return code, mas
    mbox.add_alias(alias)
    listed.append(mbox)
    return code, listed


def mails_ok (mails, debug=0):
    """Check whether mails are ok.
    """
    isOk = True
    if isinstance(mails, str):
        listed = [mails]
    else:
        listed = mails
    for m in listed:
        ma = MailAlias(m)
        y = ma.mainMail
        if debug > 0:
            print("m:", ma.mail, "as:", "(invalid)" if y == "" else y)
            print("ma.last:", ma.last)
        isOk = y != ""
        if not isOk:
            break
    return isOk


class AnyMail:
    """
    AnyMail abstract class
    """
    mail = None
    patMail = None
    last = (None, None, None)

    def init_anymail(self, m=""):
        self.mail = m
        self.patMail = re.compile(MAIL_REGEX)
        self.last = ("", "", "")


    def valid_mail(self, m, invalid="") -> str:
        assert self.patMail is not None
        domain = ""
        res = re.match(self.patMail, m)
        isOk = res is not None
        if isOk:
            isOk = m.find("..") == -1
        if isOk:
            domain = res.group(2)
        if domain and check_mail_domain(domain):
            self.last = (res.group(1), "@", domain)
            return m
        self.last = ("", "", "")
        return invalid


class MailAlias(AnyMail):
    """Mail Alias(es)
    """
    def __init__(self, mainMail, domain=(), alias=None):
        self.domain = domain
        self.init_anymail(mainMail)
        self.set_mail(mainMail)
        list_alias = [] if alias is None else alias
        self.alias = list_alias
        self.add_alias(list_alias)


    def get_mail (self):
        return self.mainMail


    def set_mail(self, mainMail=""):
        assert isinstance(mainMail, str)
        self.mainMail = self.valid_mail(mainMail)


    def add_alias(self, alias):
        if isinstance(alias, (list, tuple)):
            isOk = True
            for a in alias:
                isOk = self.add_alias(a)
                if not isOk:
                    return False
        else:
            isOk = self.valid_alias(alias, self.domain)
            if isOk:
                self.alias.append(alias)
        return isOk


    def valid_alias(self, alias, optDomain=None, debug=0):
        isOk = self.valid_mail(alias) != ""
        if optDomain is not None:
            checkDomain = check_domain(optDomain)
            if not checkDomain:
                isOk = False
        cprint(debug, "valid_alias('{}', '{}'): {}"
               "".format(alias, optDomain, "OK" if isOk else "NotOk"))
        assert isinstance(isOk, bool)
        return isOk


    def __str__ (self):
        s = self.mainMail
        return s


def check_domain(astr, debug=0) -> bool:
    assert isinstance(astr, str)
    dom = astr if astr.endswith(".") else (astr + ".")
    trees = dom.split(".")
    for sub in trees[:-1]:
        if not sub:
            return False
    assert sub
    # Check whether domain makes sense
    isOk = valid_tld("." + sub)
    return isOk


def check_mail_domain(astr, debug=0) -> bool:
    """ Same as check_domain(), but for mail name, e.g. abc@domain.com
    """
    basicOk = astr and not astr.endswith(".")
    isOk = basicOk and check_domain(astr, debug)
    cprint(debug, "Debug:",
           f"check_mail_domain({astr}), isOk? {isOk}, basicOk? {basicOk}")
    return isOk


def valid_tld(name) -> bool:
    """ Valid Top Level Domain, e.g. '.com', '.pt', '.uk', etc. """
    if not name or not name.startswith("."):
        return False
    sub = name[1:]
    isOk = len(sub) >= 2 and sub.isalnum()
    if not isOk:
        return False
    if isinstance(strict_TLD, (list, tuple)) and strict_TLD:
        isOk = name in strict_TLD
    return isOk


#
# Main script
#
if __name__ == "__main__":
    main()
