import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.backend.fast_api.fast_api import app
from src.backend.fast_api.repository import task_repository


@pytest_asyncio.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    print("FINISHED")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_and_teardown(client):
    delete_all_data(client)
    await upload_test_data(client)
    yield
    delete_all_data(client)


def delete_all_data(client):
    task_repository.delete_all_tasks()


async def upload_test_data(client):
    predefined_tasks = [
        {
            'title': 'Learn Python',
            'description': 'Study the basics of Python programming.',
            'done': False
        },
        {
            'title': 'Build a REST API',
            'description': 'Create a simple REST API using FastAPI.',
            'done': False
        }
    ]

    for task in predefined_tasks:
        await client.post('/tasks', json=task)


@pytest.mark.asyncio
async def test_get_tasks(client):
    response = await client.get('/tasks')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert 'id' in data[0]


@pytest.mark.asyncio
async def test_get_task(client):
    response = await client.get('/tasks/1')
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['title'] == 'Learn Python'


@pytest.mark.asyncio
async def test_get_task_not_found(client):
    response = await client.get('/tasks/999')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_task(client):
    new_task = {'title': 'Test task', 'description': 'Test description'}
    response = await client.post('/tasks', json=new_task)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['title'] == 'Test task'


@pytest.mark.asyncio
async def test_update_task(client):
    updated_task = {'title': 'Updated task', 'description': 'Updated description'}
    response = await client.put('/tasks/1', json=updated_task)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Updated task'


@pytest.mark.asyncio
async def test_delete_task(client):
    response = await client.delete('/tasks/1')
    assert response.status_code == 204
    data = response.json()
    assert 'result' in data
    assert data['result'] is True
