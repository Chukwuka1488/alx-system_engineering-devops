#!/usr/bin/python3
"""
Script that, using a REST API, for a given employee ID, returns
information about his/her TODO list progress and exports it to a JSON file.
"""

import json
import requests
from sys import argv

if __name__ == "__main__":
    session = requests.Session()

    employee_id = argv[1]
    base_url = "https://jsonplaceholder.typicode.com/users/{}"
    user_url = base_url.format(employee_id)
    todos_url = "{}/todos".format(user_url)

    user_response = session.get(user_url)
    todos_response = session.get(todos_url)

    if user_response.status_code != 200 or todos_response.status_code != 200:
        print("Error: Unable to fetch data for employee ID {}"
              .format(employee_id))
        sys.exit(1)

    user_data = user_response.json()
    todos_data = todos_response.json()

    employee_name = user_data['username']

    tasks = []
    for todo in todos_data:
        task = {"task": todo['title'],
                "completed": todo['completed'],
                "username": employee_name}
        tasks.append(task)

    with open('{}.json'.format(employee_id), 'w') as jsonfile:
        json.dump({employee_id: tasks}, jsonfile)
