from jose import JWTError, jwt
from typing import Annotated
from datetime import datetime, timedelta,date
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status,BackgroundTasks,Security
from pydantic import ValidationError
import schemas
import bcrypt
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
from fastapi_pagination import paginate, Page, add_pagination
from typing import Optional
import models
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
import query
import utils



reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
origins = ["*"]
#database connection
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/files", StaticFiles(directory="files"), name="files")

@app.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),db:Session=Depends(utils.get_db)):
    user = query.get_user(db,form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    hashed_pass = user.password
    if not utils.verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": utils.create_access_token(user.username),
        "refresh_token": utils.create_refresh_token(user.username),
    }


@app.post('/users',)
async def register_user(form_data:schemas.UserCreate,db:Session=Depends(utils.get_db)):
    user_query = query.create_user(db=db,form_data=form_data)
    return user_query


@app.get('/users',response_model=list[schemas.UserGet])
async def filter_user(user_name:Optional[str]=None,id:Optional[int]=None,db:Session=Depends(utils.get_db),request_user:schemas.UserGet=Depends(utils.get_current_user)):
    user_query = query.filterquery_user(db=db,id=id,username=user_name)
    return user_query


@app.post('/books')
async def Book_add(file:UploadFile=File(),
                   title:Annotated[str,Form()]=None,
                   title_mono:Annotated[str,Form()]=None,
                   title_known:Annotated[str,Form()]=None,
                   author:Annotated[str,Form()]=None,
                   author_mono:Annotated[str,Form()]=None,
                   commentator:Annotated[str,Form()]=None,
                   commentator_mono:Annotated[str,Form()]=None,
                   translator:Annotated[str,Form()]=None,
                   translator_mono:Annotated[str,Form()]=None,
                   compiler:Annotated[str,Form()]=None,
                   compiler_mono:Annotated[str,Form()]=None,
                   date_written:Annotated[date,Form()]=None,
                   language:Annotated[str,Form()]=None,
                   subjects:Annotated[str,Form()]=None,
                   quantity_sheet:Annotated[str,Form()]=None,
                   quantity_ill:Annotated[str,Form()]=None,
                   lines:Annotated[str,Form()]=None,
                   size:Annotated[str,Form()]=None,
                   paper:Annotated[str,Form()]=None,
                   copyist:Annotated[str,Form()]=None,
                   copy_date:Annotated[date,Form()]=None,
                   copy_place:Annotated[str,Form()]=None,
                   type_handwriting:Annotated[str,Form()]=None,
                   cover:Annotated[str,Form()]=None,
                   cover_color:Annotated[str,Form()]=None,
                   stamp:Annotated[str,Form()]=None,
                   text_begin:Annotated[str,Form()]=None,
                   text_exbegin:Annotated[str,Form()]=None,
                   text_ammabegin:Annotated[str,Form()]=None,
                   text_end:Annotated[str,Form()]=None,
                   text_exend:Annotated[str,Form()]=None,
                   colophon:Annotated[str,Form()]=None,
                   defects:Annotated[str,Form()]=None,
                   fixation:Annotated[str,Form()]=None,
                   note:Annotated[str,Form()]=None,
                   descript_auth:Annotated[str,Form()]=None,
                   columns:Annotated[str,Form()]=None,
                   images:Annotated[list[str],Form()]=None,
                   inventory_number:Annotated[str,Form()]=None,
                   db:Session=Depends(utils.get_db),
                   request_user:schemas.UserGet=Depends(utils.get_current_user)):
    filename = utils.generate_random_filename()+file.filename
    file_path = f"files/{filename}"
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            buffer.write(chunk)
    book_add_query = query.book_create(db=db,
                                       file=file_path,
                                       title=title,
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
                                       size=size,
                                       columns=columns,
                                       paper=paper,
                                       copyist=copyist,
                                       copy_date=copy_date,
                                       copy_place=copy_place,
                                       type_handwriting=type_handwriting,
                                       cover=cover,
                                       cover_color=cover_color,
                                       stamp=stamp,
                                       text_ammabegin=text_ammabegin,
                                       text_begin=text_begin,
                                       text_exbegin=text_exbegin,
                                       text_end=text_end,
                                       text_exend=text_exend,
                                       colophon=colophon,
                                       defects=defects,
                                       fixation=fixation,note=note,user_id=request_user.id,
                                       descript_auth=descript_auth,
                                       images=images,
                                        inventory_number=inventory_number
                                       )
    return book_add_query


