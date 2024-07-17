import json
import boto3
from prompt_engineering import prompt_classification
import csv
from io import StringIO



s3_client = boto3.client('s3')

# Bedrock client used to interact with APIs around models
bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-east-1'
)

# Bedrock Runtime client used to invoke and question the models
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)




def lambda_handler(event, context):

    bucket_name = 'recrutement-projet'
    file_name = 'candidates_classification.csv'

    s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
   # print("s3_response:", s3_response)

    file_data = s3_response["Body"].read().decode('utf-8')
    #print("file_data:", file_data)
    
    file_data_io = StringIO(file_data)
    
    # Lire les données CSV sans pandas
    csv_reader = csv.DictReader(file_data_io)    
    
    
    
    prompt = prompt_classification(event,csv_reader)
    print(prompt)

    modelId = "anthropic.claude-v2"

    prompt = "Human: " + prompt + "\n\nAssistant:"

    body = json.dumps(
        {
            "prompt": prompt,
            "max_tokens_to_sample": 1525,
            "temperature": 0.7,
            "stop_sequences": ["\n\nHuman:"]
        }
    )

    # The call made to the model
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=modelId,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    completion = response_body.get('completion')
    print(completion)
    
  
    return completion 
