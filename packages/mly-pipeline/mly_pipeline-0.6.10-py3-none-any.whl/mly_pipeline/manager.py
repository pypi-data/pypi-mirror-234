
import os
# Scipy and numpy env parameters that limit the threads
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import json
import pickle
import argparse
import sys ,time
import pandas as pd
import os
import logging
import subprocess
import random

from mly.tools import dirlist
from mly.datatools import *
from .search_functions import *
from dqsegdb2.query import query_segments
from gwpy.segments import Segment, SegmentList, DataQualityFlag
from gwpy.time import from_gps, to_gps
from datetime import datetime


# # # Managing arguments
# 
# List of arguments to pass:
arguments = [

    "restriction",
    "timeUnit"
]

#Construct argument parser:
parser = argparse.ArgumentParser()

parser.add_argument('--restriction')
parser.add_argument('--timeUnit')


# Pass arguments
args = parser.parse_args()

# Store arguments in dictionary:
kwdict = {}
for argument in arguments:
    kwdict[argument] = getattr(args, argument)
    
with open('config.json') as json_file:
    config = json.load(json_file)
    
config={ **kwdict , **config}


# # # Initialising logging
log_level = logging.getLevelName(config["log_level"])

# create logger
logger = logging.getLogger("logger_for_manager")
logger.setLevel(log_level)



# create console handler and set level to debug
ch = logging.handlers.TimedRotatingFileHandler('log/manager.log', when='H',interval=12, backupCount=1,)
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)





