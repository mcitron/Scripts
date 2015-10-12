#! /usr/bin/env python
from __future__ import division

import sys
import os
import re
import commands
import getopt

import threading

import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime

queue_list = [ "hepshort.q", "hepmedium.q", "heplong.q" ]
graph_data = "data/q_data"
outfile = "/home/hep/sr505/public_html/q/test.png"

loop=False

# 600 for 10 mins
interval_seconds = 600
days_to_keep = 7

# get (floor) for number of intervals we'll need at current sampling rate
intervals_per_day = 86400 // interval_seconds
intervals_to_keep = intervals_per_day * days_to_keep

def file_len(fname):
    f = open(fname)
    i = 0
    for i,l in enumerate(f):
        pass
    return i+1

def trim_file_head(fname,n_lines):
    f = open(fname,"r")
    line_list = []
    for i,l in enumerate(f):
        if i >= n_lines: 
            line_list.append(l);
    f.close()
    f = open(fname,"w")
    for item in line_list:
        f.write(item)
    f.close()


def get_queue_status():
    n_entries = file_len(graph_data)
    # account for needing one line to write out new info to
    trim_lines =  ((n_entries - intervals_to_keep) + 1) 
    if trim_lines > 0:
        trim_file_head(graph_data,trim_lines)
        # trim from the top of file (the old entries)
    usage_list = [] 
    for q in queue_list :
        used = total = 0;
        cmd = 'qstat -f -q ' + q
        (error, qsumm) = commands.getstatusoutput(cmd)
        qsumm_lines = re.split('\n+',qsumm)
        qsumm_lines = [s for s in qsumm_lines if q in s]
        for line in qsumm_lines :
            fields = re.split('[ @/]+',line)
            used+=int(fields[4])
            total+=int(fields[5])
        usage = (used / total) * 100.
        usage_list.append(usage)
    f = open(graph_data,"a")
    for item in usage_list :
        f.write(str(item))
        f.write(" ")
    f.write("\n")
    f.close()
    # wait X seconds then run this all again

def draw_q_data():
    f = open( graph_data, "r" ) 
    queue_data = [ [] for i in range(len(queue_list)) ]
    for line in f.readlines():
        temp_list = line.split()
        if len(temp_list) == len(queue_list):
            for i in range(len(queue_list)):
                queue_data[i].append(float(temp_list[i]))
    xvals = range(len(queue_data[0]))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i,yval in enumerate(queue_data):
        ax.plot(xvals,yval,"-o",label=queue_list[i],markevery=intervals_to_keep-1)
    leg = ax.legend(loc=0)
    ax.grid(True)
    ax.set_xlabel('Time')
    ax.set_ylabel('Usage / %')
    ax.set_title('Batch Queue Usage')
    axis_range = [ 0, intervals_to_keep+20, 0., 100. ]
    ax.axis(axis_range)
    ax.xaxis.set_ticks( range(0,intervals_to_keep+intervals_per_day,intervals_per_day) )
    label_numbers = range(days_to_keep,-1,-1)
    list_of_labels = []
    for item in label_numbers:
        if item > 1 :
            new_str = str(item) + " days ago"
        elif item == 1:
            new_str = str(item) + " day ago"
        else:
            new_str = "Today"
        list_of_labels.append(new_str)
    ax.xaxis.set_ticklabels( list_of_labels )
    ax.tick_params('x',labelsize='small')

    for t in leg.get_texts():
        t.set_fontsize('small')
    plt.savefig(outfile)

def write_html_file():
    cureent_time = datetime.now()
    f = open("/home/hep/sr505/public_html/q/index.html","w")
    f.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN")
    f.write("\"http://www.w3.org/TR/html4/strict.dtd\">")
    f.write("<HTML>")
    f.write("   <HEAD>")
    f.write("        <TITLE>Imperial Batch Queue Usage</TITLE>")
    f.write("    </HEAD>")
    f.write("    <BODY>")
    f.write("        <table border=\"0\">")
    f.write("        <tr>")
    f.write("           <td><b>Last Updated</b>: " + str(current_time) + "</td>")
    f.write("        </tr>")
    f.write("        <tr>")
    f.write("           <td><img src=\"test.png\" alt=\"Batch Queue Graph\" /></td")
    f.write("        </tr>")
    f.write("        </table >")
    f.write("    </BODY>")
    f.write("</HTML>")
    f.close()

def start_loop(LOOP=False):
    get_queue_status()
    draw_q_data()
    write_html_file()
    if LOOP:
        threading.Timer(interval_seconds, start_loop).start() 
        
def main(argv=None):
    start_loop(loop)

if __name__ == "__main__":
    main()
