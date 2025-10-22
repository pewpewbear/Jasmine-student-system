"""
GUI Controller - Handles GUI interactions and business logic
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.database import Database
from models.student import Student
from services.auth_service import is_valid_email, is_valid_password, authenticate
from services.id_service import new_student_id, new_subject_id
from services.grading_service import grade_from_mark
import random

class GUIController:
    """Main GUI controller for handling user interactions"""
    
    def __init__(self):
        self.db = Database()
        self.current_student = None
        
    def open_student_portal(self, parent):
        """Open student portal window"""
        StudentPortalWindow(parent, self)
        
    def open_admin_portal(self, parent):
        """Open admin portal window"""
        AdminPortalWindow(parent, self)

class StudentPortalWindow:
    """Student portal window for login/registration"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Student Portal")
        self.window.geometry("600x700")
        self.window.configure(bg='#f8f9fa')
        self.window.minsize(500, 600)
        
        # Center the window
        self.center_window()
        
        # Configure styles
        self.setup_styles()
        
        self.create_interface()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configure styles for the student portal"""
        style = ttk.Style()
        
        # Configure form styles
        style.configure('PortalTitle.TLabel', 
                       font=('Segoe UI', 20, 'bold'), 
                       background='#f8f9fa',
                       foreground='#2c3e50')
        
        style.configure('FormLabel.TLabel', 
                       font=('Segoe UI', 11, 'bold'), 
                       background='#f8f9fa',
                       foreground='#2c3e50')
        
        style.configure('FormEntry.TEntry', 
                       font=('Segoe UI', 11),
                       padding=(10, 8))
        
        style.configure('PortalButton.TButton', 
                       font=('Segoe UI', 11, 'bold'),
                       background='#3498db',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 10))
        
        style.map('PortalButton.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#21618c')])
        
        style.configure('SuccessButton.TButton', 
                       font=('Segoe UI', 11, 'bold'),
                       background='#27ae60',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 10))
        
        style.map('SuccessButton.TButton',
                 background=[('active', '#229954'),
                           ('pressed', '#1e8449')])
        
        style.configure('Card.TFrame', 
                       background='white',
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Modern.TFrame', 
                       background='#f8f9fa',
                       relief='flat')
        
    def create_interface(self):
        """Create the student portal interface"""
        main_frame = ttk.Frame(self.window, style='Modern.TFrame', padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="25")
        header_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        header_frame.columnconfigure(0, weight=1)
        
        # Title with icon
        title_label = ttk.Label(header_frame, text="👨‍🎓 Student Portal", 
                               style='PortalTitle.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Access your academic dashboard", 
                                  font=('Segoe UI', 12),
                                  background='white',
                                  foreground='#6c757d')
        subtitle_label.grid(row=1, column=0)
        
        # Login frame
        login_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="25")
        login_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        login_frame.columnconfigure(1, weight=1)
        
        # Login title
        login_title = ttk.Label(login_frame, text="🔐 Login to Your Account", 
                               font=('Segoe UI', 14, 'bold'),
                               background='white',
                               foreground='#2c3e50')
        login_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Email
        email_label = ttk.Label(login_frame, text="📧 Email Address:", style='FormLabel.TLabel')
        email_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(login_frame, textvariable=self.email_var, 
                               style='FormEntry.TEntry', width=35)
        email_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Password
        password_label = ttk.Label(login_frame, text="🔒 Password:", style='FormLabel.TLabel')
        password_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, 
                                 show="*", style='FormEntry.TEntry', width=35)
        password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Login button
        login_btn = ttk.Button(login_frame, text="🚀 Login", 
                              style='PortalButton.TButton', command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Divider
        divider_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        divider_frame.grid(row=2, column=0, pady=20, sticky=(tk.W, tk.E))
        divider_frame.columnconfigure(0, weight=1)
        
        # Divider line with text
        divider_line = ttk.Frame(divider_frame, height=1, style='Modern.TFrame')
        divider_line.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        divider_text = ttk.Label(divider_frame, text="OR", 
                                font=('Segoe UI', 10, 'bold'),
                                background='#f8f9fa',
                                foreground='#6c757d')
        divider_text.grid(row=0, column=0)
        
        # Registration frame
        reg_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="25")
        reg_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))
        reg_frame.columnconfigure(1, weight=1)
        
        # Registration title
        reg_title = ttk.Label(reg_frame, text="📝 New Student Registration", 
                              font=('Segoe UI', 14, 'bold'),
                              background='white',
                              foreground='#2c3e50')
        reg_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Name
        name_label = ttk.Label(reg_frame, text="👤 Full Name:", style='FormLabel.TLabel')
        name_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.reg_name_var = tk.StringVar()
        name_entry = ttk.Entry(reg_frame, textvariable=self.reg_name_var, 
                              style='FormEntry.TEntry', width=35)
        name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Email
        email_label = ttk.Label(reg_frame, text="📧 Email Address:", style='FormLabel.TLabel')
        email_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.reg_email_var = tk.StringVar()
        reg_email_entry = ttk.Entry(reg_frame, textvariable=self.reg_email_var, 
                                   style='FormEntry.TEntry', width=35)
        reg_email_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Password
        password_label = ttk.Label(reg_frame, text="🔒 Password:", style='FormLabel.TLabel')
        password_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.reg_password_var = tk.StringVar()
        reg_password_entry = ttk.Entry(reg_frame, textvariable=self.reg_password_var, 
                                     show="*", style='FormEntry.TEntry', width=35)
        reg_password_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Password requirements
        req_label = ttk.Label(reg_frame, text="Password must start with uppercase, have at least 5 letters, then at least 3 digits", 
                             font=('Segoe UI', 9),
                             background='white',
                             foreground='#6c757d',
                             wraplength=400)
        req_label.grid(row=4, column=0, columnspan=2, pady=(0, 15))
        
        # Register button
        register_btn = ttk.Button(reg_frame, text="✨ Create Account", 
                                 style='SuccessButton.TButton', command=self.register)
        register_btn.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Close button
        close_btn = ttk.Button(main_frame, text="❌ Close", 
                              style='PortalButton.TButton', command=self.window.destroy)
        close_btn.grid(row=4, column=0, pady=20)
        
    def login(self):
        """Handle login"""
        email = self.email_var.get().strip()
        password = self.password_var.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
            
        student = authenticate(email, password, self.controller.db)
        if student:
            self.controller.current_student = student
            messagebox.showinfo("Success", f"Welcome back, {student.name}!")
            self.window.destroy()
            StudentDashboardWindow(self.parent, self.controller)
        else:
            messagebox.showerror("Error", "Invalid credentials")
            
    def register(self):
        """Handle registration"""
        name = self.reg_name_var.get().strip()
        email = self.reg_email_var.get().strip()
        password = self.reg_password_var.get()
        
        if not name or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format. Must end with @anything.uts.edu.au")
            return
            
        if not is_valid_password(password):
            messagebox.showerror("Error", "Invalid password format. Must start with uppercase, have at least 5 letters, then at least 3 digits.")
            return
            
        if self.controller.db.find_by_email(email):
            messagebox.showerror("Error", "Email already registered")
            return
            
        # Create new student
        student_id = new_student_id(self.controller.db)
        student = Student(student_id, name, email, password)
        self.controller.db.upsert(student)
        
        messagebox.showinfo("Success", f"Registration successful! Your student ID is {student_id}")
        
        # Clear form
        self.reg_name_var.set("")
        self.reg_email_var.set("")
        self.reg_password_var.set("")

class StudentDashboardWindow:
    """Student dashboard for subject management"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title(f"Student Dashboard - {controller.current_student.name}")
        self.window.geometry("1000x750")
        self.window.configure(bg='#f8f9fa')
        self.window.minsize(900, 650)
        
        # Center the window
        self.center_window()
        
        # Configure styles
        self.setup_styles()
        
        self.create_interface()
        self.refresh_subjects()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configure styles for the dashboard"""
        style = ttk.Style()
        
        # Dashboard styles
        style.configure('DashboardTitle.TLabel', 
                       font=('Segoe UI', 18, 'bold'), 
                       background='#f8f9fa',
                       foreground='#2c3e50')
        
        style.configure('CardTitle.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       background='white',
                       foreground='#2c3e50')
        
        style.configure('StatLabel.TLabel', 
                       font=('Segoe UI', 10, 'bold'), 
                       background='white',
                       foreground='#6c757d')
        
        style.configure('StatValue.TLabel', 
                       font=('Segoe UI', 16, 'bold'), 
                       background='white',
                       foreground='#2c3e50')
        
        style.configure('DashboardButton.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       background='#3498db',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))
        
        style.map('DashboardButton.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#21618c')])
        
        style.configure('SuccessButton.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       background='#27ae60',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))
        
        style.map('SuccessButton.TButton',
                 background=[('active', '#229954'),
                           ('pressed', '#1e8449')])
        
        style.configure('WarningButton.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       background='#f39c12',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(12, 8))
        
        style.map('WarningButton.TButton',
                 background=[('active', '#e67e22'),
                           ('pressed', '#d35400')])
        
        style.configure('Card.TFrame', 
                       background='white',
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Modern.TFrame', 
                       background='#f8f9fa',
                       relief='flat')
        
    def create_interface(self):
        """Create the student dashboard interface"""
        main_frame = ttk.Frame(self.window, style='Modern.TFrame', padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Header section
        header_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="25")
        header_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        header_frame.columnconfigure(1, weight=1)
        
        # Welcome message
        welcome_label = ttk.Label(header_frame, text=f"👋 Welcome back, {self.controller.current_student.name}!", 
                                style='DashboardTitle.TLabel')
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Student info in a modern layout
        info_left = ttk.Frame(header_frame, style='Modern.TFrame')
        info_left.grid(row=1, column=0, sticky=tk.W)
        
        student_id_label = ttk.Label(info_left, text="🆔 Student ID:", style='StatLabel.TLabel')
        student_id_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        student_id_value = ttk.Label(info_left, text=self.controller.current_student.id, 
                                   style='StatValue.TLabel')
        student_id_value.grid(row=0, column=1, sticky=tk.W)
        
        email_label = ttk.Label(info_left, text="📧 Email:", style='StatLabel.TLabel')
        email_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        email_value = ttk.Label(info_left, text=self.controller.current_student.email, 
                               style='StatValue.TLabel')
        email_value.grid(row=1, column=1, sticky=tk.W)
        
        # Quick stats on the right
        stats_right = ttk.Frame(header_frame, style='Modern.TFrame')
        stats_right.grid(row=1, column=1, sticky=tk.E)
        
        # Calculate quick stats
        subject_count = len(self.controller.current_student.subjects)
        avg_mark = self.controller.current_student.avg_mark()
        status = "PASS" if self.controller.current_student.is_pass() else "FAIL"
        
        stats_text = f"📊 Subjects: {subject_count}/4\n📈 Average: {avg_mark}\n🎯 Status: {status}"
        stats_label = ttk.Label(stats_right, text=stats_text, 
                               font=('Segoe UI', 11, 'bold'),
                               background='white',
                               foreground='#2c3e50',
                               justify='right')
        stats_label.grid(row=0, column=0, sticky=tk.E)
        
        # Subjects section
        subjects_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        subjects_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        subjects_frame.columnconfigure(0, weight=1)
        subjects_frame.rowconfigure(1, weight=1)
        
        # Subjects title
        subjects_title = ttk.Label(subjects_frame, text="📚 Subject Enrollment", style='CardTitle.TLabel')
        subjects_title.grid(row=0, column=0, pady=(0, 15), sticky=tk.W)
        
        # Subject treeview with modern styling
        tree_frame = ttk.Frame(subjects_frame, style='Modern.TFrame')
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        columns = ('Subject ID', 'Mark', 'Grade', 'Status')
        self.subject_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.subject_tree.heading('Subject ID', text='📋 Subject ID')
        self.subject_tree.heading('Mark', text='📊 Mark')
        self.subject_tree.heading('Grade', text='🎯 Grade')
        self.subject_tree.heading('Status', text='📈 Status')
        
        self.subject_tree.column('Subject ID', width=120, anchor='center')
        self.subject_tree.column('Mark', width=80, anchor='center')
        self.subject_tree.column('Grade', width=80, anchor='center')
        self.subject_tree.column('Status', width=100, anchor='center')
        
        self.subject_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.subject_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.subject_tree.configure(yscrollcommand=scrollbar.set)
        
        # Action buttons with modern styling
        buttons_frame = ttk.Frame(subjects_frame, style='Modern.TFrame')
        buttons_frame.grid(row=2, column=0, pady=(15, 0))
        
        enroll_btn = ttk.Button(buttons_frame, text="➕ Enroll Subject", 
                               style='SuccessButton.TButton', command=self.enroll_subject)
        enroll_btn.grid(row=0, column=0, padx=(0, 10))
        
        remove_btn = ttk.Button(buttons_frame, text="➖ Remove Subject", 
                               style='WarningButton.TButton', command=self.remove_subject)
        remove_btn.grid(row=0, column=1, padx=(0, 10))
        
        password_btn = ttk.Button(buttons_frame, text="🔐 Change Password", 
                                 style='DashboardButton.TButton', command=self.change_password)
        password_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Academic status section
        status_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        status_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(2, weight=1)
        
        # Status title
        status_title = ttk.Label(status_frame, text="📊 Academic Status", style='CardTitle.TLabel')
        status_title.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky=tk.W)
        
        # Status cards
        # Average mark card
        avg_card = ttk.Frame(status_frame, style='Card.TFrame', padding="15")
        avg_card.grid(row=1, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        avg_card.columnconfigure(0, weight=1)
        
        avg_label = ttk.Label(avg_card, text="📈 Average Mark", style='StatLabel.TLabel')
        avg_label.grid(row=0, column=0, pady=(0, 5))
        self.avg_label = ttk.Label(avg_card, text="--", style='StatValue.TLabel')
        self.avg_label.grid(row=1, column=0)
        
        # Status card
        status_card = ttk.Frame(status_frame, style='Card.TFrame', padding="15")
        status_card.grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        status_card.columnconfigure(0, weight=1)
        
        status_label = ttk.Label(status_card, text="🎯 Academic Status", style='StatLabel.TLabel')
        status_label.grid(row=0, column=0, pady=(0, 5))
        self.status_label = ttk.Label(status_card, text="--", style='StatValue.TLabel')
        self.status_label.grid(row=1, column=0)
        
        # Enrollment card
        quota_card = ttk.Frame(status_frame, style='Card.TFrame', padding="15")
        quota_card.grid(row=1, column=2, padx=(10, 0), sticky=(tk.W, tk.E))
        quota_card.columnconfigure(0, weight=1)
        
        quota_label = ttk.Label(quota_card, text="📚 Enrollment", style='StatLabel.TLabel')
        quota_label.grid(row=0, column=0, pady=(0, 5))
        self.quota_label = ttk.Label(quota_card, text="0/4", style='StatValue.TLabel')
        self.quota_label.grid(row=1, column=0)
        
        # Footer with logout button
        footer_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        footer_frame.grid(row=3, column=0, pady=(20, 0))
        
        logout_btn = ttk.Button(footer_frame, text="🚪 Logout", 
                                style='DashboardButton.TButton', command=self.window.destroy)
        logout_btn.grid(row=0, column=0)
        
    def refresh_subjects(self):
        """Refresh the subjects display"""
        # Clear existing items
        for item in self.subject_tree.get_children():
            self.subject_tree.delete(item)
            
        # Add subjects with status indicators
        for subject in self.controller.current_student.subjects:
            # Determine status based on grade
            if subject.grade in ['HD', 'D', 'C', 'P']:
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
                
            self.subject_tree.insert('', 'end', values=(
                subject.id, 
                subject.mark, 
                subject.grade, 
                status
            ))
            
        # Update status cards
        avg_mark = self.controller.current_student.avg_mark()
        status = "PASS" if self.controller.current_student.is_pass() else "FAIL"
        quota = len(self.controller.current_student.subjects)
        
        # Update with modern styling
        self.avg_label.config(text=f"{avg_mark}")
        self.status_label.config(text=f"{status}")
        self.quota_label.config(text=f"{quota}/4")
        
    def enroll_subject(self):
        """Enroll in a new subject"""
        if len(self.controller.current_student.subjects) >= 4:
            messagebox.showerror("Error", "Cannot enroll more than four (4) subjects")
            return
            
        # Generate random mark and grade
        mark = random.randint(25, 100)
        grade = grade_from_mark(mark)
        subject_id = new_subject_id(self.controller.current_student)
        
        # Create and add subject
        from models.subject import Subject
        subject = Subject(subject_id, mark, grade)
        self.controller.current_student.add_subject(subject)
        self.controller.db.upsert(self.controller.current_student)
        
        messagebox.showinfo("Success", f"Enrolled subject {subject_id} with mark {mark} (grade {grade}). [{len(self.controller.current_student.subjects)}/4]")
        self.refresh_subjects()
        
    def remove_subject(self):
        """Remove a subject"""
        selection = self.subject_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a subject to remove")
            return
            
        item = self.subject_tree.item(selection[0])
        subject_id = str(item['values'][0])  # Ensure it's a string
        
        # Check if subject exists before attempting removal
        subject_exists = any(s.id == subject_id for s in self.controller.current_student.subjects)
        if not subject_exists:
            messagebox.showerror("Error", f"Subject {subject_id} not found in student's subjects")
            return
        
        if self.controller.current_student.remove_subject_by_id(subject_id):
            self.controller.db.upsert(self.controller.current_student)
            messagebox.showinfo("Success", f"Removed subject {subject_id}")
            self.refresh_subjects()
        else:
            messagebox.showerror("Error", f"Failed to remove subject {subject_id}")
            
    def change_password(self):
        """Change password dialog"""
        dialog = PasswordChangeDialog(self.window, self.controller)
        self.window.wait_window(dialog.dialog)

class PasswordChangeDialog:
    """Password change dialog"""
    
    def __init__(self, parent, controller):
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Change Password")
        self.dialog.geometry("400x200")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_interface()
        
    def create_interface(self):
        """Create password change interface"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Change Password", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=(0, 20))
        
        # New password
        ttk.Label(main_frame, text="New Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.new_password_var = tk.StringVar()
        new_password_entry = ttk.Entry(main_frame, textvariable=self.new_password_var, show="*", width=30)
        new_password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Confirm password
        ttk.Label(main_frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.confirm_password_var = tk.StringVar()
        confirm_password_entry = ttk.Entry(main_frame, textvariable=self.confirm_password_var, show="*", width=30)
        confirm_password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Change", command=self.change_password).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).grid(row=0, column=1, padx=5)
        
    def change_password(self):
        """Handle password change"""
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        if not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill in both fields")
            return
            
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if not is_valid_password(new_password):
            messagebox.showerror("Error", "Invalid password format. Must start with uppercase, have at least 5 letters, then at least 3 digits.")
            return
            
        self.controller.current_student.change_password(new_password)
        self.controller.db.upsert(self.controller.current_student)
        messagebox.showinfo("Success", "Password changed successfully")
        self.dialog.destroy()

class AdminPortalWindow:
    """Admin portal window"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.window = tk.Toplevel(parent)
        self.window.title("Admin Portal")
        self.window.geometry("1200x800")
        self.window.configure(bg='#f8f9fa')
        self.window.minsize(1000, 700)
        
        # Center the window
        self.center_window()
        
        # Configure styles
        self.setup_styles()
        
        self.create_interface()
        self.refresh_students()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configure styles for the admin portal"""
        style = ttk.Style()
        
        # Admin portal styles
        style.configure('AdminTitle.TLabel', 
                       font=('Segoe UI', 20, 'bold'), 
                       background='#f8f9fa',
                       foreground='#2c3e50')
        
        style.configure('AdminCardTitle.TLabel', 
                       font=('Segoe UI', 14, 'bold'), 
                       background='white',
                       foreground='#2c3e50')
        
        style.configure('AdminButton.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       background='#3498db',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        style.map('AdminButton.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#21618c')])
        
        style.configure('DangerButton.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       background='#e74c3c',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        style.map('DangerButton.TButton',
                 background=[('active', '#c0392b'),
                           ('pressed', '#a93226')])
        
        style.configure('SuccessButton.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       background='#27ae60',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        style.map('SuccessButton.TButton',
                 background=[('active', '#229954'),
                           ('pressed', '#1e8449')])
        
        style.configure('WarningButton.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       background='#f39c12',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        style.map('WarningButton.TButton',
                 background=[('active', '#e67e22'),
                           ('pressed', '#d35400')])
        
        style.configure('Card.TFrame', 
                       background='white',
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Modern.TFrame', 
                       background='#f8f9fa',
                       relief='flat')
        
    def create_interface(self):
        """Create admin interface"""
        main_frame = ttk.Frame(self.window, style='Modern.TFrame', padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Header section
        header_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="25")
        header_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        header_frame.columnconfigure(0, weight=1)
        
        # Title with icon
        title_label = ttk.Label(header_frame, text="👨‍💼 Admin Portal", style='AdminTitle.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Comprehensive Student Management Dashboard", 
                                  font=('Segoe UI', 12),
                                  background='white',
                                  foreground='#6c757d')
        subtitle_label.grid(row=1, column=0)
        
        # Students management section
        students_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        students_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        students_frame.columnconfigure(0, weight=1)
        students_frame.rowconfigure(1, weight=1)
        
        # Students title
        students_title = ttk.Label(students_frame, text="👥 All Students", style='AdminCardTitle.TLabel')
        students_title.grid(row=0, column=0, pady=(0, 15), sticky=tk.W)
        
        # Students treeview with modern styling
        tree_frame = ttk.Frame(students_frame, style='Modern.TFrame')
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        columns = ('Student ID', 'Name', 'Email', 'Avg Mark', 'Status', 'Subjects')
        self.students_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Configure columns with icons
        self.students_tree.heading('Student ID', text='🆔 Student ID')
        self.students_tree.heading('Name', text='👤 Name')
        self.students_tree.heading('Email', text='📧 Email')
        self.students_tree.heading('Avg Mark', text='📊 Avg Mark')
        self.students_tree.heading('Status', text='🎯 Status')
        self.students_tree.heading('Subjects', text='📚 Subjects')
        
        self.students_tree.column('Student ID', width=100, anchor='center')
        self.students_tree.column('Name', width=150, anchor='w')
        self.students_tree.column('Email', width=200, anchor='w')
        self.students_tree.column('Avg Mark', width=100, anchor='center')
        self.students_tree.column('Status', width=100, anchor='center')
        self.students_tree.column('Subjects', width=100, anchor='center')
        
        self.students_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.students_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        # Action buttons with modern styling
        buttons_frame = ttk.Frame(students_frame, style='Modern.TFrame')
        buttons_frame.grid(row=2, column=0, pady=(15, 0))
        
        refresh_btn = ttk.Button(buttons_frame, text="🔄 Refresh", 
                                style='AdminButton.TButton', command=self.refresh_students)
        refresh_btn.grid(row=0, column=0, padx=(0, 10))
        
        grade_btn = ttk.Button(buttons_frame, text="📊 Group by Grade", 
                              style='SuccessButton.TButton', command=self.group_by_grade)
        grade_btn.grid(row=0, column=1, padx=(0, 10))
        
        partition_btn = ttk.Button(buttons_frame, text="📈 Partition Pass/Fail", 
                                 style='WarningButton.TButton', command=self.partition_pass_fail)
        partition_btn.grid(row=0, column=2, padx=(0, 10))
        
        remove_btn = ttk.Button(buttons_frame, text="🗑️ Remove Student", 
                               style='DangerButton.TButton', command=self.remove_student)
        remove_btn.grid(row=0, column=3, padx=(0, 10))
        
        clear_btn = ttk.Button(buttons_frame, text="⚠️ Clear Database", 
                              style='DangerButton.TButton', command=self.clear_database)
        clear_btn.grid(row=0, column=4, padx=(0, 10))
        
        # Footer
        footer_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        footer_frame.grid(row=2, column=0, pady=(20, 0))
        
        close_btn = ttk.Button(footer_frame, text="🚪 Close", 
                              style='AdminButton.TButton', command=self.window.destroy)
        close_btn.grid(row=0, column=0)
        
    def refresh_students(self):
        """Refresh students display"""
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
            
        # Add students with status indicators
        students = self.controller.db.read_all()
        for student in students:
            avg_mark = student.avg_mark()
            status = "✅ PASS" if student.is_pass() else "❌ FAIL"
            subject_count = len(student.subjects)
            
            self.students_tree.insert('', 'end', values=(
                student.id, 
                student.name, 
                student.email, 
                f"{avg_mark:.1f}" if avg_mark != 0 else "--", 
                status, 
                f"{subject_count}/4"
            ))
            
    def group_by_grade(self):
        """Group students by grade"""
        students = self.controller.db.read_all()
        grade_counts = {"HD": 0, "D": 0, "C": 0, "P": 0, "F": 0}
        
        for student in students:
            if not student.subjects:
                continue
                
            # Use highest grade among all subjects
            highest_grade = "F"
            for subject in student.subjects:
                if subject.grade == "HD":
                    highest_grade = "HD"
                elif subject.grade == "D" and highest_grade not in ["HD"]:
                    highest_grade = "D"
                elif subject.grade == "C" and highest_grade not in ["HD", "D"]:
                    highest_grade = "C"
                elif subject.grade == "P" and highest_grade not in ["HD", "D", "C"]:
                    highest_grade = "P"
                    
            grade_counts[highest_grade] += 1
            
        message = f"Grade Distribution:\nHD: {grade_counts['HD']}\nD: {grade_counts['D']}\nC: {grade_counts['C']}\nP: {grade_counts['P']}\nF: {grade_counts['F']}"
        messagebox.showinfo("Grade Distribution", message)
        
    def partition_pass_fail(self):
        """Partition students by pass/fail"""
        students = self.controller.db.read_all()
        pass_students = [s for s in students if s.is_pass()]
        fail_students = [s for s in students if not s.is_pass()]
        
        message = f"Pass/Fail Partition:\n\nPASS: {len(pass_students)} students\n"
        for student in pass_students:
            message += f"  {student.id} {student.name} (avg {student.avg_mark()})\n"
            
        message += f"\nFAIL: {len(fail_students)} students\n"
        for student in fail_students:
            message += f"  {student.id} {student.name} (avg {student.avg_mark()})\n"
            
        messagebox.showinfo("Pass/Fail Partition", message)
        
    def remove_student(self):
        """Remove a student"""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a student to remove")
            return
            
        item = self.students_tree.item(selection[0])
        student_id = str(item['values'][0])  # Ensure it's a string
        student_name = item['values'][1]
        
        # Check if student exists before attempting removal
        all_students = self.controller.db.read_all()
        student_exists = any(s.id == student_id for s in all_students)
        if not student_exists:
            messagebox.showerror("Error", f"Student {student_id} not found in database")
            return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove student {student_name} ({student_id})?"):
            if self.controller.db.remove_by_id(student_id):
                messagebox.showinfo("Success", f"Removed student {student_id}")
                self.refresh_students()
            else:
                messagebox.showerror("Error", f"Failed to remove student {student_id}")
                
    def clear_database(self):
        """Clear the database"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the entire database? This action cannot be undone."):
            self.controller.db.clear()
            messagebox.showinfo("Success", "Database cleared")
            self.refresh_students()
