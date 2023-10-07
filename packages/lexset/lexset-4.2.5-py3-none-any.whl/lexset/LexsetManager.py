import requests
import json
import yaml
import base64
import time
from tqdm import tqdm
import os
import re
import random
import shutil
from concurrent.futures import ThreadPoolExecutor


def merge_datasets(json_dirs, percentages, output_json_path, output_img_dir):
    merged_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    # Validate if percentages length is the same as json_dirs
    if len(json_dirs) != len(percentages):
        print("Error: The lengths of json_dirs and percentages must be the same.")
        exit(1)

    img_id = 1  # Keep track of image IDs
    ann_id = 1  # Keep track of annotation IDs
    
    # Create output image directory if it doesn't exist
    if not os.path.exists(output_img_dir):
        os.makedirs(output_img_dir)
    
    # Loop over each JSON directory to merge them
    for i, (json_dir, percentage) in enumerate(zip(json_dirs, percentages)):
        json_path = os.path.join(json_dir, "coco_annotations.json")
        
        with open(json_path, "r") as f:
            data = json.load(f)
        
        # Calculate number of images to keep
        total_images = len(data["images"])
        keep_count = int(total_images * (percentage / 100.0))
        
        # Randomly sample images
        sampled_images = random.sample(data["images"], keep_count)
        
        # Build a set of sampled image IDs for annotation filtering
        sampled_image_ids = {img["id"] for img in sampled_images}
        
        # Filter annotations based on sampled image IDs
        sampled_annotations = [ann for ann in data["annotations"] if ann["image_id"] in sampled_image_ids]
        
        # Update image IDs and move images to new folder
        for img in sampled_images:
            new_img = img.copy()
            new_img["id"] = img_id
            
            # Identify all associated files for this image based on the UUID
            uuid_search = re.search(r'([a-f0-9\-]+)', img["file_name"])
            if uuid_search:
                uuid = uuid_search.group(1)
                associated_files = [f for f in os.listdir(json_dir) if f.startswith(uuid)]
                
                for associated_file in associated_files:
                    old_img_path = os.path.join(json_dir, associated_file)
                    new_img_path = os.path.join(output_img_dir, associated_file)
                    
                    # Copy the file to the new directory
                    shutil.copy(old_img_path, new_img_path)
            
            merged_data["images"].append(new_img)
            img_id += 1
        
        # Update annotation IDs
        for ann in sampled_annotations:
            new_ann = ann.copy()
            new_ann["id"] = ann_id
            new_ann["image_id"] = ann["image_id"] + img_id - 1  # Update to new image id
            
            merged_data["annotations"].append(new_ann)
            ann_id += 1
        
        # Merge categories (assumes that categories are the same across all JSON files)
        if i == 0:
            merged_data["categories"] = data["categories"]
    
    # Save the merged JSON
    with open(output_json_path, "w") as f:
        json.dump(merged_data, f)

