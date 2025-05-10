from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    coverage_start_date = Column(Date, nullable=False)
    coverage_end_date = Column(Date, nullable=False)
    entity_type = Column(String)
    
    # Relationships
    job_forms = relationship("JobForm", back_populates="job", cascade="all, delete-orphan")

class JobForm(Base):
    __tablename__ = "job_forms"
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    form_number = Column(String)
    entity_type = Column(String)
    locality_type = Column(String)
    locality = Column(String)
    due_date = Column(Date)
    extension_due_date = Column(Date)
    
    # Relationships
    job = relationship("Job", back_populates="job_forms")