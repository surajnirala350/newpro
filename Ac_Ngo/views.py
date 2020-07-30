from django.shortcuts import render, redirect
from django.contrib import messages
from Ac_Admin.models import Department_Table
from Ac_Ngo.models import NGOS_Table, Suggestion_Table, Article_Table


# NGO Registrtion view
def ngo_registration(request):
    try:
        username = request.session['username']
        qs = NGOS_Table.objects.all()
        if request.method == 'POST':
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            address = request.POST.get('address')
            username = request.POST.get('username')
            password = request.POST.get('password')
            NGOS_Table(
                name=name, mobile=mobile, email=email,
                address=address, username=username, password=password,
            ).save()
            return render(request, 'ac_ngo/ngo_register.html', {'data': qs, 'rmessage': 'Ngo registered successfully'})
        else:
            return render(request, 'ac_ngo/ngo_register.html', {'data': qs})
    except KeyError:
        return redirect('admin_login')


# NGO Login check
ngos_id = None
def ngo_login_check(request):
    username = request.POST.get('ngo_username')
    password = request.POST.get('ngo_password')
    ng_qs = NGOS_Table.objects.get(username=username,password=password)
    if ng_qs:
        global ngos_id
        request.session['username'] = username
        ngos_id = ng_qs.ngo_id
        qs = Article_Table.objects.filter(ngo_id=ngos_id)
        return render(request, 'ac_ngo/ngo_index.html',{'list':qs})
    else:
        messages.error(request, 'Invalid Ngo Login')
        return redirect('ngo_login')


# Update NGOS
def update_ngos(request):
    try:
        username = request.session['username']
        qs1 = NGOS_Table.objects.all()
        up_name = request.GET.get('name')
        qs2 = NGOS_Table.objects.filter(name=up_name)
        if request.method == 'POST':
            name = request.POST.get('name')
            new_name = request.POST.get('new_name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            address = request.POST.get('address')
            username = request.POST.get('username')
            password = request.POST.get('password')
            res = NGOS_Table.objects.filter(name=name).update(
                name=new_name, mobile=mobile, email=email,
                address=address, username=username, password=password, )
            return render(request, 'ac_ngo/ngo_register.html', {'data': qs1, 'umessage': 'Ngo is updated successfully'})
        return render(request, 'ac_ngo/ngo_register.html', {'up_name': qs2, 'data': qs1})
    except KeyError:
        return redirect('admin_login')


# Delete NGOS
def delete_ngos(request):
    try:
        username = request.session['username']
        ngo_name = request.GET.get('name')
        qs = NGOS_Table.objects.filter(name=ngo_name)
        if qs:
            qs.delete()
            qs1 = NGOS_Table.objects.all()
            return render(request, 'ac_ngo/ngo_register.html', {'data': qs1, 'message': 'Ngo Is Deleted'})
        return redirect('ngo_register')
    except KeyError:
        return redirect('admin_login')


#  ngos Suggestions View
def ngo_suggestion_view(request):
    try:
        username = request.session['username']
        qs1 = Department_Table.objects.all()
        if request.method == 'POST':
            ngo_id = request.POST.get('ngo_id')
            dept_name = request.POST.get('dept_name')
            sug_message = request.POST.get('sugs_message')
            Suggestion_Table(
                dept_name_id=dept_name, message=sug_message, ).save()
            return redirect('suggestion')
        else:
            return render(request, 'ac_ngo/ngo_suggestions.html', {'data1': qs1, 'data2': ngos_id})
    except KeyError:
        return redirect('ngo_login')


# Suggestions list
def suggestions_list(request):
    try:
        username = request.session['username']
        qs = Suggestion_Table.objects.all()
        return render(request,'ac_ngo/suggestions_list.html',{'data1':qs})
    except KeyError:
        return redirect('ngo_login')


# Suggestions Delete
def delete_suggestions(request):
    try:
        username = request.session['username']
        del_id = request.POST.get('del_id')
        qs = Suggestion_Table.objects.filter(sugs_id=del_id)
        if qs:
            qs.delete()
            return redirect('suggestions_list')
        else:
            return redirect('suggestions_list')
    except KeyError:
        return redirect('ngo_login')


# Articles
def ngo_article(request):
    try:
        username = request.session['username']
        qs = Article_Table.objects.all()
        if request.method == 'POST':
            ng_id = request.POST.get('ng_id')
            name = request.POST.get('name')
            message = request.POST.get('message')
            Article_Table(
                name=name, ngo_id_id=ng_id, message=message).save()
            return render(request, 'ac_ngo/ngo_articles.html', {'data': ngos_id, 'art_data': qs})
        else:
            return render(request, 'ac_ngo/ngo_articles.html', {'data': ngos_id, 'art_data': qs})
    except KeyError:
        return redirect('ngo_login')


def article_home(request):
    try:
        username = request.session['username']
        qs = Article_Table.objects.filter(ngo_id=ngos_id)
        return render(request,'ac_ngo/ngo_index.html',{'list':qs})
    except KeyError:
        return redirect('ngo_login')

# Ngo Logout
def ngo_logout(request):
    try:
       del request.session['username']
       request.session.modified = True
    except:
        return redirect('ngo_login')
    return redirect('ngo_login')