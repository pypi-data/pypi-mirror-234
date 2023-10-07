from pathlib import Path
from datetime import datetime, timedelta
from time import sleep
import os, json
import pandas as pd
from gwpy.time import from_gps

# Loading config
with open('config.json') as json_file:
    config = json.load(json_file)

# Function to create symbolic link of the status page into public html
def create_symlink(source: Path, destination: Path) -> None:
    if destination.is_symlink():
        print(f"Symlink already exists at {destination}")
    else:
        try:
            destination.symlink_to(source)
            print(f"Symlink created at {destination}")
        except OSError as e:
            print(f"Creation of the symlink at {destination} failed: {e}")
def find_json_file(directory):

    files = os.listdir(directory)
    for file in files:
        if ".json" in file:
            jsonfile = file
            break

    return directory+'/'+jsonfile

def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

def create_event_table():
    pd_table = None

    search_path = f"{config['path']}/{config['trigger_directory']}"

    events = os.listdir(search_path)
    if len(events)!=0:
        for event_dir in events:
            
            event_name = event_dir.split('-')[0]
            json_file_path = find_json_file(search_path+'/'+event_dir)

            with open(json_file_path) as json_file:
                event_info = json.load(json_file)


            event_info['datetime'] = str(from_gps(event_info['central_time'] ))

            del event_info['scores']
            del event_info['gpstime']

            file_prefix = json_file_path.split('/')[-1][:-5]

            event_info['ifos'] = ''.join(event_info['ifos'])
            event_info['far'] = f"{event_info['far']:.4e} Hz"
            event_info['SNR'] = f"{event_info['SNR']:.2f}"
            event_info['central_time'] = f"{event_info['central_time']:.3f}"
            event_info['central_freq'] = f"{event_info['central_freq']:.1f} Hz"
            event_info['duration'] = f"{event_info['duration']:.5f} sec"
            event_info['bandwidth'] = f"{event_info['bandwidth']:.1f} Hz"


            event_info['GraceDB_ID'] = event_name
            event_info['GraceDB_ID_url'] = f"https://gracedb-test.ligo.org/events/{event_name}/view/"

            event_info['strain_plot_url'] = f"trigger_directory/{event_dir}/{file_prefix}_strain.png"
            event_info['tf_map_url'] = f"trigger_directory/{event_dir}/{file_prefix}_tfmap.png"
            event_info['correlation_plot_url'] = f"trigger_directory/{event_dir}/{file_prefix}_correlation.png"

            event_info['Timeseries'] = "link"
            event_info['TFmap'] = "link"
            event_info['Correlation'] = "link"

            columns = list(event_info.keys())
            columns.insert(0, columns.pop(columns.index('datetime')))
            columns.insert(0, columns.pop(columns.index('GraceDB_ID')))



            if pd_table is None:

                pd_table = pd.DataFrame(event_info,index=[0])
            
            else:
                event_info = pd.DataFrame(event_info,index=[0])
                pd_table = pd.concat([pd_table,event_info],ignore_index=True)
                

        pd_table= pd_table[columns]
        pd_table= pd_table.sort_values(by='central_time',ignore_index=True,ascending=False)

        pd_table['GraceDB_ID'] = pd_table.apply(lambda x: make_clickable(x['GraceDB_ID_url'], x['GraceDB_ID']), axis=1)
        pd_table['Timeseries'] = pd_table.apply(lambda x: make_clickable(x['strain_plot_url'], x['Timeseries']), axis=1)
        pd_table['Correlation'] = pd_table.apply(lambda x: make_clickable(x['correlation_plot_url'], x['Correlation']), axis=1)
        pd_table['TFmap'] = pd_table.apply(lambda x: make_clickable(x['tf_map_url'], x['TFmap']), axis=1)

        #pd_table['GraceDB_ID'] = pd_table.apply(lambda x: make_clickable(x['GraceDB_ID_url'], x['GraceDB_ID']), axis=1)

        del pd_table['GraceDB_ID_url']
        del pd_table['strain_plot_url']
        del pd_table['correlation_plot_url']
        del pd_table['tf_map_url']
        
        pd_table= pd_table.set_index('GraceDB_ID')

        pd_table = pd_table.style.to_html(index=False,classes='center')
        
    else:

        pd_table = "No events found"

    return pd_table


