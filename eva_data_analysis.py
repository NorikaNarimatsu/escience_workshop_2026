# https://data.nasa.gov/resource/eva.json (with modifications)

import json
import csv
import datetime as dt
import matplotlib.pyplot as plt


input_file = open('eva-data.json', 'r')
output_file = open('eva_data_analysis.csv','w')
graph_file = 'cumulative_eva_graph.png'

fieldnames = ("EVA #", "Country", "Crew    ", "Vehicle", "Date", "Duration", "Purpose")

data=[]

for i in range(375):
    line=input_file.readline()
    print(line)
    data.append(json.loads(line[1:-1]))

#data.pop(0)
## Comment out this bit if you don't want the spreadsheet

csv_writer=csv.writer(output_file)


time = []
date =[]

index=0
for record in data:
    print(data[index])
    # and this bit
    csv_writer.writerow(data[index].values())
    if 'duration' in data[index].keys():
        duration_str=data[index]['duration']
        if duration_str == '':
            pass
        else:
            time_obj=dt.datetime.strptime(duration_str,'%H:%M')
            hours_decimal = dt.timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second).total_seconds()/(60*60)
            print(time_obj,hours_decimal)
            time.append(hours_decimal)
            if 'date' in data[index].keys():
                date.append(dt.datetime.strptime(data[index]['date'][0:10], '%Y-%m-%d'))
                #date.append(data[j]['date'][0:10])

            else:
                time.pop(0)
    index+=1

cumulative_time=[0]
for duration in time:
    cumulative_time.append(cumulative_time[-1]+duration)

date,time = zip(*sorted(zip(date, time)))

plt.plot(date,cumulative_time[1:], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