def main(config):

    config = checkOutputDirectoryArguments(config)

    # The size in which we group the outputs
    if config['maxDataFrameSize']==None: 
        config['maxDataFrameSize']=3600

    maxDataFrameSize = int(config['maxDataFrameSize'])


    # This is the time scale to use for the plots
    timeUnitDict={1:'s', 60:'m', 3600:'h', 24*3600:'days',30*24*3600:'months', 365*24*3600:'years'}

    if config['timeUnit']==None: 
        config['timeUnit']=3600
    else:
        config['timeUnit']=int(config['timeUnit'])
        

    sys.stdout.flush()


    lastdatetimehour = -1 # Hour index so that some processes run every hour only

    while (1):
        logger.debug(f"PROCESSES before output management: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        loopT0=time.time()
        
        output_directory = config['output_directory']
        
        frameSizeCheck=0
        fileList = dirlist(output_directory)
        dFramesList  = []
        jsonList = []
        # Listing the files in the directory
        # Separating the json from pkl
        for file in fileList:

            if ".json" in file:
                jsonList.append(file)
            elif ".pkl" in file:
                dFramesList.append(file)

        # if there are no new outputs we skip that step
        if len(jsonList)!=0: 

            # We expect that every time the manager runs, there is a tempFrame
            # file that might have events but it is not of the size we group
            # them (maxDataFrameSize). 
            try:

                with open(output_directory+'tempFrame.pkl','rb') as obj:
                    tempFrame = pickle.load(obj)
            # The first time manager is running this file is created instead.
            except Exception as e:
                tempFrame = pd.DataFrame(columns = ['gpstime','far','ifos'
                                                    ,'coincidence','coherency'
                                                    ,'combined','trigger'])
                logger.info(f"Creating tempfile for the first time.")

            # The size of the frame
            initialTempFrameSize=len(tempFrame)

            # A check value to make sure we add all the json files.
            frameSizeCheck = len(jsonList) + initialTempFrameSize

            # Adding all the events in json format to the tempFrame
            for file in jsonList:
                try:
                    with open(output_directory+file,"r") as jf:
                        p=json.load(jf)
                        jf.close()
                except Exception as e:
                    logger.warning(f"Exception in loading json file {file}, {e}")
                    continue



            # Reformating the score parameters to the desired format.
                for k in list(p['scores'].keys()):
                    p[k]=p['scores'][k]
                # Making a list of ifos to avoid line breaking into two
                p['ifos'] = [p['ifos']]

                if file[0]=='N':
                    p['trigger']=False
                elif file[0]=='T':
                    p['trigger']=True
                else:
                    p['trigger']=False


                del(p['scores'])  
                tempFrame=pd.concat([tempFrame, pd.DataFrame.from_dict(p)]
                                    ,ignore_index=True)

            # Reseting index and sorting by GPS time
            tempFrame=tempFrame.sort_values(by="gpstime").reset_index(drop=True)
            # Rearanging the columns
            tempFrame = tempFrame[['gpstime','far','ifos','coincidence','coherency'
                                ,'combined','trigger']]
            # Chopping the tempFrame to chuncs of maxDataFrameSize outputs
            # IMPORTANT: We don't separate them by hour, we just collect 
            # maxDataFrameSize of them together
            while len(tempFrame) > maxDataFrameSize:

                # Creating a newframe to include the maxDataFrameSize instances
                newFrame=tempFrame[:maxDataFrameSize]
                with open(output_directory+str(newFrame['gpstime'][0])+"-"
                        +str(newFrame['gpstime'][maxDataFrameSize-1])
                        +"_"+str(maxDataFrameSize)+'.pkl', 'wb') as output:
                    pickle.dump(newFrame, output, 4)

                logger.info("Saving group of outputs: ", output_directory+str(newFrame['gpstime'][0])+"-"
                    +str(newFrame['gpstime'][maxDataFrameSize-1])
                    +"-"+str(maxDataFrameSize)+'.pkl')

                # Removing the newframe from tempFrame
                tempFrame=tempFrame[maxDataFrameSize:].reset_index(drop=True)

                frameSizeCheck-=maxDataFrameSize

            # What is left in tempFrame, overights the tempFrame.pkl
            with open(output_directory+'tempFrame.pkl', 'wb') as output:
                pickle.dump(tempFrame, output, 4)
                logger.info(f"Saving the incomplete group of outputs: {output_directory}tempFrame.pkl")

            
            # We remove all json files already included in a dataFrame
            for file in jsonList:
                os.system("rm "+output_directory+file )


            
        logger.debug(f"PROCESSES before FAR management: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        # # # FileSystem for FAR management
        #
        # Listing all files saved in the temp file (files to be managed)
        detectors= list( det for det in config['detectors'])
        
        t0=time.time()

        numberOfFiles={}
        fileNumbers={}
        dataSetDict={}
        
        # For each detector we count how many files have been saved in all
        # detectors and we sort them.
        for det in detectors:
            numberOfFiles[det] = len(dirlist(config['masterDirectory']+'/temp/'+det))
            fileNumbers[det] = sorted(list(file.split('_')[0] for file in dirlist(
                config['masterDirectory']+'/temp/'+det)))
            dataSetDict[det] = []

        # If there are no files we skip this step
        if len(fileNumbers[detectors[0]])==0:
            logger.info(f"Empty temp directory")
            #time.sleep(60)
            
        # If the files included in temp are less than maxDataFrameSize, we skip
        # this step.
        elif (int(float(fileNumbers[detectors[0]][-1]))
            -int(float(fileNumbers[detectors[0]][0]))) < maxDataFrameSize:
            logger.info(f"Not enough data \
                        {maxDataFrameSize - (int(float(fileNumbers[detectors[0]][-1])) -  int(float(fileNumbers[detectors[0]][0])))}\
                        to run the FAR test yet")
            
        # If the files included in temp are enough we group them
        elif (int(float(fileNumbers[detectors[0]][-1]))
            -int(float(fileNumbers[detectors[0]][0]))) >= maxDataFrameSize:
            
            c=0
            
            # We keep track of the files used to delete them later
            filesToDelete=[]
            
            # Checking that all detectors have the same number of files
            logger.debug(f"Number of files for each detector: {list(len(fileNumbers[det]) for det in detectors)}")
            
            lastFileNumber=None
            # print("group size check: ",len(fileNumbers[detectors[0]][:int(maxDataFrameSize)]))
            
            for filenumber in fileNumbers[detectors[0]][:int(maxDataFrameSize)]:

                # For each file we in first detector we check that it exists in the
                # other detectors too. 
                if all( list( os.path.isfile(config['masterDirectory']
                                            +'/temp/'+det+'/'+fileNumbers[detectors[0]][c]
                                            +'_1.pkl') for det in detectors)):
                    _temp_dataSetDict = {}

                    try:
                        for det in detectors:
                                _temp_dataSetDict[det] = DataPod.load(config['masterDirectory']
                                                        +'/temp/'+det+'/'+str(filenumber)+'_1.pkl')
                        for det in detectors:

                            dataSetDict[det].append(_temp_dataSetDict[det])

                    except Exception as e:

                        logger.warning("Empty file detected: "+config['masterDirectory']
                                            +'/temp/'+det+'/'+str(filenumber)+'_1.pkl')

                            
                        
                    lastFileNumber=int(float(filenumber))
                    filesToDelete.append(str(filenumber)+'_1.pkl')
                    
                    
                
                # Othewise we delete it and it can't be used
                else:
                    filesToDelete.append(str(filenumber)+'_1.pkl')
                
                c+=1

            # We use those two for name creation
            first = str(int(float(fileNumbers[detectors[0]][0])))
            last = str(lastFileNumber)
            # print('first,last: ',first,last)
            
            # Saving the instances in dataSets
            for det in detectors:
                _set = DataSet(dataSetDict[det])
                name = first+'-'+last+'_'+str(len(_set))
                _set.save(config['masterDirectory']+'/' + det + '/' + name)

                # # Deleting files that already passed.
                for file in filesToDelete:
                    try:
                        os.system("rm "+config['masterDirectory']+'/temp/'+det+'/'+file)
                    except Exception as e:
                        pass

        logger.debug(f"PROCESSES before efficiency and buffers management: {subprocess.check_output(['pgrep','-c', '-w','-u',config['user_name']]) }")

        # # # Efficiency test buffer management
        #

        if os.path.isdir(config['efficiencies']):
            manage_efficiency_test(config)

        # # # FAR test management 
        #

        manage_FAR_inefernce_files(config)
        
        # Updates latest segment plot
        if datetime.now().hour != lastdatetimehour:
            print('start segments plot')
            segments_plot()
            print('end segments plot')

        # Update FAR plot
        far_plot()
        # # # Update status page
        manage_status_page()  

        # Timing
        logger.info(f"Manager loop time:{time.time()-loopT0}, waiting 5 minutes ... ")
        sys.stdout.flush()

        time.sleep(5*60)
        





def manage_efficiency_test(config = None):

    if config is None:
        with open('config.json') as json_file:
            config = json.load(json_file)

    np.random.seed(config['seed'])
    random.seed(config['seed'])

    # # # Efficiency test buffer management
    
    
    # How many inferences to wait to run the test, roughly how often in seconds

    efficiencyTestBuffer = config["eff_config"]["howOften"]

    # We load all the buffer pods that live in temp
    buffer_set = []
    pod_list = dirlist(config['bufferDirectory']+"/temp")
    # Shuffling the pods so that the ones used are randomly distributed along the time.
    random.shuffle(pod_list)
    
    num_pods = len(pod_list)
    
    # If number of the buffer pods are more than maxDataFrameSize, we 
    # putting them in a dataSet to be used.
    logger.info(f"Buffer size accumulated: {num_pods}/{efficiencyTestBuffer} .Start efficiency test: {num_pods >= efficiencyTestBuffer}")
    # I there are enough buffer pods we can save them to be used in an efficiency test.
    if num_pods >= efficiencyTestBuffer:
        
        for each_pod in pod_list[:efficiencyTestBuffer]:
            pod = DataPod.load(config['bufferDirectory']+"/temp/"+each_pod) 
            buffer_set.append(pod)

        buffer_dataset = DataSet(buffer_set)
        buffer_dataset.save(config['bufferDirectory']+"/BUFFER_SET")

        # Deleting the files in temp
        for each_pod in pod_list:    
            os.remove(config['bufferDirectory']+"/temp/"+each_pod)
        
        issue_efficiency_test()
        logger.info(f"Efficiency test initiated")

def issue_efficiency_test():
    os.system("nohup python -m mly_pipeline.make_eff_estimation --mode condor > efficiencyTest.out &")

def manage_FAR_inefernce_files(config = None):

    if config is None:
        with open('config.json') as json_file:
            config = json.load(json_file)
    # # # FAR test management 
    #

    # The list of all temporary inference files
    if os.path.isdir(config['falseAlarmRates']):
        if config['far_config']['restriction']==None: 
            config['far_config']['restriction']=0.0
        
        restriction=float(config['far_config']['restriction'])
        
        inference_temp_files = dirlist(config['falseAlarmRates'])

        for directory in ['hourly', 'condor', 'FARfile','temp']:
            if directory in inference_temp_files: inference_temp_files.remove(directory)


        # The list of all the files in hourly (grouped by hour/DAG of generation)
        hourly_files = dirlist(config['falseAlarmRates']+"/hourly")

        # The list of all condor dagman directories
        condor_files =  dirlist(config['falseAlarmRates']+"/condor")

        # The group names (start-end gps) in inference_temp_files
        inference_temp_files_groups = list(file.split("_")[0] for file in inference_temp_files)
        inference_temp_files_groups = list(dict.fromkeys(inference_temp_files_groups))

        # The group names inside hourly
        hourly_files_groups = list(file.split("_")[0] for file in hourly_files)

        # The group names of condor directories
        condor_groups= list(file.split("_")[0] for file in condor_files)

        logger.debug(f"HOURLY GROUPS: {len(hourly_files_groups)}")
        logger.debug(f"TEMP GROUPS: {len(inference_temp_files_groups)}")

        # First we will go through the files that already have a group inside hourly
        # We will add them in their corresponding hourly group file and remove them 
        # from inference_temp_files

        for hgroup, hfile_name in zip(hourly_files_groups, hourly_files):

            if hgroup in inference_temp_files_groups:

                with open(config['falseAlarmRates']+"/hourly/"+hfile_name,'rb') as obj:
                    hfile = pickle.load(obj)
                
                hfile_size = int(hfile_name.split("_")[-1][:-4])

                to_remove_from_inference_temp_files = []

                for file_name in inference_temp_files:
                    
                    if hgroup in file_name:

                        with open(config['falseAlarmRates']+"/"+file_name,'rb') as obj:
                            file = pickle.load(obj)

                        file = file[file['score'] >= restriction]

                        hfile = pd.concat([hfile, file], ignore_index=True)
                        
                        # Adding the size of the file to the hourly file
                        hfile_size += int(file_name.split("_")[-1][:-4])

                        #TEMPORARY
                        os.system("rm "+config['falseAlarmRates']+"/"+file_name)
                        to_remove_from_inference_temp_files.append(file_name)

                new_hfile_name = "_".join(hfile_name.split("_")[:-1])+"_"+str(hfile_size)
                with open(config['falseAlarmRates']+"/hourly/"+new_hfile_name+'.pkl', 'wb') as output:
                    pickle.dump(hfile, output, 4)

                os.system("rm "+config['falseAlarmRates']+"/hourly/"+hfile_name)

                for file_name in to_remove_from_inference_temp_files:
                    inference_temp_files.remove(file_name)

        # Now we can create new hourly files for the new groups that appeared
        # First we reset the inference_temp_files. There will be no already existing froup
        # for those files

        # Reseting temp_file_groups 
        inference_temp_files_groups = list(file.split("_")[0] for file in inference_temp_files)
        inference_temp_files_groups = list(dict.fromkeys(inference_temp_files_groups))

        # A check to make sure all files left do not belong in an existing group.
        check = all( [ all([hgroup not in file for file in inference_temp_files]) for hgroup in hourly_files_groups] )
        logger.debug(f"All groups left are new: {check}")


        for tgroup in inference_temp_files_groups:

            to_remove_from_inference_temp_files = []

            for file_name in inference_temp_files:

                if tgroup in file_name:

                    if len(to_remove_from_inference_temp_files)==0:

                        with open(config['falseAlarmRates']+"/"+file_name,'rb') as obj:
                            new_hfile = pickle.load(obj)

                        new_hfile_size = int(file_name.split("_")[-1][:-4])

                        to_remove_from_inference_temp_files.append(file_name)
                    
                    else:

                        with open(config['falseAlarmRates']+"/"+file_name,'rb') as obj:
                            file = pickle.load(obj)

                        new_hfile = pd.concat([new_hfile, file], ignore_index=True)

                        new_hfile_size += int(file_name.split("_")[-1][:-4])

                        to_remove_from_inference_temp_files.append(file_name)

            new_hfile_name = tgroup+"_"+str(new_hfile_size)
            with open(config['falseAlarmRates']+"/hourly/"+new_hfile_name+'.pkl', 'wb') as output:
                pickle.dump(new_hfile, output, 4)

            logger.info(f"Informing / Saving FAR file : {config['falseAlarmRates']}/hourly/{new_hfile_name}.pkl")

            for file_name in to_remove_from_inference_temp_files:
                inference_temp_files.remove(file_name)

                #TEMPORARY
                os.system("rm "+config['falseAlarmRates']+"/"+file_name)

        logger.debug(f"This should be zero, inference_temp_files: {len(inference_temp_files)}")


        hourly_files = dirlist(config['falseAlarmRates']+"/hourly") 

        for i, hfile_name in enumerate(hourly_files):

            if i==0: 
                with open(config['falseAlarmRates']+"/hourly/"+hfile_name,'rb') as obj:
                    farfile = pickle.load(obj)

                farfile_size = int(hfile_name.split("_")[-1][:-4])
            else:
                
                with open(config['falseAlarmRates']+"/hourly/"+hfile_name,'rb') as obj:
                    farfile_part = pickle.load(obj)

                farfile = pd.concat([farfile, farfile_part], ignore_index=True)

                farfile_size += int(hfile_name.split("_")[-1][:-4])

        # Deleting the old FARfile before creating the new one (they have the size of tests on their name).
        farfile_to_delete = None
        old_far_files = dirlist(config['falseAlarmRates']+"/FARfile")
        for file in old_far_files:
            if 'FARfile_interpolation' not in file:
                farfile_to_delete = file
                logger.info(f"FARfile to be replaced: {farfile_to_delete}")
                break 

        if len(hourly_files)!=0:
            with open(config['falseAlarmRates']+"/FARfile/FARfile_"+str(farfile_size)+".pkl", 'wb') as output:
                pickle.dump(farfile, output, 4)

                logger.info(f"New FARfile saved: {config['falseAlarmRates']}/FARfile/FARfile_{farfile_size}.pkl")

            far_interpolation_output = far_interpolation(farfile, farfile_size, inverse = False)
            far_interpolation_output_inverse = far_interpolation(farfile, farfile_size, inverse = True)

            with open(config['falseAlarmRates']+"/FARfile/FARfile_interpolation.pkl", 'wb') as output:
                pickle.dump( far_interpolation_output , output, 4)
            with open(config['falseAlarmRates']+"/FARfile/FARfile_interpolation_reserve.pkl", 'wb') as output:
                pickle.dump( far_interpolation_output , output, 4)
                
            with open(config['falseAlarmRates']+"/FARfile/FARfile_interpolation_inverse.pkl", 'wb') as output:
                pickle.dump(far_interpolation_output_inverse , output, 4)
            with open(config['falseAlarmRates']+"/FARfile/FARfile_interpolation_inverse_reserve.pkl", 'wb') as output:
                pickle.dump(far_interpolation_output_inverse , output, 4)
            
            logger.info(f"New FARfile interpolations saced")

            if (farfile_to_delete is not None 
                    and farfile_to_delete!="FARfile_"+str(farfile_size)+".pkl"):
                os.system("rm "+config['falseAlarmRates']+"/FARfile/"+farfile_to_delete)
            
        # Overwriting config farfile when enough files
        if len(hourly_files)!=0 and (farfile_size) >= 1*365*24*3600 and (config['farfile'] != config['falseAlarmRates']+"/FARfile"):

            with open('config.json') as json_file:
                _config = json.load(json_file)
                _config['farfile'] = config['falseAlarmRates']+"/FARfile"
            with open("config.json", "w") as config_json:
                json.dump(_config, config_json,indent=4)
                config_json.close()

            logger.info(f"FARFILE UPDATED FROM THE TEMPORARY TO THE SEARCH LOCAL!")
            raise SystemError("This is just an interuption to load the new FAR sourse.")


# add here the page function
def manage_status_page():
    os.system("nohup python -m mly_pipeline.create_status_page --mode condor > status_page.out &")

def far_plot():

    farfile_path = config['farfile']


    for file in os.listdir(farfile_path):
        if 'interpolation' not in file:
            main_file = file
            break


    interpolation= farfile_path + '/FARfile_interpolation.pkl'
    inverse_interpolation= farfile_path + '/FARfile_interpolation_inverse.pkl'

    testnums=int(main_file.split('_')[-1][:-4])
    years_of_background = "{:0.2f}".format(testnums/365/24/3600)

    with open(interpolation,'rb') as handle:
        interp= pickle.load(handle)

    with open(inverse_interpolation,'rb') as handle:
        inverse= pickle.load(handle)

    s = np.arange(1e-2,1,1e-4)

    halfday_score = inverse(1/(12*3600))
    month_score = inverse(1/(30*24*3600))
    year_score = inverse(1/(365*24*3600))
    fouryear_score = inverse(1/(4*365*24*3600))

    # print(month_score,year_score,fouryear_score)

    data = interp(s)*24*3600*365
    # print(data[-1])
    fig, ax  = plt.subplots()

    ax.axis([s[0], 1, data[-1], data[0]])

    ax.loglog(s,data) # IFAR months
    ax.axvline(x=halfday_score,ls='--',color='black',label ='2/day')#,color=colours[i])
    ax.axvline(x=month_score,ls='--',color='green',label ='1/month')#,color=colours[i])
    ax.axvline(x=year_score,ls='--',color='orange',label = '1/year')#,color=colours[i])
    ax.axvline(x=fouryear_score,ls='--',color='red', label = '1/4years')#,color=colours[i])
    ax.set_title(f"Background score distribution of {years_of_background} years")
    ax.set_ylabel("IFAR (years)")
    ax.set_xlabel("Scores")

    ax.text(halfday_score, 1e3, "{:6.3f}".format(halfday_score), color ='black',fontweight ='bold',horizontalalignment = 'right',verticalalignment ='top')
    ax.text(month_score, 1e2, "{:6.3f}".format(month_score), color ='green',fontweight ='bold',horizontalalignment = 'right',verticalalignment ='top')
    ax.text(year_score, 1e1, "{:6.3f}".format(year_score), color ='orange',fontweight ='bold',horizontalalignment = 'right',verticalalignment ='top')
    ax.text(fouryear_score, 1e0, "{:6.3f}".format(fouryear_score), color ='red',fontweight ='bold',horizontalalignment = 'right',verticalalignment ='top')


    ax.legend()

    plt.savefig('far.png')


def segments_plot():


    detectors = config['detectors']

    if 'ONLINE' in config['search_mode']:

        end = int(to_gps(datetime.now().date()))-3600
        start = end-3600*24*3+3600

    elif 'OFFLINE' in config['search_mode'] and isinstance(config['segment_list'],(list,tuple)):

        start = config['segment_list'][0]
        end = config['segment_list'][-1]

    else:

        print('NO VALID SEGMENT INPUT WAS PROVIDED')

    detector_active_flag =  {'H': 'H1:DMT-ANALYSIS_READY:1'
                            ,'L': 'L1:DMT-ANALYSIS_READY:1'
                            ,'V': 'V1:ITF_SCIENCE:1'}
    detector_segments =[]

    time0 = time.time()
    for det in detectors:
        individual_detector_segment = query_segments(detector_active_flag[det], start, end)['active']
        detector_segments.append(individual_detector_segment)

    time1 = time.time()-time0

    coincident_segments = SegmentList(detector_segments[0])
    for segment in detector_segments[1:]:
        coincident_segments = coincident_segments & segment

    time2 = time.time()-time1


    files = sorted(os.listdir(config['masterDirectory']+'/'+detectors[0]))
    slist = SegmentList([])

    for file in files:
        try:

            start_gps = int(file.split('-')[0])
            duration = int(file.split('_')[1].split('.')[0])
            slist.append(Segment(start_gps,start_gps+duration + 1 ))
        except Exception as e:

            print(file,':', e)

    slist = slist.coalesce() 

    slist = slist & SegmentList([Segment(start, end)])
    time3 = time.time()-time2

    flag = DataQualityFlag(name=' '
                    , active=slist
                    , known=coincident_segments)

    plot = flag.plot(color='gwpy:ligo-hanford',alpha =0.6)
    #plt.title('Processed Segments the last 3 days')
    plot.savefig('segment_plot.png')


if __name__ == "__main__":
        
    main(config)
    


