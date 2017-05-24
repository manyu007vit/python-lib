from log_utils import search_log_lines, search_log_lines_gz, timedelta_total_seconds
import datetime
import os

dirname = '/opt/nds/tstvm/log/'

now = datetime.datetime.now()
myfile = open(str(now)+'.csv', 'w')

# Search for logline and perform some action
try:
    count_dict = {}
    for filename in os.listdir(dirname):
        if 'tstvm.log' in filename and filename.endswith(".gz"):
            log_lines = search_log_lines_gz(dirname + filename, searchstring='Pushing Status Recieved')
        elif 'tstvm.log' in filename and filename.endswith(".log"):
            log_lines = search_log_lines(dirname + filename, lookbacktime=5000, searchstring='Pushing Status Recieved')
        else:
            continue
        # print log_lines
        for l in log_lines:
            if l['user'] == 'CATCHUP':
                if l['scheduleInstanceId'] in count_dict:
                    count_dict[l['scheduleInstanceId']]['times'].append({'log_time': l['log_time'], 'thread': l['thread']})
                    count_dict[l['scheduleInstanceId']]['count'] += 1
                else:
                    count_dict[l['scheduleInstanceId']] = {'times': [{'log_time': l['log_time'], 'thread': l['thread']}], 'count': 1}

    for key, value in count_dict.items():
        # if value['count'] == 2:
        #     log_time1 = datetime.datetime.strptime(value['times'][0]['log_time'], '%Y/%m/%d %H:%M:%S.%f')
        #     log_time2 = datetime.datetime.strptime(value['times'][1]['log_time'], '%Y/%m/%d %H:%M:%S.%f')
        #     diff = int((log_time1 - log_time2).total_seconds() / 60)
        #     if diff < 60:
        #         myfile.writelines(key + ',' + str(value) + '\n')
        if value['count'] > 1:
            myfile.writelines(key + ',' + str(value) + '\n')
except Exception as error:
    print error.message
    myfile.close()
myfile.close()
