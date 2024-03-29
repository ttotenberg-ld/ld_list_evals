from utils.apiHandler import checkRateLimit as api_call
from utils.newApiHandler import checkRateLimit as new_api_call
import json
import os
from dotenv import load_dotenv

load_dotenv()


'''
Set your LaunchDarkly instance information here
'''
API_KEY = os.environ["API_KEY"]
PROJECT_KEY = os.environ["PROJECT_KEY"]
ENVIRONMENT_KEY = os.environ["ENVIRONMENT_KEY"]



'''
Define API call information
'''
flag_list_url = f'/flags/{PROJECT_KEY}'

def total(arr):
    sum = 0

    for i in arr:
        sum = sum + i
 
    return(sum)


def get_flag_list():
    response = api_call("GET", flag_list_url, API_KEY, {}).json()
    response_list = response['items']
    number_of_flags = len(response_list)
    flag_list = []

    for i in range(number_of_flags):
        flag_list.append(response['items'][i]['key'])
    
    return flag_list

# Main function
def get_flag_usage():

    # Get the list of flags, print it just because
    flag_list = get_flag_list()
    print(flag_list)

    # Create a text file for output
    file = open('output.txt', 'w')

    # Iterate through the list of flags
    for i in flag_list:
        # Write the flag key
        file.write(f'{i}: ')
        # Get a series of usage entries over a time period (default is for the past 30 days)
        flag_usage_url = f'/usage/evaluations/{PROJECT_KEY}/{ENVIRONMENT_KEY}/{i}'

        print(f"Trying for flag {i}")
        response = new_api_call("GET", flag_usage_url, API_KEY, {}).json()

        series = response["series"]
        series_value = []

        # Iterate through series entries, and add up the values
        for entry in series:
            for key, value in entry.items():
                if key != "time":
                    series_value.append(value)
            
        
        series_total = total(series_value)
        # Write the total to the text file
        file.write(f'{series_total} \n')

    
    file.close()

if __name__ == "__main__":
    get_flag_usage()