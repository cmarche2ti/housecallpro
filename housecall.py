from datetime import datetime
import json

visits = []
hits = []

# function to convert posix time to utc
def parse_time(t):
    pt = int(t)
    return datetime.utcfromtimestamp(pt).strftime("%Y-%m-%d %H:%M:%S")


# read in file and parse json
with open("ga_sessions_20160801.json", "r") as f:
    for line in f:
        g = json.loads(line)
        visit = {}
        visit["key"] = g["fullVisitorId"] + g["visitId"]
        visit["full_visitor_id"] = g["fullVisitorId"]
        visit["visit_id"] = g["visitId"]
        visit["visit_number"] = g["visitNumber"]
        visit["visit_start_time"] = parse_time(g["visitStartTime"])
        visit["browser"] = g["device"]["browser"]
        visit["country"] = g["geoNetwork"]["country"]
        visits.append(visit)
        for h in g["hits"]:
            hit = {}
            hit["visit_key"] = visit["key"]
            hit["hit_number"] = h["hitNumber"]
            hit["hit_type"] = h["type"]
            hit["timestamp"] = parse_time(int(g["visitStartTime"]) + int(h["time"]))
            hit["page_path"] = h["page"]["pagePath"]
            hit["page_title"] = h["page"]["pageTitle"]
            hit["hostname"] = h["page"]["hostname"]
            hits.append(hit)

# write dictionaries to json files
with open("visits.json", "w") as outfile:
    for visit in visits:
        json.dump(visit, outfile)
        outfile.write("\n")

with open("hits.json", "w") as outfile:
    for hit in hits:
        json.dump(hit, outfile)
        outfile.write("\n")

