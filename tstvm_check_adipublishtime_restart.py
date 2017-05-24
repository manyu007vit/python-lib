from log_utils import search_log_lines, search_log_lines_gz
import datetime
import os

dirname = '/opt/nds/tstvm/log/'

now = datetime.datetime.now()
myfile = open(str(now)+'.csv', 'w')

myfile.write('scheduleInstanceId' + ',' + 'eventStartDateTime' + ',' + 'eventEndDateTime' + ',' + 'AdiPublishTime' + '\n')

# Search for logline and perform some action
try:
    count = 0
    min1 = 0
    max1 = 0
    avg = 0
    sum_array = 0
    diff_arr = []
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
                enddatetime = datetime.datetime.strptime(l['eventStartDateTime'], '%Y/%m/%d %H:%M:%S.%f')
                log_time = datetime.datetime.strptime(l['log_time'], '%Y/%m/%d %H:%M:%S.%f')
                diff = int((log_time - enddatetime).total_seconds() / 60)
                diff_arr.append(diff)
                count += 1
                myfile.write(l['scheduleInstanceId'] + ',' + l['eventStartDateTime'] + ',' + l['eventEndDateTime'] + ',' + str(diff) + '\n')
                # print "published {0}min after the event ended".format(diff)
    sum_array = sum(diff_arr)
    avg = sum_array / count
    min1 = min(diff_arr)
    max1 = max(diff_arr)
    print min1, max1, avg, sum_array, count
    myfile.write('\n')
    myfile.write('\n')
    myfile.write('count' + ',' + 'min' + ',' + 'max' + ',' + 'avg' + '\n')
    myfile.write(str(count) + ',' + str(min1) + ',' + str(max1) + ',' + str(avg) + '\n')
except Exception as error:
    print error.message
    myfile.close()
    exit(2)
myfile.close()
