from datetime import datetime, timedelta
import re
import os.path
import gzip

regex = '(.*?) \[(.*?)\] \[(.*?)\]: (.*?) \[(.*?)\] (.*?)$'


def search_log_lines(logfile, lookbacktime=5, searchstring=None):
    print search_log_lines.__name__ + " Starting"
    log_lines = []
    if os.path.exists(logfile):
        now = datetime.now()
        lookback = timedelta(minutes=lookbacktime)
        oldest = (now - lookback).strftime('%Y/%m/%d %H:%M:%S')

        lines = []
        print "Reading file:"+logfile
        with open(logfile, 'r') as f:
            for line in f:
                if line[:19] > oldest and searchstring in line:
                    lines.append(line)
        for line in lines:
            line = line.replace('\"', '')
            line_regex = re.split(regex, line)
            kvstring = line_regex[len(line_regex)-2]
            logline_dict = {}
            logline_dict['log_time'] = line_regex[1]
            logline_dict['class'] = line_regex[2]
            logline_dict['thread'] = line_regex[3]
            logline_dict['logmode'] = line_regex[4]
            logline_dict['FCID'] = line_regex[5]
            logline_dict.update(dict(item.split("=",1) for item in kvstring.split(",")))
            log_lines.append(logline_dict)
    else:
        raise Exception('File not found')
    print search_log_lines.__name__+" Ended"
    return log_lines


def search_log_lines_gz(logfile, searchstring=None):
    print search_log_lines_gz.__name__ + " Starting"
    log_lines = []
    if os.path.exists(logfile):

        lines = []
        print "Reading file:" + logfile
        f = gzip.open(logfile, 'rb')
        # with gzip.open(logfile, 'rb') as f:
        for line in f.read():
            if searchstring in line:
                lines.append(line)
        for line in lines:
            line = line.replace('\"', '')
            line_regex = re.split(regex, line)
            kvstring = line_regex[len(line_regex)-2]
            logline_dict = {}
            logline_dict['log_time'] = line_regex[1]
            logline_dict['class'] = line_regex[2]
            logline_dict['thread'] = line_regex[3]
            logline_dict['logmode'] = line_regex[4]
            logline_dict['FCID'] = line_regex[5]
            logline_dict.update(dict(item.split("=",1) for item in kvstring.split(",")))
            log_lines.append(logline_dict)
    else:
        raise Exception('File not found')
    print search_log_lines_gz.__name__+" Ended"
    return log_lines


def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6
