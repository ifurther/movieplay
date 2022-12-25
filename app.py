import os,platform,json,requests,time,threading,configparser
from pathlib import Path,PosixPath
from urllib.parse import urlparse
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from movieplay.downdriver import WindowsDownloadDriver,LinuxDownloadDriver
from movieplay.dirversetting import FirefoxDriver,ChromeDriver
from movieplay import initconfig
config = configparser.ConfigParser()
if Path('config.ini').exists():
    config.read('config.ini')
else:
    initconfig
    config.read('config.ini')
work_dir = Path(config['GLOBAL']['WORKDIR'])
runtimes = int(config['GLOBAL']['RUNNUMBER'])
target_url = config['MOVIE']['MOVIEURL']
movie_time = int(config['MOVIE']['MOVIETIME'])
total_cpu = int(config['THREAD']['TABNUMBER'])

print('work dir:',work_dir.absolute())
target_os = platform.system()
target_architecture = platform.architecture()
threadingLocal = threading.local()

BROWSER_PATH = {
    '360jisu': 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\\360chrome.exe',
    'chrome': 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe',
    'edge': 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe',
    'firefox': 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\\firefox.exe'
}

#HEADER = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/106.0"
AGENT = UserAgent(browsers=['edge', 'chrome','firefox'])
HEADER = AGENT.random
with open('data/firefoxdiverdownloadlist.json','r') as ch:
    firefox_links = json.load(ch)
with open('data/chromediverdownloadlist.json','r') as ch:
    chrome_links = json.load(ch)

if target_os == 'Windows':
    from movieplay.get_win_browser import get_browser_path
    if target_os == 'Windows' and target_architecture == ('64bit', 'WindowsPE'):
        paths_dict = get_browser_path(BROWSER_PATH)
        if 'chrome' in paths_dict:
            WN_BROWSER = 'chrome'
            CHROME_BINARY = paths_dict['chrome']
            CHROME_VERSION = list(Path(CHROME_BINARY).parent.iterdir())[0].name
        elif 'firefox' in paths_dict:
            WN_BROWSER = 'firefox'
            FIREFOX_BINARY = paths_dict['firefox']
            FIREFOX_VERSION = os.popen("{} --version".format(FIREFOX_BINARY)).read().strip('Mozilla Firefox  ').strip()
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
                CHROME_VERSION = os.popen("{} --version".format(CHROME_BINARY)).read().strip('Google Chrome ').strip()
            elif Path('/usr/bin/firefox').exists():
                LN_BROWSER = 'firefox'
                FIREFOX_BINARY = '/usr/bin/firefox'
                FIREFOX_VERSION = os.popen("{} --version".format(FIREFOX_BINARY)).read().strip('Mozilla Firefox  ').strip()
            downloaddriver = LinuxDownloadDriver('64bit','Linux', LN_BROWSER)
            downloaddriver.download(chrome_links, firefox_links)
            downloaddriver.extract(work_dir)
elif target_os == "darwin":
    # OS X
    if Path("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome").exists():
        LN_BROWSER = 'chrome'
        CHROME_BINARY = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'
def run_driver():
    if downloaddriver.browser == 'chrome':
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_argument("--incognito")
        if work_dir.parent == Path('.'):
            binary_path = work_dir.joinpath(downloaddriver.driverfilename).absolute()
        else:
            binary_path = work_dir.joinpath(downloaddriver.driverfilename).as_posix()
        opts.binary_location = Path(CHROME_BINARY).as_posix()
        Fdriver = ChromeDriver(HEADER, target_url, binary_path, opts)
    elif downloaddriver.browser == 'firefox':
        from selenium.webdriver.firefox.options import Options
        opts = Options()
        opts.add_argument("--incognito")
        if work_dir.parent == Path('.'):
            binary_path = work_dir.joinpath(downloaddriver.driverfilename).absolute()
        else:
            binary_path = work_dir.joinpath(downloaddriver.driverfilename).as_posix()
        Fdriver = FirefoxDriver(HEADER, target_url, FIREFOX_BINARY, binary_path, opts)

    Fdriver.getpage()
    try:
        element = WebDriverWait(Fdriver.driver, 15).until(
            EC.presence_of_element_located((By.ID, "movie_player")
        ))
        element.click()
        time.sleep(movie_time)
    finally:
        Fdriver.driver.quit()
for runi in range(runtimes):
    print('({}/{}) running times'.format(runi+1,runtimes+1))
    if target_os == 'Windows':
        if WN_BROWSER == 'firefox':
            print('Firefox version: {}'.format(FIREFOX_VERSION))
        elif WN_BROWSER == 'chrome':
            print('Chrome version: {}'.format(CHROME_VERSION))
    elif target_os == 'Linux':
        if LN_BROWSER == 'firefox':
            print('Firefox version: {}'.format(FIREFOX_VERSION))
        elif LN_BROWSER == 'chrome':
            print('Chrome version: {}'.format(CHROME_VERSION))
    for i in range(total_cpu):
        t = threading.Thread(target=run_driver)
        t.start()
    time.sleep(movie_time*2)
