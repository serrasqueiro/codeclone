#!/bin/sh
#
# copy_playlists.sh -- (c)2019 Henrique Moreira


WIN_BASH_T=/t


usage ()
{
 echo "$0:
	Copy playlists from PC to my server.
"
 exit 0
}


#
# find_plays() -- find playlists
#
find_plays ()
{
 local RES=0
 local PL_DIR=/mnt/tmp/listas
 local D_LIST="Music/ OneDrive/"

 is_windows
 if [ $? != 0 ]; then
	cd /c/users/h
	PL_DIR=$WIN_BASH_T/${PL_DIR}
 else
	cd /opt/local
 fi
 if [ ! -d $PL_DIR ]; then
	echo "Creating dir: $PL_DIR"
	mkdir -p $PL_DIR
	[ $? != 0 ] && return 4
 fi
 find $D_LIST -type f -name '*.vpl' -exec cp -av {} $PL_DIR \;
 find $D_LIST -type f -name '*.wpl' -exec cp -av {} $PL_DIR \;
 RES=$?
 return $RES
}


is_windows ()
{
 echo $SYSTEMROOT | grep -i win > /dev/null
 [ $? = 0 ] && return 1
 return 0
}


#
# Main script
#

if [ 1 = 1 ]; then
	find_plays
fi

# Exit status
exit $RES

