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
  """Reliefweb combines all situation reports into one field(description). This function
  generates a summary with the initial event report as the description
  and the 5 most recent situation reports as a list of reports.

  Args:
      description (html as str): html as str from Reilfweb event description. The p tags contain
      situation report text, the a tags contain report source and date. 

  Returns:
      summary(list)[description, reports] : two value list with description and list 
      of situation reports in that order.
  """
  updates = []
  desc_html = BeautifulSoup(description, "html.parser")
  source_dates = desc_html.findAll("a")
  descriptions = desc_html.findAll("p")

  for date, report in zip(source_dates, descriptions):
    report_txt = report.text
    #the inner html of each p tag includes the date at the end in ()
    #update only grabs the text without the uneeded date
    report = report_txt[0:report_txt.rfind("(")]
    report_date = date.text
    event = [report_date, report]
    updates.append(event)
  
  desc = updates[0][1]
  #Some events have 50+ reports. Cutting off reports at 5 most recent.
  reports = updates[:-6:-1]
  summary = [desc, reports]

  return summary
  

def relevance_check(events):
  """Checks events for situation report updates from last month, if recent reports
  exist, the event is added to a list of objects to be returned.  This function is neeeded
  because Reliefweb will list ongoing events that may be years old.  We only want ongoing events
  with recent updates. 

  Args:
      events (list): List of event objects already standardized by the general parser

  Returns:
      relevent_events[list]: list of event objects that have at least 1 report from the previous month.
  """
  today = datetime.today()
  first_of_the_month = today.replace(day=1)
  current_month = today.strftime("%b %Y")
  last_month = (first_of_the_month - timedelta(days=1)).strftime("%b %Y")
  relevent_events = []
  for event in events:
    relevance = False
    for report in event["reports"]:
      if current_month in report[0] or last_month in report[0]:
        relevance = True
    if relevance is True:
      relevent_events.append(event)
  return relevent_events


async def img_parser(event_type):
  pass


def general_parser(data):
  """Takes JSON data from reliefweb and standardizes to match LastWeekEarth events
  allowing multiple sources on LastWeekEarth.  The order below is important.

  Args:
      data(list): json data from reliefweb

  Returns:
      events(list): returns json, list of event objects standardized for LastWeekEarth
  """
  events = []
  for event in data:
    event_tmp = {}
    event_tmp["source"] = "reliefweb"
    event_tmp["id"] = event["id"]
    event_tmp["status"] = event["fields"]["status"]
    event_tmp["imgPath"] = "placeholder"
    event_tmp["title"] = event["fields"]["name"]
    event_tmp["category"] = event["fields"]["primary_type"]["name"]
    summary = summary_maker(event["fields"]["description-html"])
    event_tmp["description"] = summary[0]
    event_tmp["reports"] = summary[1]
    event_tmp["path"] = None
    #the location from reliefweb is listed in lon lat order in a dict , we want the location in a list with lat first
    event_tmp["location"] = [point for point in event["fields"]["primary_country"]["location"].values()][::-1]
    event_tmp["date"] = event["fields"]["date"]["created"]
    events.append(event_tmp)

  return events


