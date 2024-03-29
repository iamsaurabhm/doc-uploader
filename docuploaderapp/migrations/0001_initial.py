# Generated by Django 4.0.1 on 2022-02-07 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paraplanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paraplanner', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name_plural': 'status',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default='', max_length=100)),
                ('client_name', models.CharField(default='', max_length=100)),
                ('adviser_name', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('submitted_at', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('document', models.FileField(blank=True, upload_to='documents')),
                ('query', models.TextField(max_length=500)),
                ('paraplanner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='docuploaderapp.paraplanner')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='docuploaderapp.status')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
