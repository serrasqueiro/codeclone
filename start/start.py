# start.py  (c)2018  Henrique Moreira

"""
  start: manages codeclone repo.

  This is part of codeclone repository.

  Compatibility: python 2 and 3.

  Author:  Henrique Moreira
  github:  https://github.com/serrasqueiro/codeclone
"""


import sys


#
# usage()
#
def usage ():
  print("""python start.py COMMAND

Commands are:
    test          I test myself!
    check         Checks current repository.
""")
  sys.exit( 0 )
  pass


#
# run_program()
#
def run_program (args):
  validCmds = {
    'test':[0, []],
    'check':[1, []],
    'the-end':[999, []]
    }
  if len( args )<1:
      usage()
  cmd = args[ 0 ]
  if cmd not in validCmds:
    usage()
  cmdNr = validCmds[ cmd ][ 0 ]
  cmdOpt = validCmds[ cmd ][ 1 ]
  code = run_command( cmdNr, cmdOpt, args[ 1: ] )
  return code


#
# run_command()
#
def run_command (cmdNr, cmdOpt, opts):
  code = 0
  if cmdNr >= 999:
    print("run_command", cmdNr, "cmdOpt:", cmdOpt)
    print(">", opts)
    code = 0 if len( opts )<=0 else int( opts[ 0 ] )
    print("Exiting with code:", code)
    return code
  return code



if __name__=="__main__":
  code = run_program( sys.argv[ 1: ] )
  if type(code)==int and code!=0:
    sys.exit( code )
  pass

