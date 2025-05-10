import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.db_schema import Student, Test, TutoringSession

def get_student_ids(session: Session, args):
    if args.names == None:
        return []
    else:
        student_names = args.names
        student_ids = session.scalars(sa.select(Student.id).where(Student.name.in_(student_names))).all()

    return student_ids