#! /usr/bin/env python

from commands import getoutput
from bcolors import bcolors

#ALL_USERS  = getoutput( "ls -l /home/hep/ | awk '{print $3" "}' | uniq" ).split()

# this should really be done with just a list rather than this output as it's
# fucking slow
#CMS_USERS    = getoutput( "ls -l /vols/cms0{1..4} | awk '{print $3" "}' | sort | uniq" ).split()
#T2K_USERS    = getoutput( "ls -l /vols/t2k{,01,02,03}/users | awk '{print $3" "}' |  sort | uniq" ).split()
#MICE_USERS   = getoutput( "ls -l /vols/mice{,2,3} | awk '{print $3" "}' | sort | uniq" ).split()
#LISA_USERS   = getoutput( "ls -l /vols/lisa00 | awk '{print $3" "}' | sort | uniq" ).split()
#ZEPLIN_USERS = getoutput( "ls -l /vols/zeplin00 | awk '{print $3" "}' | sort | uniq" ).split()

CMS_USERS = [ "aeg04", "ajg06", "ap401", "as1604", "awr01", "bbetchar", "bm409",
              "collngdj", "db1110", "elaird1", "gfball", "gkarapos", "hflaeche",
              "jm1103", "kjd110", "lgouskos", "magnan", "mc308", "mc3909",
              "mj509", "mk1009", "mp801", "mperuzzi", "mpioppi", "mryan",
              "mstoye", "nashja", "nrompoti", "nsaoulid", "nw709", "obuchmue",
              "pd108", "rjb3", "rjn04", "root", "sn2409", "sr505", "stuartw",
              "tapper", "trommers", "twhyntie", "zph04", "dauncey"
            ]

LHCB_USERS = [ "arichard", "as1905", "cp309", "egede", "etournef", "gc110",
               "is110", "kap01", "lhcb", "mpatel2", "mwillia1", "pns04", "po10",
               "rharji",  "sch11", "stc09", "tb200",  ]

T2K_USERS = [ "bs610", "gmk04", "itaylor", "jdobson", "jfv00", "jonssonp",
              "ms2609", "pds06", "pguzowsk", "pm304", "sd708", "ss3309",
              "wascko", "yoshiu", "akaboth"
            ]

LISA_USERS = [ "em909", "tjs", "pwass", "ac108", "haraujo" ]

MICE_USERS = [ ]
ZEPLIN_USERS = [ ]


GROUP_NAMES = { "cms" : CMS_USERS, "t2k" : T2K_USERS, "mice" : MICE_USERS,
                "lisa" : LISA_USERS, "zeplin" : ZEPLIN_USERS,
                "lhcb" : LHCB_USERS }

GCOL = { "cms" : bcolors.BLUE, "t2k" : bcolors.ORANGE, "mice" : bcolors.PINK,
         "lisa" : bcolors.RED, "zeplin" : bcolors.GREEN, "lhcb" : bcolors.LGREEN
       }

def get_users_group( user ) :
    g = None
    for group,users in GROUP_NAMES.iteritems() :
        if user in users :
            return group
    return g

def get_users_full_name( user ) :
    finger_user = getoutput( "finger %s" % user ).split()
    pos =  finger_user.index("Name:")
    pos2= finger_user.index("Directory:")
    return " ".join(finger_user[pos+1:pos2])

def get_users_color( user ) :
    return GCOL.get( get_users_group( user ), "" )
