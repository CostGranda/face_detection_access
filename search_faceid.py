import boto3

if __name__ == "__main__":

    bucket='facedetectionaccess'
    collectionId='PerceptioAcccessControl'
    photoId='1708be1b-bf46-4608-abab-95bfae123b47'

    client=boto3.client('rekognition')
    tokens=True
    response=client.search_faces(CollectionId=collectionId,
                                FaceId=photoId,
                                FaceMatchThreshold=99,
                                MaxFaces=1)
    facesMatching=response['FaceMatches']
    imageid = ''
    for match in facesMatching:
        print('FaceId:' + match['Face']['FaceId'])
        print('ExternalImageId: {}'.format(match['Face']['ExternalImageId']))
        imageid = match['Face']['ExternalImageId']
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print()
    
    #Subir(consecutivo)


def Subir(imageid):
    consecutivo = imageid[-5:-4]
    
