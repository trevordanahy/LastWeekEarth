from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests,json, aiohttp, asyncio

#FastAPI Setup
LastWeekEarth = FastAPI()
templates = Jinja2Templates(directory="templates")
LastWeekEarth.mount("/static", StaticFiles(directory="static"), name="static")


#Async HTTP request setup start
session = None
@LastWeekEarth.on_event('startup')
async def startup_event():
  global session
  session = aiohttp.ClientSession()


#Endpoints
@LastWeekEarth.get("/")
async def Homepage(request: Request):
  """
  returns the homepage template
  """
  return templates.TemplateResponse("home.html", {"request": request})


@LastWeekEarth.get("/eonet/")
async def Get_Eonet():
  """
  fetches data from NASA EONET API and returns the json results
  """
  url = "https://eonet.sci.gsfc.nasa.gov/api/v3/events?days=7"
  async with session.get(url) as response:
    events = await response.json()
    return events


#Async HTTP request setup end
@LastWeekEarth.on_event('shutdown')
async def shutdown_event():
  await session.close()