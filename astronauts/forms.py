from django import forms
from django.contrib.auth import get_user_model  # Use get_user_model for custom user models
from .models import Mission, Astronaut, BMIRecord
from .models import BMIRecord

# Get the correct User model
User = get_user_model()

class AstronautForm(forms.ModelForm):
    class Meta:
        model = Astronaut
        fields = ['name', 'missions', 'age', 'joined_date']

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['name', 'start_date', 'end_date', 'objectives', 'crew_members', 'status']  # Use 'objectives' instead of 'description'

class MissionAssignmentForm(forms.ModelForm):
    crew_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),  # Include only active users
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for selection
        required=True,  # Optional: True by default
        label="Assign Crew Members",
    )

    class Meta:
        model = Mission
        fields = ['name', 'start_date', 'end_date', 'objectives', 'crew_members']

    def clean_crew_members(self):
        # Optional: Add custom validation for crew members
        crew_members = self.cleaned_data.get('crew_members')
        if crew_members.count() < 1:
            raise forms.ValidationError("At least one crew member must be assigned.")
        return crew_members

class BMIRecordForm(forms.ModelForm):
    class Meta:
        model = BMIRecord
        fields = [
            'weight',
            'height',
            'oxygen_level',
            'glycerol_level',
            'calorie_intake',
            'daily_stool',
            'water_intake',
        ]
