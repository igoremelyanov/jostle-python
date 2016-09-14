# this is a function that is used to put the test result and build number into saucelabs
import httplib
import base64
try:
    import json
except ImportError:
    import simplejson as json

config = {"username": "dwightivany",
          "access-key": "07000591-4070-4f57-99d4-33cddd236991"}

base64string = base64.encodestring('%s:%s' % (config['username'], config['access-key']))[:-1]

def set_test_status(jobid, result, build):
    body_content = json.dumps({"passed": result ,"build": build}) #converts everything inside {} to json object
    connection =  httplib.HTTPConnection("saucelabs.com")
    connection.request('PUT', '/rest/v1/%s/jobs/%s' % (config['username'], jobid),
                       body_content, headers={"Authorization": "Basic %s" % base64string})
    result = connection.getresponse()
    return result.status == 200

