#! /usr/bin/env python3

import os, sys, json, argparse, subprocess

def _parser():

    arguments = ["search_mode"
                 ,"path"
                 ,"output_directory"
                 ,"trigger_directory"
                 ,"masterDirectory"
                 ,"bufferDirectory"
                 ,"falseAlarmRates"
                 ,"efficiencies"
                 ,"detectors"
                 ,"reset"
                 ,"far"]

    
    #Construct argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--search_mode', type=str
                        , default = "DEFAULT_OFFLINE"
                        , help = "For automatically setting the pipeline for different uses"
                        , required = False)

    parser.add_argument('-p', '--path', type=str
                        , default = "./mlyPipelineOrigin"
                        , help = "The path and name of the"
                        +" directory to be used by mlyPipeline."
                        , required = False)

    parser.add_argument('-o', '--output_directory', type=str
                        , default = 'output_directory'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the results from every inference."
                        , required = False)

    parser.add_argument('-t', '--trigger_directory', type=str
                        , default = 'trigger_directory'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the triggers."
                        , required = False)

    parser.add_argument('-m', '--masterDirectory', type=str
                        , default = 'masterDirectory'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the plots from the triggers."
                        , required = False)

    parser.add_argument('-b', '--bufferDirectory', type=str
                        , default = 'bufferDirectory'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the data around every instance (buffer) to be used"
                        +" for the efficiecy tests"
                        , required = False)

    parser.add_argument('-f', '--falseAlarmRates', type=str
                        , default = 'falseAlarmRates'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the false alarm rate data."
                        , required = False)

    parser.add_argument('-e', '--efficiencies', type=str
                        , default = 'efficiencies'
                        , help = "The name of the"
                        +" directory to be used by mlyPipeline for the storage"
                        +" of the false alarm rate data."
                        , required = False)

    parser.add_argument('-d', '--detectors', type=str
                        , default = 'HLV'
                        , help = "The initials of the detectors used"
                        , required = False)
    
    parser.add_argument('-R', '--reset', type=bool
                        , default = False
                        , help = "If true it will ovewright the target path"
                        + " with a clean new filesystem."
                        , required = False)

    parser.add_argument('-far', '--far', type=bool
                        , default = True
                        , help = "If true it will include the FAR scripts used for background estimation. This is only for OFFLINE searches"
                        , required = False)




    
    # Pass arguments:
    args = parser.parse_args()
    
    # Store arguments in dictionary:
    kwargs = {}
    for argument in arguments:
        kwargs[argument] = getattr(args, argument)

    return kwargs
   
def connect_path_relatively_to(path_to_change,path_to_connect):
    common_part = []
    for dir in path_to_change.split('/'):
        if dir in path_to_connect.split('/'):
            common_part.append(dir)
        else:
            break

    common_part = '/'.join(common_part)

    new_path_to_change = path_to_change.split(common_part)
    
    return '..'+new_path_to_change[-1]

