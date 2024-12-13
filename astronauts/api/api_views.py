from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AstronautSerializer
from astronauts.models import Astronaut  # Replace 'Astronaut' with your actual model name
from rest_framework.renderers import JSONRenderer

class AstronautListAPIView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        astronauts = Astronaut.objects.all()
        if not astronauts.exists():
            return Response({"message": "API is working, but no astronauts found!"}, status=status.HTTP_200_OK)

        serializer = AstronautSerializer(astronauts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AstronautSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
