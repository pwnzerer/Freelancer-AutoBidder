import json
import math
import time
from cgi import test
from ctypes import cast
from email import message
from pathlib import Path
from pickle import LIST
from typing import List, Optional
from urllib import request, response

import requests
import starlette.status as status
import uvicorn
from decouple import config
from fastapi import Body, Depends, FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic.fields import ModelField
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models
from database import SessionLocal, engine
from initialize import headers
from initialize_driver import *
from loginfunc import *
from models import templatesinfo
from scrapper import *

# from ssl import _PasswordType

models.Base.metadata.create_all(bind=engine)


class TemplateRequest(BaseModel):
    template_name: str
    templates: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


user = config("USER_NAME", cast=str)
password = config("USER_PASWORD", cast=str)


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/login", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
async def login_caller(request: Request, user: str = Form(...), password: str = Form(...)):
    driver = initialize_driver()
    login(driver, user, password)
    wow = RedirectResponse("/settings", status_code=status.HTTP_302_FOUND)
    return wow


@app.get("/settings", response_class=HTMLResponse)
async def settingspage(request: Request):
    return templates.TemplateResponse("scrapper_parameters.html", {"request": request})


@app.post("/settings")
async def settings_page(
    request: Request,
    python: bool = Form(False),
    html: bool = Form(False),
    html5: bool = Form(False),
    webdev: bool = Form(False),
    api: bool = Form(False),
    flask: bool = Form(False),
    mlearn: bool = Form(False),
    dsci: bool = Form(False),
    selwebdriv: bool = Form(False),
    sel: bool = Form(False),
    mvisanal: bool = Form(False),
    finance: bool = Form(False),
    js: bool = Form(False),
    nodejs: bool = Form(False),
    angular: bool = Form(False),
    reactjs: bool = Form(False),
    reactnative: bool = Form(False),
):
    jobidlist = []
    if python:
        jobidlist.append("13")
    if html:
        jobidlist.append("323")
    if html5:
        jobidlist.append("335")
    if webdev:
        jobidlist.append("1031")
    if api:
        jobidlist.append("1087")
    if flask:
        jobidlist.append("1094")
    if mlearn:
        jobidlist.append("292")
    if dsci:
        jobidlist.append("761")
    if selwebdriv:
        jobidlist.append("1112")
    if sel:
        jobidlist.append("1679")
    if mvisanal:
        jobidlist.append("1876")
    if finance:
        jobidlist.append("1665")
    if js:
        jobidlist.append("99")
    if nodejs:
        jobidlist.append("500")
    if angular:
        jobidlist.append("704")
    if reactjs:
        jobidlist.append("759")
    if reactnative:
        jobidlist.append("1314")
    paramz = make_params(jobidlist)
    all_jobs = get_all_jobs(FREELANCE_BASE_URL, headers, paramz)
    time_to_bid(all_jobs)
    return templates.TemplateResponse("scrapper_parameters.html", {"request": request})


@app.get("/addtemplate", response_class=HTMLResponse)
# this param remember db: Session = Depends(get_db)
async def add_templates(request: Request, db: Session = Depends(get_db)):
    # template_data = templatesinfo("asdadsa", "asdadasda", "asdasd")
    # db.add(template_data)
    # db.commit()
    alltempdata = db.query(templatesinfo).all()
    return templates.TemplateResponse("maketemplate.html", {"request": request, "alltempdata": alltempdata})


@app.post("/addtemplate")
async def addtemplates(
    request: Request,
    templatename: str = Form(...),
    templatetext: str = Form(...),
    keywords: str = Form(...),
    db: Session = Depends(get_db),
):
    alltempdata = db.query(templatesinfo).all()
    template_data = templatesinfo(templatename, templatetext, keywords)
    db.add(template_data)
    db.commit()
    return templates.TemplateResponse("maketemplate.html", {"request": request, "alltempdata": alltempdata})


# @app.get("/")
# async def get_form_data(
#     ml_keywords: List[str] = Query(ml_keywords),
#     is_ml: bool = Query(
#         False,
#         choices=(True, False),
#         description="is ML tempalte service is required - by default False",
#     ),
#     wb_keywords: List[str] = Query(web_keywords),
#     is_wb: bool = Query(
#         False,
#         choices=(True, False),
#         description="is Web tempalte service is required - by default False",
#     ),
#     mb_keywords: List[str] = Query(mob_keywords),
#     is_mb: bool = Query(
#         False,
#         choices=(True, False),
#         description="is Mobile tempalte service is required - by default False",
#     ),
#     wp_keywords: List[str] = Query(wordpress_keywords),
#     is_wp: bool = Query(
#         False,
#         choices=(True, False),
#         description="is Word Press tempalte service is required - by default False",
#     ),
# ):
#     payload = {
#         "ml": {
#             "is_ml": is_ml,
#             "ml_keywords": ml_keywords,
#         },
#         "wb": {
#             "is_wb": is_wb,
#             "wb_keywords": wb_keywords,
#         },
#         "mb": {
#             "is_mb": is_mb,
#             "mb_keywords": mb_keywords,
#         },
#         "wp": {
#             "is_wp": is_wp,
#             "wp_keywords": wp_keywords,
#         },
#     }
#     print(payload)

#     main(payload)

#     return {"message": "all good", "payload": json.dumps(payload)}
