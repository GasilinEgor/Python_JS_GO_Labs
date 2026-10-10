Схема базы данных


Roles
role_id: int -> PK
role_name: str

User
user_id: int -> PK
role_id: int -> FK
password: password

Tokens
token_id: int -> PK
user_id: int -> FK
token: str
expires_at: datetime

UniversitySubjects
subject_id: int -> PK
subjct_name: str

StudentSchedule
shedule_id: int -> PK
student_id: int -> FK
subject_id: int -> FK
date: date
pair_count: int

Marks
marks_id: int -> PK
shedule_id: int -> FK
mark: int