#! /bin/bash

#
# Prints a summary of the batch queues
#

# which queues are we interested in
queue_list="hepshort hepmedium heplong"

# get a list of users currently running jobs
USERS=`qstat -q "*" -u "*" | awk '{ if ($4!="user" && $4!="") print $4}' \
    | sort -u`
echo -e "USER\t R\tQW"
for u in $USERS; do
  # get users running and queued jobs on all queues in the system (could do a
  # for loop here over queue_list...
  # count=0; for q in $queue_list; do (( count+=`...` ))
  count=`qstat -q "*" -u $u | awk '\
    { if ($5=="r") running++; else if ($5=="qw") queued++} \
        END{printf("%d\t%d",running,queued)}'`
  #field length chekc for output
  if [ ${#u} -lt 8 ]; then
    echo -e "$u\t $count"
  else
    echo -e "$u $count"
  fi
done | sort -r $2

echo " _______________________________"
echo -e "| Queue\t\tFree\t(Total) |"
echo "|===============================|"

for q in $queue_list; do
  queue_summary=`qstat -f | grep $q | awk '{print $3}' |   \
    awk -F"/" '{total+=$3; used+=$2} END {free=total-used; \
    print free "\t(" total")"}'`
  echo -e "| $q:\t$queue_summary\t|"
done
echo "|_______________________________|"
