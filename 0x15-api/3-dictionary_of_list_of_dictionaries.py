#!/usr/bin/python3
"""
Script that, using a REST API, for all employees, returns
information about his/her TODO list progress and exports it to a JSON file.
"""

import json
import requests

if __name__ == "__main__":
    session = requests.Session()

    users_url = "https://jsonplaceholder.typicode.com/users"
    users_response = session.get(users_url)

    if users_response.status_code != 200:
        print("Error: Unable to fetch data for employees")
        sys.exit(1)

    users_data = users_response.json()

    all_tasks = {}

    for user_data in users_data:
        employee_id = user_data['id']
        employee_name = user_data['username']

        todos_url = "https://jsonplaceholder.typicode.com/users/{}/todos".format(employee_id)
        todos_response = session.get(todos_url)

        if todos_response.status_code != 200:
            print("Error: Unable to fetch data for employee ID {}"
                  .format(employee_id))
            continue

        todos_data = todos_response.json()

        tasks = []
        for todo in todos_data:
            task = {"username": employee_name,
                    "task": todo['title'],
                    "completed": todo['completed']}
            tasks.append(task)

        all_tasks[employee_id] = tasks

    with open('todo_all_employees.json', 'w') as jsonfile:
        json.dump(all_tasks, jsonfile)
