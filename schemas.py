from pydantic import BaseModel,validator
from fastapi import Form,UploadFile,File
from typing import Optional,Annotated,Dict
from datetime import datetime,time
from fastapi import Form


class UserGet(BaseModel):
    id:int
    password :str
    username :str
    full_name:str
    class Config:
        orm_mode=True
class UserUpdate(BaseModel):
    id:int
    password:Optional[str]=None
    username :Optional[str]=None
    full_name:Optional[str]=None
    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    password:str
    username:str
    fullname:Optional[str]



class Books(BaseModel):
    id:int
    user_id:int
    title:Optional[str]=None
    title_mono:Optional[str]=None
    title_known:Optional[str]=None
    title_known:Optional[str]=None
    author:Optional[str]=None
    author_mono:Optional[str]=None
    commentator:Optional[str]=None
    commentator_mono:Optional[str]=None
    translator:Optional[str]=None
    translator_mono:Optional[str]=None
    compiler:Optional[str]=None
    compiler_mono:Optional[str]=None
    date_written:Optional[str]=None
    language:Optional[str]=None
    subjects:Optional[str]=None
    quantity_sheet:Optional[str]=None
    quantity_ill:Optional[str]=None
    lines:Optional[str]=None
    columns:Optional[str]=None
    size:Optional[str]=None
    paper:Optional[str]=None
    copyist:Optional[str]=None
    copy_date:Optional[str]=None
    copy_place:Optional[str]=None
    type_handwriting:Optional[str]=None
    cover:Optional[str]=None
    cover_color:Optional[str]=None
    stamp:Optional[str]=None
    text_begin:Optional[str]=None
    text_exbegin:Optional[str]=None
    text_ammabegin:Optional[str]=None
    text_end:Optional[str]=None
    text_exend:Optional[str]=None
    colophon:Optional[str]=None
    defects:Optional[str]=None
    fixation:Optional[str]=None
    note:Optional[str]=None
    descript_auth:Optional[str]=None
    file:Optional[str]=None
    created_at:Optional[datetime]=None
    images:Optional[list]=None
    class Config:
        orm_mode=True



