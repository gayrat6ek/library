from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table,Time,JSON,VARCHAR,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID,ARRAY,JSONB
from datetime import datetime
import pytz 
import uuid
timezonetash = pytz.timezone("Asia/Tashkent")
Base = declarative_base()



class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    password = Column(String,)
    username = Column(VARCHAR(100))
    full_name = Column(VARCHAR(255),nullable=True)
    user_book = relationship('Books',back_populates='book_user')

class Books(Base):
    __tablename__= 'books'
    id = Column(Integer,primary_key=True,index=True)
    inventory_number = Column(String,nullable=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    book_user = relationship('Users',back_populates='user_book')
    title = Column(String)
    title_mono = Column(String,nullable=True)   
    title_known = Column(String,nullable=True)
    author = Column(String)
    author_mono = Column(String,nullable=True)
    commentator = Column(String,nullable=True)
    commentator_mono = Column(String,nullable=True)
    translator  = Column(String,nullable=True)
    translator_mono = Column(String,nullable=True)
    compiler = Column(String,nullable=True)
    compiler_mono = Column(String,nullable=True)
    date_written = Column(Date,nullable=True)
    language = Column(VARCHAR(100),nullable=True)
    subjects = Column(String,nullable=True)
    quantity_sheet = Column(VARCHAR(150),nullable=True)
    quantity_ill = Column(VARCHAR(150),nullable=True)
    lines = Column(Integer,nullable=True)
    columns = Column(Integer,nullable=True)
    size = Column(VARCHAR(100),nullable=True)
    paper = Column(VARCHAR(100),nullable=True)
    copyist = Column(VARCHAR(255),nullable=True)
    copy_date = Column(Date,nullable=True)
    copy_place = Column(String,nullable=True)
    type_handwriting = Column(VARCHAR(200),nullable=True)
    cover = Column(VARCHAR(100),nullable=True)
    cover_color = Column(VARCHAR(200),nullable=True)
    stamp = Column(VARCHAR(255),nullable=True)
    text_begin = Column(String,nullable=True)
    text_exbegin = Column(String,nullable=True)
    text_ammabegin = Column(String,nullable=True)
    text_end = Column(String,nullable=True)
    text_exend = Column(String,nullable=True)
    colophon = Column(String,nullable=True)
    defects = Column(String,nullable=True)
    fixation = Column(String,nullable=True)
    note = Column(String,nullable=True)
    descript_auth = Column(String,nullable=True)
    file = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    images = Column(ARRAY(String),nullable=True)






