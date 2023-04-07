import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    eventname = event['Records'][0]['eventName']
    timestamp = event['Records'][0]['eventTime']
    sns_message = str("Modification has been done in One of Your Bucket \n\n BUCKET NAME: "+ bucket +"\n\n FILE NAME: " + key + "\n\n OPERATION: " + eventname + "\n\n TimeStamp: " + Time + "\n\n" )
    try:
        print(eventname)
        if eventname == "ObjectRemoved:Delete":
            print("File is being Deleted")
            sns_message += str("File Deleted")
        else:
            response = s3.get_object(Bucket=bucket, Key=key)
            sns_message += str("FILE CONTENT TYPE: " + str(response['ContentType']) + "\n\nFILE CONTENT: " + str(response['Body'].read()))
            print("CONTENT TYPE: " + response['ContentType'])
        print(str(sns_message))
        subject= "S3 Bucket[" + bucket + "] Event[" + eventname + "] Time[" + timestamp + "]"
        print(subject)
        sns_response = sns.publish(
        TargetArn='arn:aws:sns:us-west-2:0122324358:kennethtestsns',
        Message= str(sns_message),
        Subject= str(subject)
        )
    except Exception as e:
        print(e)
        raise e