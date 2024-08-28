from uuid import uuid4

import requests
import pytest
import uuid

ENDPOINT = "https://todo.pixegami.io"
CREATE_TASK = "/create-task"
GET_TASK = "/get-task/"
LIST_TASKS = "/list-tasks/"
UPDATE_TASKS = "/update-task"
DELETE_TASK = "/delete-task/"

def test_health_check_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    payload = new_task_payload()
    # Use PUT request to create a task
    create_task_response = create_task(payload)
    # Assert that the request was successful
    assert create_task_response.status_code == 200
    create_task_data = create_task_response.json()
    task_id = create_task_data["task"]["task_id"]
    # Use GET request to verify the task was created
    get_task_response = get_task(task_id)
    assert  get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

def test_can_update_task():
    # Create task
    payload = new_task_payload()
    # Use PUT request to create a task
    create_task_response = create_task(payload)
    # Assert request was successful
    assert create_task_response.status_code == 200
    create_task_data = create_task_response.json()
    task_id = create_task_data["task"]["task_id"]
    updated_task_payload = {
      "content": "Updated task",
      "user_id": payload["user_id"],
      "task_id": task_id,
      "is_done": True
    }
    # Update task
    update_task_response = update_task(updated_task_payload)
    # Assert request was successful
    assert update_task_response.status_code == 200
    # Get task
    current_task_response = get_task(task_id)
    # Validate changes
    current_task_data = current_task_response.json()
    assert current_task_data["content"] == updated_task_payload["content"]
    assert current_task_data["is_done"] == updated_task_payload["is_done"]

def test_can_list_tasks():
    # Create N tasks
    number_of_tasks = 3
    payload = new_task_payload()
    for _ in range(number_of_tasks):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # Get all tasks
    list_tasks_response = list_tasks(payload["user_id"])
    assert list_tasks_response.status_code == 200
    list_tasks_data = list_tasks_response.json()
    # Verify the correct number of tasks exist
    task_count = list_tasks_data["tasks"]
    assert len(task_count) == number_of_tasks

def test_can_delete_task():
    # Create a task
    payload = new_task_payload()
    # Use PUT request to create a task
    create_task_response = create_task(payload)
    # Assert request was successful
    assert create_task_response.status_code == 200
    create_task_data = create_task_response.json()
    task_id = create_task_data["task"]["task_id"]
    # Delete task
    delete_task_response = delete_task(task_id)
    assert  delete_task_response.status_code == 200
    # Verify that the task no longer exists
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404

# Utility functions
def create_task(payload):
    return requests.put(ENDPOINT + CREATE_TASK, json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + UPDATE_TASKS, json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + GET_TASK + task_id)

def list_tasks(user_id):
    return requests.get(ENDPOINT + LIST_TASKS + user_id)

def delete_task(task_id):
    return requests.delete(ENDPOINT + DELETE_TASK + task_id)

def new_task_payload():
    user_id = f"test_user_{uuid4().hex}"
    content = f"New task {uuid4().hex}"
    return {
      "content": content,
      "user_id": user_id,
      "is_done": False
    }
