#!/usr/bin/python3
"""
Script that, using a REST API, for a given employee ID, returns
information about his/her TODO list progress and exports it to a CSV file.
"""

import csv
import requests
import sys


def export_employee_todo_to_csv(employee_id):
    base_url = "https://jsonplaceholder.typicode.com/users/{}"
    user_url = base_url.format(employee_id)
    todos_url = "{}/todos".format(user_url)

    user_response = requests.get(user_url)
    todos_response = requests.get(todos_url)

    if user_response.status_code != 200 or todos_response.status_code != 200:
        print("Error: Unable to fetch data for employee ID {}"
              .format(employee_id))
        return

    user_data = user_response.json()
    todos_data = todos_response.json()

    employee_name = user_data['name']

    with open('{}.csv'.format(employee_id), 'w', newline='') as csvfile:
        taskwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for todo in todos_data:
            taskwriter.writerow([employee_id, employee_name,
                                 todo['completed'], todo['title']])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <employee_id>")
        sys.exit(1)

    employee_id = sys.argv[1]
    export_employee_todo_to_csv(employee_id)
