from sqlalchemy.orm import Session
import models
import schemas
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime 
from sqlalchemy import or_,and_,Date,cast
import schemas
import utils


def create_user(db:Session,form_data:schemas.UserCreate):
    query = models.Users(full_name=form_data.fullname,username = form_data.username,password =utils.hash_password(password=form_data.password))
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_user(db:Session,form_data:schemas.UserUpdate):
    query = db.query(models.Users).filter(models.Users.id==form_data.id).first()
    if query:
        if form_data.password is not None:
            query.password = utils.hash_password(password=form_data.password)
        if form_data.username is not None:
            query.username = form_data.username
        if form_data.full_name is not None:
            query.full_name = form_data.full_name
        db.commit()
        db.refresh(query)
    return query

def filterquery_user(db:Session,id,username):
    query = db.query(models.Users)
    if id is not None:
        query = query.filter(models.Users.id==id)
    if username is not None:
        query = query.filter(models.Users.username.ilike(f"%{username}%"))
    return query.all()


def get_user(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()


def book_create(db:Session,language,file,title,title_known,title_mono,author,author_mono,commentator,commentator_mono,translator,translator_mono,compiler,compiler_mono,date_written,subjects,quantity_ill,quantity_sheet,lines,size,columns,paper,copyist,copy_date,copy_place,type_handwriting,cover,cover_color,stamp,text_begin,text_exbegin,text_ammabegin,text_end,text_exend,colophon,defects,fixation,note,descript_auth,user_id,images,inventory_number):
    query = models.Books(user_id=user_id,
                         title=title,
                         file=file,
                         title_known=title_known,
                         title_mono=title_mono,
                         author=author,
                         author_mono=author_mono,
                         commentator=commentator,
                         commentator_mono=commentator_mono,
                         translator=translator,
                         translator_mono=translator_mono,
                         compiler=compiler,
                         compiler_mono=compiler_mono,
                         date_written=date_written,
                         language=language,
                         subjects=subjects,
                         quantity_ill=quantity_ill,
                         quantity_sheet=quantity_sheet,
                         lines=lines,
                         columns=columns,
                         size=size,
                         paper=paper,
                         copyist=copyist,
                         copy_date=copy_date,
                         copy_place=copy_place,
                         type_handwriting=type_handwriting,
                         cover=cover,
                         cover_color=cover_color,
                         stamp=stamp,
                         text_begin=text_begin,
                         text_exbegin=text_exbegin,
                         text_ammabegin=text_ammabegin,
                         text_end=text_end,
                         text_exend=text_exend,
                         colophon=colophon,
                         defects=defects,
                         fixation=fixation,
                         note=note,
                         descript_auth=descript_auth,
                         images=images,
                        inventory_number=inventory_number,
                         )

    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def book_filter(db:Session,illustration,title,author,language,subjects,inventory_number):
    query = db.query(models.Books)
    if illustration is not None:
        query = query.filter(models.Books.cover==illustration)
    if title is not None:
        query = query.filter(models.Books.title.ilike(f"%{title}%"))
    if author is not None:
        query = query.filter(models.Books.author.ilike(f"%{author}%"))
    if language is not None:
        query = query.filter(models.Books.language.ilike(f"%{language}%"))
    if subjects is not None:
        query = query.filter(models.Books.subjects.ilike(f"%{subjects}%"))
    if inventory_number is not None:
        query = query.filter(models.Books.inventory_number.ilike(f"%{inventory_number}%"))
    return query.all()