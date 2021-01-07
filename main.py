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


async def get_reliefweb():
  """Fetches current humanitarian with current and alert status from the 
  UN OCHA Reliefweb API.

  Returns:
      cleaned_events(list): list of event objects from Reliefweb API
  """
  async with session.post(reliefweb.url, json=reliefweb.params) as response:
    res = await response.json()
    cleaned_events = [event for event in res["data"]]
    return cleaned_events

#Endpoints
@LastWeekEarth.get("/")
async def Homepage(request: Request):
  """returns the homepage template

  Args:
      request FastAPI Object: FastAPI object for handling get requests

  Returns:
      html(str): returns homepage
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
  """Standardizes data from get_reliefweb function and removes unrelevant data from the dataset
  Purpose is to 

  Returns:
      relevent_events(list) : JSON, list of standardized event objects and checked for relevancy
  """
  data = await get_reliefweb()
  events = reliefweb.general_parser(data)
  relevent_events = reliefweb.relevance_check(events)
  return relevent_events


#Async HTTP request setup end
@LastWeekEarth.on_event('shutdown')
async def shutdown_event():
  await session.close()