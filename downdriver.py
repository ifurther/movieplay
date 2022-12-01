import platform,json,requests,tarfile
from zipfile import ZipFile
from pathlib import Path
from urllib.parse import urlparse

target_os = platform.system()
target_architecture = platform.architecture()



class DownloadDriver():
    def __init__(self,type_,os_):
        self.type = type_
        self.os = os_
    
    def getfilename(self,link):
        return urlparse(link)[2].split('/')[-1]

    def downloadfile(self,link):
        name = self.getfilename(link)
        r = requests.get(link, stream = True)

        with open(name,"wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

class WindowsDownloadDriver(DownloadDriver):
    def __init__(self, type_, os_, WN_BROWSER):
        super().__init__(type_, os_)
        self.browser = WN_BROWSER

    def download(self, chrome_links, firefox_links):
        if 'chrome' == self.browser:
            for link in chrome_links['links']:
                if link['os'] == 'windows':
                    self.link = link['link']
                    self.filename = self.getfilename(self.link)
                    self.downloadfile(self.link)
        elif 'firefox' == self.browser:
            for link in firefox_links['links']:
                if link['os'] == 'windows':
                    self.link = link['link']
                    self.filename = self.getfilename(self.link)
                    self.downloadfile(self.link)
    def extract(self,work_dir):
        if Path(self.filename).exists():
            with ZipFile(self.filename) as myzip:
                myzip.extractall(work_dir)
                self.driverfilename = myzip.namelist()[0]

class LinuxDownloadDriver(DownloadDriver):
    def __init__(self, type_, os_, LN_BROWSER):
        super().__init__(type_, os_)
        self.browser = LN_BROWSER
        
    def download(self, chrome_links, firefox_links):
        if Path('/usr/bin/google-chrome').exists():
            for link in chrome_links['links']:
                if link['os'] == 'linux':
                    self.link = link['link']
                    self.filename = self.getfilename(self.link)
                    if not Path(self.filename).exists():
                        self.downloadfile(self.link)
        elif Path('/usr/bin/firefox').exists():
            for link in firefox_links['links']:
                if link['os'] == 'linux':
                    self.link = link['link']
                    self.filename = self.getfilename(self.link)
                    self.downloadfile(self.link)
    def extract(self,work_dir):
        if Path(self.filename).exists():
            if '.zip' in self.filename:
                with ZipFile(self.filename) as myzip:
                    myzip.extractall(work_dir)
                    self.driverfilename = myzip.namelist()[0]
            else:
                tarfiles = tarfile.open(self.filename)
                self.driverfilename = tarfiles.getmembers()[0].name
                tarfiles.extractall()