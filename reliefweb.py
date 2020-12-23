from datetime import datetime, timedelta
from bs4 import BeautifulSoup


url = "https://api.reliefweb.int/v1/disasters"
param_fields = [ 
  "description-html", "status", "primary_country", "primary_type", "url_alias", "date"
  ]

async def update_parser(description):
  updates = []
  desc_html = BeautifulSoup(description, "html.parser")
  source_dates = desc_html.findAll("a")
  descriptions = desc_html.findAll("p")

  for date, report in zip(source_dates, descriptions):
    event = []
    report_date = date.text
    report_txt = report.text
    #the inner html of each p tag includes the date at the end in ()
    #update only grabs the text without the uneeded date
    update = report_txt[0:report_txt.rfind("(")]

    event.append(report_date)
    event.append(update)
    updates.append(event)

  return updates
  

async def relevance_check(events):
  pass

async def img_parser(event_type):
  pass

async def general_parser(data):
  events = []

  for source in data:
    for event in source["events"]:
      description = event["fields"]["description-html"]
      event_tmp = {}
      event_tmp["source"] = "reliefweb"
      event_tmp["id"] = event["id"]
      event_tmp["status"] = event["fields"]["status"]
      event_tmp["imgPath"] = "placeholder"
      event_tmp["title"] = event["fields"]["name"]
      event_tmp["category"] = event["fields"]["primary_type"]["name"]
      event_tmp["updates"] = await update_parser(description)
      #description grabs the 1st update as it is the most descriptive of the event. 
      event_tmp["description"] = event_tmp["updates"][0][1]
      event_tmp["path"] = None
      #the location from reliefweb is listed in lon lat order in a dict , we want the location in a list with lat first
      event_tmp["location"] = [point for point in event["fields"]["primary_country"]["location"].values()][::-1]
      event_tmp["date"] = event["fields"]["date"]["created"]
      events.append(event_tmp)

  return events


