from odoo import http
from odoo.http import request
from .response import *
from .tasks_helper import *
from urllib.parse import parse_qs
import json


class TasksAPI(http.Controller):

    @http.route('/api/task', type='http', auth='none', methods=['POST'], csrf=False)
    def create_task(self):
        data = json.loads(request.httprequest.data.decode('utf-8'))
        data = check_data(data)
        if isinstance(data, str):
            return response(message=data, status=400)
        else:
            task = request.env['todo.tasks'].sudo().create(data)
            return response(message="Task created successfully", data=task_to_dict(task), status=201)

    @http.route('/api/task/<int:task_id>', type='http', auth='none', methods=['GET'], csrf=False)
    def get_task(self, task_id):
        task = request.env['todo.tasks'].sudo().browse(task_id)

        if not task.exists():
            return response(message="Task not found", status=404)
        else:
            return response(message="Task retrieved successfully", data=task_to_dict(task))

    @http.route('/api/tasks', type='http', auth='none', methods=['GET'], csrf=False)
    def get_tasks(self):
        prams = parse_qs(request.httprequest.query_string.decode('utf-8'))
        domain = []
        page = 1
        offset = 0
        limit = 100
        if 'state' in prams:
            state = prams['state'][0]
            if state in ['new', 'in_progress', 'completed', 'closed']:
                domain.append(('state', '=', state))
            else:
                return response(message="Invalid state parameter", status=400)

        if 'page' in prams:
            try:
                page = int(prams['page'][0])
                if page < 1:
                    return response(message="Page number must be greater than 0", status=400)
                offset = (page - 1) * limit
            except ValueError:
                return response(message="Invalid page parameter", status=400)

        tasks = request.env['todo.tasks'].sudo().search(domain, offset=offset, limit=limit, order='id DESC')
        pages = request.env['todo.tasks'].sudo().search_count(domain)
        pagination_info = {
            'page': page,
            'limit': limit,
            'total_pages': (pages + limit - 1) // limit,
        }
        tasks_data = [task_to_dict(task) for task in tasks]
        return response(message="Tasks retrieved successfully", pagination_info=pagination_info, data=tasks_data)

    @http.route('/api/task/<int:task_id>', type='http', auth='none', methods=['PUT'], csrf=False)
    def update_task(self, task_id):
        data = json.loads(request.httprequest.data.decode('utf-8'))
        task = request.env['todo.tasks'].sudo().browse(task_id)

        if not task.exists():
            return response(message="Task not found", status=404)

        data = check_data_fields(data)

        if isinstance(data, str):
            return response(message=data, status=400)
        else:
            task.write(data)
            return response(message="Task updated successfully", data=task_to_dict(task))

    @http.route('/api/task/<int:task_id>', type='http', auth='none', methods=['DELETE'], csrf=False)
    def delete_task(self, task_id):
        task = request.env['todo.tasks'].sudo().browse(task_id)

        if not task.exists():
            return response(message="Task not found", status=404)

        task.unlink()
        return response(message="Task deleted successfully", status=204)
