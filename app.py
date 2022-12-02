import platform,json,requests,time,threading
from pathlib import Path
from urllib.parse import urlparse
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from downdriver import WindowsDownloadDriver,LinuxDownloadDriver
from headless import FirefoxDriver,ChromeDriver

work_dir = Path('.')
target_url = 'https://youtu.be/FcMKA16LmHA'
movie_time = 170
total_cpu = 2

print('work dir:',work_dir.absolute())
target_os = platform.system()
target_architecture = platform.architecture()
threadingLocal = threading.local()

BROWSER_PATH = {
    '360jisu': 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\\360chrome.exe',
    'chrome': 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe',
    'edge': 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe',
    'firefox': 'SOFTWARE\Clients\StartMenuInternet\FIREFOX.EXE\DefaultIcon'
}

HEADER = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/106.0"

with open('firefoxdiverdownloadlist.json','r') as ch:
    firefox_links = json.load(ch)
with open('chromediverdownloadlist.json','r') as ch:
    chrome_links = json.load(ch)

if target_os == 'Windows':
    from get_win_browser import get_browser_path
    if target_os == 'Windows' and target_architecture == ('64bit', 'WindowsPE'):
        paths_dict = get_browser_path(BROWSER_PATH)
        if 'chrome' in paths_dict:
            WN_BROWSER = 'chrome'
            CHROME_BINARY = paths_dict['chrome']
        elif 'firefox' in paths_dict:
            WN_BROWSER = 'firefox'
            FIREFOX_BINARY = paths_dict['firefox']
        downloaddriver = WindowsDownloadDriver('64bit', 'Windows', WN_BROWSER)
        downloaddriver.download(chrome_links, firefox_links)
        downloaddriver.extract(work_dir)



elif target_os == 'Linux':
    if target_os == 'Linux' and target_architecture == ('64bit', 'ELF'):
        try:
            import gnupg
            HAVE_GNUPG = True
        except:
            HAVE_GNUPG = False
        finally:
            if Path('/usr/bin/google-chrome').exists():
                LN_BROWSER = 'chrome'
                CHROME_BINARY = '/usr/bin/google-chrome'
            elif Path('/usr/bin/firefox').exists():
                LN_BROWSER = 'firefox'
                FIREFOX_BINARY = '/usr/bin/firefox'
            downloaddriver = LinuxDownloadDriver('64bit','Linux', LN_BROWSER)
            downloaddriver.download(chrome_links, firefox_links)
            downloaddriver.extract(work_dir)

def run_driver():
    if downloaddriver.browser == 'chrome':
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_argument("--incognito")
        opts.binary_location = Path(CHROME_BINARY).as_posix()
        Fdriver = ChromeDriver(HEADER, target_url, work_dir.joinpath(downloaddriver.driverfilename).as_posix(), opts)
    elif downloaddriver.browser == 'firefox':
        from selenium.webdriver.firefox.options import Options
        opts = Options()
        opts.add_argument("--incognito")
        Fdriver = FirefoxDriver(HEADER, target_url, FIREFOX_BINARY, work_dir.joinpath(downloaddriver.driverfilename).as_posix(), opts)    

    Fdriver.getpage()
    try:
        element = WebDriverWait(Fdriver.driver, 15).until(
            EC.presence_of_element_located((By.ID, "movie_player")
        ))
        element.click()
        time.sleep(movie_time)# 等待时常
    finally:
        Fdriver.driver.quit()
for i in range(total_cpu):
    t = threading.Thread(target=run_driver)
    t.start()