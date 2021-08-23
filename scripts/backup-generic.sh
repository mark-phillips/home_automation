#!/bin/bash
#
#  System specific backup file
#
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

sudo tar --dereference --exclude='.npm' --exclude='.cache' --exclude='*.pdf' --exclude='*.m4a' --exclude='*Downloads/incomplete*' --exclude='*iPlayerDownloads*' -czvf $BACKUP_DIR/backup-${host}.tgz  ~pi /etc/*
