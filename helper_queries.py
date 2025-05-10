import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.db_schema import Student, Test, TutoringSession

def get_student_ids(session: Session, args): # will need to change this to user IDs once I revamp DB
    if args.name == None:
        return []
    else:
        student_names = args.name
        student_ids = session.scalars(sa.select(Student.id).where(Student.name.in_(student_names))).all()

    return student_ids