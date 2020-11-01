# malias.py  (c)2020  Henrique Moreira

"""
  Basic mail alias (or other text alias)

  Compatibility: python 3.
"""

# pylint: disable=missing-docstring, invalid-name, line-too-long


import sys
import re


def main():
    """ Main script """
    args = sys.argv[1:]
    code = test_malias(args)
    if code is None:
        print("""malias COMMAND [options]

Commands are:
  help
          This help.

  test
          Test alias file.
""")
        code = 0
    assert isinstance(code, int) and code <= 255
    sys.exit(code)


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
    if cmd == "test":
        return run_test(param, verbose)
    print("Invalid command: {}\n".format(cmd))
    return None


def run_test(param, verbose):
    """Run simple 'test'
    """
    listed = []
    code = read_malias(param[0], param[1:], listed, verbose)
    for ma in listed:
        print("Mailbox:", ma.mainMail)
        for m in ma.alias:
            print("\t{}".format(m))
        print(end = "" if len(listed) <= 1 else "\n")
    return code


def read_malias (inFile, mailBoxes, listed, debug=0):
    """read mail alias
    """
    numberOfM = len(mailBoxes)
    if debug > 0:
        print("Reading", inFile, "; n# mailBoxes: {}".format(numberOfM))
    isOk = mails_ok(mailBoxes)
    if not isOk:
        return 3
    try:
        q = open(inFile, "rb")
    except PermissionError:
        return 13
    cont = q.read()
    # Make sure there is no '\r'
    if cont.find( "\r".encode() ) >= 0:
        return 6
    with open(inFile, "r") as p:
        cont = p.read().splitlines()
    for a in cont:
        pre = ""
        s = a.strip( " \t\r" )
        if a != s:
            if debug > 0:
                pre = "(ERROR: unstripped line) "
                print( pre+s )
            return 5
    code, mas = process_malias(cont, debug)
    for ma in mas:
        if numberOfM > 0 and ma.mainMail not in mailBoxes:
            continue
        listed.append(ma)
        if debug > 0:
            print("MailAlias({}), alias #{}".format( ma, len(ma.alias) ))
            idx = 0
            for a in ma.alias:
                idx += 1
                print("alias({:02d}): {}".format( idx, a ))
    return code


def process_malias (cont, debug=0):
    """process mail alias
    """
    assert isinstance(cont, list)
    assert isinstance(debug, int)
    code = 0
    mas = []
    listed = []
    ma = MailAlias( "" )
    n = cont.count( "Mailbox Alias:" )
    if debug>0:
        print("process_malias(),",
              "#{} line(s), 'Mailbox Alias:' {}".format( len(cont), n ))
    i = 0
    isAlias = True
    mbox = None
    mboxStr = ""
    last = None
    alias = []
    beforeLast = None
    for a in cont:
        if a=="Mailbox Alias:":
            if mboxStr=="":
                code = 103
                break
            isAlias = False
            mboxStr = ""
        elif isAlias:
            if mbox is not None:
                isOk = mbox.add_alias( alias )
                if not isOk:
                    if debug>0:
                        print("Invalid mail(s):", alias)
                    code = 104
                    break
                listed.append( mbox )
                alias = []
            isOk = ma.valid_mail( a )!=""
            if isOk:
                posAt = a.find( "@" )
                assert posAt>0  # e.g. w@yourdomain.com --> ownDomain is 'yourdomain.com'
                ownDomain = a[ posAt+1: ]
                mbox = MailAlias( a, ownDomain )
                mboxStr = a
                i += 1
                if debug>0:
                    print("Mailbox#{}:".format(i), mbox)
            else:
                if debug>0:
                    print("Invalid mailbox:", a)
                code = 101
                break
        elif a=="":
            if last=="":
                if beforeLast=="":
                    code = 102
                    break
                isAlias = True
        else:
            isOk = ma.valid_mail( a )!=""
            if isOk:
                alias.append( a )
            else:
                if debug>0:
                    print("Wrongly formed mail:", a)
                code = 105
                break
        beforeLast = last
        last = a
    assert mbox
    if code!=0:
        return code, mas
    mbox.add_alias( alias )
    listed.append( mbox )
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
        ma = MailAlias( m )
        y = ma.mainMail
        if debug>0:
            print("m:", ma.mail, "as:", "(invalid)" if y=="" else y)
            print("ma.last:", ma.last)
        isOk = y!=""
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

    def init_anymail (self, m=""):
        self.mail = m
        self.patMail = re.compile( '^([A-Za-z0-9]+[A-Za-z0-9._-]*)@([a-z0-9]+[a-z0-9_-]*[.][a-z0-9][a-z0-9._-]*)$' )
        self.last = ("", "", "")


    def valid_mail (self, m, invalid=""):
        assert self.patMail is not None
        res = re.match(self.patMail, m)
        isOk = res is not None
        if isOk:
            isOk = m.find( ".." )==-1
        if isOk:
            self.last = (res.group( 1 ), "@", res.group(2))
            return m
        self.last = ("", "", "")
        return invalid


class MailAlias(AnyMail):
    """Mail Alias(es)
    """
    def __init__ (self, mainMail, domain=(), alias=None):
        self.domain = domain
        self.init_anymail( mainMail )
        self.set_mail( mainMail )
        list_alias = [] if alias is None else alias
        self.alias = list_alias
        self.add_alias(list_alias)


    def get_mail (self):
        return self.mainMail


    def set_mail (self, mainMail=""):
        assert isinstance(mainMail, str)
        self.mainMail = self.valid_mail( mainMail )


    def add_alias (self, alias):
        if isinstance(alias, (list, tuple)):
            isOk = True
            for a in alias:
                isOk = self.add_alias( a )
                if not isOk:
                    return False
        else:
            isOk = self.valid_alias(alias, self.domain)
            if isOk:
                self.alias.append( alias )
        return isOk


    def valid_alias (self, alias, optDomain=None, debug=0):
        isOk = self.valid_mail( alias )
        if optDomain is not None:
            assert isinstance(optDomain, str)
            # ToDo: check whether domain makes sense
        if debug > 0:
            print("valid_alias('{}', '{}'): {}"
                  "".format(alias, optDomain, isOk))
        return isOk


    def __str__ (self):
        s = self.mainMail
        return s

#
# Main script
#
if __name__ == "__main__":
    print("Please import, test only, follows...")
    main()
