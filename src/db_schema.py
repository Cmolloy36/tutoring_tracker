import sqlalchemy as sa
from sqlalchemy.orm import Session, mapped_column, Mapped, relationship, backref

class Base(sa.orm.DeclarativeBase):
    pass

class Student(Base): # Change this to user, use table inheritance. Create student and tutor subclasses
    __tablename__ = 'students_table'

    tutoring_sessions = relationship(
        "TutoringSession",
        backref="student",
        cascade="all, delete-orphan",
        single_parent=True  # Ensures a session can belong to only one student
    )

    tests = relationship(
        "Test",
        backref="student",
        cascade="all, delete-orphan",
        single_parent=True  # Ensures a test can belong to only one student
    )

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    updated_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    parent: Mapped[str] = mapped_column()
    taking_SAT: Mapped[bool]
    taking_ACT: Mapped[bool]
    target_SAT: Mapped[int] = mapped_column(nullable=True,default=None)
    target_ACT: Mapped[int] = mapped_column(nullable=True,default=None)
    actual_SAT: Mapped[int] = mapped_column(nullable=True,default=None)
    actual_ACT: Mapped[int] = mapped_column(nullable=True,default=None)
    active_student: Mapped[bool] = mapped_column(default=True)
    num_sessions: Mapped[int] = mapped_column(default=0)
    # fk_tutors: Mapped[int] = mapped_column(sa.ForeignKey(Tutor.id))

    def __repr__(self) -> str:
        return (
    f"Student(id={self.id!r}, name={self.name!r}, email={self.email!r}, parent={self.parent!r}, "
    f"created_at={self.created_at}, updated_at={self.updated_at}, "
    f"taking_SAT={self.taking_SAT!r}, taking_ACT={self.taking_ACT!r}, "
    f"target_SAT={self.target_SAT!r}, target_ACT={self.target_ACT!r}, "
    f"actual_SAT={self.actual_SAT!r}, actual_ACT={self.actual_ACT!r}, "
    f"active_student={self.active_student!r}, num_sessions={self.num_sessions!r})")
        
class TutoringSession(Base):
    __tablename__ = 'sessions_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    updated_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    date_completed = sa.Column(sa.TIMESTAMP,nullable=True) # how to input the date?
    session_notes: Mapped[str] = mapped_column(nullable=True)
    fk_students: Mapped[int] = mapped_column(sa.ForeignKey(Student.id))
    # fk_tests: Mapped[int] = mapped_column(sa.ForeignKey(Test.id))

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}, "
    f"created_at={self.created_at}, updated_at={self.updated_at}, "
    f"session_notes={self.session_notes}")
        
class Test(Base):
    __tablename__ = 'tests_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    updated_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    test_type: Mapped[str] = mapped_column()
    test_name: Mapped[str] = mapped_column()
    date_completed = sa.Column(sa.TIMESTAMP)
    is_practice_test: Mapped[bool] = sa.Column(sa.BOOLEAN,default=True,nullable=False)
    fk_students: Mapped[int] = mapped_column(sa.ForeignKey(Student.id))

    __mapper_args__ = {
        "polymorphic_identity": "test",
        "polymorphic_on": "test_type",
    }

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}, date_completed={self.date_completed}, "
    f"test_type={self.test_type!r}, practice_test={self.is_practice_test!r}")

class SAT(Test):
    __tablename__ = 'SAT_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.ForeignKey(Test.id), primary_key=True)
    english_score: Mapped[int] = mapped_column()
    math_score: Mapped[int] = mapped_column()

    __mapper_args__ = {
        "polymorphic_identity": "SAT",
    }

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}, date_completed={self.date_completed}, "
    f"test_type={self.test_type!r}, practice_test={self.is_practice_test!r}, "
    f"english_score={self.english_score!r}, math_score={self.math_score!r}, ")

class PSAT(Test):
    __tablename__ = 'PSAT_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.ForeignKey(Test.id), primary_key=True)
    english_score: Mapped[int] = mapped_column()
    math_score: Mapped[int] = mapped_column()

    __mapper_args__ = {
        "polymorphic_identity": "PSAT",
    }

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}, date_completed={self.date_completed}, "
    f"test_type={self.test_type!r}, practice_test={self.is_practice_test!r}, "
    f"english_score={self.english_score!r}, math_score={self.math_score!r}")

class ACT(Test):
    __tablename__ = 'ACT_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.ForeignKey(Test.id), primary_key=True)
    english_score: Mapped[int] = mapped_column()
    math_score: Mapped[int] = mapped_column()
    reading_score: Mapped[int] = mapped_column()
    science_score: Mapped[int] = mapped_column()

    __mapper_args__ = {
        "polymorphic_identity": "ACT",
    }

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}, date_completed={self.date_completed}, "
    f"test_type={self.test_type!r}, practice_test={self.is_practice_test!r}, "
    f"english_score={self.english_score!r}, math_score={self.math_score!r}, "
    f"reading_score={self.reading_score!r}, science_score={self.science_score!r}, ")