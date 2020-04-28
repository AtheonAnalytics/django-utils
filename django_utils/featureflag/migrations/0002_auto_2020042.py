# Generated by Django 3.0.5 on 2020-04-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20200427_0911'),
        ('featureflag', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientflag',
            options={'verbose_name_plural': 'Client Flags'},
        ),
        migrations.AlterField(
            model_name='clientflag',
            name='client',
            field=models.ManyToManyField(blank=True, help_text='Activate this flag for these sites.', to='clients.Client'),
        ),
        migrations.AlterField(
            model_name='clientflag',
            name='everyone',
            field=models.NullBooleanField(help_text='Flip this flag on (Yes) or off (No) for everyone, overriding all other settings. Leave as Unknown to use normally.'),
        ),
        migrations.AlterField(
            model_name='clientflag',
            name='note',
            field=models.TextField(blank=True, help_text='Note where this Flag is used.'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='active',
            field=models.BooleanField(default=False, help_text='Is this flag active?'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='note',
            field=models.TextField(blank=True, help_text='Note where this Switch is used.'),
        ),
    ]
