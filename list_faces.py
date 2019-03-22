import boto3

if __name__ == "__main__":

    bucket='facedetectionaccess'
    collectionId='PerceptioAcccessControl'

    client=boto3.client('rekognition')
    token=True
    maxResults=1
    response=client.list_faces(CollectionId=collectionId)
    print('Results for Collection')
    print('Faces listed:')						
    while token:
        faces=response['Faces']
        for face in faces:
            print (face)
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collectionId,
                                    NextToken=nextToken,MaxResults=maxResults)
        else:
            token=False