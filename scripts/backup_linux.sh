#!/bin/bash
BACKUP_DIR=~/linux-backup-`hostname`/
if [ ! -d ${BACKUP_DIR} ]; then
  echo mkdir -p ${BACKUP_DIR}
  mkdir -p ${BACKUP_DIR}
fi
echo "Backing up to "$BACKUP_DIR

#
## To restore
## ==========
##  Under Debian/Ubuntu Linux type the following two commands 
##  to reinstall all the programs:
##  Once list is imported, use the dselect commmand to install the packages
# sudo apt-key add $BACKUP_DIR/Repo.keys
# sudo cp -R $BACKUP_DIR/sources.list* /etc/apt/
# sudo apt-get update
# sudo apt-get install dselect
# sudo dpkg --set-selections < $BACKUP_DIR/installed-software.log
# sudo apt-get dselect-upgrade -y
#
#
dpkg --get-selections > $BACKUP_DIR/installed-software.log
sudo cp -R /etc/apt/sources.list* $BACKUP_DIR/
sudo apt-key exportall > $BACKUP_DIR/Repo.keys

cp /etc/fstab $BACKUP_DIR
crontab -l > ${BACKUP_DIR}/crontab.bak
