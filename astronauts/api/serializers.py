from rest_framework import serializers
from astronauts.models import Astronaut  # Replace 'Astronaut' with your actual model name

class AstronautSerializer(serializers.ModelSerializer):
    class Meta:
        model = Astronaut
        fields = '__all__'  # Or specify the fields explicitly
