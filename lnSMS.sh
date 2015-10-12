#! /bin/bash

shopt -s extglob # we want to use ls with regex

val[0]="100"
val[1]="73"
val[2]="86"

suffix[0]=""
suffix[1]="0"
suffix[2]="1"

# use relative symbolic links
for dir in $@;
do
    # store original directory
    odir=`pwd`
    cd $dir
    typedir=${dir%/v[0-9]*}
    base=${typedir##*/}
    for i in {0..2};
    do
        file=`find ./ -regextype posix-extended -regex ".*_${val[$i]}(\.7)?.*\.root"`
        target="$base${suffix[$i]}.root"
        if [[ -f $target ]]; then
            read -n1 -p "Overwrite $target (y/n)?"
            if [[ "$REPLY" == [yY] ]]; then
                echo Removing $target
                rm -r $target
            else
                echo Skipping $target
                continue
            fi
        fi
        echo "Symlinking $file to $target"
        ln  -s $file $target
    done
    cd $odir
done
