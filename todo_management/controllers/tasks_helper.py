from gevent.testing.travis import commands
from odoo import http
from odoo.http import request
from datetime import datetime


def task_to_dict(task):
    return {
        'id': task.id,
        'ref': task.ref if task.ref else "New",
        'name': task.name,
        'description': task.description,
        'assign_to': task.assign_to.id,
        'due_date': str(task.due_date),
        'is_late': task.is_late,
        'estimated_time': task.estimated_time,
        'state': task.state,
        'active': task.active,
        'total_time': task.total_time,
        'task_line_ids': [{
            'id': line.id,
            'date': str(line.date),
            'description': line.description,
            'duration': line.duration
        } for line in task.task_line_ids] if task.task_line_ids else []
    }

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def prepare_task_lines(task_lines):
    commands = []

    for line in task_lines:
        if not isinstance(line, dict):
            return "Each task line must be a dictionary"

        if not all(k in line for k in ['date', 'description', 'duration']):
            return "Each task line must have date, description, and duration"

        if not is_valid_date(line['date']):
            return "Invalid date format in task line. Use YYYY-MM-DD."

        if not isinstance(line['duration'], int) or line['duration'] <= 0:
            return "Duration must be a positive integer in task line"

        commands.append((0, 0, {
            'date': line['date'],
            'description': line['description'],
            'duration': line['duration']
        }))

    return commands


def check_data_fields(data):
    if 'name' in data and not isinstance(data['name'], str) or not data['name'].strip():
        return "Task name must be a non-empty string"

    if 'description' in data and not isinstance(data['description'], str):
        return "Description must be a string"

    assign_id = data['assign_to'] if 'assign_to' in data else 0
    if not request.env['res.users'].sudo().browse(assign_id).exists():
        return "Assigned user with ID " + assign_id + " does not exist"

    if 'due_date' in data and not isinstance(data['due_date'], str) or not is_valid_date(data['due_date']):
        return "Invalid due date format. Use YYYY-MM-DD."

    if 'estimated_time' in data and not isinstance(data['estimated_time'], int) or data['estimated_time'] <= 0:
        return "Estimated time must be a positive integer"

    if 'state' in data and data['state'] not in ['new', 'in_progress', 'completed', 'closed']:
        return "Invalid state. Allowed values are: new, in_progress, completed, closed"

    if 'active' in data and not isinstance(data['active'], bool):
        return "Active must be a boolean value"

    if 'task_line_ids' in data:
        if not isinstance(data['task_line_ids'], list):
            return "Task line IDs must be a list of dictionaries"

        commands = prepare_task_lines(data['task_line_ids'])

        if isinstance(commands, str):
            return commands
        else:
            data['task_line_ids'] = commands

    return data


def check_data(data):
    if not data:
        return "No data provided"

    required_fields = ['name', 'description', 'assign_to', 'due_date', 'estimated_time']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return "Missing required fields: " + ", ".join(missing_fields)

    return check_data_fields(data)
