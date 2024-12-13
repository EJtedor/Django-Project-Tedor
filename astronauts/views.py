from django.shortcuts import render, get_object_or_404, redirect
from .models import Mission
from .forms import MissionForm
from django.contrib.auth.decorators import login_required
from .models import BMIRecord
from .forms import BMIRecordForm
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib import messages  # Import for user messages

from django.shortcuts import redirect

@login_required
def save_records(request):
    if request.method == 'POST':
        # Extracting data from POST
        weight = float(request.POST.get('weight', 0))
        height = float(request.POST.get('height', 0))
        oxygen_level = float(request.POST.get('oxygen', 95))
        glycerol_level = float(request.POST.get('glycerol', 100))
        calorie_intake = float(request.POST.get('calories', 2000))
        daily_stool = float(request.POST.get('stool', 100))
        water_intake = float(request.POST.get('water', 2000))

        # Save to the BMIRecord model
        BMIRecord.objects.create(
            astronaut=request.user,
            weight=weight,
            height=height,
            oxygen_level=oxygen_level,
            glycerol_level=glycerol_level,
            calorie_intake=calorie_intake,
            daily_stool=daily_stool,
            water_intake=water_intake
        )

        # Redirect to dashboard
        return redirect('astronaut_dashboard')

    # Redirect back to the BMI calculator if the method is not POST
    return redirect('bmi_calculator')





def bmi_calculator(request):
    return render(request, 'astronauts/bmi_calculator.html')

@login_required
def astronaut_dashboard(request):
    # Fetch the latest record for the logged-in user
    latest_record = BMIRecord.objects.filter(astronaut=request.user).order_by('-recorded_at').first()
    
    # Calculate BMI if there's a latest record
    bmi = None
    if latest_record and latest_record.height > 0:
        bmi = latest_record.weight / ((latest_record.height / 100) ** 2)

    # Pass data to the template
    return render(request, 'astronauts/dashboard.html', {
        'latest_record': latest_record,
        'bmi': bmi
    })

@login_required
def bmi_records(request):
    # Corrected filter to use the `astronaut` field
    bmi_records = BMIRecord.objects.filter(astronaut=request.user).order_by('-recorded_at')
    context = {
        'bmi_records': bmi_records,
        'weights': [record.weight for record in bmi_records],
        'heights': [record.height for record in bmi_records],
        'dates': [record.recorded_at for record in bmi_records]
    }
    return render(request, 'astronauts/bmi_records.html', context)

@login_required
def bmi_list(request):
    records = BMIRecord.objects.filter(astronaut=request.user).order_by('-recorded_at')
    return render(request, 'astronauts/bmi_list.html', {'records': records})

@login_required
def bmi_create(request):
    form = BMIRecordForm(request.POST or None)
    if form.is_valid():
        record = form.save(commit=False)
        record.astronaut = request.user
        record.save()
        return redirect('bmi_list')
    return render(request, 'astronauts/bmi_form.html', {'form': form})

@login_required
def bmi_update(request, pk):
    record = get_object_or_404(BMIRecord, pk=pk, astronaut=request.user)
    form = BMIRecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('bmi_list')
    return render(request, 'astronauts/bmi_form.html', {'form': form, 'record': record})

@login_required
def bmi_delete(request, pk):
    record = get_object_or_404(BMIRecord, pk=pk, astronaut=request.user)
    if request.method == 'POST':
        record.delete()
        return redirect('bmi_list')
    return render(request, 'astronauts/bmi_confirm_delete.html', {'record': record})

@login_required
def astronaut_dashboard(request):
    """
    View to display the astronaut dashboard.
    """
    return render(request, 'astronauts/dashboard.html')

@login_required
def mission_list(request):
    """Displays a list of all missions."""
    missions = Mission.objects.all().order_by('-start_date')
    return render(request, 'astronauts/mission_list.html', {'missions': missions})

@login_required
def mission_detail(request, pk):
    """Displays the details of a single mission."""
    mission = get_object_or_404(Mission, pk=pk)
    return render(request, 'astronauts/mission_detail.html', {'mission': mission})

@login_required
def mission_create(request):
    form = MissionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mission_list')
    return render(request, 'astronauts/mission_form.html', {'form': form, 'mission': None})


@login_required
def mission_update(request, pk):
    """Handles updating an existing mission."""
    mission = get_object_or_404(Mission, pk=pk)
    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            return redirect('mission_detail', pk=pk)
    else:
        form = MissionForm(instance=mission)
    return render(request, 'astronauts/mission_form.html', {'form': form, 'mission': mission})

@login_required
def mission_delete(request, pk):
    """Handles deleting a mission."""
    mission = get_object_or_404(Mission, pk=pk)
    if request.method == 'POST':
        mission.delete()
        return redirect('mission_list')
    return render(request, 'astronauts/mission_confirm_delete.html', {'mission': mission})
