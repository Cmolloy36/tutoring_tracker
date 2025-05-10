import sqlalchemy as sa
from sqlalchemy.orm import Session, mapped_column, Mapped, relationship, backref

class Base(sa.orm.DeclarativeBase):
    pass

class Student(Base):
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

    def __repr__(self) -> str:
        return (
    f"Student(id={self.id!r}, name={self.name!r}, email={self.email!r}, parent={self.parent!r}, "
    f"created_at={self.created_at}, updated_at={self.updated_at}, "
    f"taking_SAT={self.taking_SAT!r}, taking_ACT={self.taking_ACT!r}, "
    f"target_SAT={self.target_SAT!r}, target_ACT={self.target_ACT!r}, "
    f"actual_SAT={self.actual_SAT!r}, actual_ACT={self.actual_ACT!r}, "
    f"active_student={self.active_student!r}, num_sessions={self.num_sessions!r})"
    )
        
class TutoringSession(Base):
    __tablename__ = 'sessions_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    updated_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    session_notes: Mapped[str] = mapped_column()
    fk_students: Mapped[int] = mapped_column(sa.ForeignKey(Student.id))
    # fk_test: Mapped[int] = mapped_column(sa.ForeignKey(Test.id))

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}, "
    f"created_at={self.created_at}, updated_at={self.updated_at}, "
    f"session_notes={self.session_notes}"
    )
        
class Test(Base):
    __tablename__ = 'tests_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    updated_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    # taken_at = sa.Column(sa.TIMESTAMP)
    test_type: Mapped[str] = mapped_column()
    is_practice_test: Mapped[bool] = sa.Column(sa.BOOLEAN,default=True,nullable=False)
    fk_students: Mapped[int] = mapped_column(sa.ForeignKey(Student.id))

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}, "
    f"test_type={self.test_type!r}, practice_test={self.is_practice_test!r}"
    )