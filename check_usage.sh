#! /bin/bash
EXPECTED_ARGS=2

# bail if we dont get 4 args
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: `basename $0` <username> <folder>" 
  echo "Using defaults <your user> <pwd>"
  USERNAME=`whoami`
  FOLDER=`pwd`
else
  USERNAME=$1
  FOLDER=$2
fi

#ls -lR $FOLDER | grep $USERNAME | \
#    awk -v user=$USERNAME -v loc=$FOLDER -F" " \
#    'BEGIN { x = 0 }; 
#        { x += $5 }; 
#     END { print user " is using " x/1048576 "MB in " loc }'

# find $FOLDER \( ! -regex '.*/\..*' \) -type f -user $USERNAME
# find $FOLDER -type f -not -name ".*" -user $USERNAME

find $FOLDER -user $USERNAME -exec ls -l {} \; 2>/dev/null |  \
    awk -v user=$USERNAME -v loc=$FOLDER -F" " \
    'BEGIN { x = 0 }; 
        { x += $5 }; 
     END { print user " is using " x/1048576 "MB in " loc }'
