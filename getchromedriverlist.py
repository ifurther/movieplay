import requests,json
import xml.etree.ElementTree as ET

chrome_driver_version = '108.0.5359.71'
file_base_url = 'https://chromedriver.storage.googleapis.com/'
url = 'https://chromedriver.storage.googleapis.com/?delimiter=/&prefix={}/'.format(chrome_driver_version)
r = requests.get(url)

def getCountContents(root):
    y=0
    for child in root:
        if 'Contents' in child.tag:
           y+=1
    return y-2

def getjsondata(root):
    driverlinklist={}
    for actor in root.findall('{http://doc.s3.amazonaws.com/2006-03-01}Contents'):
        Key = actor.find('{http://doc.s3.amazonaws.com/2006-03-01}Key')
        ETag = actor.find('{http://doc.s3.amazonaws.com/2006-03-01}ETag')
        if 'win32' in Key.text:
            driverlinklist['windows']=[file_base_url+Key.text,ETag.text.replace('\"','')]
        elif 'linux' in Key.text:
            driverlinklist['linux']=[file_base_url+Key.text,ETag.text.replace('\"','')]
        elif 'mac64' in Key.text:
            driverlinklist['mac64']=[file_base_url+Key.text,ETag.text.replace('\"','')]
    no = len(driverlinklist)
    data = {
         "name": "driver link list",
         "links": [{
         "os": key,
         "link": link,
         "md5": md5
         } for key, [link, md5] in driverlinklist.items()]
      }
    return no,data

if r.ok:
    root = ET.fromstring(r.content)
    no, data = getjsondata(root)
    if getCountContents(root) == no:
        with open('chromediverdownloadlist.json','w') as ch:
            json.dump(data,ch)
        print('finished')

