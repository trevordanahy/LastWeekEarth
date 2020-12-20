from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

LastWeekEarth = FastAPI()
templates = Jinja2Templates(directory="templates")
LastWeekEarth.mount("/static", StaticFiles(directory="static"), name="static")


@LastWeekEarth.get("/")
async def Homepage(request: Request):
  """
  returns the homepage template
  """
  return templates.TemplateResponse("home.html", {"request": request})