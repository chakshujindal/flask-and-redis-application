from flask import Flask, jsonify, request, Response
from CacheModel import *
from settings import *
import redis
import json
import random
import time

redis_host = ""  # pass your redis server ip inside double quotes eg: "175.0.1.1"
redis_port = 6379
redis_password = ""  # pass your redis password inside double quotes eg: "Password@123"
                # Setting password is optional, if not required, comment this line and remove the password=redis_password in line 15


redis_cache = redis.Redis(host=redis_host, port=redis_port, password=redis_password)


def response_time(start_time, end_time):
    resp_time = end_time - start_time
    return resp_time


# Function to GET all the cache instances
# With caching, with database
@app.route("/caching_app/cache", methods=["GET"])
def get_all_cache():
    start_time = time.time()
    cache_all = Cache.get_all_cache()
    for cache in cache_all:
        update_in_redis = redis_cache.set("cache" + str(cache['cacheID']), str(cache))
    end_time = time.time()
    resp_time = end_time - start_time
    return jsonify({'cache': cache_all})


# Function to GET all the cache instances
# Without caching, only database
@app.route("/caching_app", methods=["GET"])
def get_all_cache_db():
    start_time = time.time()
    cache_all = Cache.get_all_cache()
    end_time = time.time()
    resp_time = end_time - start_time
    return jsonify({'cache': cache_all})


# Function to GET the specific cache instance by providing cacheID
# With caching, with database
@app.route("/caching_app/cache/id/<cacheID>", methods=["GET"])
def get_by_id(cacheID):
    start_time = time.time()
    cache_instance = json.dumps(redis_cache.get('cache'+cacheID).decode())
    if not cache_instance:
        cache_instance = Cache.get_cache_by_id(cacheID)
        redis_cache.set('cache' + cache_instance.cacheID, str(cache_instance.json()))
        # redis_cache.set('cache' + cache_instance.cacheID, json.dumps(cache_instance.json()))
        # redis_cache.set('cache' + cache_instance.cacheID, jsonify(cache_instance))
    end_time = time.time()
    resp_time = end_time - start_time
    return jsonify({'cache': json.loads(cache_instance)})


# Function to GET the specific cache instance by providing cacheID
# Without caching, only database: possible as cacheID is key for redis, one can only fetch redis data with the key
@app.route("/caching_app/id/<cacheID>", methods=["GET"])
def get_by_id_db(cacheID):
    start_time = time.time()
    cache_instance = Cache.get_cache_by_id(cacheID)
    end_time = time.time()
    resp_time = end_time - start_time
    return jsonify({'cache': cache_instance})


# Function to GET the specific cache instance by providing nodeName
# Without caching, only database : as cacheID is key for redis, and one cannot fetch redis data with a fragment of value of the key
# to be used if NAME is unique: Going forward, our service will only allow unique names, made this function keeping future enhancements in mind
@app.route("/caching_app/name/<nodeName>", methods=["GET"])
def get_by_name_db(nodeName):
    start_time = time.time()
    cache_instance = Cache.get_cache_by_name(nodeName)
    end_time = time.time()
    resp_time = end_time - start_time
    return jsonify({'cache': cache_instance})


# Function to GET the specific cache instance by providing ip
# Without caching, only database : as cacheID is key for redis, and one cannot fetch redis data with a fragment of value of the key
# to be used if IP is unique
@app.route("/caching_app/ip/<ip>", methods=["GET"])
def get_by_ip_db(ip):
    start_time = time.time()
    cache_instance = Cache.get_cache_by_ip(ip)
    end_time = time.time()
    resp_time = end_time - start_time
    return jsonify({'cache': cache_instance})


# Function to UPDATE cache information by providing cacheID
# With caching, with database
@app.route("/caching_app/cache/<cacheID>", methods=['PUT'])
def update_cache(cacheID):
    start_time = time.time()
    cache_instance = request.get_json(force=True)
    if 'nodeName' in cache_instance:
        new = Cache.update_name(cacheID, cache_instance['nodeName'])
        redis_cache.set('cache' + new.cacheID, str(new.json()))
        # redis_cache.set('cache' + new.cacheID, json.dumps(new.json()))
    response = Response("Successfully updated cache instance", 204, mimetype='application/json')
    # response.headers['Location'] = "/caching_app/cache/" + str(cacheID)
    end_time = time.time()
    resp_time = end_time - start_time
    return response


# Function to UPDATE cache information by providing cacheID
# Without caching, only database
@app.route("/caching_app/<cacheID>", methods=['PUT'])
def update_cache_db(cacheID):
    start_time = time.time()
    cache_instance = request.get_json(force=True)
    if 'nodeName' in cache_instance:
        Cache.update_name(cacheID, cache_instance['nodeName'])
    response = Response("Successfully updated cache instance", 204, mimetype='application/json')
    # response.headers['Location'] = "/caching_app/" + str(cacheID)
    end_time = time.time()
    resp_time = end_time - start_time
    return response


