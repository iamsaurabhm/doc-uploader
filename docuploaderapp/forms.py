from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from docuploaderapp.models import *


class UserAddForm(UserCreationForm):
    '''
    Extending UserCreationForm - with email
    '''
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username', 'class': 'form-control', }))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'email@gmail.com', 'class': 'form-control', }))

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
                # field.widget.attrs['class'] += ' placeholder'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = 'password'

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        qry = User.objects.filter(email=email)

        domain_list = ['xyz.com', 'abc.com']
        # get me whatever after @, eg. gmail.com
        get_zedpath_domain = email.split('@')[1]

        print(get_zedpath_domain in domain_list)

        if qry.exists():
            '''
            True - Queryset exist run validation message here
            '''
            raise forms.ValidationError(
                'email {0} already exists'.format(email))

        elif get_zedpath_domain not in domain_list:
            print('test - not in domain')
            raise forms.ValidationError('email does not contain domain')

        return email


class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username', 'class': 'form-control', }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'password', 'class': 'form-control', }))


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['company_name', 'client_name', 'adviser_name',
                  'submitted_at', 'due_date', 'paraplanner', 'status', 'query', 'document',]

        labels = {'company_name': 'Company Name', 'client_name': 'Client Name',
                  'adviser_name': 'Adviser Name', 'submitted_at': 'Date Submitted',
                  'due_date': 'Due Date', 'paraplanner': 'Paraplanner', 'status': 'Status',
                  'document': 'Document', 'query': 'Query'}

        widgets = {
            # 'username' : forms.TextInput(attrs={'class':'form-control', 'id':'width',}),
            'company_name': forms.TextInput(attrs={'class': 'form-control ', 'id': 'width', }),
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'width', }),
            'adviser_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'width', }),
            'submitted_at': forms.DateInput(attrs={'class': 'datepicker form-control', }),
            'due_date': forms.DateInput(attrs={'class': 'datepicker form-control', }),
            'paraplanner': forms.Select(attrs={'class': 'form-select text', 'id': 'width'}),
            'status': forms.Select(attrs={'class': 'form-select text', 'id': 'width', }),
            'query': forms.Textarea(attrs={'class': 'form-control', 'id': 'width', }),
        }
 