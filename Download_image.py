import json
import requests
import boto3
from botocore.exceptions import NoCredentialsError
import os
import time

# Function to read JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
     #   file = open('file_path')
        data=json.load(file)
        print(data)
    return data

# Function to download an image from a URL
def download_image(url, local_filename):

    response = requests.get(url, stream=True)
    time.sleep(10)
    print(response.status_code)

    if response.status_code == 200:
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return local_filename
    else:
        print(f"Failed to download image from {url}")
        return None

# Function to upload a file to S3
# def upload_to_s3(file_name, bucket, object_name=None):
#   s3_client = boto3.client('s3')
#   try:
#       s3_client.upload_file(file_name, bucket, object_name or file_name)
#       print(f'File uploaded successfully to {bucket}/{object_name or file_name}')
#   except FileNotFoundError:
#       print("The file was not found")
#    except NoCredentialsError:
#      print("Credentials not available")

# Main function
def main():
   # script_dir = os.path.dirname(__file__)
    #input_file = os.path.join(script_dir, '/Users/krishnakumarsiramulu/PycharmProjects/pythonProject/data/inp.json')
#  bucket_name = ' s3://sowmyanewproj/Sowmya/'


 # Read input JSON file
    data = read_json('/Users/krishnakumarsiramulu/PycharmProjects/json folder/input.json')

    # Process each image URL
    for image in data['images']:
        image_url = image['url']
        local_filename = image_url.split('/')[-1]
        print(local_filename)

        # Download the image
        downloaded_file = download_image(image_url, local_filename)

        if downloaded_file:
            # Upload the image to S3
            print(downloaded_file)
            session = boto3.Session(
                aws_access_key_id='AKIA6ODU27P5VMVNK4RI',
                aws_secret_access_key='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',
            )
            s3 = session.resource('s3')
            # Filename - File to upload
            # Bucket - Bucket to upload to (the top level directory under AWS S3)
            # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
            s3.meta.client.upload_file(Filename = downloaded_file,
                                       Bucket='sowmyanewproj',
                                       Key = downloaded_file)

            # Remove the local file after uploading
            os.remove(downloaded_file)

if __name__ == "__main__":
  main()
