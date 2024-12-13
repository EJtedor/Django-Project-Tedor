from django.contrib import admin
from .models import Astronaut, BMIRecord

# Register the Astronaut model
@admin.register(Astronaut)
class AstronautAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'joined_date', 'get_email')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'  # Rename the column in admin panel

# Register the BMIRecord model
@admin.register(BMIRecord)
class BMIRecordAdmin(admin.ModelAdmin):
    list_display = (
        'astronaut', 
        'weight', 
        'height', 
        'oxygen_level', 
        'glycerol_level', 
        'calorie_intake', 
        'daily_stool', 
        'water_intake', 
        'recorded_at'
    )
