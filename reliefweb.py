from datetime import datetime, timedelta


url = "https://api.reliefweb.int/v1/disasters"
param_fields = [ 
  "description", "description-html", "status", "primary_country", "primary_type", "url_alias", "date"
  ]

async def description_parser(description):
  pass

async def relevance_check(events):
  pass

async def general_parser(data):
  pass

async def img_parser(event_type):
  pass
