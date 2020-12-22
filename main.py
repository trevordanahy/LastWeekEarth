from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests,json, aiohttp, asyncio

import reliefweb

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


async def get_reliefweb(status):
  async with session.get(reliefweb.url, params = {
    "appname": "LastWeekEarth",
    "filter[field]": "status",
    "filter[value]": status,
    "fields[include][]": reliefweb.param_fields}) as response:
    res = await response.json()
    cleaned_events = [event for event in res["data"]]
    event_list = {"events": cleaned_events}
    return res

#Endpoints
@LastWeekEarth.get("/")
async def Homepage(request: Request):
  """
  returns the homepage template
  """
  return templates.TemplateResponse("home.html", {"request": request})


@LastWeekEarth.get("/eonet/")
async def Eonet_Provider():
  """
  fetches data from NASA EONET API and returns the json results
  """
  url = "https://eonet.sci.gsfc.nasa.gov/api/v3/events?days=7"
  async with session.get(url) as response:
    events = await response.json()
    return events


@LastWeekEarth.get("/reliefweb/")
async def Reliefweb_Provider():
  """
  fetches current humanitarian with current and alert status from the 
  UN OCHA Reliefweb API and returns the json results
  """
  data = await asyncio.gather(
    get_reliefweb("current"),
    get_reliefweb("alert"))
  return data


#Async HTTP request setup end
@LastWeekEarth.on_event('shutdown')
async def shutdown_event():
  await session.close()