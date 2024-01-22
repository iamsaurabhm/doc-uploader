from email import message
from tkinter.tix import Form
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from docuploader import settings
from docuploaderapp.models import *
from .forms import DocumentForm, UserLogin, UserAddForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.core.mail import send_mail


class Home(View):

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    # 	return super(Home, self).dispatch(*args, **kwargs)
    
    
    def get(self, request):
        form = DocumentForm()
        doc = Document.objects.all()
        # st = get_object_or_404(Document, pk=status)
        return render(request, 'app/home.html', {'form': form, 'doc': doc, })

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Document has been uploaded",
             extra_tags='alert alert-success alert-dismissible show')
            return HttpResponseRedirect('/home')
# return render(request, 'app/home.html', {'form':form})
# return redirect('app/home.html')
        return HttpResponse("Invalid")


class Doc_Status(View):
    def get(self, request, pk):
        doc = Document.objects.get(pk=pk)
        return render(request, 'app/doc_status.html', {'doc': doc,})


def Uploaded_Doc(request):
    dataset = dict()
    form = DocumentForm()
    doc = Document.objects.all()
    
    #Pagination
    pag = Document.objects.only("client_name", "company_name", "paraplanner", "status")
    
    paginator = Paginator(pag, 5)
    page_num = request.GET.get('page')

    users = paginator.get_page(page_num)
    try:
        users = paginator.get_page(page_num)
    except PageNotAnInteger:
        users = paginator.get_page(1)
    except EmptyPage:
        users = paginator.get_page(paginator.num_pages)
    #Pagination End
    
    #Search
    search_term = ''
    
    if 'search' in request.GET:
        search_term = request.GET['search']
        users = doc.filter(Q(client_name__icontains=search_term) | 
                           Q(company_name__icontains=search_term)
                         )
    
    #Search
    
    dataset['form'] = form
    dataset['doc'] = doc
    dataset['users'] = users
    # dataset['search_term'] = search_term
    # st = get_object_or_404(Document, pk=status)
    return render(request, 'app/doc.html', dataset)

 
def Update(request, id):
    if request.method == 'POST':
        up = Document.objects.get(pk=id)
        doc_form = DocumentForm(request.POST, instance=up)
        if doc_form.is_valid():
            doc_form.save()
            messages.info(request, "Data has been updated")
    else:
        up = Document.objects.get(pk=id)
        doc_form = DocumentForm(instance=up)
    return render(request, 'app/update.html', {'form': doc_form})

def delete_data(request, id):
    if request.method == 'POST':
        delete = Document.objects.get(pk=id)
        delete.delete()
        return HttpResponseRedirect('/document')


def Register(request):
    
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            # instance = form.save(commit=False)
            # instance.save()
            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST['email']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            #Sending Email
            subject = 'Welcome to Zedpath'
            message = f'Hi {username}, Your account has been created. You can login by clicking on the given link.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list, fail_silently = False )

            # user = authenticate(username=username,)
            messages.success(request, 'Account created for {0} !!!'.format(
                username), extra_tags='alert alert-success alert-dismissible show')
            return redirect('register')
        else:
            messages.error(request, 'Username or password is invalid',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('register')

    form = UserAddForm()
    return render(request, 'app/register.html', {'form': form})


def Login(request):
    # user will redirect to home page if already login
    if request.user.is_authenticated:
        return redirect('home')

    
    form = UserLogin()
    login_user = request.user
    
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user and user.is_active:
                login(request, user)
                if user.is_authenticated:
                    return redirect('home')
            else:
                messages.error(request, 'Account is invalid',
                               extra_tags='alert alert-error alert-dismissible show')
                return redirect('login')
        else:
            return HttpResponse('data not valid')

    form = UserLogin()
    return render(request, 'app/login.html', {'form': form})


def Logout(request):
    logout(request)
    return redirect('login')
