from django.shortcuts import render, redirect
from .models import profile
from django.db.models import Q
import os


def login(r):
    if r.method == 'POST':
        name = r.POST['name']
        email = r.POST['email']
        img = r.FILES.get('fileupload', None)
        user = profile.objects.create(name=name, email=email, proPic=img)
        user.save()

    return render(r, 'login.html', locals())


def Prof(r):
    profiles = profile.objects.all()
    return render(r, 'newProf.html', {'profiles':profiles})
    #return render(r, 'newProf.html', locals())


def update(r, id):
    pro = profile.objects.get(id=id) #pro = Object, profile = Database
    if r.method == 'POST':
        name = r.POST['name']
        email = r.POST['email']
        img = r.FILES.get('fileupload')
        user = profile.objects.get(id=id)
        if len(r.FILES) != 0:
            if len(user.proPic) > 0:
                os.remove(user.proPic.path)
            user.proPic = img

        pro.name = name
        pro.email = email
        pro.proPic = img
        pro.save()

        return redirect('Prof')

    return render(r, 'Update.html', locals())



def delete(r, id):
    pro = profile.objects.get(id=id)
    if pro.proPic:
        os.remove(pro.proPic.path) 
    pro.delete()
    return redirect('Prof')

def search(r):
    if r.method == 'GET':
        search = r.GET.get('search')
        profiles = profile.objects.filter(Q(name__icontains=search)|Q(email=search))
        return render(r,'newProf.html',{'profiles':profiles})
    else:
        profiles = []
    return render(r,'Prof/',locals())

