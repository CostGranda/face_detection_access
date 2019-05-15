import boto3
import os
from os import getenv 

class SimpleStorageServicce():
    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.bucket = getenv('DEV_BUCKET')
        self.image = getenv('SAVED_IMAGE')

    def upload_file(self, faceMatch, bucket='testambda'):
        """Upload the taken pic to S3 according to the name convention.
        Validate the last number in the pic secuencce and 'append' the new one.
        Example: If the last photo for Sebastian Giraldo is Sebastian_Giraldo_5.jpg 
                the method rename the new pic to Sebastian_Giraldo_6.jpg and upload it.
        
        Args:
            faceMatch (list): This list contains the name of the person with access and the similarity score.
            bucket (str): Bucket to upload the picture.
        """
        # Sends the prefix ommiting the number and extension 
        key = self.__get_last_item(faceMatch[0][:-5])
        # Last numer in photosecuente
        actual_secuence = key[-5:-4]
        # Increase the actual by 1
        image_name = key.replace(actual_secuence, str(int(actual_secuence)+1))
        # Rename the local file
        os.rename(self.image, image_name )
        # Upload the new renamed file.
        self.s3.meta.client.upload_file(image_name, bucket, image_name)
    
    def __list_files(self, prefix):
        response = self.s3.meta.client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        if response['KeyCount']:
            return response['Contents']

    
    def __get_last_item(self, prefix):
        response = self.__list_files(prefix)
        # Key of the last item in bucket
        key = response[-1]['Key']
        print("key: ",key)
        return key
