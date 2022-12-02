import requests,json

url = 'https://api.github.com/repos/mozilla/geckodriver/releases/latest'

r = requests.get(url)

json_data = json.loads(r.content)
driverlinklist={}
for link in json_data['assets']:
    link_str = link['browser_download_url']
    if 'win64' in link_str:
        driverlinklist['windows']=link_str
    elif 'linux64' in link_str and 'asc' not in link_str:
        driverlinklist['linux']=link_str
    elif 'macos' in link_str:
        driverlinklist['mac64']=link_str
no = len(driverlinklist)

data = {
     "name": "driver link list",
     "links": [{
     "os": key,
     "link": link
     } for key, link in driverlinklist.items()]
}


with open('firefoxdiverdownloadlist.json','w') as ch:
    json.dump(data,ch)
