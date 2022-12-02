from selenium import webdriver
from pathlib import Path

#uas = UserAgent()

#opts = Options()

#opts.add_argument("--incognito")  # 使用無痕模式。用 selenium開瀏覽器已經很乾淨了，但疑心病重的可以用一下

# proxy setting
#proxy = "socks5://localhost:9050"
#opts.add_argument('--proxy-server={}'.format(proxy))  # 讓 selenium透過 tor訪問 internet

HEADER = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
#ua = uas.chrome
#opts.add_argument("user-agent={}".format(ua))         # 使用偽造的 user-agent

#driver = webdriver.Chrome(executable_path='/path/to/your/chromedriver',chrome_options=opts)

# 使用 selenium開啟瀏覽器

#driver.get('http://gs.statcounter.com/detect')  # 訪問 statcounter來確認目前瀏覽器的 user-agent

class Driver():
    def __init__(self, header, url, proxy=None) -> None:
        self.url = url
        self.header = header
        self.proxy = proxy
        self.driver = webdriver
    
    def getpage(self):
        self.driver.get(self.url)
        
class FirefoxDriver(Driver):
    def __init__(self, header, url, firefox_binary, executable_path, options) -> None:
        super().__init__(header, url)
        self.firefox_binary = firefox_binary
        self.executable_path = executable_path
        #self.profile = webdriver.FirefoxProfile("profilemodel")
        #adblockfile = 'ublock_origin-1.45.2.xpi'
        #self.profile.add_extension(adblockfile)
        self.driver = webdriver.Firefox(firefox_binary = self.firefox_binary, executable_path = self.executable_path, options=options) # firefox_profile = self.profile

class ChromeDriver(Driver):
    def __init__(self, header, url, executable_path, options) -> None:
        super().__init__(header, url)
        self.executable_path = executable_path
        self.driver = webdriver.Chrome(executable_path = self.executable_path, options=options)