class simulation:
    #init 
    def __init__(self, token, userID, organizationID = None):

        #set the user id and token
        self.user_id = userID
        self.token = token

        #set the organization id
        if organizationID is not None:
            self.organization_id = organizationID
        else:
            self.organization_id = 0
            print("\n\033[1;31;40mOrganization ID not provided. \033[0m", end ="\n")
            print("\33[3;37;40mTo set an organization ID, use the setOrganization_id method. \33[0m")

    def setOrganization_id(self, organizationID):
        self.organization_id = organizationID
        print("\n\33[1;32;40mOrganization ID set to: " + str(self.organization_id)+"\33[0m")

    def get_dataset_id(self):

        self.dataset_ids = []
        try:
            print("\n\33[3;37;40mGetting dataset ID for simulation ID(s): " + str(self.simulation_id) + "-->\33[0m")

            dataset_ids = []
            for i in range(len(self.simulation_id) if type(self.simulation_id) is list else 1):
                
                if isinstance(self.simulation_id, int):
                    self.simulation_id = [self.simulation_id]

                url = "https://lexsetapi.lexset.ai/api/simulations/getsimulationstatus?id=" + str(self.simulation_id[i])

                payload={}
                headers = {
                'Authorization': 'Bearer ' + str(self.token)
                }

                response = requests.request("GET", url, headers=headers, data=payload )

                if response.status_code == 401:
                    print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                    return("Unauthorized")
                elif response.status_code == 200:
                    parseResponse = json.loads(response.text)
                    dataset_ids.append(parseResponse["datasets"][0]["id"])
                    self.complete = parseResponse["isComplete"]
                else:
                    print("\33[1;31;40mgetDataset_id() Error: " + str(response.status_code) + "\33[0m")
                    return(response.status_code)

            time.sleep(1)

            self.dataset_id = dataset_ids
            if len(self.dataset_id) == 1:
                print("\33[1;32;40mDataset ID(s) found: " + str(self.dataset_id[0]) + "\33[0m")
                return self.dataset_id[0]
            else:
                print("\33[1;32;40mDataset ID(s) found: " + str(self.dataset_id) + "\33[0m")
            return self.dataset_id

        except:
            print("\n\33[1;31;40mSimulation ID(s) not set. Use the setSimulation_id method to set the simulationID. \n\33[0m")
            return

    def setSimulation_id(self, simulationID):
        self.simulation_id = simulationID
        print("\n\33[1;32;40mSimulation ID(s) set to: " + str(self.simulation_id) + "\n\33[0m")

    def get_organization_simulations(self,state, limit = 100):

        #CHECK REQUESTED STATE
        if(state == "RUNNING" or state == "COMPLETED" or state == "CREATED" or state == "QUEUED"):
            print("\33[3;37;40mGetting simulations for organizationID: " + str(self.organization_id) + "-->\33[0m")
        else:
            print("\33[1;31;40mInvalid State: " + state + "\33[0m")
            print("\33[3;37;40mValid States: RUNNING, COMPLETED, CREATED\33[0m")
            return

        url = "https://lexsetapi.lexset.ai/api/Simulations/GetSimulationsByOrganization?orgid=" + (str(self.organization_id)) +"&state=" + state

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        #PARSE RESPONSE
        response = requests.request("GET", url, headers=headers, data=payload )

        if response.status_code == 401:
            print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
            return("Unauthorized")

        #if the request is successful    
        if response.status_code == 200:
            parseResponse = json.loads(response.text)
            
            data = parseResponse
            sorted_data = sorted(data, key=lambda x: x['timestamp'])
            #CLEAN UP DATA AND RETURN
            simulation_list = []
            for d in sorted_data:
                temp_dict = {
                    'userid': d['userid'],
                    'timestamp': d['timestamp'],
                    'name': d['name'],
                    'description': d['description'],
                    'nodes': d['requestedNodeCount'],
                    'simulation_id': d['id'],
                    'complete': d['isComplete'],
                }
                if 'datasets' in d and len(d['datasets']) > 0:
                    temp_dict['dataset_id'] = d['datasets'][0]['id']

                simulation_list.append(temp_dict)

            return simulation_list[limit *-1:]

        else:
            print("\33[1;31;40mget_organization_simulations() Error: " + str(response.status_code) + "\33[0m")
            return(response.status_code)

    def download(self, localPath="NONE", workers=2):
        #CHECK IF DATASET ID IS SET
        try:
            id_list = self.dataset_id
        except:
            self.get_dataset_id()
            id_list = self.dataset_id

        #DIVIDE DATASET INTO PARTS
        def divide_into_parts(file_size, num_workers):
            part_size = file_size // num_workers
            part_starts = [i * part_size for i in range(num_workers)]
            part_ends = [(i + 1) * part_size - 1 for i in range(num_workers - 1)] + [file_size - 1]
            return list(zip(part_starts, part_ends))
        # MERGE THE BIN FILES
        def combine_bin_files(bin_files, destination):
            with open(destination, "wb") as outfile:
                for bin_file in bin_files:
                    with open(bin_file, "rb") as readfile:
                        shutil.copyfileobj(readfile, outfile)
        #CLEAN UP BIN FILES
        def delete_bin_files(parts):
            for i in range(parts):
                os.remove(f"part{i}.bin")

        #function that downloads a part of the file and saves it to disk
        def download_part(start, end, part_number, progress_bar):
            headers = {"Authorization": f"Bearer {bearer_token}", "Range": f"bytes={start}-{end}"}
            response = requests.get(url, headers=headers, stream=True)

            with open(f"part{part_number}.bin", "wb") as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    f.write(chunk)
                    progress_bar.update(len(chunk))

        if self.complete == True:
            print("\33[1;32;40mSimulation(s) complete. Downloading... \33[0m")
        else:
            print("\33[1;31;40mSimulation(s) not complete. Please wait for simulation to complete before downloading. \33[0m")
            return

        for id in id_list:
            url = "https://coreapi.lexset.ai/api/dataset/download/" + str(id) + "/dataset.zip"
            bearer_token = self.token
            
            headers = {"Authorization": f"Bearer {bearer_token}"}

            session = requests.Session()
            response = session.get(url, headers=headers, stream=True)
                
            #MAKE REQUEST TO GET THE FILE SIZE FROM THE HEADERS note: we could possibly remove this if we chane the server side code.
            if response.status_code == 401:
                print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                return("Unauthorized")
            if response.status_code == 200:
                file_size = int(response.headers["content-length"])
            else:
                print("\33[1;31;40mdownload() Error: " + str(response.status_code) + "\33[0m")
                return(response.status_code)
            session.close()

            #divide the file into parts
            parts = divide_into_parts(file_size, workers)

            # create a progress bar for each part
            progress_bars = [tqdm(total=end-start, desc=f"part_{i}", leave= False) for i, (start, end) in enumerate(parts)]

            #distribute the download of each part to a thread
            with ThreadPoolExecutor() as executor:
                for i, (start, end) in enumerate(parts):
                    future = executor.submit(download_part, start, end, i, progress_bars[i])

            if localPath == "NONE":
                destination = str(id) + "_dataset.zip"
            else:
                destination = localPath + "/" + str(id) + "_" + "dataset.zip"

            #combine files and delete the parts
            combine_bin_files([f"part{i}.bin" for i in range(len(parts))], destination)
            time.sleep(5)
            delete_bin_files(workers)
            time.sleep(5)


    def create_simulation(self, simulationPath, simulationName, description, nodeCount, numImages):
        url = "https://lexsetapi.lexset.ai/api/Simulations/NewSimulation"

        #encode the config in Base64
        with open(simulationPath) as fast:
            simString = json.dumps(yaml.load(fast, Loader=yaml.FullLoader))
            simEncoded = base64.b64encode(simString.encode("utf-8"))
            self.simEncodedstr = str(simEncoded, "utf-8")

        payload = json.dumps({
          "id": 0,
          "userid": self.user_id,
          "name": simulationName,
          "description": description,
          "simulationconfig": self.simEncodedstr,
          "requestednodecount": nodeCount,
          "randomseed": 1,
          "renderjobid": 0,
          "imagecount": numImages
        })
        headers = {
          'Authorization': 'Bearer ' + self.token,
          'Content-Type': 'application/json'
        }

        #PARSE RESPONSE
        response = requests.request("POST", url, headers=headers, data=payload )
        parseResponse = json.loads(response.text)
        responseCode = response.status_code

        if responseCode == 401:
            print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
            return("Unauthorized")
        if responseCode == 200:
            #update simulation IDs
            self.simulation_id = parseResponse["id"]
            self.dataset_id = parseResponse["datasetid"]

            print("\n\33[1;32;40mSimulation ID "+ str(self.simulation_id) +" created.\nThe simulation name is --> " + str(simulationName)+"\33[0m")
            time.sleep(1)
        else:
            print("\33[1;31;40mcreate_simulation() Error: " + str(response.status_code) + "\33[0m")
            return(responseCode)

    def delete_simulation(self):
        headers = {'Authorization': 'Bearer ' + str(self.token)}

        #convert simulation id into an array if not already
        if type(self.simulation_id) is not list:
            self.simulation_id = [self.simulation_id]
        
        for id in self.simulation_id:
            #Parse Response
            response = requests.delete(f'https://lexsetapi.lexset.ai/api/simulations/archivesimulation?id={id}', headers=headers)
            if response.status_code == 401:
                print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                return("Unauthorized")
            if response.status_code == 200:
                print("\n\33[1;32;40mSimulation ID "+ str(self.simulation_id) +" deleted successfully.\33[0m")
                return("Success")
            else:
                print("\33[1;31;40mdelete_simulation() Error: " + str(response.status_code) + "\33[0m")
                return(response.status_code)

    def add_file(self, location, type="None"):
        
        url = "https://lexsetapi.lexset.ai/api/UserDataManagement/uploaduserfile"

        if type == "None":
            print("\33[1;31;40mPlease specify a file type, LIST_ALL, RELATIONSHIPS or COLORMAP \33[0m")
            return
        if type == "RELATIONSHIPS":
            path = location
            self.realationships = path
            payload={'userid': str(self.user_id)}
        if type == "COLORMAP":
            path = location
            self.colormap = path
            payload={'userid': str(self.user_id),'filetype': '1'}

        name = path.split("/")

        files=[('files',(str(name[len(name)-1]),open(str(path),'rb'),'application/octet-stream'))]
        headers = {'Authorization': 'Bearer ' + str(self.token)}
        response = requests.request("POST", url, headers=headers, data=payload, files=files )
        
        if response.status_code == 401:
            print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
            return("Unauthorized")
        if response.status_code == 200:
            print("\n\33[1;32;40mFile [" + str(name[len(name)-1]) + "] uploaded successfully.\33[0m")
            return("Success")
        else:
            print("\33[1;31;40madd_file() Error: " + str(response.status_code) + "\33[0m")
            return(response.status_code)

    def active_nodes(self):
        url = "https://lexsetapi.lexset.ai/api/simulations/GetActiveSimulations/?userid=" + str(self.user_id)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token,
        }

        response = requests.request("GET", url, headers=headers, data=payload )

        if response.status_code == 401:
            print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
            return("Unauthorized")
        if response.status_code == 200:
            #update if sim is complete or not complete
            parseResponse = json.loads(response.text)
            nodes = 0

            #iterate through the list of simulations and add the number of active nodes
            y = parseResponse
            for item in range(len(y)):
                if (y[item]['hasStarted']== True) :
                    nodes = nodes + int(y[item]['requestedNodeCount'])

            if nodes == 0:
                print("\n\33[3;37;40mNo active nodes.\33[0m")   
            if nodes > 0:
                print("\n\33[3;37;40mActive nodes: " + str(nodes) + "\33[0m")  

        else:
            print("\33[1;31;40mactive_nodes() Error: " + str(response.status_code) + "\33[0m")
            return(response.status_code)

        return nodes

    def start(self):
        #convert simulation id into an array if not already
        if type(self.simulation_id) is not list:
            self.simulation_id = [self.simulation_id]
        
        for id in self.simulation_id:            

            url = "https://lexsetapi.lexset.ai/api/Simulations/QueueSimulation?id=" + str(id)

            payload={}
            headers = {
            'Authorization': 'Bearer ' + self.token
            }

            response = requests.request("POST", url, headers=headers, data=payload )

            if response.status_code == 401:
                print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                return("Unauthorized")
            if response.status_code == 200:
                print("\n\33[1;32;40mSimulation ID "+ str(self.simulation_id) +" started successfully.\33[0m")
                #parseResponse = json.loads(response.text)
                time.sleep(5)
                return("success")
            else:
                print("\33[1;31;40mstart() Error: " + str(response.status_code) + "\33[0m")
                return(response.status_code)        

    def dequeue(self):
        #convert simulation id into an array if not already
        if type(self.simulation_id) is not list:
            self.simulation_id = [self.simulation_id]
        
        for id in self.simulation_id:            

            url = "https://lexsetapi.lexset.ai/api/Simulations/RemoveSimulationFromQueue?id=" + str(id)

            payload={}
            headers = {
            'Authorization': 'Bearer ' + self.token
            }

            response = requests.request("DELETE", url, headers=headers, data=payload )

            if response.status_code == 401:
                print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                return("Unauthorized")
            if response.status_code == 200:
                print("\n\33[1;32;40mSimulation ID "+ str(self.simulation_id) +" removed from queue.\33[0m")
                #parseResponse = json.loads(response.text)
                time.sleep(5)
                return("success")
            if response.status_code == 400:
                print("\n\33[1;32;40mSimulation ID "+ str(self.simulation_id) +" not in queue.\33[0m")
                #parseResponse = json.loads(response.text)
                time.sleep(5)
                return("warning")
            else:
                print("\33[1;31;40mstart() Error: " + str(response.status_code) + "\33[0m")
                return(response.status_code)        

    def stop(self):

        #convert simulation id into an array if not already
        if type(self.simulation_id) is not list:
            self.simulation_id = [self.simulation_id]
        

        for id in self.simulation_id:
            url = "https://lexsetapi.lexset.ai/api/simulations/stopsimulation?id=" + str(id)

            payload={}
            headers = {
            'Authorization': 'Bearer ' + self.token
            }

            response = requests.request("POST", url, headers=headers, data=payload )
            
            if response.status_code == 401:
                print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                return("Unauthorized")
            if response.status_code == 200:
                #parseResponse = json.loads(response.text)
                print("\n\33[1;32;40mSimulation ID "+ str(self.simulation_id) +" stopped successfully.\33[0m")
                time.sleep(5)
                return("success")
            else:
                print("\33[1;31;40mstop() Error: " + str(response.status_code) + "\33[0m")
                return(response.status_code)

    def get_progress(self):
        #convert simulation id into an array if not already
        if type(self.simulation_id) is not list:
            self.simulation_id = [self.simulation_id]
        
        for id in self.simulation_id:

            url = "https://lexsetapi.lexset.ai/api/simulations/getstatus?id=" + str(id)

            payload={}
            headers = {
            'Authorization': 'Bearer ' + self.token
            }

            response = requests.request("GET", url, headers=headers, data=payload )

            if response.status_code == 401:
                print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                return("Unauthorized")

            if response.status_code == 200:
                parseResponse = json.loads(response.text)
                print("\n\33[1;32;40mSimulation ID "+ str(self.simulation_id) +" progress: " + str(parseResponse['percentComplete']) + "% complete\33\n[0m")
                return(parseResponse)
            else:
                print("\33[1;31;40mget_progress() Error: " + str(response.status_code) + "\33[0m")
                print("\33[3;37;40mCheck simulation status with the get_status method.\33[0m")
                return(response.status_code)

    def get_status(self):
        #convert simulation id into an array if not already
        if type(self.simulation_id) is not list:
            self.simulation_id = [self.simulation_id]

        #initilze status_list
        self.status_list = []
        for id in self.simulation_id:

            url = "https://lexsetapi.lexset.ai/api/simulations/getsimulationstatus?id=" + str(id)

            payload={}
            headers = {
            'Authorization': 'Bearer ' + self.token
            }

            response = requests.request("GET", url, headers=headers, data=payload )
            
            if response.status_code == 401:
                print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                return("Unauthorized")
            if response.status_code == 200:
                #update if sim is complete or not complete
                parseResponse = json.loads(response.text)
                
                if parseResponse == None:
                    return False
                else:
                    isComplete = parseResponse["isComplete"]
                    hasStarted = parseResponse["hasStarted"]

                    status_dict = {'isComplete': isComplete, 'hasStarted': hasStarted}
                    status_tuple = (id, isComplete, hasStarted)
                    self.status_list.append(status_tuple)
            else:
                print("\33[1;31;40mget_status() Error: " + str(response.status_code) + "\33[0m")
                return(response.status_code)
        
        for status in self.status_list:
            print("\33[1;32;40mSimulation ID "+ str(status[0]) +" status:\33[0m")
            print("\33[1;32;40mComplete = " + str(status[1]) + "\33[0m")
            print("\33[1;32;40mHas started = " + str(status[2]) + "\n\33[0m")
        
        return self.status_list


    def gcp_transfer(self, bucketName):

        #convert simulation id into an array if not already
        if type(self.simulation_id) is not list:
            self.simulation_id = [self.simulation_id]
        
        for sim in self.simulation_id:
                
            url = "https://coreapi.lexset.ai/api/userdatamanagement/TransferDatasetToGcp?userid=" + str(self.user_id) + "&simulationId=" + str(sim) + "&bucketName=" + bucketName
            
            payload={}
            headers = {
            'Authorization': 'Bearer ' + self.token
            }
            response = requests.request("GET", url, headers=headers, data=payload )

            if response.status_code == 401:
                print("\33[1;31;40mUnauthorized: " + str(response.status_code) + "\33[0m")
                return("Unauthorized")
            if response.status_code == 200:
                print("\33[1;32;40mSuccess transfer to GCP in progress.\33[0m")
                parseResponse = json.loads(response.text)
                return(parseResponse)
            else:
                print("\33[1;31;40mgetDataset_id() Error: " + str(response.status_code) + "\33[0m")
                return(response.status_code)
            
            time.sleep(5)
