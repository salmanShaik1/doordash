import json
import pandas as pd
import boto3

def lambda_handler(event, context):
    # TODO implement
    bucket=event['Records'][0]['s3']['bucket']['name']
    Key=event['Records'][0]['s3']['object']['key']
    s3_client=boto3.client('s3')
    response=s3_client.get_object(Bucket=bucket,Key=Key)
    object=response['Body'].read().decode('utf-8')
    print(object,type(object))
    records=object.strip().split('\n')
    print(records)
    data=[json.loads(line) for line in records]
    
    required=[]
    for item in data:
        if item["status"]=="delivered":
            required.append(item)
    final_string='\n'.join(json.dumps(record) for record in required)
    
    s3_client.put_object(
        Bucket='doordashprocessed',  # Correct parameter name
        Key='filtered_data.json',  # Specify a new key for the filtered data
        Body=final_string.encode('utf-8')  # Body should be bytes
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
