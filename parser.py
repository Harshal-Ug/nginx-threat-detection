import re
import csv
parsed_logs = []

pattern = r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\[(?P<timestamp>[^\]]+)\]\s"(?P<method>\w+)\s(?P<url>\S+)\s(?P<http_version>[^"]+)"\s(?P<status>\d+)\s(?P<size>\d+)\s"[^"]*"\s"(?P<user_agent>[^"]*)"'

with open ("nginx.log", 'r') as f:
    for line in f:
        match = re.search(pattern,line)
        if match:
            parsed_logs.append(match.groupdict())

with open ("nginx_logs.csv",'w',newline = '') as f:
    fieldnames = ['ip','timestamp','method','url','http_version','status','size','user_agent']
    writer = csv.DictWriter(f,fieldnames)
    writer.writeheader()
    writer.writerows(parsed_logs)

print("Parsed logs written to nginx_logs.csv")