def createRunAllScript(**kwargs):
    
    """ Creating a script called runall.sh that withing the search director will
    run and manage all the scripts needed for the search.
    """
        
    with open(kwargs['path'] + '/' + 'runall.sh','w') as f:
        
        # Sourcing mlyPipeline module
        #f.write("source=" + kwargs['mlyPipelineSource'] + "\n")
        
        # Things to write only if OFFLINE mode is active 
        # (OFFLINE is not complete)
        if "OFFLINE" not in kwargs['search_mode']:
            
            # Loop that checks the state of the jobs and doesn't stop
            f.write("while true" + "\n")
            f.write("do" + "\n")
            
            # Collection of the process ids of the scripts
            f.write("   processID=()"+ "\n")
            # Used to sinchronise the independent scripts of the search
            f.write("   unixtime=$(date +%s)" + "\n")
            # The number of paralel schripts to run 
            # !Note: If you change this from the config, you will have to 
            #        edit in the runall.sh script by hand.
            f.write("   STEP="+str(kwargs['parallel_scripts'])+ "\n\n")
            
            # Lopp to run the scripts for the search
            f.write("   for INITIAL in `seq 0 $(($STEP-1))`" + "\n")
            f.write("   do" + "\n\n")
            f.write("       nohup python -m mly_pipeline.search"
                            +" --splitter [$STEP,$INITIAL]"
                            +" --time_reference $unixtime" 
                            +" &> search_step_$INITIAL.out & processID+=($(echo $!)) ; echo $!>>.jobids.txt" + "\n\n")
            f.write("   done" + "\n\n\n")
        
            # Script that runs the manager script
            f.write("   nohup python -m mly_pipeline.manager &> manager.out & processID+=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
            
            # If the search runs as expected by default, it will also run scripts
            # for generating timelags and running FAR tests.
            if kwargs['far_config']['far_enabled']:
                f.write("   nohup python -m mly_pipeline.continuous_FAR --mode generation &> continuous_FAR_generation.out & processID+=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("   nohup python -m mly_pipeline.continuous_FAR --mode inference &> continuous_FAR_inference.out & inferenceID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
            
            # # # Maintenance of jobs 
            
            # If total_failure becomes 1, the script runs everything from scratch
            f.write("    total_failure=0" + "\n")
            
            # Sometimes the FAR script might stal indefinetly for unknow reasons
            # related to triton package, so if it does we restart it.
            if kwargs['far_config']['far_enabled']:

               f.write("    staling_points=0" + "\n")
            
            # We add the number of timelag files present to see if our rate of 
            # doing FAR inference is efficient. Check the monitor.txt present in
            # the search directory, if there are too many zeros we can increase
            # our timelag production - "lags", always along with "batches". If
            # there are no zeros, we need to decrease the "lags" or inference 
            # does not work properly.
            f.write("    echo $(ls falseAlarmRates/temp | wc -l) >> monitor.txt" + "\n")
                    
            # Loop that checks if the main (not inference) scripts are running
            # every minute.
            f.write("    while [ $total_failure -ne 1 ]" + "\n")
            f.write("    do" + "\n")
            f.write("        sleep 60" + "\n\n")
                    
            # Updating the number of lag files for monitoring
            f.write("        echo $(ls falseAlarmRates/temp | wc -l) >> monitor.txt" + "\n")
            
            # Checking all scripts (not inference), if one fails total_failure=1
            f.write("        for pid in \"${processID[@]}\"" + "\n")
            f.write("        do" + "\n")
                    
            f.write("            if ! ps $pid > /dev/null" + "\n")
            f.write("            then" + "\n")
            f.write("                total_failure=1" + "\n")
            f.write("                echo total failure" + "\n")
            f.write("                break" + "\n")
            f.write("            fi" + "\n") 
            f.write("        done" + "\n")

            # Specifically for inference script we check seperatelly, if it
            # doesn't look properly we rerun only the inference script. 
            if kwargs['far_config']['far_enabled']:

            
                # Checking if the number of inference files stays 0 for a long time.
                # If lag files increase without any new inference files, that means
                # staling, and we add a staling point. If not we reset it to 0.
                f.write("        if [ $(ls falseAlarmRates | wc -l) -eq 4 ] && [ $(ls falseAlarmRates/temp | wc -l) -ne 0 ]" + "\n")
                f.write("        then" + "\n")
                f.write("            echo stalling points increase to $staling_points" + "\n")   
                f.write("            ((staling_points=staling_points+1))" + "\n")
                f.write("        else" + "\n")
                f.write("            staling_points=0" + "\n")
                f.write("        fi" + "\n")

                # In case inference script gets killed or we have at least 5 minutes
                # of staling, we restart inference script. Although, we keep the 
                # corresponding unix time it got killed in the name of the  output
                # file.
                f.write("        if ! ps $inferenceID > /dev/null || [ $staling_points -gt 5 ]"+ "\n")
                f.write("        then" + "\n")
                f.write("            singularity instance stop --all" + "\n")
                f.write("            nohup python -m mly_pipeline.continuous_FAR --mode inference >"
                                    +" continuous_FAR_inference_$(date +%s).out 2>&1"
                                    +" & inferenceID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("        fi" + "\n")

                    
            f.write("   done" + "\n")
                    
            # If the previous loop exits, it means there was a total_failure=1
            # So we will have to rerun everything. But first we kill the python
            # scripts (inference included).
            # !Note: We are not remove any condor jobs from the lag generation
            #        script because they do not interfere with the scripts.
            f.write("   for pid in \"${processID[@]}\"" + "\n")
            f.write("   do" + "\n")
            f.write("       kill $pid" + "\n")
            f.write("   done" + "\n")
            
            if kwargs['search_mode'] not in ["O3MDC" , 'BENCHMARK_MDC_OFFLINE']:
                f.write("   kill $inferenceID" + "\n")
                f.write("   singularity instance stop --all" + "\n")

            f.write("done" + "\n")
        
        # Currently the offline script is very simple (under developement)
        else:

            if kwargs['far_config']['far_enabled']:

                f.write("nohup python -m mly_pipeline.offline_search --mode set_file_system &> set_file_system.out & echo $!>>.jobids.txt" + "\n\n")
                
                f.write("while [ $(ls masterDirectory/*.py | wc -l) -eq 0 ] " + "\n")
                f.write("    do " + "\n")
                f.write("        sleep 10" + "\n")
                f.write("    done" + "\n\n")

                f.write("nohup python -m mly_pipeline.continuous_FAR --mode generation &> continuous_FAR_generation.out & generationID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("nohup python -m mly_pipeline.continuous_FAR --mode inference &> continuous_FAR_inference.out & inferenceID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")

                # Checking if the number of inference files stays 0 for a long time.
                # If lag files increase without any new inference files, that means
                # staling, and we add a staling point. If not we reset it to 0.
                
                f.write("staling_points=0" + "\n")
                f.write("# The batches of generation times the dagmans" + "\n")
                f.write("max_inference_files=$(( $(jq .far_config.batches config.json) * $(ls masterDirectory/*.py | wc -l)  ))" + "\n")

                f.write("premature_ending_points=0" + "\n")

                f.write("# While the number of far files generated is not equal to max inference files" + "\n")
                f.write("while [ $(($(ls falseAlarmRates | wc -l) - 4)) -lt $max_inference_files ]" + "\n")
                f.write("do" + "\n")
                
                f.write("        echo FAR completion: $(($(ls falseAlarmRates | wc -l) - 4)) / $max_inference_files" + "\n")
                f.write("        sleep 300" + "\n\n")

                f.write("        if [ $(ls falseAlarmRates | wc -l) -eq 4 ] && [ $(ls falseAlarmRates/temp | wc -l) -ne 0 ]" + "\n")
                f.write("        then" + "\n")
                f.write("            echo stalling points increase to $staling_points" + "\n")   
                f.write("            ((staling_points=staling_points+1))" + "\n")
                f.write("        else" + "\n")
                f.write("            staling_points=0" + "\n")
                f.write("        fi" + "\n\n")

                # In case inference script gets killed or we have at least 5 minutes
                # of staling, we restart inference script. Although, we keep the 
                # corresponding unix time it got killed in the name of the  output
                # file.
                f.write("        if ! ps $inferenceID > /dev/null || [ $staling_points -gt 5 ]"+ "\n")
                f.write("        then" + "\n")
                f.write("            singularity instance stop --all" + "\n")
                f.write("            nohup python -m mly_pipeline.continuous_FAR --mode inference >"
                                    +" continuous_FAR_inference.out 2>&1"
                                    +" & inferenceID=($(echo $!)) ; echo $!>>.jobids.txt" + "\n")
                f.write("        fi" + "\n\n")                        
                        
                f.write("        if [ $(condor_q -autoformat RequestMemory | wc -l) -eq 0 ] && [ $(($(ls falseAlarmRates | wc -l) - 4)) -ne 0 ] " + "\n")
                f.write("        then    " + "\n")
                f.write("            ((premature_ending_points=premature_ending_points+1))" + "\n")
                f.write("            echo premature ending points increased: $premature_ending_points / 3" + "\n")
                f.write("        fi" + "\n\n")

                f.write("        if [ $premature_ending_points -ge 3 ]" + "\n")
                f.write("        then " + "\n")
                f.write("            break" + "\n")
                f.write("        fi" + "\n\n")

                f.write("done" + "\n")

                f.write("kill $inferenceID $generationID" + "\n")
                f.write("singularity instance stop --all" + "\n")

                f.write("python -c \"from mly_pipeline.manager import manage_FAR_inefernce_files; manage_FAR_inefernce_files()\" "+ "\n")
                f.write("# Need to add a manager of FAR files at the beggining of offline search"+ "\n")
            
            # Making the FAR plot for the status page
            f.write("python -c \"from mly_pipeline.manager import far_plot, segments_plot; far_plot(); segments_plot();\" "+ "\n")

            # If FAR is already calculated we only need this to run
            f.write("nohup python -m mly_pipeline.offline_search &> search.out & echo $!>>.jobids.txt" + "\n\n")



def main():
    
    kwargs = _parser()

    if kwargs['path'][-1]=="/" : kwargs['path'] = kwargs['path'][:-1]
    
    
    if os.path.isdir(kwargs['path']) and kwargs['reset'] == True:
                
        
        print(kwargs['path']," is going to be reset")
        print("Are you sure you want to delete the contents of that directory?")
        answer = input()
        
        if answer in ['yes','y','YES','Yes','Y']:
            
            os.system("rm -r "+kwargs['path'])
            os.system("mkdir "+kwargs['path'])
            
        else:
            
            raise ValueError("Initialization stoped from user")

    elif os.path.isdir(kwargs['path']) and kwargs['reset'] == False:
        
        raise ValueError("The directory you try to create already exist"
                         +". Run the same command but with `-R True` to "
                         +"ovewright the directory.")
    
    elif not os.path.isfile(kwargs['path']):
        
        os.system("mkdir "+kwargs['path'])
        
    else:
        raise ValueError("Wrong input for file", os.path.isfile(kwargs['path'])
                         , kwargs['reset'] == True)
        
    print(f"Search mode selected: {kwargs['search_mode']}")

    frames_dict = dict(   DEFAULT_ONLINE = {'H':"" ,'L':"" ,'V':""}

                        ,DEFAULT_OFFLINE = {'H':"" ,'L':"" ,'V':""}

                        , O4_ONLINE = {'H':"/dev/shm/kafka/H1/"
                                      ,'L':"/dev/shm/kafka/L1/"
                                      ,'V':"/dev/shm/kafka/V1/"}

                        , O3MDC = {'H':"/dev/shm/kafka/H1_O3ReplayMDC/"
                                  ,'L':"/dev/shm/kafka/L1_O3ReplayMDC/"
                                  ,'V':"/dev/shm/kafka/V1_O3ReplayMDC/"}

                        , O3REPLAY = {'H':"/dev/shm/kafka/H1_O3ReplayMDC/"
                                     ,'L':"/dev/shm/kafka/L1_O3ReplayMDC/"
                                     ,'V':"/dev/shm/kafka/V1_O3ReplayMDC/"}

                        , BENCHMARK_MDC_OFFLINE = {'H':"/scratch/florent.robinet/BurstBenchmark/"
                                              ,'L':"/scratch/florent.robinet/BurstBenchmark/"
                                              ,'V':"/scratch/florent.robinet/BurstBenchmark/"}
                    )

    channels_dict = dict( DEFAULT_ONLINE = {'H':"" ,'L':"" ,'V':""}
    
                        ,DEFAULT_OFFLINE = {'H':"" ,'L':"" ,'V':""}

                        , O4_ONLINE = {'H':"H1:GDS-CALIB_STRAIN_CLEAN"
                                      ,'L':"L1:GDS-CALIB_STRAIN_CLEAN"
                                      ,'V':"V1:Hrec_hoft_16384Hz_Gated"}

                        , O3MDC = {'H':"H1:GDS-CALIB_STRAIN_INJ1_O3Replay"
                                  ,'L':"L1:GDS-CALIB_STRAIN_INJ1_O3Replay"
                                  ,'V':"V1:Hrec_hoft_16384Hz_INJ1_O3Replay"}

                        , O3REPLAY = {'H':"H1:GDS-CALIB_STRAIN_O3Replay"
                                     ,'L':"L1:GDS-CALIB_STRAIN_O3Replay"
                                     ,'V':"V1:Hrec_hoft_16384Hz_INJ1_O3Replay"}

                        , BENCHMARK_MDC_OFFLINE = {'H':"H1:STRAIN_BURST_0"
                                                  ,'L':"L1:STRAIN_BURST_0"
                                                  ,'V':"V1:STRAIN_BURST_0"}
                                )
    
    state_vector_channel_dict = dict( 
                          DEFAULT_ONLINE = {'H':"" ,'L':"" ,'V':""}
    
                        , DEFAULT_OFFLINE = None

                        , O4_ONLINE = {'H':'H1:GDS-CALIB_STATE_VECTOR'
                                      ,'L':'L1:GDS-CALIB_STATE_VECTOR'
                                      ,'V':'V1:DQ_ANALYSIS_STATE_VECTOR'}

                        , O3MDC = None

                        , O3REPLAY = None

                        , BENCHMARK_MDC_OFFLINE = None
                                )

    if kwargs['search_mode'] == "BENCHMARK_MDC_OFFLINE":
        segment_list_default = "/home/vasileios.skliris/public_html/benchmark_segments.txt"
    else:
        segment_list_default = []


    # # # # # # # CONFIG FILE # # # # # # #

    configuration = dict(
        

    # Mode that creates some presets if used
    search_mode  = kwargs["search_mode"],
    # # # Directory organisation 
    
    output_directory = kwargs["output_directory"],
    trigger_directory = kwargs["trigger_directory"],
    masterDirectory = kwargs["masterDirectory"],
    bufferDirectory = kwargs["bufferDirectory"],
    falseAlarmRates = kwargs["falseAlarmRates"],
    efficiencies = kwargs["efficiencies"],
    log = "log",
    # Logging level
    log_level = "INFO",
        
    # User name
    
    user_name = os.environ['HOME'].split("/")[-1],


    accounting_group_user = os.environ['HOME'].split("/")[-1],
    # Acounting Group
    accounting_group = "ligo.dev.o4.burst.allsky.mlyonline",

    # Search directory path
    path = os.path.abspath(kwargs['path']),
        
        
    # # # Generator Parameters    
    
    # Num samples per second to feed into models.
    fs=1024,           
        
    # Time duration of segments to analyse (analysis window).
    duration=1,         
        
    # Number of segments to analyse, keep to 1 for real-time analysis.
    size=1,
    
    # Detectors used for this search
    detectors = kwargs['detectors'],
    
    # Frame file prefixes to use
    frames_directory= frames_dict[kwargs['search_mode']],
    
    # The channels to use, INJ is the MDC and NOISE is O3-replay
    channels = channels_dict[kwargs['search_mode']],

    # The channels used for the state vector in online searches
    state_vector_channels= state_vector_channel_dict[kwargs['search_mode']],

    segment_list = segment_list_default,

    max_continuous_segment = 10000,
    # # # Fetching data related parameters 

    # The number of search script running. (The number of scripts must be more than 
    # the time it takes to process one instance of data.)

    parallel_scripts=4,

    # Number of seconds to wait between each read attempt.
    wait=0.5,
        
    # Number of seconds required for PSD calculation.
    required_buffer=16,  
        
    # Number of seconds before current GPS time to begin search.
    start_lag=92,
        
    # If search time is left behind by that amount of seconds it skips ahead.
    gps_reset_time=32,
        
    # FAR file that is used to calculate FAR. It is used only at
    # the beggining of the search, until there is enough background estimation.
    
    farfile= ("/home/vasileios.skliris/mly-hermes/outputs/FARfile" if (kwargs['far'] and 'ONLINE' in kwargs['search_mode']) else kwargs["falseAlarmRates"]+"/FARfile" ),
    
    # # # Models 
        
    # Model1 path, conincidence model.
    model1_path=("/home/mly/models/model1_32V_No5.h5"), 
        
    # Model2 path, coherence model.
    model2_path=("/home/mly/models/model2_32V_No6.h5"),  
        
    # Path to parameter estimation models.

    td_pe_model_path="/home/mly/models/td_model",
    fd_pe_model_path="/home/mly/models/fd_model",    

    # # # Skymap parameters
    
    # Skymap run option
    skymap = 0,

    # Heilpix nside number for generated skymap.
    nside=64,  
        

    # # # Efficiency calculation parametersp

    # Testing configuration
    eff_config = dict( injectionDirectoryPath="/home/mly/injections/" # Injection directories
                      ,injectionsWithHRSS = ['SGE70Q3'
                                            ,'SGE153Q8d9'
                                            ,'SGL153Q8d9'
                                            ,'WNB250'] if "OFFLINE" not in kwargs['search_mode'] else []
                      ,injectionsWithSNR = ['cbc_20_20'
                                             ,'wnb_03_train_pod'
                                             ,'cusp_00'] if "OFFLINE" not in kwargs['search_mode'] else []
                      ,injectionHRSS = "1e-22,1e-21,1e-22"
                      ,injectionSNR =  "0,50,5"
                      ,testSize = "100"
                      ,howOften = 3600),

    far_config = dict( 
                    # Enabling or not the calculation of FAR.
                    far_enabled = True if kwargs['far'] else False
                    # Number of timelags used.
                    ,batch_size=1024
                    # It is used only at the beggining of a search until a FAR is estimated.
                    ,threshold = 2.3148e-05 if "OFFLINE" in kwargs['search_mode'] else 1/3600
                    # The score from which we keep FAR statistics.
                    ,restriction = 0.0001
                    # The maximum lag to be used. Determines the DataSet size of the saved instances.
                    ,max_lag = 3600
                    # The amount of lags to use for each file. Depends on the capasity to produce them.
                    ,lags = 1024
                    # Then number of condor jobs per file to be used for timelags. With a file of
                    # size 3600 (max_lag) this will create jobs that will produce files
                    # of ~3600*lags/batches. Change with caution.
                    ,batches = 64
                    # GPU devices to use. If not defined it will just load the local visible ones.
                    ,visible_gpu_devices = "local"
                    # The GPU number(s)) (run nvidia-smi to see the numbers), to use for the tests.
                    ,selectedGPUs = [0]
                    # Maximum amount of dags to run at the same time in condor for the generation of data.
                    ,parallelGenerations = 3
                    ),
                         
    # # # MISC
    
    # The group size of the files that used to save the outputs    
    maxDataFrameSize = 3600,
    
    # The destination of the triggers, None means testing mode with FAKEIDs.
    trigger_destination = "playground" if kwargs['search_mode'] in ["O3MDC"] else None,

    # Random number generator seed
    seed = 921101

    

    )


    os.system("mkdir " + configuration['path'] +"/"+ configuration['output_directory'])
    os.system("mkdir " + configuration['path'] +"/"+ configuration['trigger_directory'])
    os.system("mkdir " + configuration['path'] +"/"+ configuration['log'])

    if not ("OFFLINE" in kwargs['search_mode'] and not kwargs['far']):

        os.system("mkdir " + configuration['path'] +"/"+ configuration['masterDirectory'])
        os.system("mkdir " + configuration['path'] +"/"+ configuration['masterDirectory'] 
                +"/temp")

        for det in configuration['detectors']:
            os.system("mkdir " + configuration['path'] +"/"+ configuration['masterDirectory'] 
                    +"/"+ det)
            os.system("mkdir " + configuration['path'] +"/"+ configuration['masterDirectory'] 
                    +"/temp/"+ det)

        os.system("mkdir " + configuration['path'] +"/"+ configuration['bufferDirectory'])
        os.system("mkdir " + configuration['path'] +"/"+ configuration['bufferDirectory'] 
                +"/temp")
        
        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates'])
        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/hourly")
        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/FARfile")
        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/condor")

        os.system("mkdir " + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/temp")
        # os.system("mkdir -p /scratch/"+user_name+"/" + configuration['path'].split("/")[-1] +"/"+ configuration['falseAlarmRates']+"/temp")
        # os.system("ln -s /scratch/"+user_name+"/" + configuration['path'].split("/")[-1] +"/"+ configuration['falseAlarmRates']+"/temp"+" "
        #                                        + configuration['path'] +"/"+ configuration['falseAlarmRates']+"/temp")

        
        
        os.system("mkdir " + configuration['path'] +"/"+ configuration['efficiencies'])
        os.system("mkdir " + configuration['path'] +"/"+ configuration['efficiencies'] 
                +"/history")
        




    # Saving config file to json format
    with open(configuration['path'] +"/"+"config.json", "w") as config_json:
        json.dump(configuration, config_json,indent=4)
        config_json.close()

    
    createRunAllScript(**configuration)

def _start_search():

    #Construct argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--search_path', type=str
                        , default = "./"
                        , help = "The path to the search to start"
                        , required = False)

    # Pass arguments:
    args = parser.parse_args()
    

    search_path = getattr(args, "search_path")      

    if os.path.isfile(search_path+"runall.sh"):

        os.system(f"cd {search_path} ; nohup sh runall.sh &> runall.out & echo $!>>.jobids.txt")
        print("Search has started!")

    else:

        raise FileNotFoundError(f"The path provided {search_path} does not have a runall.sh file to start the search.")

      
def _end_search():

        #Construct argument parser:
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--search_path', type=str
                        , default = "./"
                        , help = "The path to the search to start"
                        , required = False)

    # Pass arguments:
    args = parser.parse_args()
    

    search_path = getattr(args, "search_path")      
    if os.path.isfile(search_path+".jobids.txt"):

        with open(f"{search_path}/.jobids.txt", "r") as idfile:
            idfile_ = idfile.read()
  
        # replacing end of line('/n') with ' ' and
        # splidfile.read()
    
        # replacing end of line('/n') with ' ' and
        # splitting the text it further when '.' is seen.
        job_id_list = idfile_.replace('\n', ' ').split(" ")
    
        for id_ in job_id_list:
            try:
                os.system(f"kill {str(id_)} >/dev/null 2>&1")#,stderr=subprocess.STDOUT)
            except Exception as e:
                pass

        try:
            os.system(f"singularity instance stop --all >/dev/null 2>&1")
        except Exception as e:
            pass

        os.system(f">{search_path}/.jobids.txt")

        print("Search stopped")
    else:

        raise FileNotFoundError(f"The path provided {search_path} does not have a .jobids.txt file to start the search.")


def _status_page():

    from .manager import manage_status_page
    manage_status_page()


    


if __name__ == "__main__":
    
     main()

