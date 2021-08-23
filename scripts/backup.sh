#!/bin/bash
export host=$HOSTNAME
if [ -z ${host} ]; then host="RASPBERRYPI"; fi
export BACKUP_DIR=/mnt/samsung/backups/computers+phones/${host}
if [ ! -d ${BACKUP_DIR} ]; then
  echo mkdir -p ${BACKUP_DIR}
  mkdir -p ${BACKUP_DIR}
fi
echo
echo === Backing up $host to ${BACKUP_DIR}===
echo ~/bin/backup_linux.sh
echo ----------------------------------------
~/bin/backup_linux.sh

echo 
echo === Rotate backups ===
echo ----------------------------------------
sudo rm  $BACKUP_DIR/backup-${host}.2.tgz
sudo mv $BACKUP_DIR/backup-${host}.1.tgz  $BACKUP_DIR/backup-${host}.2.tgz
sudo mv $BACKUP_DIR/backup-${host}.tgz  $BACKUP_DIR/backup-${host}.1.tgz
sudo rm  $BACKUP_DIR/backup-${host}.tgz

echo
echo === Host specific backup ===
echo ~/bin/backup-${host}.sh
echo ----------------------------------------
~/bin/backup-${host}.sh
