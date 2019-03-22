import boto3

if __name__ == "__main__":

    bucket='facedetectionaccess'
    collectionId='PerceptioAcccessControl'
    #photo='Sebastian_Giraldo_1.jpg'
    client=boto3.client('rekognition')

    response=client.index_faces
    for i in range(1,6):
        response=client.index_faces(CollectionId=collectionId,
                                    Image={'S3Object':{'Bucket':bucket,'Name': 'Jorge_Granda_{}.jpg'.format(i)}},
                                    ExternalImageId='Jorge_Granda_{}.jpg'.format(i),
                                    MaxFaces=1,
                                    QualityFilter="AUTO",
                                    DetectionAttributes=['ALL'])

        print ('Results for ' + 'Jorge_Granda_{}.jpg'.format(i)) 	
        print('Faces indexed:')						
        for faceRecord in response['FaceRecords']:
            print('  Face ID: ' + faceRecord['Face']['FaceId'])
            print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

        print('Faces not indexed:')
        for unindexedFace in response['UnindexedFaces']:
            print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
            print(' Reasons:')
            for reason in unindexedFace['Reasons']:
                print('   ' + reason)