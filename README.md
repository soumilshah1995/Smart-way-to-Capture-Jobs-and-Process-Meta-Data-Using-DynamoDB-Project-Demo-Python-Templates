
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)]

# Smart way to Capture Jobs and Process Meta Data Using DynamoDB | Project Demo | Python Templates

![Task_1024x576](https://user-images.githubusercontent.com/39345855/196048848-ebb8d6db-d94f-4f44-a8de-22e6331547dc.png)

#### Video : https://www.youtube.com/watch?v=OuqhoAZwFYw

### How to Use

```
class Jobs(object):
    def __init__(self):
        self.process_instance = Process()
        self.__create_process()

    def __create_process(self):
        self.process_instance.create()
        self.process_instance.progress()

    def run(self):
        response_1 = self.step_1()
        response_2 = self.step_2()

        self.process_instance.success()

    @dynamodb_task()
    def step_1(self):
        print("some business rules and code goes here ")
        print("some more business rules and code goes here ")

    @dynamodb_task()
    def step_2(self):
        raise ("OUCH")
        print("some business rules and fucntion calls logs  ")

```

## Explanations 
*     @dynamodb_task()
*  Whenever  you Decorate the method with dynamodb task this will log the meta data in dynamodb. this logs task start time and end time and status of task 
* Status can be Success | Progress | Failed 

##### Since teh method raised exception it marks process Failed 
![image](https://user-images.githubusercontent.com/39345855/196049088-1e9356fe-f348-4a19-92c2-2e89e531aa81.png)

#### tasks 
![image](https://user-images.githubusercontent.com/39345855/196049188-120c6a29-af18-4471-aff0-59587b531553.png)


## GSI

![image](https://user-images.githubusercontent.com/39345855/196049295-8db02650-1d42-427e-938f-9753f27d3c44.png)

*  GS1 gives you all Task for a given Process 
*  GSI2 gives you all process for a guiven day and you can use SK to filter by status or any other things if needed 
*  GSI3 gives you all process for month 

* TTL feilds will delete as the records and process get olders 