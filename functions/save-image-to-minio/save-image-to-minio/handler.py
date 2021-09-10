import json
from os import error
from minio import Minio
from minio.commonconfig import Tags
from urllib import request 
from os import getenv

def handle(req):
    try:
        handlefun(req)
    except Exception as x:
        print("-------ERROR:", x)


def handlefun(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    data_dict = json.loads(req)
    # print ("URL is: " + data_dict["url"])
    # print ("Bucket path is: " + data_dict["path"])
    bucket_name = data_dict["path"].split("/")[0]
    bucket_path = data_dict["path"].split("/",maxsplit=1)[1]

    host = getenv('MINIO_HOST', 'minio.minio.svc.cluster.local')
    port = getenv('MINIO_PORT', '9000')
    accesskey = getenv('MINIO_ACCESS_KEY', 'admin')
    secretkey = getenv('MINIO_SECRET_KEY', 'password')
  
    client = Minio(endpoint=host + ':'+ port, access_key=accesskey, secret_key=secretkey, secure=False)

    # Get image
    data = request.urlopen(data_dict["url"])

    if not client.bucket_exists(bucket_name):
        # print("ERROR: Bucket " + bucket_name + " does not exist. Creating now ...")
        client.make_bucket(bucket_name)
    
    filename = data_dict["url"].split("/")[-1]

    # Upload & tag file
    tags = Tags(for_object=True)
    tags["function"] = "url2bucket"
    result = client.put_object(
        bucket_name, 
        bucket_path + '/' + filename, 
        data, length=-1, 
        part_size=10*1024*1024, 
        tags=tags,
        metadata={'Content-type': data.getheader('Content-type')}
    )
    
    # Get presigned url
    presigned_url = client.get_presigned_url(
    "GET",
    bucket_name,
    result.object_name,
    )
    
    response = {
        'presigned_url':presigned_url,
        'bucket_name': bucket_name,
        'object_name': result.object_name
    }
    
    print(json.dumps(response))
     

# if __name__=="__main__":
#     with open('' , 'r') as file:
#         data = file.read().replace('\n', '')
#     print(handle(data))
