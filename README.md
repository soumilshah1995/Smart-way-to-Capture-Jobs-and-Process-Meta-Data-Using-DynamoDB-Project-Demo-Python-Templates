
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)]

# Smart way to Capture Jobs and Process Meta Data Using DynamoDB | Project Demo | Python Templates | Alerts 





#### Overview: 
In this article, I will present a solution that will allow you to easily monitor and capture status for running jobs and tasks. Capturing the details allows us to determine how long a process takes, what the status of the process is, and if necessary, dive into Task level details. When a job runs, it generates a unique process (GGUID), which represents the running or ongoing work. The process will have a start and end time and will display the status of ongoing activities. Each task in the process will have a name, a start and end time, and a status. If a task fails, the process status will be marked as failed. If a user needs more visibility for a function, they can simply log the function with decorator and all details will be captured in dynamodb for that task. I will demonstrate how to design and implement these solutions.

# Architecture 
![capture drawio](https://user-images.githubusercontent.com/39345855/197229798-7c209d51-b44d-4856-860e-b6fab1d63957.png)


# Frontend 
![image](https://user-images.githubusercontent.com/39345855/196523801-54b00e18-f1a3-4ea3-8b6c-f153b72dee8b.png)

* Shows all process that ran for given Day 
![p2](https://user-images.githubusercontent.com/39345855/196511340-d5c27bec-235c-48f6-bcb0-f68b383aa9d2.PNG)
* Shows all Task for Given Process for given Day (Query GSI View )

### Alerts 
![image](https://user-images.githubusercontent.com/39345855/197229526-39d072db-c600-47d7-a1b9-e6c79958fe7c.png)
* Sends Alerts for failed process using kinesis streams lambda and SNS 


#### Video : https://www.youtube.com/watch?v=OuqhoAZwFYw

#### Read Article : https://www.linkedin.com/pulse/smart-way-capture-monitor-report-status-python-jobs-using-soumil-shah

#### change and add your email where you would like
please email address in  severless.yml 
Email address will recive alerts for failed process 
```
  MySubscription:
      Type: AWS::SNS::Subscription
      Properties:
        Endpoint: your_email.com
        Protocol: email
        TopicArn: !Ref 'SNSTopic'
```


#### Install and Deploy Stack 

```
command 1: npm install -g serverless

command 2: serverless config credentials --provider aws --key XXXX  --secret XXXXX -o

command 3: serverless deploy

```

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
        raise Exception ("OUCH")
        print("some business rules and fucntion calls logs  ")

```

## Explanations 
*     @dynamodb_task()
*  Whenever  you Decorate the method with dynamodb task this will log the meta data in dynamodb. this logs task start time and end time and status of task 
* Status can be Success | Progress | Failed 

##### Since the method raised exception it marks process Failed 
![image](https://user-images.githubusercontent.com/39345855/196049088-1e9356fe-f348-4a19-92c2-2e89e531aa81.png)

##### Exceptionj we generated in code can benn seen 
![image](https://user-images.githubusercontent.com/39345855/196055412-f7ffd009-057d-493d-86eb-44e0c132ac4d.png)


#### tasks 
![image](https://user-images.githubusercontent.com/39345855/196049188-120c6a29-af18-4471-aff0-59587b531553.png)


## GSI

![image](https://user-images.githubusercontent.com/39345855/196049295-8db02650-1d42-427e-938f-9753f27d3c44.png)

*  GS1 gives you all Task for a given Process 
*  GSI2 gives you all process for a guiven day and you can use SK to filter by status or any other things if needed 
*  GSI3 gives you all process for month 

* TTL feilds will delete as the records and process get olders 





-------------------------------------------------------------------------------------
## Soumil Nitin Shah 
Bachelor in Electronic Engineering |
Masters in Electrical Engineering | 
Master in Computer Engineering |

* Website : http://soumilshah.com/
* Github: https://github.com/soumilshah1995
* Linkedin: https://www.linkedin.com/in/shah-soumil/
* Blog: https://soumilshah1995.blogspot.com/
* Youtube : https://www.youtube.com/channel/UC_eOodxvwS_H7x2uLQa-svw?view_as=subscriber
* Facebook Page : https://www.facebook.com/soumilshah1995/
* Email : shahsoumil519@gmail.com
* projects : https://soumilshah.herokuapp.com/project


* I earned a Bachelor of Science in Electronic Engineering and a double master’s in Electrical and Computer Engineering. I have extensive expertise in developing scalable and high-performance software applications in Python. I have a YouTube channel where I teach people about Data Science, Machine learning, Elastic search, and AWS. I work as data collection and processing Team Lead at Jobtarget where I spent most of my time developing Ingestion Framework and creating microservices and scalable architecture on AWS. I have worked with a massive amount of data which includes creating data lakes (1.2T) optimizing data lakes query by creating a partition and using the right file format and compression. I have also developed and worked on a streaming application for ingesting real-time streams data via kinesis and firehose to elastic search

