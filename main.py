import json
from flask import jsonify
from google.oauth2 import service_account
from oauth2client.client import GoogleCredentials
import googleapiclient.discovery
from google.cloud import storage

serviceAccountName='<サービスアカウント名>'
bucketName='<GCSバケット名>'
blobName='<GCSへ配置する鍵の名前>'

def rotate_sakey(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # サービスアカウントの鍵情報を取得
    try:
        credentials = GoogleCredentials.get_application_default()
        service = googleapiclient.discovery.build('iam', 'v1', credentials=credentials)

        oldkeys = service.projects().serviceAccounts().keys().list(
                    name='projects/-/serviceAccounts/' + serviceAccountName,
                    keyTypes="USER_MANAGED"
                  ).execute()
    except Exception as e:
        response = jsonify({'message':'error', 'error': str(e)})
        response.status_code = 500
        return response

    # サービスアカウントの鍵を再作成
    try:
        newkey = service.projects().serviceAccounts().keys().create(
                    name='projects/-/serviceAccounts/' + serviceAccountName, body={}
                ).execute()
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucketName)
        blob = bucket.blob(blobName)
        blob.upload_from_string(json.dumps(newkey, sort_keys=True, indent=4, separators=(",", ": ")),content_type="application/json")
        #print(json.dumps(newkey, sort_keys=True, indent=4, separators=(",", ": ")))
    except Exception as e:
        response = jsonify({'message':'error', 'error': str(e)})
        response.status_code = 500
        return response
    
    # サービスアカウントの鍵を削除
    for oldkey in oldkeys['keys']:
       print('Key: ' + oldkey['name'])
       try:
            service.projects().serviceAccounts().keys().delete(name=oldkey['name']).execute()
       except Exception as e:
            response = jsonify({'message':'error', 'error': str(e)})
            response.status_code = 500
            return response

    response = jsonify({'message':'success'})
    response.status_code = 200
    return response
