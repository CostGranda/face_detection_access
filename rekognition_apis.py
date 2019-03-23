import boto3  # AWS SDK
from dotenv import load_dotenv  # DotEnv
import rtsp  # Cam Protoccol for StreamReader
from os import getenv  # Get environment variale


class RekognitionApis():

    def __init__(self):
        """Instance and Environment variables initialization
        """
        load_dotenv()  # Load env variables
        self.client = boto3.client(getenv('CLIENT'))
        # AWS Collection to store metadata
        self.collectionId = getenv('COLLECTION')
        # S3 bucket for indexing the images
        self.bucket = getenv('BUCKET')
        # Minimun percentaje to pass
        self.threshold = 80
        # Amount of faces in API results
        self.maxFaces = 1

    def create_collection(self, name):
        """Create a collection on AWS Rekognition to store metadata
        Args:
            name (str): Name for the collection

        Returns:
            None
        """
        print('Creating collection:' + name)
        response = self.client.create_collection(
            CollectionId=name)
        # Amazon Resource Name
        print('Collection ARN: ' + response['CollectionArn'])
        # Http response code
        print('Status code: ' + str(response['StatusCode']))
        print('Done...')

    def list_faces(self):
        """ List faces on the collection.
        Validate if there is more than one result on the response array otherwise,
        breaks the loop.

        """
        # To avoid infinity loop
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
            # Format the string as Name_LastName_X.jpg
            name_secuence = '{}_{}.jpg'.format(name, secuence)
            response = self.client.index_faces(CollectionId=self.collectionId,
                                               Image={'S3Object': {
                                                   'Bucket': self.bucket, 'Name': name_secuence}},
                                               ExternalImageId=name_secuence,
                                               MaxFaces=self.maxFaces,
                                               QualityFilter="AUTO",
                                               DetectionAttributes=['ALL'])

            print('Results for {}'.format(name_secuence))
            print('Faces indexed:')
            for faceRecord in response['FaceRecords']:
                print('  Face ID: ' + faceRecord['Face']['FaceId'])
                print('  Location: {}'.format(
                    faceRecord['Face']['BoundingBox']))

            # Get the faces with Indexing problems
            print('Faces not indexed:')
            for unindexedFace in response['UnindexedFaces']:
                print(' Location: {}'.format(
                    unindexedFace['FaceDetail']['BoundingBox']))
                print(' Reasons:')
                for reason in unindexedFace['Reasons']:
                    print('   ' + reason)

    def search_by_id(self, photoId):
        """Get the similarity score comparing the ID with the existing ones in the collection
        Args:
            photoId (str): ID in format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
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

    def search_by_image(self, imageFile='input.jpg', mode='local'):
        """Gets the similarity score sending the image in ByteArray.
        If the local parameter is specified it gets the imagen from the same folder
        of the sccript, otherwise it gets the image from am AWS S3 bucket.

        Args:
            fileName (str): 
            mode (str): Local image or S3 image.

        Returns:
            None
        """
        if mode == 'local':
            with open(imageFile, 'rb') as image:
                response = self.client.search_faces_by_image(CollectionId=self.collectionId,
                                                             Image={
                                                                 'Bytes': image.read()},
                                                             FaceMatchThreshold=self.threshold,
                                                             MaxFaces=self.maxFaces)
        elif mode == 's3':
            # TODO Get the name of the image on the bucket
            fileName = ''
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