@app.post('/files')
async def get_images(files: list[UploadFile],db:Session=Depends(utils.get_db),request_user:schemas.UserGet=Depends(utils.get_current_user)):
    file_obj_list = []
    if files:
        for file in files:
            filename = utils.generate_random_filename()+file.filename
            file_path = f"files/{filename}"
            with open(file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            file_obj_list.append(file_path)
    return {"files": file_obj_list}



@app.get('/books',response_model=Page[schemas.Books])
async def filter_book(title:Optional[str]=None,
                      inventory_number:Optional[str]=None,
                      author:Optional[str]=None,
                      language:Optional[str]=None,
                      subjects:Optional[str]=None,
                    illustration:Optional[str]=None,
                    tomb:Optional[str]=None,
                    id:Optional[int]=None,
                      db:Session=Depends(utils.get_db)):
    book_query = query.book_filter(db=db,
                                   title=title,
                                   author=author,
                                   language=language,
                                   subjects=subjects,
                                   illustration=illustration,
                                   inventory_number=inventory_number,
                                   id=id,
                                   tomb=tomb)
    return paginate(book_query)
    
@app.put('/books',response_model=schemas.Books)
async def update_book(id:Annotated[int,Form()]=None,
                      file:UploadFile=File(None),
                      title:Annotated[str,Form()]=None,
                      title_mono:Annotated[str,Form()]=None,
                      title_known:Annotated[str,Form()]=None,
                      author:Annotated[str,Form()]=None,
                        author_mono:Annotated[str,Form()]=None,
                        commentator:Annotated[str,Form()]=None,
                        commentator_mono:Annotated[str,Form()]=None,
                        translator:Annotated[str,Form()]=None,
                        
                        translator_mono:Annotated[str,Form()]=None,
                        compiler:Annotated[str,Form()]=None,
                        compiler_mono:Annotated[str,Form()]=None,
                        date_written:Annotated[str,Form()]=None,
                        language:Annotated[str,Form()]=None,
                        subjects:Annotated[str,Form()]=None,
                        quantity_sheet:Annotated[str,Form()]=None,
                        quantity_ill:Annotated[str,Form()]=None,
                        lines:Annotated[str,Form()]=None,
                        size:Annotated[str,Form()]=None,
                        paper:Annotated[str,Form()]=None,
                        copyist:Annotated[str,Form()]=None,
                        copy_date:Annotated[str,Form()]=None,
                        copy_place:Annotated[str,Form()]=None,
                        type_handwriting:Annotated[str,Form()]=None,
                        cover:Annotated[str,Form()]=None,
                        cover_color:Annotated[str,Form()]=None,
                        stamp:Annotated[str,Form()]=None,
                        text_begin:Annotated[str,Form()]=None,
                        text_exbegin:Annotated[str,Form()]=None,
                        text_ammabegin:Annotated[str,Form()]=None,
                        text_end:Annotated[str,Form()]=None,
                        text_exend:Annotated[str,Form()]=None,
                        colophon:Annotated[str,Form()]=None,
                        defects:Annotated[str,Form()]=None,
                        fixation:Annotated[str,Form()]=None,
                        note:Annotated[str,Form()]=None,
                        descript_auth:Annotated[str,Form()]=None,
                        columns:Annotated[str,Form()]=None,
                        images:Annotated[list[str],Form()]=None,
                        inventory_number:Annotated[str,Form()]=None,
                        db:Session=Depends(utils.get_db),
                        request_user:schemas.UserGet=Depends(utils.get_current_user)):
                      
    filename = utils.generate_random_filename()+file.filename
    book = query.book_update(db=db,
                      id=id,
                        file=filename, 
                        title=title,
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
                        size=size,
                        columns=columns,
                        paper=paper,
                        copyist=copyist,
                        copy_date=copy_date,
                        copy_place=copy_place,
                        type_handwriting=type_handwriting,
                        cover=cover,
                        cover_color=cover_color,
                        stamp=stamp,
                        text_ammabegin=text_ammabegin,
                        text_begin=text_begin,
                        text_exbegin=text_exbegin,
                        text_end=text_end,
                        text_exend=text_exend,
                        colophon=colophon,
                        defects=defects,
                        fixation=fixation,note=note,user_id=request_user.id,
                        descript_auth=descript_auth,
                        images=images,
                        inventory_number=inventory_number
                        )
    
    return book


@app.get("/books/search",response_model=Page[schemas.Books])
async def search_book(data:str,db:Session=Depends(utils.get_db)):
    return paginate(query.books_search(db=db,data=data))


add_pagination(app)