try:
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

    load_dotenv(".env")

except Exception as e:
    print("Error: {}".format(e))


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
    sk = NumberAttribute(null=True)

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


# --------------------------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------------------------


class Status(Enum):

    success = "success"
    progress = "progress"
    failed = "failed"


class Datetime(object):
    @staticmethod
    def get_year_month_day():
        """
        Return Year month and day
        :return: str str str
        """
        dt = datetime.now()
        year = dt.year
        month = dt.month
        day = dt.day
        return year, month, day


class Process:
    def __init__(self):
        self.process_id = None

    def create(self):
        try:
            self.process_id = f"Process#{uuid.uuid4().__str__()}"
            year, month, day = Datetime.get_year_month_day()

            ProcessModel(
                pk=self.process_id,
                sk=self.process_id,
                process_start_date=str(datetime.now()),
                ttl=set_ttl_time(),
                gsi_date_month=f"{year}-{month}",
                gsi_date_day=f"{year}-{month}-{day}",
            ).save()

            return True

        except Exception as e:
            return None

    def failed(self, error_message="Error"):
        try:
            print("inside failed process ", self.process_id)
            for items in ProcessModel.query(str(self.process_id), limit=1):
                print("process",self.process_id)
                print("status", Status.failed.value)

                items.process_status = str(Status.failed.value)
                items.process_error_message = str(error_message)
                items.process_end_date = str(datetime.now())

                items.save()

            return True
        except Exception as e:
            print("process failed close", e)
            return False

    def success(self):
        try:
            for items in ProcessModel.query(str(self.process_id)):
                items.process_status = Status.success.value
                items.process_end_date = str(datetime.now())
                items.save()
            return True
        except Exception as e:
            return False

    def progress(self):
        try:
            for items in ProcessModel.query(str(self.process_id)):
                items.process_status = str(Status.progress.value)
                items.save()
            return True
        except Exception as e:
            print("Failed to close process ", e)
            return False


class Task:
    def __init__(self):
        self.task_id = None

    def create(self, name="", process_id=""):
        try:
            self.task_id = f"Task#${uuid.uuid4().__str__()}"
            year, month, day = Datetime.get_year_month_day()
            ProcessModel(
                pk=self.task_id,
                sk=self.task_id,
                task_start_date=str(datetime.now()),
                ttl=set_ttl_time(),
                # gsi_date_month=f"{year}-{month}",
                # gsi_date_day=f"{year}-{month}-{day}",
                task_name=name,
                gs1_process=process_id
            ).save()
            return True

        except Exception as e:
            return None

    def failed(self, error_message="Error"):
        try:

            for items in ProcessModel.query(str(self.task_id)):

                items.task_status = str(Status.failed.value)
                items.task_error_message = str(error_message,)
                items.task_end_date = str(datetime.now())
                items.save()
            return True
        except Exception as e:
            return False

    def success(self):
        try:
            for items in ProcessModel.query(str(self.task_id)):
                items.task_status = Status.success.value.__str__()
                items.task_end_date = str(datetime.now())

                items.save()
            return True
        except Exception as e:
            print("faield to close task ")
            return False

    def progress(self):
        try:
            for items in ProcessModel.query(str(self.task_id)):
                items.task_status = Status.progress.value
                items.save()
            return True
        except Exception as e:
            return False


# ------------------------------------------------------------------------------------------------
# Decorators
# --------------------------------------------------------------------------------------------


def dynamodb_task(argument=None):

    def real_decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            process_id = self.process_instance.process_id

            task_instance = Task()
            task_instance.create(name=function.__name__.__str__(), process_id=process_id)

            try:
                task_instance.progress()

                if kwargs == {}:
                    response = function(self)
                else:
                    response = function(self, kwargs)

                task_instance.success()
                return response
            except Exception as e:
                print("*******ERRROR*********", e)
                response = {"status": -1, "error": {"message": str(e)}}

                task_instance.failed(error_message=str(response))
                self.process_instance.failed(error_message=str(response))
                raise Exception(response)



        return wrapper

    return real_decorator


# ------------------------------------------------------------------------------------------------
# Business Class

#
class Jobs(object):
    def __init__(self):
        self.process_instance = Process()
        self.__create_process()

    def __create_process(self):
        self.process_instance.create()
        self.process_instance.progress()

    def run(self):
        response_1 = self.step_1_start_jobs()
        response_2 = self.step_2_hello()

        self.process_instance.success()

    @dynamodb_task()
    def step_1_start_jobs(self):
        print("some business rules and code goes here ")
        print("some more business rules and code goes here ")

    @dynamodb_task()
    def step_2_hello(self):
        raise Exception ("ERROR ")





# --------------------------------------------------------------------------------------------



def main():

    helper =Jobs()
    helper.run()

main()