from datetime import datetime, timedelta


url = "https://api.reliefweb.int/v1/disasters"
param_fields = [ 
  "description", "description-html", "status", "primary_country", "primary_type", "url_alias", "date"
  ]

async def description_parser(description):
  pass

async def relevance_check(events):
  pass

async def img_parser(event_type):
  pass

async def general_parser(data):
  events = []

  for source in data:
    for event in source["events"]:
     event_tmp = {}
     event_tmp["source"] = "reliefweb"
     event_tmp["id"] = event["id"]
     event_tmp["status"] = event["fields"]["status"]
     event_tmp["imgPath"] = "placeholder"
     event_tmp["title"] = event["fields"]["name"]
     event_tmp["category"] = event["fields"]["primary_type"]["name"]
     event_tmp["updates"] = "placeholder"
     event_tmp["description"] = "placeholder"
     event_tmp["path"] = None
     #the location from reliefweb is listed in lon lat order in a dict , we want the location in a list with lat first
     event_tmp["location"] = [point for point in event["fields"]["primary_country"]["location"].values()][::-1]
     event_tmp["date"] = event["fields"]["date"]["created"]
     events.append(event_tmp)

  return events


