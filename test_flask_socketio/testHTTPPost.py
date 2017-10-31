import json
import httplib

conn = httplib.HTTPConnection(host='192.168.20.140', port=3000)
conn.request('POST', '/face_recognizer')
response = conn.getresponse()
data = response.read()
print data