from flask import Flask, request, jsonify

app = Flask(__name__)
users = []
tasks = []

@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if any(user['username'] == username for user in users):
        return jsonify({'error': 'Username already exists'}), 400

    user = {
        'id': len(users) + 1,
        'username': username,
        'password': password
    }
    users.append(user)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    if user:
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data['title']
    description = data['description']
    due_date = data['due_date']
    assigned_to = data['assigned_to']
    task = {
        'id': len(tasks) + 1,
        'title': title,
        'description': description,
        'due_date': due_date,
        'assigned_to': assigned_to,
        'completed': False
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(tasks), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        data = request.get_json()
        task['title'] = data['title']
        task['description'] = data['description']
        task['due_date'] = data['due_date']
        task['assigned_to'] = data['assigned_to']
        task['completed'] = data['completed']
        return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        tasks.remove(task)
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/search', methods=['GET'])
def search_tasks():
    keyword = request.args.get('keyword')
    filtered_tasks = [task for task in tasks if
                      keyword.lower() in task['title'].lower() or keyword.lower() in task['description'].lower()]
    return jsonify(filtered_tasks), 200

if __name__ == '__main__':
    app.run(debug=True)
