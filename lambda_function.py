import json
import boto3

def lambda_handler(event, context):
    runtime = boto3.client("sagemaker-runtime")
    ENDPOINT_NAME = "phishing-endpoint"
    
    print(f"Otrzymano zdarzenie: {json.dumps(event)}") # To pokaże nam co wysłał front-end
    
    try:
        # Parsowanie body
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        urls = body.get("texts", [])
        
        print(f"Analizuję linki: {urls}")
        
        # Wywołanie SageMakera
        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps({"texts": urls})
        )
        
        result = json.loads(response["Body"].read().decode())
        print(f"Wynik z modelu: {result}")
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps(result)
        }
    except Exception as e:
        print(f"KATASTROFA: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }