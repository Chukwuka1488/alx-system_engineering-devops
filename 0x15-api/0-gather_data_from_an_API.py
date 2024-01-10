#!/usr/bin/python3
"""
Script that, using a REST API, for a given employee ID, returns
information about his/her TODO list progress.
"""

import requests
import sys

def get_employee_todo_progress(employee_id):
    session = requests.Session()

    base_url = "https://jsonplaceholder.typicode.com/users/{}"
    user_url = base_url.format(employee_id)
    todos_url = "{}/todos".format(user_url)

    user_response = session.get(user_url)
    todos_response = session.get(todos_url)

    if user_response.status_code != 200 or todos_response.status_code != 200:
        print("Error: Unable to fetch data for employee ID {}"
              .format(employee_id))
        return

    user_data = user_response.json()
    todos_data = todos_response.json()

    employee_name = user_data['name']
    total_tasks = len(todos_data)
    done_tasks = len([todo for todo in todos_data if todo['completed']])

    print("Employee {} is done with tasks({}/{})"
          .format(employee_name, done_tasks, total_tasks))
    for todo in todos_data:
        if todo['completed']:
            print("\t {}".format(todo['title']))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]
    get_employee_todo_progress(employee_id)
