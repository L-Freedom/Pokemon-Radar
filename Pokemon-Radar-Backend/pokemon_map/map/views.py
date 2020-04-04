from django.shortcuts import render
from django.http import HttpResponse
import json

import boto3
import s2sphere

from db_accessor import *

SQS_QUEUE_NAME = "awseb-e-nn8ptrekuw-stack-AWSEBWorkerQueue-F5JLXXQV1LR3"
# Create your views here.

def break_down_area_to_cell(north, south, west, east):
    result = []

    region = s2sphere.RegionCoverer()
    region.min_level = 15
    region.max_level = 15
    p1 = s2sphere.LatLng.from_degrees(north, west)
    p2 = s2sphere.LatLng.from_degrees(south, east)

    rect = s2sphere.LatLngRect.from_point_pair(p1, p2)
    area = rect.area()

    if(area * 1000 * 1000 * 100 > 7):
        print DBG + "The area is too big, return ..."
        #logger.info(DBG + "The area is too big, return ...")
        return

    cell_ids = region.get_covering(rect)
    result += [cell_id.id() for cell_id in cell_ids]

    return result

def scan_area(north, south, west, east):

    #1.Find all points to search within the area
    cell_ids = break_down_area_to_cell(north, south, west, east)
    if(cell_ids is None):
        return


    #2. Send request to elastic beanstalk worker server
    work_queue = boto3.resource(
        'sqs',
        aws_access_key_id="AKIAIRWWDGYARZOOHJYQ",
        aws_secret_access_key="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",
        region_name="us-west-2").get_queue_by_name(QueueName=SQS_QUEUE_NAME)

    for cell_id in cell_ids:
        work_queue.send_message(MessageBody=json.dumps({"cell_id":cell_id}))

    return


def pokemons(request):

    #1. Get longitude and latitude
    north = request.GET["north"]
    south = request.GET["south"]
    east = request.GET["east"]
    west = request.GET["west"]

    #2. Query database
    result = get_pokemons_from_db(north, south, west, east)

    #3. Publish for crawl jobs
    scan_area(float(north), float(south), float(west), float(east))

    return HttpResponse(json.dumps(result))