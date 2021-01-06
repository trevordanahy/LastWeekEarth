from datetime import datetime, timedelta
from bs4 import BeautifulSoup


url = "https://api.reliefweb.int/v1/disasters"
return_fields = [ 
  "description-html", "status", "primary_country", "primary_type", "url_alias", "date"
  ]
params = {
  "appname": "lastweekearth",
  "filter": {
    "field": "status",
    "value": ["current", "alert"],
    "operator": "OR"
  },
  "fields": {
    "include": return_fields
  },
  "limit": 50
}

def summary_maker(description):
  """
  Generates a summary with the initial event report as the description
  and the 5 most recent situation reports. 

  Args:
      description (string): html with p and a tags for each report, each a tag
      contains the source and date of the report.

  Returns:
      list : two value list with description and list of situation reports
  """
  reports = []
  desc_html = BeautifulSoup(description, "html.parser")
  source_dates = desc_html.findAll("a")
  descriptions = desc_html.findAll("p")

  for date, report in zip(source_dates, descriptions):
    event = []
    report_txt = report.text
    #the inner html of each p tag includes the date at the end in ()
    #update only grabs the text without the uneeded date
    report = report_txt[0:report_txt.rfind("(")]
    report_date = date.text
    event.append(report_date)
    event.append(report)
    reports.append(event)
  
  desc = reports[0][1]
  #Some events have 50+ reports. Cutting off reports at 5 most recent.
  reports = reports[:5:-1]
  summary = [desc, reports]

  return summary
  

async def relevance_check(events):
  pass

async def img_parser(event_type):
  pass

def general_parser(data):
  events = []
  for event in data["events"]:
    description = event["fields"]["description-html"]
    event_tmp = {}
    event_tmp["source"] = "reliefweb"
    event_tmp["id"] = event["id"]
    event_tmp["status"] = event["fields"]["status"]
    event_tmp["imgPath"] = "placeholder"
    event_tmp["title"] = event["fields"]["name"]
    event_tmp["category"] = event["fields"]["primary_type"]["name"]
    summary = summary_maker(description)
    event_tmp["description"] = summary[0]
    event_tmp["updates"] = summary[1]
    event_tmp["path"] = None
    #the location from reliefweb is listed in lon lat order in a dict , we want the location in a list with lat first
    event_tmp["location"] = [point for point in event["fields"]["primary_country"]["location"].values()][::-1]
    event_tmp["date"] = event["fields"]["date"]["created"]
    events.append(event_tmp)

  return events


