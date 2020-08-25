#!/usr/bin/env python

import os
import sys
import time
import datetime
import pytz
import csv

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

cf = None


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1000.0 #1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.2f %s" % (num, x)
        num /= step_unit

def now_iso8601_time(h_delta):

    t = time.time() - (h_delta * 3600)
    r = datetime.datetime.fromtimestamp(int(t), tz=pytz.timezone("UTC")).strftime('%Y-%m-%dT%H:%M:%SZ')
    return r

def zone_traffic(zone_id,date_before,date_after):
    query="""
    query {
      viewer {
          zones(filter: {zoneTag: "%s"} ) {
          httpRequests1dGroups(limit:40, filter:{date_lt: "%s", date_gt: "%s"}) {
            sum { bytes }
            #sum { countryMap { bytes, requests, clientCountryName } }
            #dimensions { date }
          }
        }
      }
    }
    """ % (zone_id, date_before[0:10], date_after[0:10]) # only use yyyy-mm-dd part for httpRequests1dGroups

    # query - always a post
    try:
        r = cf.graphql.post(data={'query':query})
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/graphql.post %d %s - api call failed' % (e, e))

    ## only one zone, so use zero'th element!
    zone_info = r['data']['viewer']['zones'][0]

    httpRequests1dGroups = zone_info['httpRequests1dGroups']
    result = 0
    for element in httpRequests1dGroups:
        for k,v in element.items():
           result = int(v['bytes'])
    return result

def main():
    global cf
    total = 0

    # Grab the zone name
    try:
        zone_name = sys.argv[3]
        params = {'name':zone_name, 'per_page':1}
    except IndexError:
        params = {'per_page':100}       
        #exit('usage: example_graphql zone')
    # cloudflare 的 申請 email 和 Global API Key
    cf = CloudFlare.CloudFlare(email='xxxxxxxxxxxxx@gmail.com', token='xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    # grab the zone identifier
    try:
        zones = cf.zones.get(params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.get %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones - %s - api call failed' % (e))
    try:
        date_after = sys.argv[1]
        date_before = sys.argv[2]
    except:
        date_before = now_iso8601_time(0) # now
        date_after = now_iso8601_time(7 * 24) # 7 days worth
    #print( date_before)  
    #print( date_after)
   
    with open('Output.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for zone in zones:
            zone_id = zone['id']
            zone_name = zone['name']
            #print(zone_name)
            bandwith = zone_traffic(zone_id,date_before,date_after)
            #print(zone_name)
            #print(bandwith)
            total += bandwith  
            writer.writerow([zone_name,convert_bytes(bandwith)])
        writer.writerow("")       
        writer.writerow(['total',convert_bytes(total)])       
if __name__ == '__main__':
    main()
    exit(0)
