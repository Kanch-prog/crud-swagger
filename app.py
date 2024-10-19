from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# In-memory data storage for employees
employees_data = [
    {'id': 1, 'name': 'Abhilash Gaurav'},
    {'id': 2, 'name': 'Ramish Verma'}
]

# Resource class for all employees
class EmployeesResource(Resource):
    def get(self):
        """
        Get a list of all employees
        ---
        responses:
          200:
            description: A list of employees
        """
        return employees_data, 200

    def post(self):
        """
        Add a new employee
        ---
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: Employee
              required:
                - name
              properties:
                name:
                  type: string
                  description: The name of the employee
        responses:
          201:
            description: The added employee
          400:
            description: Bad request
        """
        data = request.get_json()
        new_id = employees_data[-1]['id'] + 1 if employees_data else 1
        new_employee = {'id': new_id, 'name': data['name']}
        employees_data.append(new_employee)
        return new_employee, 201

# Resource class for a single employee
class EmployeeResource(Resource):
    def put(self, employee_id):
        """
        Update an existing employee
        ---
        parameters:
          - in: path
            name: employee_id
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
              id: Employee
              properties:
                name:
                  type: string
                  description: The name of the employee
        responses:
          200:
            description: The updated employee
          404:
            description: Employee not found
        """
        data = request.get_json()
        for employee in employees_data:
            if employee['id'] == employee_id:
                employee['name'] = data['name']
                return employee, 200
        return {'message': 'Employee not found'}, 404

    def delete(self, employee_id):
        """
        Delete an existing employee
        ---
        parameters:
          - in: path
            name: employee_id
            type: integer
            required: true
        responses:
          200:
            description: Employee deleted successfully
          404:
            description: Employee not found
        """
        for i, employee in enumerate(employees_data):
            if employee['id'] == employee_id:
                deleted_employee = employees_data.pop(i)
                return {'message': 'Employee deleted successfully', 'employee': deleted_employee}, 200
        return {'message': 'Employee not found'}, 404

# Adding resources to the API
api.add_resource(EmployeesResource, '/employees')
api.add_resource(EmployeeResource, '/employee/<int:employee_id>')

if __name__ == '__main__':
    app.run(debug=True)
