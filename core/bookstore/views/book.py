
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from bookstore.serializers import BookSerializer
from rest_framework import status
from minio import Minio
from io import BytesIO
from django.http import FileResponse

class GetTestBookGenericAPIView(GenericAPIView):
    serializer_class = BookSerializer

    def get(self, request):
        return get_object_data()
        pass
        
    
    
def get_object_data():
    client = Minio("bookstoreminio.darkube.app",
        access_key="a4l0tgkwhZbC3M6r1LJkbrDHc9PQQiy9",
        secret_key="dJe8LfUeo0DjymeHd36nu6Q8GCiC4khg",
    )
    # Get the object from MinIO
    response = client.get_object("python-test-bucket", "Django for Professionals.pdf")
    
    # Read the object data
    data = response.read()
    
    # Create a BytesIO object from the data
    data_io = BytesIO(data)
    
    # Return the object with FileResponse
    return FileResponse(data_io,as_attachment=True, filename="Django for Professionals.pdf", content_type="application/pdf")