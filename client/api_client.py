import linecache
import json
import requests 

start = 1
end = 50
i=start

while i <= end:     
    line = linecache.getline('./output.txt', i)
    myjson = json.loads(line)
    response = requests.post('http://localhost:80/invoiceitem', json=myjson)
    i+=1