from importlib import import_module
from django.shortcuts import redirect,render
from .models import Disease
from .resource import DiseaseResource
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def Upload_Disease(request):
    if request.method=='POST':
        dis_resource=DiseaseResource()
        dataset=Dataset()
        new_disease=request.FILES['mydisease']

        if not new_disease.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'upload_disease.html')

        imported_data=dataset.load(new_disease.read(),format='xlsx')
        for data in imported_data:
            value=Disease(data[0],data[1],data[2])
            value.save()
    return render(request,'upload_diseases.html')

def view_Disease(request):
    disease=Disease.objects.all()
    print(disease)
    return render(request,'view_disease.html',{'disease':disease})

def addDisease(request):
    if request.method == 'POST':
        new_disease=request.POST['disease']
        new_complexity=request.POST['complexity']
        d=Disease(d_name=new_disease,complexity=new_complexity)
        d.save()
    return redirect('uploadfile')
