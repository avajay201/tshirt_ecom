from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactUsSerializer
from products.utils import get_first_serializer_error


class SubmitContactUsView(APIView):
    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your message has been submitted successfully."}, status=status.HTTP_201_CREATED)
        error = get_first_serializer_error(serializer.errors)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
