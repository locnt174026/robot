# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 09:38:46 2021

@author: kyo
"""
import redis
import json
import time
r = redis.Redis(
    host='localhost',
    port=6379, db = 1,
    password='')

arr = [[68,15],[4,5]] 

def set_coordinate_to_redis(path, start, end):
    key = str(start) + "," + str(end)
    json_arr = list()
    for point in path:
        temp = {
                'x':point[0],
                'y':point[1]
                }
        json_arr.append(temp)


    # Convert python dict to JSON str and save to Redis
    json_arr = json.dumps(json_arr)
    r.set(key, json_arr)    

start_time =time.time()
string_1= eval(r.get('1,11,33,2'))
print(string_1)
print(time.time()-start_time)