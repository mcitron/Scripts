#! /usr/bin/env python

from collections import Iterable
from array import array

def print_unpack( item, level = 0, ending_comma = False ) :
    if not isinstance( item, dict) : 
        if not isinstance( item, Iterable ) :
            print "\t"*level,"{item:.4}".format(item=item),
            if ending_comma :
                print ","
            else:
                print
        else :
            s = "(" if isinstance( item,tuple ) else "[" 
            e = ")" if isinstance( item,tuple ) else "]" 
            print "\t"*level,s,
            for i in item :
                print "{i:.4},".format(i=i),
            print e,
            if ending_comma :
                print ","
    else :
        print "\t"*level,"{"
        for key,value in item.iteritems() :
            print "\t"*(level+1),
            keystring = '"%s"' % key
            print '{k:20} : '.format( k=keystring ),
            print_unpack( value, 0, True )
        print "\t"*level,"}"

members = dir( obj )
for attr_name in members :
    if not "__" in attr_name :
        attr_data = getattr( slice, attr_name )
        print "{classname}.{obj} = ".format(classname="self", obj=attr_name),
        print_unpack( attr_data,1 )
        print
print "\n"
