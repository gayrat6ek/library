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



def book_filter(db:Session,illustration,title,author,language,subjects,inventory_number,id,tomb):
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
    if id is not None:
        query = query.filter(models.Books.id==id)
    if tomb is not None:
        query = query.filter(models.Books.text_ammabegin==tomb)
    query = query.order_by(models.Books.id.desc())
    return query.all()

def book_update(db:Session,id,language,file,title,title_known,title_mono,author,author_mono,commentator,commentator_mono,translator,translator_mono,compiler,compiler_mono,date_written,subjects,quantity_ill,quantity_sheet,lines,size,columns,paper,copyist,copy_date,copy_place,type_handwriting,cover,cover_color,stamp,text_begin,text_exbegin,text_ammabegin,text_end,text_exend,colophon,defects,fixation,note,descript_auth,images,inventory_number):
    query = db.query(models.Books).filter(models.Books.id==id).first()
    if query:
        if language is not None:
            query.language = language
        if file is not None:
            query.file = file
        if title is not None:
            query.title = title
        if title_known is not None:
            query.title_known = title_known
        if title_mono is not None:
            query.title_mono = title_mono
        if author is not None:
            query.author = author
        if author_mono is not None:
            query.author_mono = author_mono
        if commentator is not None:
            query.commentator = commentator
        if commentator_mono is not None:
            query.commentator_mono = commentator_mono
        if translator is not None:
            query.translator = translator
        if translator_mono is not None:
            query.translator_mono = translator_mono
        if compiler is not None:
            query.compiler = compiler
        if compiler_mono is not None:
            query.compiler_mono = compiler_mono
        if date_written is not None:
            query.date_written = date_written
        if subjects is not None:
            query.subjects = subjects
        if quantity_ill is not None:
            query.quantity_ill = quantity_ill
        if quantity_sheet is not None:
            query.quantity_sheet = quantity_sheet
        if lines is not None:
            query.lines = lines
        if size is not None:
            query.size = size
        if columns is not None:
            query.columns = columns
        if paper is not None:
            query.paper = paper
        if copyist is not None:
            query.copyist = copyist
        if copy_date is not None:
            query.copy_date = copy_date
        if copy_place is not None:
            query.copy_place = copy_place
        if type_handwriting is not None:
            query.type_handwriting = type_handwriting
        if cover is not None:
            query.cover = cover
        if cover_color is not None:
            query.cover_color = cover_color
        if stamp is not None:
            query.stamp = stamp
        if text_begin is not None:
            query.text_begin = text_begin
        if text_exbegin is not None:
            query.text_exbegin = text_exbegin
        if text_ammabegin is not None:
            query.text_ammabegin = text_ammabegin
        if text_end is not None:
            query.text_end = text_end
        if text_exend is not None:
            query.text_exend = text_exend
        if colophon is not None:
            query.colophon = colophon
        if defects is not None:
            query.defects = defects
        if fixation is not None:
            query.fixation = fixation
        if note is not None:
            query.note = note
        if descript_auth is not None:
            query.descript_auth = descript_auth
        if images is not None:
            query.images = images
        if inventory_number is not None:    
            query.inventory_number = inventory_number
        db.commit()
        db.refresh(query)
    return query


def books_search(db:Session,data):
    query = db.query(models.Books).filter(or_(models.Books.title.ilike(f"%{data}%"),
                                              models.Books.author.ilike(f"%{data}%"),
                                              models.Books.subjects.ilike(f"%{data}%"),
                                                models.Books.language.ilike(f"%{data}%"),
                                                models.Books.text_ammabegin.ilike(f"%{data}%"),
                                                models.Books.text_begin.ilike(f"%{data}%"),
                                                models.Books.text_exbegin.ilike(f"%{data}%"),
                                                models.Books.text_end.ilike(f"%{data}%"),
                                                models.Books.text_exend.ilike(f"%{data}%"),
                                                models.Books.title_mono.ilike(f"%{data}%"),
                                                models.Books.author_mono.ilike(f"%{data}%"),
                                                models.Books.commentator.ilike(f"%{data}%"),
                                                models.Books.commentator_mono.ilike(f"%{data}%"),
                                                models.Books.translator.ilike(f"%{data}%"),
                                                models.Books.title_known.ilike(f"%{data}%")
                                              ))
    return query.all()