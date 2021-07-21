#!/bin/bash
bash -c  "nohup tail -f /root/.megaCmd/megacmdserver.log >&0 2>1" &

echo "Performing login..."
if [[ "$USERNAME" != "NOBODY" ]] && [[ "$PASSWORD" != "CHANGEME" ]]; then
    mega-login $USERNAME $PASSWORD
else
    echo "Please specify a valid username and password with -e USERNAME and -e PASSWORD. Aborting."
    exit 1
fi

sleep 10

if [[ "$INT_SECONDS" == "" ]]; then
	echo "Please specify a valid -e INT_SECONDS command"
    	exit 1
fi

echo "Initializing sync loop..."
if [ -d /upload ]; then
	while true
	do
	    echo "start sync to mega"
	    mega-sync /upload $DEST_MEGA_FOLDER
	    sleep ${INT_SECONDS}
	done
else
    echo "Please mount the dir that you want to upload to /upload and set \$TARGET to remote dir. Aborting."
    exit 1
fi
/bin/bash $@
