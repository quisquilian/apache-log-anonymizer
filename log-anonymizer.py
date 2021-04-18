import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from apachelogs import LogParser
from pathlib import Path
from ip2geotools.databases.noncommercial import DbIpCity

#function to ingest apache logs and parse out fields
def logFileParse(paths):
    for path in paths:
        path_in_str = str(path)
        with open(path_in_str) as fp:
            for entry in parser.parse_lines(fp):

                host = entry.directives["%h"]
                logName = (str(entry.directives["%l"]) == 'None' and '-') or str(entry.directives["%l"])
                user = (str(entry.directives["%u"]) == 'None' and '-') or str(entry.directives["%u"])
                time = str(entry.request_time)
                request = entry.directives["%r"]
                status = entry.directives["%>s"]
                bytesSent = entry.directives["%O"]

                lst.append([host,logName,user,time,request,status,bytesSent])

#function to call ip2geotools api and get country code by IP address
def getCountryByIP(lst):
    for i in lst:
        response = DbIpCity.get(i[0], api_key='free')
        i[0] = response.country
        
#define variables
projectLocation = '/home/jshivers/projects/apache-log-anonymizer'
parser = LogParser("%h %l %u %t \"%r\" %>s %O")
lst = []
paths = Path(projectLocation + '/logs').glob('*.log.*')
cols = ['host', 'logName', 'user', 'time', 'request', 'status', 'bytesSent']

#call ingest and transformation functions
logFileParse(paths)
getCountryByIP(lst)

#create pandas dataframe
df = pd.DataFrame(lst, columns=cols)

#create numpy array in case of further analysis
#a = np.array(lst)
#a[:,0]

#print cleaned data to txt file
with open(projectLocation + '/output/out.txt', 'w', encoding="utf-8") as x:
    for sub_list in lst:
        for item in sub_list:  #Since attempt to write whole giv error 
            x.write(str(item) + ' ')
        x.write("\n")

#print dataframe to parquet file
table = pa.Table.from_pandas(df)
pq.write_table(table, projectLocation + '/output/out.parquet')

#read parquet file
#table2 = pq.read_table('C:/projects/apache-log-anonymizer/output/example.parquet')
#table2.to_pandas()