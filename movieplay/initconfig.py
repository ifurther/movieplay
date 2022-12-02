import configparser

config = configparser.ConfigParser()

config['GLOBAL'] = {}
config['GLOBAL']['WORKDIR']='.'
config['GLOBAL']['RUNNUMBER']=str(10)
config['THREAD'] = {}
config['THREAD']['TABNUMBER'] = str(2)
config['MOVIE'] = {}
config['MOVIE']['MOVIETIME'] = str(120)
config['MOVIE']['MOVIEURL'] = 'https://youtu.be/FcMKA16LmHA'
with open('config.ini', 'w') as configfile:
    config.write(configfile)
