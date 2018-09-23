#!/bin/sh
#
# zero_opts.sh -- Henrique Moreira
#
# Several useful commands



usage ()
{
 echo "$0 COMMAND

Commands are:
    scrub [dir]		Scrub directory.
"
 exit 0
}


scrub ()
{
 local D=$1
 local RES=0
 local S_DIR=season_jornadas_txt

 if [ "$D" ]; then
	shift
 else
	D="."
 fi
 if [ "$1" ]; then
	[ "$1" != "--s-dir" ] && usage
	shift
	S_DIR=$1
 fi
 echo "Scrubbing $D, at S_DIR: $S_DIR"
 for Y in $D/$S_DIR/20?? ; do
	if [ ! -d $Y ]; then
		echo "Wrong year dir at $D/$S_DIR"
		return 2
	fi
	#scrub_year $Y $Y/cache
	scrub_year $Y /mnt/tmp/cache
 done
 return $RES
}


scrub_year ()
{
 local Y_DIR=$1
 local CACHE_DIR=$2
 local RES=0
 local J_FILE
 local R
 local N=1
 local Z
 local NUM_J=0

 [ "$1" = "" ] && usage
 [ "$1" = "$2" ] && usage
 if [ -d $CACHE_DIR ]; then
	echo "Skipping cached S_DIR: $CACHE_DIR"
 else
	mkdir $CACHE_DIR
	[ $? != 0 ] && return 1
	echo "Created cache: $CACHE_DIR/"
	for J_FILE in $Y_DIR/jornada??.txt ; do
		[ ! -f $J_FILE ] && return 3
		let NUM_J++
	done
	echo "Journeys: $NUM_J"
	while [ $N -le $NUM_J ] ; do
		Z=$(int_02d $N)
		J_FILE="$Y_DIR/jornada${Z}.txt"
		if [ ! -f $J_FILE ]; then
			echo "Unexpected missing file: $J_FILE"
			return 8
		fi
		grep -Hns @ $J_FILE
		if [ $? = 0 ]; then
			echo "Input $J_FILE contains char: @"
			return 4
		fi
		R=$CACHE_DIR/j_${Z}.txu
		cat $J_FILE | tr \\011 @ | gstrings -c normal | j_filter > $R
		head -1 $R | grep ^"JORNADA $N"
		if [ $? != 0 ]; then
			echo "Missing heading: $R"
		fi
		let N++
	done
 fi
 return $RES
}


int_02d ()
{
 echo $* | awk '{printf "%02d", $1}'
}


j_filter ()
{
 grep -v ^Classifica | \
	cat
}


#
# Main script
#
case $1 in
	help|-h|--help)
		usage
		;;
	scrub)
		shift
		scrub $*
		RES=$?
		;;
	*)
		usage
		;;
esac

# Exit status
exit $RES

