from importlib import import_module
from django.shortcuts import render,redirect
from .models import Medicine
from .resources import MedicineResource
from django.contrib import messages
from tablib import Dataset

# Create your views here.
def Upload_Excel(request):
    if request.method=='POST':
        med_resource=MedicineResource()
        dataset=Dataset()
        new_med=request.FILES['myfile']

        if not new_med.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'home/uploadexternalfiles.html')

        imported_data=dataset.load(new_med.read(),format='xlsx')
        for data in imported_data:
            value=Medicine(data[0],data[1],data[2],data[3])
            if not Medicine.objects.filter(medicine_name=data[1],medicine_power=data[2],medicine_price=data[3]).exists():
                value.save()
            else:
                continue
    return render(request,'home/uploadexternalfiles.html')

def view_medicine(request):
    meds=Medicine.objects.all()
    print(meds)
    return render(request,'viewmeds.html',{'meds':meds})

def addMedicine(request):
    if request.method == 'POST':
        new_med=request.POST['medicine']
        new_power=request.POST['power']
        new_price=request.POST['price']
        d=Medicine(medicine_name=new_med,medicine_power=new_power,medicine_price=new_price)
        d.save()
    return redirect('uploadfile')