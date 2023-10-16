import json
import os
import re

from . import LOGGER_NAME
from .DatalakeHandler import *
from .HTTPCalller import HTTPCaller
from ast import literal_eval

log = logging.getLogger(LOGGER_NAME)


class TaskHandler:
    def __init__(self):
        self.pipeline_id = os.environ.get('PIPELINE_ID')
        self.caller = HTTPCaller()
        self.main_path = os.getcwd()
    
    # ---------------
    # GET TASKS
    # ---------------
    def get_all_tasks_definitions(self, group_name=None, readable_name=None, category=None, size='all', from_page=0):
        '''Searching Method to find the task definitions and documentation from management component of the current stage.
        By default all tasks that can be accessed. 
        The search can be modified in the query to get tasks from a group, from a category, or a task with a name displayed in the UI.
        :param: group_name: name of the group in datalake. Accepts '*' as a wild cart in search
        :param: readableName: name of the task in the UI. Accepts '*' as a wild cart in search
        :param: category: name of the category in the UI or the backend category from the task_params.json. If '*' is used, the search will be performed on the backend categories.
        :return: list of json file type elements
        '''
        # Prepare query parameters
        init_query = {"readableName": readable_name, "category": category, "groupName": group_name}
        query = format_query(init_query)

        task_list = []

        next_from_page=from_page
        while True:
            if size == 'all' or size > 1_000:
                path = f'/mgmt/task?query={query}&size=1000&from={next_from_page}' 
            else:
                path = f'/mgmt/task?query={query}&size={size}&from={next_from_page}'
            response = self.caller.get(path)
            reponse_json = response.json()
            task_list.extend(reponse_json['items'])
            next_from_page += 1_000
            if (size == 'all' and reponse_json['totalSize'] < next_from_page) or (size != 'all' and size < next_from_page):
                break

        return task_list

    # ---------------
    # BASE METHODS
    # ---------------
    def get_storage_value(self, key):
        '''Read a value from the Storage with a key
        :param: key: the key to get the value from storage

        :return: dictionary {'dataStorageId': ..., ...,  'key': 'A', 'value': '1'}
        '''

        path = f'/mgmt/store/{self.pipeline_id}/{key}'

        response = self.caller.get(path)
        return response.json()

    def set_storage_value(self, key, value):
        ''' Write a value in the storage with a corresponding key
        :param: key: the key to get the value from storage
        :param: value to set
        '''

        path = '/mgmt/store/{}/{}'.format(self.pipeline_id, key)
        headers = {'Content-Type': 'text/plain'}

        return self.caller.post(path, headers=headers, data=value)

    # -------------------------------------
    # Task Input and Output related methods
    # -------------------------------------
    def read_task_parameter_value(self, arg_name):
        '''
        Read the input value of a TASK given its name,
        and return the corresponding file JSON that can contain its ID, name or groupName.

        If the file was passed by a previous Task (dynamically) the value should contain its ID (at least), name and groupName
        If the file was selected using the File Picker with the latest version of the file, then no ID is passed

        :param: arg_name: name of the TASK parameter to be read from env variables
        :return: returns a dictionary that can contain name, groupName and id of a file ti use as the Task input
        '''

        # Get the Input value from the Env Variables
        arg_key = os.environ.get(arg_name)
        log.debug(f'Raw input for {arg_name}: {arg_key}. Type is: {type(arg_key)}')

        # this is dynamic parameter - get value from storage
        if arg_key.startswith("${"):
            # retrieve the saved value passed dynamically
            value = self.get_storage_value(key=arg_key)['value']

        # this is local value from FilePicker
        else:
            value = arg_key

        log.debug(f'Final Value for parameter {arg_name}: {value}')
        return value


    def write_task_parameter_value(self, output_name, value):
        '''
        Pass the given value in the Storage for the next TASK input

        :param: output_name: name of the Output parameter of the TASK to write for the next task
        :param: value: value to set with the corresponding key
        '''

        # Get the reference for the dynamic output
        output_key = os.environ.get(output_name)

        if output_key is None:
            raise ValueError(
                'No key matching {} - Either wrong Dynamic output name or not correctly passed on the UI'.format(output_name))

        # Write the key - file id in the storage
        self.set_storage_value(output_key, value)
        log.debug(f'File data {value} written in Storage for {output_name} argument with key {output_key}')

        return {output_name: (output_key, value)}

    # -------------------------------------------------------------
    # Combined Methods
    # 1. download file given input parameter name
    # 2. upload file and put file dictionary to the storage
    # -------------------------------------------------------------
    def download_from_input_parameter(self, arg_name, dest_file_name=None, dest_folder_name=None, save=False):
        '''
        Download the file using Parameter name and save it as dest_file_name

        :param: output_name: name of the Output parameter of the TASK to write for the next task
        :param: dest_file_name: name of the saved file including the file extension. If None it saves with original name
        :param dest_folder_name: name of the folder on the hard disk drive to save the file in. Default is None 
        :param: save: if True it saves locally the file from the input, otherwise it returns the BytesIO object (streamed from the datalake)

        :return: None if the file is saved, BytesIO object of the file if save i False
        '''

        # Read the passed Input value from the Pipeline Storage
        value = self.read_task_parameter_value(arg_name)
        log.debug(f'Arg_name: {arg_name}, Value: {value}')

        if value in [None, '']:
            raise Exception(f'Nothing found in the parameter {arg_name}: {value}')

        else:
            # Try to read the string value as a dictionary (containing the name, id, groupname keys) or keep as string
            try:
                file_dict = literal_eval(value)
                log.debug('{} reads as dict'.format(value))
            except:
                file_dict = value
                log.debug('{} reads as string'.format(value))

            if isinstance(file_dict, str):
                # Check if a simple ID was passed as value (for BACKWARD COMPATIBILITY)
                regex_id = '[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'

                if re.search(regex_id, file_dict):
                    # Re-format as dictionary with id key
                    file_dict = {"id": file_dict}

                else:
                    raise Exception('Wrongly formatted value passed as Input: {}'.format(value))


        log.debug(f"Input Value Retrieved - File Dict: {file_dict}")


        # Download the corresponding file
        dh = DatalakeHandler()

        if 'id' in file_dict.keys(): 
            log.debug('Downloading file by id')

            # Download by ID
            file_id = file_dict['id']

            # Return None if file saved on disk else BytesIO object
            return dh.download_by_id(file_id=file_id, dest_file_name=dest_file_name, dest_folder_name=dest_folder_name, save=save)


        elif 'name' in file_dict.keys():
            log.debug('Downloading file by name')

            # Download by name & group
            file_group = file_dict['groupName'] if 'groupName' in file_dict.keys() else None
            file_name = file_dict['name']

            # Return None if file saved on disk else BytesIO object
            return dh.download_by_name(file_name=file_name,
                                       group_name=file_group,
                                       dest_file_name=dest_file_name,
                                       dest_folder_name=dest_folder_name,
                                       save=save)

        else:
            raise Exception(f'File cannot be downloaded by given parameter name: {arg_name}')



    def upload_to_output_parameter(self, output_name, file, group_name, file_upload_name=None, file_type='SOURCE', partial_update=False, sync=True):
        '''
        Upload the file to the datalake as the Output of the TASK
        and pass its ID in the Storage for the next TASK input

        :param: output_name: name of the Output parameter of the TASK to write for the next task
        :param: file: Either the object to stream to the datalake, either the path of the file to upload to the datalake
        :param: group_name: group where to upload the output file
        :param: file_upload_name: name of the file to upload on the datalake
                    - MANDATORY if the file is a python object and not a path to a file saved on the disk
        :param: file_type: file type on the datalake among SOURCE, NCSV ...
        :param: sync: whether we should wait for the
        '''

        # Upload the file to datalake
        uploader = DatalakeHandler()

        file_id, file_name = uploader.upload_file(file=file,
                                                  group_name=group_name,
                                                  file_upload_name=file_upload_name,
                                                  file_type=file_type,
                                                  partial_update = partial_update,
                                                  sync=sync)

        log.debug('File {} uploaded to {} with ID {}'.format(file, group_name, file_id))



        # Write the json containing the id, name, groupName in the Pipeline Storage
        try:
            value = json.dumps({'id': file_id, 'name': file_name, 'groupName': group_name})
            return self.write_task_parameter_value(output_name=output_name, value=value)

        except ValueError:
            log.warning(f'Output {output_name} not connected to another task -no value written in the Pipeline Storage')
            return
