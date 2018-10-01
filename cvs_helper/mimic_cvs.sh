#!/bin/sh
#
# mimic_cvs.sh -- several commands to help CVS maintenance


[ "$BASE_DIR" = "" ] && BASE_DIR=$CVSROOT
[ "$BASE_DIR" = "" ] && BASE_DIR=$HOME


usage ()
{
 echo "$0 command [options]

Commands are:
	dir_perm	Dump dir permissions over x path(s).

	dir_perm_check	Check dir permissions.

	fix_perm	Fix dir permissions from CVS permissions.
"
 exit 0
}


function dir_perm ()
{
 local RES=2
 local D

 for D in $* ; do
	cd $BASE_DIR/$D
	[ $? != 0 ] && continue
	find * -type d -printf '%m:%p\n' | sort -nr
	RES=$?
 done
 return $RES
}


function dir_perm_check ()
{
 local RES
 local D

 for D in $* ; do
	if [ ! -d $BASE_DIR/$D ]; then
		echo "Bummer: $BASE_DIR/$D"
		return 2
	fi
 done
 dir_perm $* | grep " "
 RES=$?
 if [ $RES = 0 ]; then
	echo "Not OK: $BASE_DIR, $*"
	return 1
 fi
 echo "Ok: $*"
 return 0
}


function fix_perm ()
{
 local RES
 local D
 local PAIR

 local PERM
 local DNAME
 local S0
 local S1

 for D in $* ; do
	for PAIR in $(dir_perm $D) ; do
		echo $PAIR | grep : > /dev/null
		RES=$?
		if [ $RES != 0 ]; then
			echo "Ignoring: $PAIR"
		else
			PERM=$(echo $PAIR | sed 's/:.*//')
			DNAME=$(echo $PAIR | sed 's/[^:]*://')
			[ "$PERM" ] && chmod --changes $PERM $DNAME
		fi
	done
 done
 RES=0
 return $RES
}


#
# Main script
#
[ "$*" = "" ] && usage

case $1 in
	-h|--help)
		usage
		;;
	dir_perm)
		shift
		dir_perm $*
		RES=$?
		exit $RES
		;;
	dir_perm_check)
		shift
		dir_perm_check $*
		RES=$?
		exit $RES
		;;
	fix_perm)
		shift
		fix_perm $*
		RES=$?
		exit $RES
		;;
	*)
		usage;;
esac

# Exit status
exit $RES