# Updating page time 
status_check_interval = timedelta(seconds=10.0)
status_timeout = timedelta(seconds=60.0)

# These two will stay the same for now
search_path = Path(config['path']) 
status_page_path = Path(config['path']) / "status.html"

search_directory_name =search_path.name

search_symlink_path =  Path(f"/home/{config['user_name']}/public_html/{search_path.name}")

# Create symlink from search directory to status page directory:
create_symlink(search_path, search_symlink_path)

canary_file_path = Path(f"{search_path}/log/search.log")
seg_plot_path = Path(f"segment_plot.png")
far_plot_path = Path(f"far.png")
eff_plot_path = Path(f"Efficiencies.png")

event_table = create_event_table()


# the html code which will go in the file GFG.html
html_template = \
f"""
<!DOCTYPE html>
<html>
<head>
	<title>MLy-Pipeline Status Page</title>
	<script>
    
        // Check status
        var monitorStarted = new Date();
        
        function updateLastModifiedTime() {{
             // Load the file using XMLHttpRequest
            var xhr = new XMLHttpRequest();
            xhr.open('HEAD', './{canary_file_path}', true);
            xhr.onreadystatechange = function() {{
                if (xhr.readyState === 4) {{
                    // Get the last modified time of the file
                    var fileLastModified = new Date(xhr.getResponseHeader('Last-Modified'));

                    // Get the current time
                    var currentTime = new Date();
                    
                    console.log(fileLastModified)
                    console.log(currentTime)

                    // Calculate the difference in seconds between the two times
                    var timeDiffInSeconds = (currentTime - fileLastModified) / 1000;

                    // Check if more than timeout seconds have passed since the last modification time
                    if (timeDiffInSeconds > {status_timeout.seconds}) {{
                        document.getElementById('current-status').innerHTML = "Offline since " + monitorStarted;
                        monitorStarted = new Date();
                    }} else {{
                        document.getElementById('current-status').innerHTML = "Online since " + monitorStarted;
                    }}
                    
                    // Update log last modified time
                    document.getElementById('log-last-modified').innerHTML = fileLastModified;
                }}
            }};
            xhr.send();
        }}
        
        // create a new timestamp     
        
        function refreshImage(){{   
            // create a new timestamp 
            var timestamp = new Date().getTime();  

            var el = document.getElementById("far-plot");  

            var queryString = "?t=" + timestamp;    

            el.src = "{far_plot_path}";    
        }}
        
        
        updateLastModifiedTime();
        
        // Update the last modified time every check miliseconds
		setInterval(updateLastModifiedTime, {status_check_interval.seconds * 1000});
        setInterval(refreshImage, {status_check_interval.seconds * 1000});

	</script>
    </head>
    <body>
        <h1>MLy-Pipeline Status Page</h1>
        <!-- <h2>Search directory: {config['path']}</h2> -->
        <!-- <p>Status: <span id="current-status"></span></p> -->
        <!-- <p>Log Last Modified: <span id="log-last-modified"></span></p> -->
        <h2>Processed segments over available segments</h2>
        <img src="{seg_plot_path}" alt="Segments" id = "seg-plot">

        <h2>Inverse False Alarm Rate</h2>
        <img src="{far_plot_path}" alt="False Alarm Rate" id = "far-plot">

        <h2>Efficiency</h2>
        <img src="{eff_plot_path}" alt="Efficiency" id = "eff-plot">
        
        <h2>List of triggers</h2>
        <h3>{event_table} </h3>
    </body>
    </html>

"""
  
# writing the code into the file
with open(status_page_path, 'w') as f:
    f.write(html_template)
