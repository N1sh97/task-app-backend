from sqlalchemy import Column, Integer, String
from .database import Base


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    task_status = Column(String, nullable=False)
