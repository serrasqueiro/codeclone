#!/bin/sh
#
# usefulness.sh -- exercise names


example ()
{
 python3 /usr/local/lib/boris/audioconsole/scripts/usefulness.py hostnames $*
}


run_useful ()
{
 python $HOME/boris/audioconsole/scripts/usefulness.py hostnames $*
 return $?
}



#
# Main script
#
if [ "$*" = "" ]; then
	echo "Enter '.' alone to quit..."
fi
run_useful $*

