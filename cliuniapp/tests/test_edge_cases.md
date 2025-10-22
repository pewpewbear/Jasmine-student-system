# Edge Case Test Scripts

## Test 1: Invalid Inputs

```
# Invalid email
> r
Enter name: Test User
Enter email: x@y.com
Error: Invalid email format. Must end with @anything.uts.edu.au

# Invalid password
> r
Enter name: Test User
Enter email: test@student.uts.edu.au
Enter password: Abc12
Error: Invalid password format. Must start with uppercase, have at least 5 letters, then at least 3 digits.

# Duplicate email
> r
Enter name: Another User
Enter email: jane.doe@student.uts.edu.au
Error: Email already registered.
```

## Test 2: Login Failures

```
# Wrong password
> l
Email: jane.doe@student.uts.edu.au
Password: WrongPassword
Error: Invalid credentials.

# Non-existent email
> l
Email: nonexistent@student.uts.edu.au
Password: Abcde123
Error: Invalid credentials.
```

## Test 3: Enrollment Limits

```
# Try to enroll 5th subject
> e
Error: Cannot enrol more than four (4) subjects.

# Remove non-existent subject
> r
Enter subject id to remove: 999
Error: Subject not found.
```

## Test 4: Admin Edge Cases

```
# Remove non-existent student
> r
Enter student id to remove: 999999
Error: Student not found.

# Invalid student ID format
> r
Enter student id to remove: 123
Error: Student ID must be 6 digits.

# Clear database cancellation
> c
Are you sure? (y/N): n
Operation cancelled.
```

## Test 6: Password Change Edge Cases

```
# Password confirmation mismatch
> c
Enter new password: Newpass123
Confirm new password: Different123
Error: Passwords do not match.

# Valid password change with confirmation
> c
Enter new password: Newpass123
Confirm new password: Newpass123
Password changed.
```

## Test 5: File System Edge Cases

```
# Missing students.data file - should be created automatically
# Corrupted students.data file - should be recreated as empty
# Empty students.data file - should work normally
```
