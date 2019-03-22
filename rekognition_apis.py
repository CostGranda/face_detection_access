import boto3  # AWS SDK
from dotenv import load_dotenv  # DotEnv
import rtsp  # Cam Protoccol for StreamReader
from os import getenv  # Get environment variale


class RekognitionApis():

    def __init__(self):
        load_dotenv()  # Load env variables
        self.client = boto3.client(getenv('CLIENT'))
        self.collectionId = getenv('COLLECTION')
        self.bucket = getenv('BUCKET')
        self.threshold = 99
        self.maxFaces = 1

    def create_collection(self):
        print('Creating collection:' + self.collectionId)
        response = self.client.create_collection(
            CollectionId=self.collectionId)
        print('Collection ARN: ' + response['CollectionArn'])
        print('Status code: ' + str(response['StatusCode']))
        print('Done...')

    def list_faces(self):
        token = True
        maxResults = 1
        response = self.client.list_faces(CollectionId=self.collectionId)
        print('Results for Collection')
        print('Faces listed:')
        while token:
            faces = response['Faces']
            for face in faces:
                print(face)
            if 'NextToken' in response:
                nextToken = response['NextToken']
                response = self.client.list_faces(CollectionId=self.collectionId,
                                                  NextToken=nextToken, MaxResults=maxResults)
            else:
                token = False

    def index_faces(self, name, from_n=1, to_n=5, ):
        """Indexa las imagenes leyendolas de S3 y las almacena en la colleción parametrizada.
        Args:
            name (str):   Nombre de la imagen para leer del bucket secuencialmente.
            from_n (int): Valor inicial X para controlar el ciclo, normalmente la primera image (Ex: name_lastname_X.jpg)
            to_n (int):   Para controlar el ciclo y recorrer todas las imagenes asociadas al nombre.

        Returns:
            None
        """
        # TODO Validate name format (name_lastname_X.jpg)
        response = self.client.index_faces
        for secuence in range(from_n, to_n+1):
            name_secuence = '{}_{}.jpg'.format(name, secuence)
            response = self.client.index_faces(CollectionId=self.collectionId,
                                               Image={'S3Object': {
                                                   'Bucket': self.bucket, 'Name': name_secuence}},
                                               ExternalImageId=name_secuence,
                                               MaxFaces=1,
                                               QualityFilter="AUTO",
                                               DetectionAttributes=['ALL'])

            print('Results for {}'.format(name_secuence))
            print('Faces indexed:')
            for faceRecord in response['FaceRecords']:
                print('  Face ID: ' + faceRecord['Face']['FaceId'])
                print('  Location: {}'.format(
                    faceRecord['Face']['BoundingBox']))

            print('Faces not indexed:')
            for unindexedFace in response['UnindexedFaces']:
                print(' Location: {}'.format(
                    unindexedFace['FaceDetail']['BoundingBox']))
                print(' Reasons:')
                for reason in unindexedFace['Reasons']:
                    print('   ' + reason)

    def search_by_id(self, photoId):
        response = self.client.search_faces(CollectionId=self.collectionId,
                                            FaceId=photoId,
                                            FaceMatchThreshold=self.threshold,
                                            MaxFaces=self.maxFaces)
        facesMatching = response['FaceMatches']
        for match in facesMatching:
            print('FaceId:' + match['Face']['FaceId'])
            print('ExternalImageId: {}'.format(
                match['Face']['ExternalImageId']))
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print()

    def search_by_image(self, fileName, mode='local'):
        imageFile = 'input.jpg'
        if mode == 'local':
            with open(imageFile, 'rb') as image:
                response = self.client.search_faces_by_image(CollectionId=self.collectionId,
                                                             Image={
                                                                 'Bytes': image.read()},
                                                             FaceMatchThreshold=self.threshold,
                                                             MaxFaces=self.maxFaces)
        elif mode =='s3':
            response = self.client.search_faces_by_image(CollectionId=self.collectionId,
                                                         Image={'S3Object': {
                                                             'Bucket': self.bucket, 'Name': fileName}},
                                                         FaceMatchThreshold=self.threshold,
                                                         MaxFaces=self.maxFaces)

        faceMatches = response['FaceMatches']
        print('Matching faces')
        for match in faceMatches:
            print('FaceId:' + match['Face']['FaceId'])
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print()
