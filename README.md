# CLI University Student System

A command-line interface (CLI) application for managing university students, their enrollments, and administrative functions.

## Features

- **Triple Interface**: Command Line (CLI), Desktop GUI (tkinter), and Web GUI (browser-based)
- **Student Management**: Register, login, and manage student accounts
- **Subject Enrollment**: Enroll in up to 4 subjects with automatic mark generation and grading
  - Shows enrollment quota (e.g., [1/4], [2/4], [3/4], [4/4])
- **Password Security**: Change password with confirmation to prevent typos
- **Administrative Functions**: View all students, group by grades, partition by pass/fail status
- **Data Persistence**: All data is stored in `io/students.data` using pickle serialization
- **Modern GUIs**: Clean, intuitive interfaces with tables, forms, and dialogs
  - **Desktop GUI**: Native tkinter application with modern styling
  - **Web GUI**: Browser-based interface with responsive design

## Requirements

- Python 3.11+
- No external dependencies (uses only standard library)

## Project Structure

```
cliuniapp/
├── app.py                  # Main application entry point
├── controllers/            # Menu controllers
│   ├── university_controller.py
│   ├── student_controller.py
│   ├── admin_controller.py
│   └── enrolment_controller.py
├── models/                 # Data models
│   ├── student.py
│   ├── subject.py
│   └── database.py
├── services/              # Business logic services
│   ├── auth_service.py
│   ├── grading_service.py
│   └── id_service.py
├── utils/                 # Utility functions
│   └── ioutils.py
├── io/                    # Data storage
│   └── students.data      # Student data file (created automatically)
└── tests/                 # Test scripts
    ├── test_happy_paths.md
    └── test_edge_cases.md
```

## How to Run

### Option 1: Launcher (Recommended)
1. Navigate to the project directory:
   ```bash
   cd /path/to/Jasmine-student-system
   ```

2. Run the launcher:
   ```bash
   python3 run_app.py
   ```

3. Choose your interface:
   - **1**: Command Line Interface (CLI)
   - **2**: Desktop GUI (tkinter)
   - **3**: Web GUI (browser-based)
   - **4**: Exit

### Option 2: Direct Interface Access

**CLI Interface:**
```bash
python3 cliuniapp/app.py
```

**Desktop GUI Interface:**
```bash
python3 cliuniapp/gui_app.py
```

**Web GUI Interface:**
```bash
python3 cliuniapp/web_gui.py
```
Then open http://localhost:8000 in your browser

## Usage

### Main Menu
- **(A) Admin**: Access administrative functions
- **(S) Student**: Student registration and login
- **(X) Exit**: Quit the application

### Student System
- **(l) login**: Login with email and password
- **(r) register**: Register a new student account
- **(x) exit**: Return to main menu

### Subject Enrollment (after login)
- **(e) enrol**: Enroll in a new subject (max 4 subjects) - shows quota [1/4, 2/4, etc.]
- **(r) remove**: Remove a subject by ID
- **(s) show**: Display enrolled subjects and grades
- **(c) change**: Change password (requires confirmation)
- **(x) exit**: Return to student menu

### Admin System
- **(s) show**: Display all students
- **(g) group students**: Group students by grade buckets
- **(p) partition students**: Separate students by pass/fail status
- **(r) remove student**: Remove a student by ID
- **(c) clear database**: Clear all data (with confirmation)
- **(x) exit**: Return to main menu

## Data Validation

### Email Format
- Must end with `@anything.uts.edu.au`
- Example: `john.doe@student.uts.edu.au`, `jane.smith@staff.uts.edu.au`

### Password Format
- Must start with an uppercase letter
- Followed by at least 4 more letters
- Ending with at least 3 digits
- Example: `Password123`, `Abcde123`

### Student ID
- 6-digit zero-padded format: `000001` to `999999`
- Automatically generated and unique

### Subject ID
- 3-digit zero-padded format: `001` to `999`
- Unique within each student's enrollment

## Grading System

Marks are randomly generated between 25-100, with grades assigned as:
- **85-100**: HD (High Distinction)
- **75-84**: D (Distinction)
- **65-74**: C (Credit)
- **50-64**: P (Pass)
- **25-49**: F (Fail)

Students pass if their average mark across all subjects is ≥ 50.

## Data Storage

- All data is persisted in `io/students.data` using Python's pickle module
- The file is created automatically if it doesn't exist
- Data is read and written atomically for each operation

## Testing

Run the test suite to verify functionality:
```bash
python3 test_app.py
```

## Known Limitations

- Simple password storage (not encrypted)
- Uses pickle for data persistence (not suitable for production)
- No concurrent access protection
- Designed for CLI use only (no GUI)

## Future Enhancements

- GUI interface
- Database backend (SQLite/PostgreSQL)
- Password encryption
- Concurrent access support
- Web interface