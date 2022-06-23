from importlib import import_module
from django.shortcuts import render,redirect
from .models import RefDoc
from .models import Doc_group
from django.core.paginator import Paginator
from .resource import refdocres
from django.contrib import messages
from django.db.models import Q
from tablib import Dataset
from django.urls import reverse
# Create your views here.
# def UploadRefDoc(request):
#     if request.method=='POST':
#         doc_resource=refdocres()
#         dataset=Dataset()
#         new_doc=request.FILES['myrefdocs']

#         if not new_doc.name.endswith('xlsx'):
#             messages.info(request,'wrong format valid xlsx')
#             return render(request,'refdoc_upload.html')

#         imported_data=dataset.load(new_doc.read(),format='xlsx')
#         for data in imported_data:
#             value=RefDoc(data[0],data[1],data[2])
#             value.save()
#     return render(request,'home/uploadexternalfiles.html')

def view_refDoc(request):
    docs=RefDoc.objects.all()
    print(docs)
    return render(request,'view_docs.html',{'docs':docs})

def addRefdoc(request,i):
    if request.method == 'POST':
        doc_name=request.POST['refdocname']
        doc_details=request.POST['refdocdetail']
        print(doc_name)
        print(doc_details)
        t1=Doc_group.objects.get(id=i)
       
        d=RefDoc(gid=t1,name=doc_name,details=doc_details)
        d.save()

    parti_cate_doc=RefDoc.objects.filter(gid=i)
    return render(request,'ref_doc_particular_group.html',{'gid':i,'parti_cate_doc':parti_cate_doc})    
    
    #----------------------------------------------------------------------

def ref_doctor_all_groups(request):
    
    g = Doc_group.objects.all().order_by('id')    
    paginator=Paginator(g, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    s={'group':g ,'page_obj':page_obj}
    return render(request,'ref_doc _all_group.html',s)

def ref_doctor_create_group(request): 
    if request.method=='POST':
        
        gname = request.POST['gname']
        group = Doc_group(gname=gname)
        group.save()

        return redirect(reverse('ref_doctor_all_groups'))
        
    else:
         #p = patient_detail.objects.all()
         #s={'patient':p}
         return render(request,'ref_doc_create_group.html')

def ref_doctor_particular_group(request,i):
    #here i is gid
    if request.method=='POST':
        t1=Doc_group.objects.get(id=i)
        doc_resource=refdocres()
        dataset=Dataset()
        new_doc=request.FILES['myrefdocs']
        
        if not new_doc.name.endswith('xlsx'):
            messages.info(request,'wrong format valid xlsx')
            return render(request,'refdoc_upload.html')

        imported_data=dataset.load(new_doc.read(),format='xlsx')
        for data in imported_data:
            value=RefDoc(data[0],data[1],data[2])
            value.gid=t1
            if not RefDoc.objects.filter(gid=t1,name=data[1],details=data[2]).exists():
                value.save()
            else:
                continue
        #parti_cate_doc=RefDoc.objects.filter(gid=i)
        #return render(request,'ref_doc_particular_group.html',{'gid':i})    
        return redirect(reverse('ref_doctor_all_groups'))
    else:

        print(i)
        parti_cate_doc=RefDoc.objects.filter(gid=i)
        paginator=Paginator(parti_cate_doc, 5)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        for j in parti_cate_doc:
            print(j.name)

        return render(request,'ref_doc_particular_group.html',{'gid':i,'page_obj':page_obj})

def print_ref_doctor(request,i):
    print_doc=RefDoc.objects.get(id=i)
    return render(request,'print_ref_doc.html',{'print_doc':print_doc})


def delete_ref_doc_group(request,i):
    grp=Doc_group.objects.get(id=i)
    grp.delete()
    return redirect('ref_doctor_all_groups')

def search_ref_doc_group(request):
    if request.method=='GET':
        query=request.GET.get('q')
        print(query)
        submitbutton=request.GET.get('submit')
        if query:
            lookups=Q(gname__iexact=query)
            results=Doc_group.objects.filter(lookups).distinct()
            print(results)
            context={'results':results,'submitbutton':submitbutton}
            template_name='ref_doc _all_group.html'
            return render(request,template_name,context)
        else:
            return redirect('ref_doctor_all_groups')
    
    else:
        return render(request, template_name)

def search_ref_doc(request):
    if request.method=='GET':
        query=request.GET.get('q')
        print(query)
        submitbutton=request.GET.get('submit')
        if query:
            lookups=Q(name__contains=query)
            results=RefDoc.objects.filter(lookups).distinct()
            print(results)
            context={'results':results,'submitbutton':submitbutton}
            template_name='ref_doc_particular_group.html'
            return render(request,template_name,context)
        else:
            return redirect('ref_doctor_all_groups')
    
    else:
        return render(request, template_name)