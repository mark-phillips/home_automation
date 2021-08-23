#!/bin/bash
if [ -z ${BACKUP_DIR} ]; then 
  echo !!!! Exit - no BACKUP_DIR set !!!!
  exit 99
fi
if [ ! -d ${BACKUP_DIR} ]; then 
  echo !!!! Exit - $ BACKUP_DIR does not exist  !!!!
  exit 99
fi
if [ -z ${host} ]; then 
  echo !!!! Exit - no host set !!!!
  exit 99
fi
echo === Backup for $host to $BACKUP_DIR ===

get_iplayer --pvr-list  > ~/pvr-list.bak

sudo tar --dereference --exclude='.npm' --exclude='.cache' --exclude='*.pdf' --exclude='*.m4a' --exclude='*Downloads*' --exclude='*iPlayerDownloads*' -czvf $BACKUP_DIR/backup-${host}.tgz  ~pi /var/www/ /etc/systemd* /etc/ssh/sshd_config /etc/init.d/monit* /etc/hosts /etc/monit* /etc/logrotate* /mnt/samsung/home_shared/*

