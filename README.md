# Apache Log File Anonymizer

This project takes Apache logs as an input source and anonymizes any personally identifiable information (PII) contained within each file. In the case of sample exercise, IP address is considered PII. The Python script leverages a public API to lookup the country code for each IP address in the log files. When the data is written to file, the IP address is replaced with the country code.

Requirements
------------

Below python modules are required to run the program.

* ```pip install numpy```
* ```pip install pandas```
* ```pip install apachelogs```
* ```pip install ip2geotools```
* ```pip install pyarrow```

Usage
-----

* Step 1
  
  Before running the script, you will need to update the project location variable (line 33) in the python file. Paste in the location where you stored the project.
    

* Step 2

  Execute script
  ```
  $ python log-anonymizer.py
  ```

Assumptions
-----------

* This program assumes log files are saved at a file location (i.e. local computer, server, shared network drive, mounted file share, ftp, etc).

* This program assumes the Apache log format is set to **"%h %l %u %t \"%r\" %>s %O**

* The file output formats consist of txt and parquet. I chose txt format mainly for readability. As the volume of data scales, I would recommend parquet for its compression efficiencies. 

Future Improvements
-------------------

* One area to improve upon would be to enable a more efficient process for obtaining country code by IP address. This program currently leverages a free API service to retrieve the country code. This step in the program is very costly. With more time, I would build a local data store which contains IP ranges by country and leverage this for much lower latency.

* One area to improve upon would be to leverage Kafka to publish apache logs to topics in real time. The log anonymizer could be a consumer of these Kafka events and process them as they occur.

* One area to improve upon would be around process performance. As the data volume increases, the compute resources will need to scale. Deploying this application on a spark cluster would greatly improve performance.