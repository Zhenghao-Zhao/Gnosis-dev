# Generated by Django 2.0.4 on 2019-07-25 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('keywords', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CollectionEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_id', models.IntegerField()),
                ('paper_title', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers', to='catalog.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='ReadingGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a name for your group.', max_length=100)),
                ('description', models.TextField(help_text='Enter a description.')),
                ('keywords', models.CharField(help_text='Keywords describing the group.', max_length=100)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReadingGroupEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_id', models.IntegerField()),
                ('paper_title', models.TextField()),
                ('date_discussed', models.DateField(blank=True, null=True)),
                ('date_proposed', models.DateField(auto_now_add=True)),
                ('proposed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers', to=settings.AUTH_USER_MODEL)),
                ('reading_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers', to='catalog.ReadingGroup')),
            ],
        ),
    ]
