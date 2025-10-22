# Happy Path Test Scripts

## Test 1: Register → Login → Enrol 4 → Show → Remove → Change PW

```
(A) Admin
(S) Student
(X) Exit
> S

(l) login
(r) register
(x) exit
> r
Enter name: Jane Doe
Enter email: jane.doe@student.uts.edu.au
Enter password: Abcde123
Registered successfully. Your student id is 000123.

(l) login
(r) register
(x) exit
> l
Email: jane.doe@student.uts.edu.au
Password: Abcde123
Login successful.

(c) change
(e) enrol
(r) remove
(s) show
(x) exit
> e
Enrolled subject 001 with mark 77 (grade D). [1/4]

> e
Enrolled subject 002 with mark 63 (grade P). [2/4]

> e
Enrolled subject 003 with mark 85 (grade HD). [3/4]

> e
Enrolled subject 004 with mark 52 (grade P). [4/4]

> s
Subjects:
  001  mark=77  grade=D
  002  mark=63  grade=P
  003  mark=85  grade=HD
  004  mark=52  grade=P
Average: 69  Status: PASS

> r
Enter subject id to remove: 003
Removed subject 003.

> c
Enter new password: Xyzab999
Confirm new password: Xyzab999
Password changed.

> x
Returning to Student menu...
```

## Test 2: Admin Functions

```
(A) Admin
(S) Student
(X) Exit
> A

(c) clear database
(g) group students
(p) partition students
(r) remove student
(s) show
(x) exit
> s
# ... lists all students in file

> p
PASS:
  000123 Jane Doe (avg 64)
FAIL:
  # any failing students

> g
HD: 1  D: 2  C: 0  P: 1  F: 0

> r
Enter student id to remove: 000123
Removed student 000123.

> c
Are you sure? (y/N): y
All students removed.

> x
Returning to University menu...
```
