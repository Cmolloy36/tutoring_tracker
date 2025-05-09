import sqlalchemy as sa
from sqlalchemy.orm import Session
from src.db_schema import Base, Student, TutoringSession

def get_students(session: Session, args):
    limit = args.limit
    if args.files == None:
        students = session.query(Student).limit(limit) # support "order by" functionality from CLI?
    else:
        student_names = args.files
        students = session.execute(sa.select(Student).where(Student.name.in_(student_names)))

    for s in students:
        print(s)
    return students

def get_tutoring_sessions(session: Session, args):
    limit = args.limit
    if args.files == None:
        students = session.query(TutoringSession).limit(limit)
    else:
        student_names = args.files
        student_fks = session.execute(sa.select(Student.id).where(Student.name.in_(student_names)))
        sessions = session.execute(sa.select(TutoringSession).where(TutoringSession.student_fk.in_(student_fks)))

    for s in sessions:
        print(s)
    return sessions