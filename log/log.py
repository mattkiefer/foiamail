import csv
from datetime import datetime
import os, shutil

### START CONFIG ###
log_dir = 'log/logs/'
logpaths = {
            'stdout' :  '', 
            'auth'   :  log_dir + 'auth.csv',
            'contact':  log_dir + 'contact.csv',
            'msg'    :  log_dir + 'msg.csv',
            'label'  :  log_dir + 'label.csv',
            'report' :  log_dir + 'report.csv',
            'att'    :  log_dir + 'att.csv',
           }
### END CONFIG ###

def log_data(logtype,data):
    for datum in data:
        datum['timestamp'] = timestamp()
        datum = stringify_dict(datum)
    write_or_append(logtype,data)
        
def timestamp():
    return datetime.now().strftime('%Y-%m-%d_%T')

def stringify_dict(datum):
    return dict((x,str(datum[x])) for x in datum)

def write_or_append(logtype,data):
    path = logpaths[logtype]
    method = 'w'
    if check_file_exists(logtype) and check_schema_match(logtype,data):
        # append if log exists and schema matches
        method = 'a'
    elif check_file_exists(logtype) and not check_schema_match(logtype,data):
        # log exists, but schema mismatch ...
        # backup old log with timestamp, 
        # then overwrite main log 
        shutil.move(path,path.replace('.', timestamp() + '.'))
    logfile = open(path,method)
    write_log(logfile,method,data)
    logfile.close()

def check_file_exists(logtype):
    return os.path.isfile(logpaths[logtype])

def check_schema_match(logtype,data):
    # check if new data matches logfile schema
    return sorted(data[0].keys()) == \
        sorted(csv.DictReader(logpaths[logtype]).fieldnames)

def write_log(logfile,method,data):
    logcsv = csv.DictWriter(logfile,data[0].keys())
    if method == 'w':
        logcsv.writeheader()
    for row in data:
        logcsv.writerow(row)
