import http.client
import json

def handler(event, context):
    try:
        conn = http.client.HTTPConnection("localhost:8001")
        conn.request("POST", "/process/", headers={"Content-Type": "application/json"})
        response = conn.getresponse()

        if response.status != 200:
            print("Request to endpoint failed with status code:", response.status)
            print("Response:", response.read().decode())

        print("Request to endpoint successful")
        print("Response:", response.read().decode())

    except Exception as err:
        print("An error occurred while making the request:", err)

    return {
        'statusCode': 200,
        'body': json.dumps('Request processed successfully')
    }