# Function to POST cache details
# With caching, with database
@app.route("/caching_app/cache", methods=["POST"])
def post_cache():
    start_time = time.time()
    data = request.get_json(force=True)
    new_cache = Cache.add_instance(data['cacheID'], data['nodeName'], data['highAvailabilityMode'], data['status'], data['comment'], data['creationDate'], data['modificationDate'], data['asset_status'], data['ip'], data['type'], data['availabilityZone'], data['network'])
    # redis_cache.set('cache' + new_cache.cacheID, json.dumps(new_cache.json()))
    redis_cache.set('cache' + new_cache.cacheID, str(new_cache.json()))
    response = Response("success", status=201, mimetype='application/json')
    # response.headers['Location'] = "/caching_app/cache/" + str(data["cacheID"])
    end_time = time.time()
    resp_time = end_time - start_time
    return response


# Function to POST cache details
# Without caching, only database
@app.route("/caching_app", methods=["POST"])
def post_cache_db():
    start_time = time.time()
    data = request.get_json(force=True)
    Cache.add_instance(data['cacheID'], data['nodeName'], data['highAvailabilityMode'], data['status'], data['comment'], data['creationDate'], data['modificationDate'], data['asset_status'], data['ip'], data['type'], data['availabilityZone'], data['network'])
    response = Response("success", status=201, mimetype='application/json')
    # response.headers['Location'] = "/caching_app/" + str(data["cacheID"])
    end_time = time.time()
    resp_time = end_time - start_time
    return response


# Function to DELETE cache instance by providing cacheID
# With caching, with database
@app.route("/caching_app/cache/id/<cacheID>", methods=["DELETE"])
def delete_by_id(cacheID):
    start_time = time.time()
    if Cache.delete_cache_by_id(cacheID):
        redis_cache.delete('cache'+cacheID)
        response = Response("Deletion successful through cache ID", status=204)
        end_time = time.time()
        resp_time = end_time - start_time
        return response


# Function to DELETE cache instance by providing cacheID
# Without caching, only database: possible as cacheID is key for redis, one can only fetch redis data with the key
@app.route("/caching_app/id/<cacheID>", methods=["DELETE"])
def delete_by_id_db(cacheID):
    start_time = time.time()
    if Cache.delete_cache_by_id(cacheID):
        response = Response("Deletion successful through cache ID", status=204)
        end_time = time.time()
        resp_time = end_time - start_time
        return response


# Function to DELETE cache instance by providing nodeName
# Without caching, only database : as cacheID is key for redis, and one cannot fetch redis data with a fragment of value of the key
# to be used if NAME is unique: Going forward, our service will only allow unique names, made this function keeping future enhancements in mind
@app.route("/caching_app/name/<nodeName>", methods=["DELETE"])
def delete_by_name_db(nodeName):
    start_time = time.time()
    if Cache.delete_cache_by_name(nodeName):
        response = Response("Deletion successful through cache name", status=204)
        end_time = time.time()
        resp_time = end_time - start_time
        return response


# Function to DELETE cache instance by providing ip
# Without caching, only database : as cacheID is key for redis, and one cannot fetch redis data with a fragment of value of the key
# to be used if IP is unique
@app.route("/caching_app/ip/<ip>", methods=["DELETE"])
def delete_by_ip_db(ip):
    start_time = time.time()
    if Cache.delete_cache_by_ip(ip):
        response = Response("Deletion successful through asset IP", status=204)
        end_time = time.time()
        resp_time = end_time - start_time
        return response


if __name__ == "__main__":

    # Script to create random dataset: creating 30,000 data entries
    # uncomment the below code from "for in range(1, 30000)" to "redis_cache.set('cache' + instance.cacheID, instance_dict)" to create database

    # for i in range(1, 30000):
    #     p = random.randint(0, 1)
    #     q = random.randint(0, 1)
    #     r = random.randint(0, 1)
    #     caID = i
    #     nName = "Instance" + str(i)
    #     haMode = "No" if p == 0 else "Yes"
    #     sts = "UP" if p == 1 else "DOWN"
    #     comm = "For Instance" + str(i)
    #     cDate = "2020-01-28"
    #     mDate = "2020-01-29"
    #     asset_sts = "GOOD" if q == 1 else "BAD"
    #     ip_adr = "175." + str(p) + "." + str(p + q + r) + "." + str(r + q)
    #     typ = "redis_cache"
    #     av_zone = "zone-1" if r == 0 else "zone-2"
    #     ntwrk = "network-1" if r == 1 else "network-2"
    #
    #     instance = Cache.add_instance(caID, nName, haMode, sts, comm, cDate, mDate, asset_sts, ip_adr, typ, av_zone,
    #                                   ntwrk)
    #     instance_dict =str(instance.json())
    #     print(instance_dict)
    #     redis_cache.set('cache' + instance.cacheID, instance_dict)
    app.run()
