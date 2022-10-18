# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
try:
    # Flask modules
    from flask   import render_template, request
    from jinja2  import TemplateNotFound

    # App modules
    from apps import app
    import boto3
    from datetime import datetime
    from flask import request

    import pynamodb.attributes as at
    from pynamodb.models import Model
    from pynamodb.attributes import *
    import uuid
    import os
    from pynamodb.connection import Connection
    from pynamodb.transactions import TransactWrite
    from pynamodb.exceptions import TransactWriteError
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
    from functools import wraps, partial
    from enum import Enum
    import logging
    from time import sleep

    from dotenv import load_dotenv
    load_dotenv("../.env")

except Exception as e:
    print("Error",e)
try:
    load_dotenv("../.env")
except Exception as e:
    print("Error",e)

print("""
os.getenv("TABLE_NAME")
""")
print(os.getenv("TABLE_NAME"))



# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template( 'home/' + path, segment=segment )
    
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None


def set_ttl_time(years=1):
    timestamp = datetime.timestamp(datetime.now() + relativedelta(years=years))
    return round(timestamp)


class ProcessModel(Model):
    class Meta:
        table_name = os.getenv("TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        region = os.getenv("AWS_REGION")

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)

    # --------Process --------------
    process_start_date = UnicodeAttribute(null=True)
    process_end_date = UnicodeAttribute(null=True)
    process_status = UnicodeAttribute(null=True)
    process_error_message = UnicodeAttribute(null=True)
    process_log_s3_path = UnicodeAttribute(null=True)

    # --------TASK --------------
    task_name = UnicodeAttribute(null=True)
    task_start_date = UnicodeAttribute(null=True)
    task_end_date = UnicodeAttribute(null=True)
    task_status = UnicodeAttribute(null=True)
    task_error_message = UnicodeAttribute(null=True)

    # ---------------TYPE----------------
    job_type = UnicodeAttribute(null=True)

    # ---------------GSI----------------
    gs1_process = UnicodeAttribute(null=True)
    gsi_date_month = UnicodeAttribute(null=True)
    gsi_date_day = UnicodeAttribute(null=True)

    # ---------------House keeping Field----------------
    ttl = NumberAttribute(null=True)
    createdBy = NumberAttribute(null=True)
    createdAt = NumberAttribute(null=True)


# ----------------VIEW MODEL 1 --------------------------------
class ProcessViewIndex(GlobalSecondaryIndex):

    """
    This class represents a global secondary index
    """

    class Meta:

        index_name = os.getenv("GS1_INDEX")
        projection = AllProjection()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        region = os.getenv("AWS_REGION")

    gs1_process = UnicodeAttribute(hash_key=True)


