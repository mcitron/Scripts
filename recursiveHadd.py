#!/usr/bin/python
import optparse
import os
import string
from collections import OrderedDict as odict
import glob
import sys,stat,shlex,subprocess
import random

def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('--maxJobsPerStage',type = int, default = 999, help="max jobs to submit per stage")
    parser.add_option('--minFilesPerJob',type = int, default = 5, help="minimum files to hadd per stage")
    parser.add_option('-q','--queue', help="choose queue",default = "hepshort.q")
    parser.add_option('-c','--concurrent', help="choose concurrency",default = 999)
    parser.add_option('-f','--force', action = "store_true", help="Don't ask for confirmation")
    parser.add_option('-o','--outputDir', help="Output directory")
    parser.add_option('-n','--name', help="Output name for hadded root file",default = "output.root")
    parser.add_option('-i','--inputDir', help="Input directory")
    options,args = parser.parse_args()
    if options.outputDir != None:
        options.outputDir = os.path.abspath(options.outputDir)
    assert options.inputDir != None, "Need input dir to be defined!"
    options.inputDir = os.path.abspath(options.inputDir)
    return options

def makeShellScript(name,commands):
    with open(name,'w') as f:
        for command in commands:
            f.write(command+"\n")
    st = os.stat(name)
    os.chmod(name, st.st_mode | stat.S_IEXEC)
    return name
def processCmd(cmd):

    args = shlex.split(cmd)
    sp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    if sp.returncode != 0: print out, err

    return out, err
def checkUserInput(force,jobsSubmit):
    totalJobs = 0
    for stage,jobDict in jobsSubmit.iteritems():
	totalJobs += len(jobDict) 
    if not force:
	userInput = None
	while (userInput is not "n" and userInput is not "y"):
	    userInput = raw_input( "Will submit {0} total jobs over {1} stages. Is this OK? [y/n]".format(totalJobs,len(jobsSubmit)) )        
	    if userInput == "n": sys.exit(1)
	    elif userInput == "y":
		pass
	    else:
		print 'Type "y" or "n" next time...'
    else:
	print "Will submit {0} total jobs over {1} stages".format(totalJobs,len(jobsSubmit))        

def prepareJobs(jobsSubmit,shellDir,nameForFile):
    jobs = odict()
    randomString = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    for stage in jobsSubmit:
        shellPath = os.path.join(shellDir,"submit_stage{0}_{1}.sh".format(stage,nameForFile))
        jobs[shellPath.split("/")[-1].replace(".sh","")+"_"+randomString] = (shellPath,len(jobsSubmit[stage]))
        commands = []
        for iChunk,chunk in enumerate(jobsSubmit[stage]):
            commands.append('command[{0}]="hadd -f {1} {2}"'.format(iChunk+1,chunk,' '.join(jobsSubmit[stage][chunk])))
        commands.append('eval ${command[${SGE_TASK_ID}]}')
        makeShellScript(shellPath,commands)
    return jobs

def submit(jobs,queue,concurrent):
    iJob = 0
    jobNames = jobs.keys()
    for jobName,(shellScript,nJobs) in jobs.iteritems():
        submitString = " ".join(["qsub",'-o /dev/null -e /dev/null',"-q",queue,"-t","1-"+str(nJobs),'-tc',str(concurrent),'-N',jobName])
        if iJob > 0:
            submitString += " -hold_jid {0}".format(jobNames[iJob-1])
        submitString += " "+shellScript
        iJob += 1
        out,err = processCmd(submitString)
        print out,err

    

def getSubmitDict(maxJobsPerStage,minFilesPerJob,files,outputDir,name):
    chunksDir = outputDir+"/chunks" 
    outputName = outputDir+"/"+name
    N = len(files)
    stage = -1
    jobsSubmit = odict()
    while N > 1:
	stage += 1
	jobsSubmit[stage] = {}
	filesPerJob = N/maxJobsPerStage
	if filesPerJob < minFilesPerJob:
	    filesPerJob = minFilesPerJob
	filesPerJob = int(filesPerJob)
        for iChunk,chunk in enumerate(chunks(files,filesPerJob)):
            lastKey = '{0}/stage{1}_chunk{2}_{3}'.format(chunksDir,stage,iChunk,name)
            jobsSubmit[stage][lastKey] = chunk
	files = jobsSubmit[stage].keys()
	N = len(jobsSubmit[stage])
    if stage == -1:
        return None
    if not os.path.exists(chunksDir): os.mkdir(chunksDir)
    jobsSubmit[stage][outputName] = jobsSubmit[stage].pop(lastKey)
    return jobsSubmit

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
	yield l[i:i+n]

def recursiveHadd(maxJobsPerStage,minFilesPerJob,force,inputDir,outputDir,name,queue,concurrent):
    assert outputDir != None,"Need outputDir to be defined!"
    nameForFile = name.replace(".root","")
    files = glob.glob(inputDir+"/*.root")
    shellDir = outputDir+"/tmp"
    jobsSubmit = getSubmitDict(maxJobsPerStage,minFilesPerJob,files,outputDir,name)
    if not os.path.exists(outputDir): os.makedirs(outputDir)
    if not os.path.exists(shellDir): os.mkdir(shellDir)
    checkUserInput(force,jobsSubmit)
    jobs = prepareJobs(jobsSubmit,shellDir,nameForFile)
    submit(jobs,queue,concurrent)

if __name__ == "__main__":
    recursiveHadd(**vars(parse_args()))
