from importlib import import_module
from django.shortcuts import render,redirect
from .models import Symptoms
from .resource import SymptomsResource
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def Upload_Symptoms(request):
    if request.method=='POST':
        dis_resource=SymptomsResource()
        dataset=Dataset()
        new_symptoms=request.FILES['mysymptoms']

        if not new_symptoms.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'upload_symptoms.html')

        imported_data=dataset.load(new_symptoms.read(),format='xlsx')
        for data in imported_data:
            value=Symptoms(data[0],data[1],data[2])
            value.save()
    return render(request,'upload_symptoms.html')

def view_Symptoms(request):
    symptoms=Symptoms.objects.all()
    print(symptoms)
    return render(request,'view_symptoms.html',{'symptoms':symptoms})

def addSymptoms(request):
    if request.method == 'POST':
        new_symptoms=request.POST['symptoms']
        new_complexity=request.POST['complexity']
        d=Symptoms(s_name=new_symptoms,complexity=new_complexity)
        d.save()
    return redirect('uploadfile')
