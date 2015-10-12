#! /usr/bin/env python

import re,time

from commands import getoutput
from operator import itemgetter
from getpass  import getuser
from bcolors import bcolors
from bcolors import setuphighlighting
from sys import argv

from userlists import GCOL
from userlists import GROUP_NAMES
from userlists import get_users_color
from userlists import get_users_full_name

__G_JOBS = {}

__G_GROUPS = {}

def uniquify(seq):
    return {}.fromkeys(seq).keys()

def makefielddict( names, widths ) :
    starts = [ sum(widths[:i]) for i in range(len(widths)) ]
    ends   = [ sum(widths[:i+1]) - 1 for i in range(len(widths)) ]
    fields = {}
    for name, start, end in zip( names, starts, ends ) :
        fields[name] = [ start, end ]
    return fields

def getuserjobs( queuenames = [ "hepshort.q", "hepmedium.q", "heplong.q" ],
                 queuetimes = [            1,             6,          72 ],
                 imminent_f = 0.10 ) :
    TITLE_LINES = 2
    field_widths = [ 8, 8, 11, 13, 6, 20, 31, 6, 12 ]
    field_titles = [ "id", "priotiry", "name", "user", "state", "start",
                     "queue", "slots", "ja-task-id" ]

    fields = makefielddict( field_titles, field_widths )

    # we could just do qstat -u *, and then assign queue = job_temp["queue"];
    # this leaves some queeud jobs unassigned to a queue, as qstat doesn't print
    # hteir queue (it only shows them in the queue listing).
    # this wuold save calls to qstat, but is less accurate
    user_jobs = {}
    expiring = {}
    for q,queue in enumerate(queuenames) :
        alljobs = getoutput('qstat -u "*" -q %s' % queue )
        joblines = alljobs.split("\n")[TITLE_LINES:]

        for job in joblines :
            job_temp = {}
            for field in fields :
                job_temp[field] = job[ fields[field][0]:fields[field][1]].rstrip()
            user   = job_temp["user"]
            state  = job_temp["state"]
            id     = job_temp["id"]

            if state == "r" :
                j_start  = time.strptime( job_temp["start"], "%m/%d/%Y %H:%M:%S" )
                begin    = time.mktime( j_start )
                end      = begin + queuetimes[q]*60*60
                now      = time.mktime( time.localtime() )
                remain   = end-now
                imminent = imminent_f*(queuetimes[q]*60*60)
                if remain < imminent :
                    expiring.setdefault(user,[]).append( id )

            if queue != '' :
                __G_JOBS[id] = queue
            job_val = 1
            if "-" in job_temp["ja-task-id"] :
                ja_fields = re.split("[-:]",job_temp["ja-task-id"])
                ja_start = int(ja_fields[0])
                ja_end   = int(ja_fields[1])
                if len(ja_fields)>2 and ja_fields[2]:
                    ja_step  = int(ja_fields[2])
                else:
                    ja_step = 1
                job_val = (ja_end - ja_start) / ja_step
            if queue == '' : # try and find the job from the global list
                queue = __G_JOBS.get( id, "" )
            for name,group in GROUP_NAMES.iteritems() :
                if user in group :
                    __G_GROUPS[name] = __G_GROUPS.get(name, 0)+job_val

            user_jobs.setdefault(user, {}).setdefault(queue, {} )[state] = \
                user_jobs.setdefault(user, {}).setdefault(queue, {}).get(state,0)+job_val
    for jobs in expiring.values() :
        uniquify(jobs)

    return user_jobs, expiring


def getqueuestatus() :
    TITLE_LINES = 1
    field_widths = [ 31, 6, 15, 9, 14, 6 ]
    field_titles = [ "machine", "qtype", "usage", "load", "arch", "states" ]
    fields = makefielddict( field_titles, field_widths )

    allservers = getoutput('qstat -f')
    serverlines = allservers.split("\n")[TITLE_LINES:]
    serverlines = [ x for x in serverlines if
        "---" not in x and not re.match("^[0-9# ]", x) and len(x)>1 ]


    queues = {}
    for server in serverlines :
        m_temp = {}
        for field in fields :
            m_temp[field] = server[ fields[field][0]:fields[field][1] ].rstrip()
        queue    = m_temp["machine"].split("@")[0]
        statuses = m_temp["usage"].split("/")
        #print statuses
        cores = { "reserved" : statuses[0],
                  "used"     : statuses[1],
                  "total"    : statuses[2]
                }
        for type,number in cores.iteritems() :
            queues.setdefault(queue, {})[type] = \
                queues.setdefault(queue,{}).get(type,0)+int(number)
    return queues

