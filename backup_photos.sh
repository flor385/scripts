#!/bin/sh

echo "\n\tPhoto backup script. For Lasta by Flor :o)\n"

BACKUP_DRIVE=/media/${USER}/rumpl

echo "Looking for the backup drive at $BACKUP_DRIVE"
if [ -d "$BACKUP_DRIVE" ]; then
	echo "Backup drive found. Can proceed.\n"
else
	echo "Backup drive NOT found. Will quit.\n"
	# exit 1
fi


Backup() {

	echo "Looking for folder to backup: $1"
	if [ -d "$1" ]; then
		DEST=$BACKUP_DRIVE/$2/
		echo "Folder $1 found."
		echo "Performing backup to folder $DEST"
		rsync -utrv $1 $DEST
		echo "Backup of $1 done.\n"
	else
		echo "Folder $1 NOT found. Skipping backup.\n"
	fi
}

Backup /media/${USER}/TRANSCEND/arhiva/ arhiva_transo
Backup /media/${USER}/KUTIJA/arhiva/ arhiva_kutija
