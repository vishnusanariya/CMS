from importlib import import_module
from django.shortcuts import render,redirect
from .models import RefDoc
from .resource import refdocres
from django.contrib import messages
from tablib import Dataset
# Create your views here.
def UploadRefDoc(request):
    if request.method=='POST':
        doc_resource=refdocres()
        dataset=Dataset()
        new_doc=request.FILES['myrefdocs']

        if not new_doc.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'refdoc_upload.html')

        imported_data=dataset.load(new_doc.read(),format='xlsx')
        for data in imported_data:
            value=RefDoc(data[0],data[1],data[2],data[3],data[4])
            value.save()
    return render(request,'refdoc_upload.html')

def view_refDoc(request):
    docs=RefDoc.objects.all()
    print(docs)
    return render(request,'view_docs.html',{'docs':docs})

def addRefdoc(request):
    if request.method == 'POST':
        doc_name=request.POST['refdocname']
        doc_prof=request.POST['refdocprofession']
        doc_addr=request.POST['refdocaddr']
        doc_con=request.POST['refdoccontact']
        d=RefDoc(name=doc_name,profession=doc_prof,address=doc_addr,contact=doc_con)
        d.save()
    return redirect('uploadfile')