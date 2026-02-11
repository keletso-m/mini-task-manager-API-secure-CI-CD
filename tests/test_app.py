import pytest
import json

from src.app import app, init_db

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'  # Use in-memory database for tests
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

@pytest.fixture
def auth_headers(client):
    """Register a user and return auth headers"""
    # Register user
    client.post('/api/register', 
                json={'username': 'testuser', 'password': 'password123'})
    
    # Login
    response = client.post('/api/login',
                          json={'username': 'testuser', 'password': 'password123'})
    
    data = json.loads(response.data)
    token = data['token']
    
    return {'Authorization': f'Bearer {token}'}

class TestAuth:
    """Test authentication endpoints"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/api/register',
                              json={'username': 'newuser', 'password': 'password123'})
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User registered successfully'
        assert 'user_id' in data
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        client.post('/api/register',
                   json={'username': 'testuser', 'password': 'password123'})
        
        response = client.post('/api/register',
                              json={'username': 'testuser', 'password': 'different'})
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'already exists' in data['message']
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields"""
        response = client.post('/api/register',
                              json={'username': 'testuser'})
        
        assert response.status_code == 400
    
    def test_register_short_password(self, client):
        """Test registration with password too short"""
        response = client.post('/api/register',
                              json={'username': 'testuser', 'password': '123'})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'at least 6 characters' in data['message']
    
    def test_login_success(self, client):
        """Test successful login"""
        client.post('/api/register',
                   json={'username': 'testuser', 'password': 'password123'})
        
        response = client.post('/api/login',
                              json={'username': 'testuser', 'password': 'password123'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        assert data['message'] == 'Login successful'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        client.post('/api/register',
                   json={'username': 'testuser', 'password': 'password123'})
        
        response = client.post('/api/login',
                              json={'username': 'testuser', 'password': 'wrongpassword'})
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['message']
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post('/api/login',
                              json={'username': 'nonexistent', 'password': 'password123'})
        
        assert response.status_code == 401

class TestTasks:
    """Test task management endpoints"""
    
    def test_create_task_success(self, client, auth_headers):
        """Test successful task creation"""
        response = client.post('/api/tasks',
                              json={'title': 'Test Task', 'description': 'Test Description'},
                              headers=auth_headers)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Task created successfully'
        assert 'task_id' in data
    
    def test_create_task_without_auth(self, client):
        """Test task creation without authentication"""
        response = client.post('/api/tasks',
                              json={'title': 'Test Task'})
        
        assert response.status_code == 401
    
    def test_create_task_missing_title(self, client, auth_headers):
        """Test task creation without title"""
        response = client.post('/api/tasks',
                              json={'description': 'No title'},
                              headers=auth_headers)
        
        assert response.status_code == 400
    
    def test_get_tasks_empty(self, client, auth_headers):
        """Test getting tasks when none exist"""
        response = client.get('/api/tasks', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['tasks'] == []
    
    def test_get_tasks_with_data(self, client, auth_headers):
        """Test getting tasks with existing tasks"""
        # Create some tasks
        client.post('/api/tasks',
                   json={'title': 'Task 1', 'description': 'First task'},
                   headers=auth_headers)
        client.post('/api/tasks',
                   json={'title': 'Task 2', 'description': 'Second task'},
                   headers=auth_headers)
        
        response = client.get('/api/tasks', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 2
        assert data['tasks'][0]['title'] == 'Task 2'  # Most recent first
    
    def test_update_task_success(self, client, auth_headers):
        """Test successful task update"""
        # Create task
        create_response = client.post('/api/tasks',
                                     json={'title': 'Original Title'},
                                     headers=auth_headers)
        task_id = json.loads(create_response.data)['task_id']
        
        # Update task
        response = client.put(f'/api/tasks/{task_id}',
                             json={'title': 'Updated Title', 'completed': True},
                             headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Task updated successfully'
    
    def test_update_nonexistent_task(self, client, auth_headers):
        """Test updating a task that doesn't exist"""
        response = client.put('/api/tasks/9999',
                             json={'title': 'Updated'},
                             headers=auth_headers)
        
        assert response.status_code == 404
    
    def test_delete_task_success(self, client, auth_headers):
        """Test successful task deletion"""
        # Create task
        create_response = client.post('/api/tasks',
                                     json={'title': 'Task to delete'},
                                     headers=auth_headers)
        task_id = json.loads(create_response.data)['task_id']
        
        # Delete task
        response = client.delete(f'/api/tasks/{task_id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Task deleted successfully'
        
        # Verify task is gone
        get_response = client.get('/api/tasks', headers=auth_headers)
        tasks_data = json.loads(get_response.data)
        assert len(tasks_data['tasks']) == 0
    
    def test_delete_nonexistent_task(self, client, auth_headers):
        """Test deleting a task that doesn't exist"""
        response = client.delete('/api/tasks/9999', headers=auth_headers)
        
        assert response.status_code == 404

class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
