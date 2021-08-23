#!/bin/bash

while [[ $# -gt 0 ]]
do
  key="$1"

  case $key in
    -o|--online_only)
    online_only=True
    shift # past argument
    echo ...showing online
    ;;
  esac
done



#sudo nmap -sn 192.168.0.0/24 | awk '/Nmap scan report for/{printf substr($0, index($0,$3)) ;}/MAC Address:/{print " => " $5}' | sort

output_dir=/mnt/samsung/backups/computers+phones
outfile_prefix=mac_addresses
outfile=${outfile_prefix}.$(date +%y%m%d-%H%M).txt
echo ...reporting to $outfile
echo Running as: `whoami `

sudo nmap -sn 192.168.0.0/24 | awk '/Nmap scan report for/{ipaddr=$5;}/MAC Address:/{print $3 " => " ipaddr " - " substr($0, index($0,$4)) }' | sort > ${output_dir}/${outfile}

# Make a list of everthing we've seen 
cat ${output_dir}/mac-consolidated-list.txt ${output_dir}/${outfile_prefix}* |sort -u > ${output_dir}/mac-consolidated-list.tmp
mv  ${output_dir}/mac-consolidated-list.tmp ${output_dir}/mac-consolidated-list.txt 

if [ $online_only ]; then 

  echo =====================================================================================
  {  cat ${output_dir}/mac-master-list.txt & awk '{print $0 "                  === ONLINE ===" }' ${output_dir}/${outfile}; }  |sort 
  echo =====================================================================================

else

  # Combine it with the master list 
  cat ${output_dir}/mac-master-list.txt ${output_dir}/mac-consolidated-list.txt |sort -u -k1,1 > ${output_dir}/mac-reconciled-list.txt
  echo =====================================================================================
  cat ${output_dir}/mac-reconciled-list.txt
  echo =====================================================================================
fi
echo ...done
rm ${output_dir}/${outfile}
