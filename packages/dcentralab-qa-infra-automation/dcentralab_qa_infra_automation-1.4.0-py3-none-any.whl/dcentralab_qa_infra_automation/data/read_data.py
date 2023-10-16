import datetime
import json
import csv
import logging.config

import pytest

"""
data driven - get parameters from files as JSON, CSV

@Author: Efrat Cohen
@Date: 11.2022
"""


def getJSONData(file_name):
    """
       read JSON file parameters
       store the data driven in global param to be able to use the parameters in everywhere in the project.

       @param file_name - JSON file path
       @return data_list - file parameters
    """
    # Open the json file
    f = open(file_name)

    # Returns JSON object as a dictionary
    data_list = json.load(f)

    # Store the data driver in global param.
    # pytest.data_driven = data_list.get("data")

    # Closing file
    f.close()
    return data_list


def getAPIJSONData(data_file, template_file):
    """
    read JSON file parameters compare with the template_file data and change the necessary sent values. In the
    template_file - put null when no need to send new value. If the keys are not the same - template_file is the
    updated,  the test fail with reason to change the data_file current key

    @param data_file - JSON file path
    @param template_file - template file that contains different data.
    @return data_list - file parameters
    """
    # Open the API data file
    file = open(data_file)

    # Returns JSON object as a dictionary
    json_list = json.load(file)

    data_list = json_list.get("data")[0]
    # Closing file
    file.close()

    # Open the template API data file
    file = open(template_file)

    # Returns JSON object as a dictionary
    template_data_list = json.load(file)

    # Closing file
    file.close()

    # Set start_date date to current next day
    nextDay = datetime.datetime.today() + datetime.timedelta(days=1)
    nextDay_date = str(nextDay.date()) + "T18:30:00+00:00"
    new_data = {"start_time": nextDay_date}
    data_list.update(new_data)

    for i, data in enumerate(template_data_list):

        # Check if current key does not exist in the Json data dictionary - fail the test with logs.
        if data not in data_list:
            logging.info("key: " + data + "does not exist in data json")
            pytest.fail("Test failed because template json data has key that does not exist in the json file, "
                        "please update the files as need.")
        assert data in data_list, "data is in the json"

        # If any key in template file has value - change the data json file with this value.
        if template_data_list.get(data) is not None:
            new_data = {data: template_data_list.get(data)}
            data_list.update(new_data)

    # Convert None to null
    for i, data in enumerate(data_list):

        if data_list.get(data) is None:
            new_data = {data: json.dumps(data_list.get(data))}
            data_list.update(new_data)

    return json_list.get("data")


def getMultiObjectsJSONData(file_name):
    """
       read JSON file parameters
       store the data driven in global param to be able to use the parameters in everywhere in the project.

       @param file_name - JSON file path
       @return data_list - file parameters
    """
    # Open the json file
    f = open(file_name)

    # Returns JSON object as a dictionary
    data_list = json.load(f)

    # Store the data driven in global param.
    pytest.data_driven = data_list

    vesting_types = pytest.data_driven.get("types")

    # Closing file
    f.close()
    return vesting_types


def getCSVData(file_name):
    """
    read CSV file parameters

    @param file_name - CSV file path
    @return data_list - file parameters
    """
    # Create an empty list
    data_list = []
    # Open CSV file
    csv_data = open(file_name, "r")
    # Create CSV reader
    reader = csv.reader(csv_data)
    # Skip header - not get the header line
    next(reader)
    # Add CSV rows to list
    for row in data_list:
        data_list.append(row)
    # return CSV data list
    return data_list
