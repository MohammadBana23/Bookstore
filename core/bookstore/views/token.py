from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..serializers import RequestEmailTokenSerializer
from rest_framework import serializers


class RequestTokenView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RequestEmailTokenSerializer(data=request.data, request=request)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Token Sent"}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
