import time
import pyak
import copy
import logging
logging.basicConfig()

import requests

import urllib3
import certifi

# http = urllib3.PoolManager(
#     cert_reqs='CERT_REQUIRED', # Force certificate check.
#     ca_certs=certifi.where(),  # Path to the Certifi bundle.
# )

# import urllib3.contrib.pyopenssl
# urllib3.contrib.pyopenssl.inject_into_urllib3()

requests.packages.urllib3.disable_warnings()

from firebase import firebase
firebase = firebase.FirebaseApplication('https://aljohri-nutopyak.firebaseio.com', None)

from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

def yak_to_dict(yak):
    yak_dict = copy.deepcopy(dict(yak.__dict__))
    yak_dict['client'] = yak.client.__dict__
    yak_dict['client']['location'] = yak_dict['client']['location'].__dict__ if type(yak_dict['client']['location']) != dict else yak_dict['client']['location']
    return yak_dict

# user_id='FFD35754D9024E83425053CB67B7C9D3'
# user_id='E76D6FF1E04E83C414E7771EF3CBBBCD'
yakker = pyak.Yakker()
print "New yakker registered with ID: %s" % yakker.id
locations = {
    "tech": pyak.Location(42.057796,-87.676634)
}

@sched.scheduled_job('interval', seconds=30)
def timed_job():
    # firebase.delete("/yaks", None)
    print "trying to get yaks.."
    yakker.update_location(locations['tech'])
    yaks = yakker.get_area_tops()
    print "Found %d yaks" % len(yaks)
    for i, yak in enumerate(yaks):
        # import pdb; pdb.set_trace()
        yak.message_id = yak.message_id.replace("R/", "")
        existing_yak = firebase.get('/yaks', yak.message_id)
        if existing_yak and existing_yak['likes'] == yak.likes: break
        result = firebase.put(url='/yaks', name=yak.message_id, data=yak_to_dict(yak), headers={'print': 'pretty'})
        print i, yak.time.strftime("%m/%e/%y %I:%M:%S"), yak.message_id, yak.likes, yak.message
    print "Sleep 10 seconds..."

timed_job()
sched.start()
