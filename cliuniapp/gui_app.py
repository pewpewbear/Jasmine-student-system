#!/usr/bin/env python3
"""
GUI University App - Main GUI Application
Modern tkinter-based interface for the University Student System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.gui_controller import GUIController

class UniversityGUI:
    """Main GUI application for the University Student System"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("University Student System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f8f9fa')
        self.root.minsize(800, 600)
        
        # Center the window
        self.center_window()
        
        # Configure style
        self.setup_styles()
        
        # Initialize controller
        self.controller = GUIController()
        
        # Create main interface
        self.create_main_interface()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color scheme
        colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db', 
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff'
        }
        
        # Configure main styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'), 
                       background='#f8f9fa',
                       foreground=colors['primary'])
        
        style.configure('Subtitle.TLabel', 
                       font=('Segoe UI', 14), 
                       background='#f8f9fa',
                       foreground=colors['dark'])
        
        style.configure('Heading.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       background='#f8f9fa',
                       foreground=colors['primary'])
        
        style.configure('Primary.TButton', 
                       font=('Segoe UI', 11, 'bold'),
                       background=colors['secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Primary.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#21618c')])
        
        style.configure('Success.TButton', 
                       font=('Segoe UI', 11, 'bold'),
                       background=colors['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Success.TButton',
                 background=[('active', '#229954'),
                           ('pressed', '#1e8449')])
        
        style.configure('Modern.TFrame', 
                       background='#f8f9fa',
                       relief='flat')
        
        style.configure('Card.TFrame', 
                       background='white',
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Status.TLabel', 
                       font=('Segoe UI', 10),
                       background='#f8f9fa',
                       foreground=colors['success'])
        
    def create_main_interface(self):
        """Create the main interface"""
        # Main frame with modern styling
        main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="40")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Header section with gradient-like effect
        header_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="30")
        header_frame.grid(row=0, column=0, pady=(0, 30), sticky=(tk.W, tk.E))
        header_frame.columnconfigure(0, weight=1)
        
        # Title with icon-like styling
        title_label = ttk.Label(header_frame, text="🎓 University Student System", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Comprehensive Student Management Platform", style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
        # Features overview
        features_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        features_frame.grid(row=2, column=0, pady=10)
        
        features_text = "✨ Student Portal • 📊 Admin Dashboard • 🔐 Secure Authentication • 📈 Academic Tracking"
        features_label = ttk.Label(features_frame, text=features_text, 
                                  font=('Segoe UI', 10), 
                                  background='white',
                                  foreground='#6c757d')
        features_label.grid(row=0, column=0)
        
        # Main action cards
        cards_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        cards_frame.grid(row=1, column=0, pady=20, sticky=(tk.W, tk.E))
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        
        # Student Portal Card
        student_card = ttk.Frame(cards_frame, style='Card.TFrame', padding="25")
        student_card.grid(row=0, column=0, padx=(0, 15), pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        student_card.columnconfigure(0, weight=1)
        
        student_icon = ttk.Label(student_card, text="👨‍🎓", font=('Segoe UI', 32))
        student_icon.grid(row=0, column=0, pady=(0, 15))
        
        student_title = ttk.Label(student_card, text="Student Portal", 
                                font=('Segoe UI', 16, 'bold'),
                                background='white',
                                foreground='#2c3e50')
        student_title.grid(row=1, column=0, pady=(0, 10))
        
        student_desc = ttk.Label(student_card, text="Access your academic records,\nenroll in subjects, and track\nyour progress", 
                                font=('Segoe UI', 10),
                                background='white',
                                foreground='#6c757d',
                                justify='center')
        student_desc.grid(row=2, column=0, pady=(0, 20))
        
        student_btn = ttk.Button(student_card, text="Enter Student Portal", 
                                style='Primary.TButton', command=self.open_student_portal)
        student_btn.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Admin Portal Card
        admin_card = ttk.Frame(cards_frame, style='Card.TFrame', padding="25")
        admin_card.grid(row=0, column=1, padx=(15, 0), pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        admin_card.columnconfigure(0, weight=1)
        
        admin_icon = ttk.Label(admin_card, text="👨‍💼", font=('Segoe UI', 32))
        admin_icon.grid(row=0, column=0, pady=(0, 15))
        
        admin_title = ttk.Label(admin_card, text="Admin Portal", 
                               font=('Segoe UI', 16, 'bold'),
                               background='white',
                               foreground='#2c3e50')
        admin_title.grid(row=1, column=0, pady=(0, 10))
        
        admin_desc = ttk.Label(admin_card, text="Manage all students, view\nacademic reports, and\noversee system operations", 
                              font=('Segoe UI', 10),
                              background='white',
                              foreground='#6c757d',
                              justify='center')
        admin_desc.grid(row=2, column=0, pady=(0, 20))
        
        admin_btn = ttk.Button(admin_card, text="Enter Admin Portal", 
                              style='Success.TButton', command=self.open_admin_portal)
        admin_btn.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Status section
        status_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        status_frame.grid(row=2, column=0, pady=20, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        status_title = ttk.Label(status_frame, text="System Status", 
                                font=('Segoe UI', 12, 'bold'),
                                background='white',
                                foreground='#2c3e50')
        status_title.grid(row=0, column=0, pady=(0, 10))
        
        # Status indicators
        status_indicators = ttk.Frame(status_frame, style='Modern.TFrame')
        status_indicators.grid(row=1, column=0, sticky=(tk.W, tk.E))
        status_indicators.columnconfigure(0, weight=1)
        status_indicators.columnconfigure(1, weight=1)
        status_indicators.columnconfigure(2, weight=1)
        
        # Database status
        db_status = ttk.Label(status_indicators, text="💾 Database: Connected", 
                             font=('Segoe UI', 10),
                             background='white',
                             foreground='#27ae60')
        db_status.grid(row=0, column=0, sticky=tk.W)
        
        # System status
        self.status_label = ttk.Label(status_indicators, text="🟢 System: Ready", 
                                     font=('Segoe UI', 10),
                                     background='white',
                                     foreground='#27ae60')
        self.status_label.grid(row=0, column=1, sticky=tk.W)
        
        # Version info
        version_label = ttk.Label(status_indicators, text="📱 Version: 2.0", 
                                font=('Segoe UI', 10),
                                background='white',
                                foreground='#6c757d')
        version_label.grid(row=0, column=2, sticky=tk.W)
        
        # Footer
        footer_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        footer_frame.grid(row=3, column=0, pady=(20, 0))
        
        exit_btn = ttk.Button(footer_frame, text="Exit Application", 
                            command=self.root.quit,
                            style='Primary.TButton')
        exit_btn.grid(row=0, column=0)
        
    def open_student_portal(self):
        """Open the student portal window"""
        self.controller.open_student_portal(self.root)
        
    def open_admin_portal(self):
        """Open the admin portal window"""
        self.controller.open_admin_portal(self.root)
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = UniversityGUI()
    app.run()
