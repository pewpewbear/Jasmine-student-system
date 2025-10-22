#!/usr/bin/env python3
"""
Web-based GUI for University Student System
Simple HTTP server with HTML/JavaScript interface
"""

import http.server
import socketserver
import json
import urllib.parse
from models.database import Database
from models.student import Student
from services.auth_service import is_valid_email, is_valid_password, authenticate
from services.id_service import new_student_id, new_subject_id
from services.grading_service import grade_from_mark
import random

class UniversityWebHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the university web interface"""
    
    def __init__(self, *args, **kwargs):
        self.db = Database()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.serve_main_page()
        elif self.path == '/student':
            self.serve_student_page()
        elif self.path == '/admin':
            self.serve_admin_page()
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/register':
            self.handle_register()
        elif self.path == '/api/login':
            self.handle_login()
        elif self.path == '/api/enroll':
            self.handle_enroll()
        elif self.path == '/api/remove_subject':
            self.handle_remove_subject()
        elif self.path == '/api/change_password':
            self.handle_change_password()
        elif self.path == '/api/get_students':
            self.handle_get_students()
        elif self.path == '/api/remove_student':
            self.handle_remove_student()
        elif self.path == '/api/clear_database':
            self.handle_clear_database()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        """Serve the main page"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>University Student System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .button-group {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 30px 0;
        }
        .btn {
            padding: 15px 30px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-primary:hover {
            background-color: #0056b3;
        }
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        .btn-success:hover {
            background-color: #1e7e34;
        }
        .status {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            color: #155724;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>University Student System</h1>
        <p style="text-align: center; color: #666;">Welcome to the University Student Management System</p>
        
        <div class="button-group">
            <a href="/student" class="btn btn-primary">Student Portal</a>
            <a href="/admin" class="btn btn-success">Admin Portal</a>
        </div>
        
        <div class="status">
            <strong>System Status:</strong> Ready
        </div>
    </div>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_student_page(self):
        """Serve the student portal page"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Portal</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            background-color: #e9ecef;
            border: none;
            cursor: pointer;
            margin-right: 5px;
        }
        .tab.active {
            background-color: #007bff;
            color: white;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .btn {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        .btn-success {
            background-color: #28a745;
        }
        .btn-danger {
            background-color: #dc3545;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .alert {
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Student Portal</h1>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('login')">Login</button>
            <button class="tab" onclick="showTab('register')">Register</button>
            <button class="tab" onclick="showTab('dashboard')" id="dashboardTab" style="display:none;">Dashboard</button>
        </div>
        
        <!-- Login Tab -->
        <div id="login" class="tab-content active">
            <h2>Student Login</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="loginEmail">Email:</label>
                    <input type="email" id="loginEmail" required>
                </div>
                <div class="form-group">
                    <label for="loginPassword">Password:</label>
                    <input type="password" id="loginPassword" required>
                </div>
                <button type="submit" class="btn">Login</button>
            </form>
        </div>
        
        <!-- Register Tab -->
        <div id="register" class="tab-content">
            <h2>New Student Registration</h2>
            <form id="registerForm">
                <div class="form-group">
                    <label for="regName">Name:</label>
                    <input type="text" id="regName" required>
                </div>
                <div class="form-group">
                    <label for="regEmail">Email:</label>
                    <input type="email" id="regEmail" required>
                </div>
                <div class="form-group">
                    <label for="regPassword">Password:</label>
                    <input type="password" id="regPassword" required>
                </div>
                <button type="submit" class="btn">Register</button>
            </form>
        </div>
        
        <!-- Dashboard Tab -->
        <div id="dashboard" class="tab-content">
            <h2>Student Dashboard</h2>
            <div id="studentInfo"></div>
            
            <h3>Subject Enrollment</h3>
            <div id="enrollmentStatus"></div>
            
            <table id="subjectsTable">
                <thead>
                    <tr>
                        <th>Subject ID</th>
                        <th>Mark</th>
                        <th>Grade</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
            
            <div style="margin-top: 20px;">
                <button class="btn" onclick="enrollSubject()">Enroll Subject</button>
                <button class="btn" onclick="changePassword()">Change Password</button>
            </div>
        </div>
        
        <div id="alerts"></div>
    </div>
    
    <script>
        let currentStudent = null;
        
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function showAlert(message, type = 'success') {
            const alertsDiv = document.getElementById('alerts');
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type}`;
            alertDiv.textContent = message;
            alertsDiv.appendChild(alertDiv);
            
            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
        
        // Login form
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email, password})
                });
                
                const result = await response.json();
                if (result.success) {
                    currentStudent = result.student;
                    showAlert('Login successful!');
                    showTab('dashboard');
                    document.getElementById('dashboardTab').style.display = 'block';
                    loadDashboard();
                } else {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                showAlert('Login failed: ' + error.message, 'danger');
            }
        });
        
        // Register form
        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('regName').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            
            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, email, password})
                });
                
                const result = await response.json();
                if (result.success) {
                    showAlert('Registration successful! Student ID: ' + result.student_id);
                    document.getElementById('registerForm').reset();
                } else {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                showAlert('Registration failed: ' + error.message, 'danger');
            }
        });
        
        function loadDashboard() {
            if (!currentStudent) return;
            
            document.getElementById('studentInfo').innerHTML = `
                <p><strong>Student ID:</strong> ${currentStudent.id}</p>
                <p><strong>Name:</strong> ${currentStudent.name}</p>
                <p><strong>Email:</strong> ${currentStudent.email}</p>
            `;
            
            const avgMark = currentStudent.subjects.reduce((sum, s) => sum + s.mark, 0) / currentStudent.subjects.length || 0;
            const status = avgMark >= 50 ? 'PASS' : 'FAIL';
            
            document.getElementById('enrollmentStatus').innerHTML = `
                <p><strong>Enrollment:</strong> ${currentStudent.subjects.length}/4</p>
                <p><strong>Average Mark:</strong> ${Math.round(avgMark)}</p>
                <p><strong>Status:</strong> ${status}</p>
            `;
            
            const tbody = document.querySelector('#subjectsTable tbody');
            tbody.innerHTML = '';
            currentStudent.subjects.forEach(subject => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${subject.id}</td>
                    <td>${subject.mark}</td>
                    <td>${subject.grade}</td>
                    <td><button class="btn btn-danger" onclick="removeSubject('${subject.id}')">Remove</button></td>
                `;
            });
        }
        
        async function enrollSubject() {
            if (!currentStudent) return;
            
            try {
                const response = await fetch('/api/enroll', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({student_id: currentStudent.id})
                });
                
                const result = await response.json();
                if (result.success) {
                    showAlert(result.message);
                    currentStudent = result.student;
                    loadDashboard();
                } else {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                showAlert('Enrollment failed: ' + error.message, 'danger');
            }
        }
        
        async function removeSubject(subjectId) {
            if (!currentStudent) return;
            
            try {
                const response = await fetch('/api/remove_subject', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({student_id: currentStudent.id, subject_id: subjectId})
                });
                
                const result = await response.json();
                if (result.success) {
                    showAlert(result.message);
                    currentStudent = result.student;
                    loadDashboard();
                } else {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                showAlert('Removal failed: ' + error.message, 'danger');
            }
        }
        
        function changePassword() {
            const newPassword = prompt('Enter new password:');
            if (!newPassword) return;
            
            const confirmPassword = prompt('Confirm new password:');
            if (newPassword !== confirmPassword) {
                showAlert('Passwords do not match', 'danger');
                return;
            }
            
            fetch('/api/change_password', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({student_id: currentStudent.id, password: newPassword})
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    showAlert('Password changed successfully');
                } else {
                    showAlert(result.message, 'danger');
                }
            })
            .catch(error => {
                showAlert('Password change failed: ' + error.message, 'danger');
            });
        }
    </script>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_admin_page(self):
        """Serve the admin portal page"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Portal</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .btn {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        .btn-danger {
            background-color: #dc3545;
        }
        .btn-success {
            background-color: #28a745;
        }
        .alert {
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Admin Portal</h1>
        
        <div>
            <button class="btn" onclick="refreshStudents()">Refresh</button>
            <button class="btn btn-success" onclick="groupByGrade()">Group by Grade</button>
            <button class="btn btn-success" onclick="partitionPassFail()">Partition Pass/Fail</button>
            <button class="btn btn-danger" onclick="clearDatabase()">Clear Database</button>
        </div>
        
        <table id="studentsTable">
            <thead>
                <tr>
                    <th>Student ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Avg Mark</th>
                    <th>Status</th>
                    <th>Subjects</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
        
        <div id="alerts"></div>
    </div>
    
    <script>
        function showAlert(message, type = 'success') {
            const alertsDiv = document.getElementById('alerts');
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type}`;
            alertDiv.textContent = message;
            alertsDiv.appendChild(alertDiv);
            
            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
        
        async function refreshStudents() {
            try {
                const response = await fetch('/api/get_students');
                const students = await response.json();
                
                const tbody = document.querySelector('#studentsTable tbody');
                tbody.innerHTML = '';
                
                students.forEach(student => {
                    const avgMark = student.subjects.reduce((sum, s) => sum + s.mark, 0) / student.subjects.length || 0;
                    const status = avgMark >= 50 ? 'PASS' : 'FAIL';
                    
                    const row = tbody.insertRow();
                    row.innerHTML = `
                        <td>${student.id}</td>
                        <td>${student.name}</td>
                        <td>${student.email}</td>
                        <td>${Math.round(avgMark)}</td>
                        <td>${status}</td>
                        <td>${student.subjects.length}</td>
                        <td><button class="btn btn-danger" onclick="removeStudent('${student.id}')">Remove</button></td>
                    `;
                });
            } catch (error) {
                showAlert('Failed to load students: ' + error.message, 'danger');
            }
        }
        
        async function groupByGrade() {
            try {
                const response = await fetch('/api/get_students');
                const students = await response.json();
                
                const gradeCounts = {HD: 0, D: 0, C: 0, P: 0, F: 0};
                
                students.forEach(student => {
                    if (student.subjects.length > 0) {
                        const highestGrade = student.subjects.reduce((highest, subject) => {
                            const gradeOrder = {HD: 5, D: 4, C: 3, P: 2, F: 1};
                            return gradeOrder[subject.grade] > gradeOrder[highest] ? subject.grade : highest;
                        }, 'F');
                        gradeCounts[highestGrade]++;
                    }
                });
                
                const message = `Grade Distribution:\\nHD: ${gradeCounts.HD}\\nD: ${gradeCounts.D}\\nC: ${gradeCounts.C}\\nP: ${gradeCounts.P}\\nF: ${gradeCounts.F}`;
                alert(message);
            } catch (error) {
                showAlert('Failed to group by grade: ' + error.message, 'danger');
            }
        }
        
        async function partitionPassFail() {
            try {
                const response = await fetch('/api/get_students');
                const students = await response.json();
                
                const passStudents = students.filter(s => {
                    const avgMark = s.subjects.reduce((sum, sub) => sum + sub.mark, 0) / s.subjects.length || 0;
                    return avgMark >= 50;
                });
                const failStudents = students.filter(s => {
                    const avgMark = s.subjects.reduce((sum, sub) => sum + sub.mark, 0) / s.subjects.length || 0;
                    return avgMark < 50;
                });
                
                let message = `Pass/Fail Partition:\\n\\nPASS: ${passStudents.length} students\\n`;
                passStudents.forEach(s => {
                    const avgMark = s.subjects.reduce((sum, sub) => sum + sub.mark, 0) / s.subjects.length || 0;
                    message += `  ${s.id} ${s.name} (avg ${Math.round(avgMark)})\\n`;
                });
                
                message += `\\nFAIL: ${failStudents.length} students\\n`;
                failStudents.forEach(s => {
                    const avgMark = s.subjects.reduce((sum, sub) => sum + sub.mark, 0) / s.subjects.length || 0;
                    message += `  ${s.id} ${s.name} (avg ${Math.round(avgMark)})\\n`;
                });
                
                alert(message);
            } catch (error) {
                showAlert('Failed to partition students: ' + error.message, 'danger');
            }
        }
        
        async function removeStudent(studentId) {
            if (!confirm('Are you sure you want to remove this student?')) return;
            
            try {
                const response = await fetch('/api/remove_student', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({student_id: studentId})
                });
                
                const result = await response.json();
                if (result.success) {
                    showAlert('Student removed successfully');
                    refreshStudents();
                } else {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                showAlert('Failed to remove student: ' + error.message, 'danger');
            }
        }
        
        async function clearDatabase() {
            if (!confirm('Are you sure you want to clear the entire database? This action cannot be undone.')) return;
            
            try {
                const response = await fetch('/api/clear_database', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({})
                });
                
                const result = await response.json();
                if (result.success) {
                    showAlert('Database cleared successfully');
                    refreshStudents();
                } else {
                    showAlert(result.message, 'danger');
                }
            } catch (error) {
                showAlert('Failed to clear database: ' + error.message, 'danger');
            }
        }
        
        // Load students on page load
        refreshStudents();
    </script>
</body>
</html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_register(self):
        """Handle student registration"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        try:
            if not name or not email or not password:
                self.send_json_response({'success': False, 'message': 'Please fill in all fields'})
                return
                
            if not is_valid_email(email):
                self.send_json_response({'success': False, 'message': 'Invalid email format. Must end with @anything.uts.edu.au'})
                return
                
            if not is_valid_password(password):
                self.send_json_response({'success': False, 'message': 'Invalid password format. Must start with uppercase, have at least 5 letters, then at least 3 digits.'})
                return
                
            if self.db.find_by_email(email):
                self.send_json_response({'success': False, 'message': 'Email already registered'})
                return
                
            # Create new student
            student_id = new_student_id(self.db)
            student = Student(student_id, name, email, password)
            self.db.upsert(student)
            
            self.send_json_response({'success': True, 'student_id': student_id})
            
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)})
    
    def handle_login(self):
        """Handle student login"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        try:
            student = authenticate(email, password, self.db)
            if student:
                # Convert student to dict for JSON serialization
                student_dict = {
                    'id': student.id,
                    'name': student.name,
                    'email': student.email,
                    'subjects': [{'id': s.id, 'mark': s.mark, 'grade': s.grade} for s in student.subjects]
                }
                self.send_json_response({'success': True, 'student': student_dict})
            else:
                self.send_json_response({'success': False, 'message': 'Invalid credentials'})
                
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)})
    
    def handle_enroll(self):
        """Handle subject enrollment"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        student_id = data.get('student_id')
        
        try:
            student = self.db.find_by_id(student_id)
            if not student:
                self.send_json_response({'success': False, 'message': 'Student not found'})
                return
                
            if len(student.subjects) >= 4:
                self.send_json_response({'success': False, 'message': 'Cannot enroll more than four (4) subjects'})
                return
                
            # Generate random mark and grade
            mark = random.randint(25, 100)
            grade = grade_from_mark(mark)
            subject_id = new_subject_id(student)
            
            # Create and add subject
            from models.subject import Subject
            subject = Subject(subject_id, mark, grade)
            student.add_subject(subject)
            self.db.upsert(student)
            
            # Return updated student
            student_dict = {
                'id': student.id,
                'name': student.name,
                'email': student.email,
                'subjects': [{'id': s.id, 'mark': s.mark, 'grade': s.grade} for s in student.subjects]
            }
            
            self.send_json_response({
                'success': True, 
                'message': f'Enrolled subject {subject_id} with mark {mark} (grade {grade}). [{len(student.subjects)}/4]',
                'student': student_dict
            })
            
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)})
    
    def handle_remove_subject(self):
        """Handle subject removal"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        
        try:
            student = self.db.find_by_id(student_id)
            if not student:
                self.send_json_response({'success': False, 'message': 'Student not found'})
                return
                
            if student.remove_subject_by_id(subject_id):
                self.db.upsert(student)
                
                # Return updated student
                student_dict = {
                    'id': student.id,
                    'name': student.name,
                    'email': student.email,
                    'subjects': [{'id': s.id, 'mark': s.mark, 'grade': s.grade} for s in student.subjects]
                }
                
                self.send_json_response({
                    'success': True,
                    'message': f'Removed subject {subject_id}',
                    'student': student_dict
                })
            else:
                self.send_json_response({'success': False, 'message': 'Subject not found'})
                
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)})
    
    def handle_change_password(self):
        """Handle password change"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        student_id = data.get('student_id')
        password = data.get('password')
        
        try:
            student = self.db.find_by_id(student_id)
            if not student:
                self.send_json_response({'success': False, 'message': 'Student not found'})
                return
                
            if not is_valid_password(password):
                self.send_json_response({'success': False, 'message': 'Invalid password format. Must start with uppercase, have at least 5 letters, then at least 3 digits.'})
                return
                
            student.change_password(password)
            self.db.upsert(student)
            
            self.send_json_response({'success': True, 'message': 'Password changed successfully'})
            
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)})
    
    def handle_get_students(self):
        """Handle get all students"""
        try:
            students = self.db.read_all()
            students_dict = []
            for student in students:
                students_dict.append({
                    'id': student.id,
                    'name': student.name,
                    'email': student.email,
                    'subjects': [{'id': s.id, 'mark': s.mark, 'grade': s.grade} for s in student.subjects]
                })
            self.send_json_response(students_dict)
        except Exception as e:
            self.send_json_response({'error': str(e)})
    
    def handle_remove_student(self):
        """Handle student removal"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        student_id = data.get('student_id')
        
        try:
            if self.db.remove_by_id(student_id):
                self.send_json_response({'success': True, 'message': f'Removed student {student_id}'})
            else:
                self.send_json_response({'success': False, 'message': 'Student not found'})
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)})
    
    def handle_clear_database(self):
        """Handle database clear"""
        try:
            self.db.clear()
            self.send_json_response({'success': True, 'message': 'Database cleared successfully'})
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)})
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run_web_server(port=8000):
    """Run the web server"""
    with socketserver.TCPServer(("", port), UniversityWebHandler) as httpd:
        print(f"University Web GUI running at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    run_web_server()
