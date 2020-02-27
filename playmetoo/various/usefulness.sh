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
case $1 in
	.)
		echo "Enter '.' alone to quit..."
		shift
		run_useful $*
		;;
	office)
		shift
		grep -E "\.docx|\.xlsx" $*
		exit $?
		;;
	*)
		run_useful $*
esac