class ProcessView(Model):
    """
    A test model that uses a global secondary index
    """

    class Meta:
        table_name = os.getenv("TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        region = os.getenv("AWS_REGION")

    pk = UnicodeAttribute(null=True)
    sk = UnicodeAttribute(null=True)

    # --------Process --------------
    process_start_date = UnicodeAttribute(null=True)
    process_end_date = UnicodeAttribute(null=True)
    process_status = UnicodeAttribute(null=True)
    process_error_message = UnicodeAttribute(null=True)
    process_log_s3_path = UnicodeAttribute(null=True)

    # --------TASK --------------
    task_name = UnicodeAttribute(null=True)
    task_start_date = UnicodeAttribute(null=True)
    task_end_date = UnicodeAttribute(null=True)
    task_status = UnicodeAttribute(null=True)
    task_error_message = UnicodeAttribute(null=True)

    # ---------------TYPE----------------
    job_type = UnicodeAttribute(null=True)

    # ---------------GSI----------------
    gsi_date_month = UnicodeAttribute(null=True)
    gsi_date_day = UnicodeAttribute(null=True)

    # ---------------House keeping Field----------------
    ttl = NumberAttribute(null=True)
    createdBy = NumberAttribute(null=True)
    createdAt = NumberAttribute(null=True)

    gs1_process = UnicodeAttribute(hash_key=True)
    view_index = ProcessViewIndex()


# ----------------VIEW MODEL 2 --------------------------------


class DayViewIndex(GlobalSecondaryIndex):

    """
    This class represents a global secondary index
    """

    class Meta:

        index_name = os.getenv("GS2_DAY_INDEX")
        projection = AllProjection()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        region = os.getenv("AWS_REGION")

    gsi_date_day = UnicodeAttribute(hash_key=True)


class DayView(Model):
    """
    A test model that uses a global secondary index
    """

    class Meta:
        table_name = os.getenv("TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        region = os.getenv("AWS_REGION")

    pk = UnicodeAttribute(null=True)
    sk = UnicodeAttribute(null=True)

    # --------Process --------------
    process_start_date = UnicodeAttribute(null=True)
    process_end_date = UnicodeAttribute(null=True)
    process_status = UnicodeAttribute(null=True)
    process_error_message = UnicodeAttribute(null=True)
    process_log_s3_path = UnicodeAttribute(null=True)

    # --------TASK --------------
    task_name = UnicodeAttribute(null=True)
    task_start_date = UnicodeAttribute(null=True)
    task_end_date = UnicodeAttribute(null=True)
    task_status = UnicodeAttribute(null=True)
    task_error_message = UnicodeAttribute(null=True)

    # ---------------TYPE----------------
    job_type = UnicodeAttribute(null=True)

    # ---------------GSI----------------
    gs1_process = UnicodeAttribute(null=True)
    gsi_date_month = UnicodeAttribute(null=True)

    # ---------------House keeping Field----------------
    ttl = NumberAttribute(null=True)
    createdBy = NumberAttribute(null=True)
    createdAt = NumberAttribute(null=True)

    gsi_date_day = UnicodeAttribute(hash_key=True)
    view_index = DayViewIndex()


# ----------------VIEW MODEL 3 --------------------------------


class MonthIndex(GlobalSecondaryIndex):

    """
    This class represents a global secondary index
    """

    class Meta:

        index_name = os.getenv("GSI_MONTH_INDEX")
        projection = AllProjection()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        region = os.getenv("AWS_REGION")

    gsi_date_month = UnicodeAttribute(hash_key=True)


class MonthView(Model):
    """
    A test model that uses a global secondary index
    """

    class Meta:
        table_name = os.getenv("TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        region = os.getenv("AWS_REGION")

    pk = UnicodeAttribute(null=True)
    sk = UnicodeAttribute(null=True)

    # --------Process --------------
    process_start_date = UnicodeAttribute(null=True)
    process_end_date = UnicodeAttribute(null=True)
    process_status = UnicodeAttribute(null=True)
    process_error_message = UnicodeAttribute(null=True)
    process_log_s3_path = UnicodeAttribute(null=True)

    # --------TASK --------------
    task_name = UnicodeAttribute(null=True)
    task_start_date = UnicodeAttribute(null=True)
    task_end_date = UnicodeAttribute(null=True)
    task_status = UnicodeAttribute(null=True)
    task_error_message = UnicodeAttribute(null=True)

    # ---------------TYPE----------------
    job_type = UnicodeAttribute(null=True)

    # ---------------GSI----------------
    gs1_process = UnicodeAttribute(null=True)
    gsi_date_day = UnicodeAttribute(null=True)

    # ---------------House keeping Field----------------
    ttl = NumberAttribute(null=True)
    createdBy = NumberAttribute(null=True)
    createdAt = NumberAttribute(null=True)

    gsi_month_day = UnicodeAttribute(hash_key=True)
    view_index = DayViewIndex()


@app.route("/get_data_day", methods=["GET", "POST"])
def get_data_day():
    print("in...")
    data = json.loads(dict(request.form).get("data"))
    date = data.get("date")
    print("date", date)
    items = [json.loads(process.to_json()) for process in DayView.view_index.query(date , scan_index_forward=True)]
    return {"data": items}

@app.route("/get_tasks", methods=["GET", "POST"])
def get_tasks():
    data = json.loads(dict(request.form).get("data"))
    process = data.get("process")
    print("process", process)

    items = [json.loads(process.to_json()) for process in
             ProcessView.view_index.query(process , scan_index_forward=True)
             ]
    return {"data": items}