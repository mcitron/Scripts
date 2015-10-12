#!/bin/bash

MC_FOLDER="/vols/cms03/mastercode/Mastercode/"

EXPECTED_ARGS=1
if [[ $# -lt $EXPECTED_ARGS ]]
then
    LOCAL_FOLDER="mastercode"
else
    LOCAL_FOLDER=$1
fi

if [[ -d "$LOCAL_FOLDER" ]] 
then
    echo folder "$LOCAL_FOLDER" already exists please provide a unique name
    exit
fi

mkdir "$LOCAL_FOLDER"
mkdir "$LOCAL_FOLDER"/"SLHAs"
mkdir "$LOCAL_FOLDER"/"output"
cp "$MC_FOLDER"/config/*.txt "$LOCAL_FOLDER"
for txt in $( ls -1 "$LOCAL_FOLDER"/*.txt ); 
do
    chmod 664 $txt
done

CURR_DIR=$PWD
cd "$MC_FOLDER"/bin/

EXEs=`ls -1 *.exe`
cd $CURR_DIR
for exe in $EXEs;
do
   ln -s "$MC_FOLDER"/bin/"$exe" "$LOCAL_FOLDER"/"$exe" 
done

echo Successfully set up mastercode working area in "$LOCAL_FOLDER"
