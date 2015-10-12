computerList=(heppc238 heppc52) 
#heppc108 - crap
#heppc164 - slc5
minUsers=99
for computer in ${computerList[@]}; 
do 
    users=$(ssh $computer 'users')
    arr=($users)
    numUsers=$(for i in ${arr[@]}; do echo $i;done | sort -n | uniq | wc -l)
    if [ "$numUsers" -eq 0 ]; then
	minUsers=$numUsers
	computerToLogInto=$computer
	break
    elif [ "$minUsers" -gt "$numUsers" ]; then
	minUsers=$numUsers
	computerToLogInto=$computer
    fi
done
echo $computerToLogInto "has "$minUsers" users - logging in there"
ssh -XY $computerToLogInto

