from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests,json, aiohttp, asyncio

import reliefweb
import eonet

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
  

async def get_eonet(url):
  async with session.get(url) as response:
    res = await response.json() 
    return res


async def get_reliefweb(url, params):
  """Fetches current humanitarian with current and alert status from the 
  UN OCHA Reliefweb API.

  Returns:
      cleaned_events(list): list of event objects from Reliefweb API
  """
  async with session.post(url, json=params) as response:
    res = await response.json()
    #cleaned_events = [event for event in res["data"]]
    return res

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
  data = await get_eonet(eonet.url)
  cleaned_events = [event for event in data["events"] if event["categories"][0]["id"] in eonet.categories]
  parsed_events = eonet.general_parser(cleaned_events)
  return parsed_events


@LastWeekEarth.get("/reliefweb/")
async def Reliefweb_Provider():
  """Standardizes data from get_reliefweb function and removes unrelevant data from the dataset
  Purpose is to 

  Returns:
      relevent_events(list) : JSON, list of standardized event objects and checked for relevancy
  """
  data = await get_reliefweb(reliefweb.url, reliefweb.params)
  cleaned_events = [event for event in data["data"]]
  events = reliefweb.general_parser(cleaned_events)
  relevent_events = reliefweb.relevance_check(events)
  return relevent_events


#Async HTTP request setup end
@LastWeekEarth.on_event('shutdown')
async def shutdown_event():
  await session.close()