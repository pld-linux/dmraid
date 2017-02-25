#!/bin/sh

# Read functions
. /lib/rc-scripts/functions

if [ -x /sbin/dmraid ]; then
	modprobe -s dm-mod >/dev/null 2>&1
	modprobe -s dm-mirror >/dev/null 2>&1
	dmraidsets=$(LC_ALL=C /sbin/dmraid -s -c -i)
	if [ "$?" = "0" ]; then
		oldIFS=$IFS
		IFS=$(echo -en "\n\b")
		for dmname in $dmraidsets ; do
			[[ "$dmname" = isw_* ]] && continue
			/sbin/dmraid -ay -i --rm_partitions -p "$dmname"
			[ -x /sbin/kpartx ] && /sbin/kpartx -u -a -p p "/dev/mapper/$dmname"
		done
		IFS=$oldIFS
	fi
fi
