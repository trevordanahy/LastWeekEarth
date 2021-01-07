#EONET JSON parsers to clean the data from NASA EONET
#Only seaLakeIce, wildfires, and volcanoes will be pulled from eonet, all other events handled by Reliefweb
#coordinates from eonet are ordered Longitude(E,W) lattitude(N,S)

url = "https://eonet.sci.gsfc.nasa.gov/api/v3/events?days=30"
categories = ["seaLakeIce", "wildfires", "volcanoes"]


def general_parser(data):
    events = []
    for event in data:
        path = event["geometry"]
        event_tmp = {}
        event_tmp["source"] = "eonet"
        event_tmp["id"] = event["id"]
        event_tmp["status"] = "alert"
        event_tmp["imgPath"] = "PLACEHOLDER to be replaced by function"
        event_tmp["title"] = event["title"]
        event_tmp["category"] = event["categories"][0]["id"]
        event_tmp["path"] = "PLACEHOLDER to be replaced by function"
        #some events have location list, we grab the last and most recent location
        event_tmp["location"] = event["geometry"][-1]["coordinates"][::-1]
        event_tmp["reports"] = "PLACEHOLDER to be replaced by function"
        event_tmp["description"] = "PLACEHOLDER to be replaced by function"
        event_tmp["date"] = event["geometry"][-1]["date"]
        events.append(event_tmp)
    return events
            