def printusers( userinfo, queuelist = ["hepshort.q", "hepmedium.q", "heplong.q"],
                username = None, userlist = None, expiring = {} ) :

    format = "%-12s"
    format += "%-17s"*(len(queuelist) )
    format += "%-8s"

    userformat =  "%-10s"
    userformat += "%-17s"*(len(queuelist) )
    userformat += "%s"

    line  = "-"*( 11 + 17*len(queuelist) + 9 )
    hline = "="*( 11 + 17*len(queuelist) + 9 )


    title = [ "User" ] + queuelist + [ "Expiring" ]
    print line
    print format % tuple(title)
    print hline
    queued_total = [0]*len(queuelist)
    total_jobs = {}
    for user, qinfo in userinfo.iteritems() :
        queuedata_string = [""]*(len(queuelist))
        for i,queue in enumerate(queuelist) :
            r,qw,o = 0,0,0
            for state,count in qinfo.get(queue,{}).iteritems() :
                if state == 'r' :
                    r  += count
                elif state == 'qw':
                    qw += count
                else :
                    o  += count
            total_jobs[user] = total_jobs.get(user,0) + r+qw+o
            queuedata_string[i] = "[%3d,%5d,%4d]" % (r,qw,o)
            queued_total[i]+=qw

        ucolor = get_users_color( user )
        if ucolor :
            print ucolor + "*" + bcolors.OFF,
        else :
            print " ",
        exp = expiring.get(user,[])
        exp = len(exp)
        if exp == 0 :
            exp = "--"
        else :
            exp = str(exp)
        pr_list =[ user ] + queuedata_string + [ exp ]
        if user == username :
            print bcolors.HIGHLIGHT + userformat % tuple(pr_list) + bcolors.OFF
        elif user in userlist :
            print bcolors.BOLD + userformat % tuple(pr_list) + bcolors.OFF
        else :
            print userformat % tuple(pr_list)
    print line
    print format % tuple( ["Queued:"] + [ "%9d" % t for t in queued_total ] + [""] )
    print line
    for group, count in __G_GROUPS.iteritems() :
        print "%s%6s%s %d" % ( GCOL[group], group, bcolors.OFF, count ),
    print
    for u in userlist :
        tjobs = total_jobs.get(u,0)
        print "%s   %s %s %s [%d]" % (bcolors.BOLD, u, bcolors.OFF, get_users_full_name(u), tjobs ),
    if userlist: print


def printexpiring( expiring ) :
    line = "-"*( 11 + 15*(len(queuelist)) )
    if len( expiring.keys() ) > 0 :
        print line
        print "Expiring"
        print line
        for user, jobs in expiring.iteritems() :
            print "\n%s%10s%s : %d" % ( get_users_color( user ), user,
                                        bcolors.OFF, len( jobs ) ),
    print

def printqueue( queueinfo ) :
    # want to sort them by cores first
    qnames =  sorted( queueinfo, key=queueinfo.get("total"), reverse=True )
    print "-"*23
    print "%-12s%5s%6s" % ( "Queue", "Free", "Total" )
    print "="*23
    format_string = "%(queue)-12s%(free)5d%(total)6d"
    for queue in qnames :
        jobs = queueinfo[queue]
        free = jobs["total"] - jobs["reserved"] - jobs["used"]
        print format_string % {'queue':queue,'free':free,'total':jobs["total"]}
    print "-"*23
    return qnames

setuphighlighting()
username = getuser()
queue_info = getqueuestatus()
queue_names = printqueue( queue_info )
user_info, expiring = getuserjobs( queue_names )
printusers( user_info, queue_names, username, argv[1:], expiring)
print "\n   [ " + bcolors.BOLD + "did you know:" + bcolors.OFF + " QSTAT will highlight usernames given as arguments ]\n"
