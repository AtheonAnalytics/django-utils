# django-utils

## feature-flag

Feature flag package which enable per client feature flags (through customizable client field reference)

## helper 

 - `RequestsHelper` wrapper for `requests` library to handle basic auth vs token and log `outbound` API requests

## logger

 - `APILoggingMixin` to log `inbound` API requests
 - `AdminActivityMiddleware` to log django admin activity
 - `CleanedJsonFormatter` logging formatter to clean sensitive data from json logs 
 - `log_with_time` context manager to log code execution time

## Making Migrations

If you need to make changes to the models in this project, you can use the dummy manage.py file to make the relevant 
migrations file.

First, you'll need to make a model for the ClientFlag model to reference. This will need to be the same as the `FEATUREFLAG_CLIENT_MODEL`
setting in the `_settings.py` file.

E.g. In `featureflag.models.py`

```python
class DummyModel(models.Model):
    dummy_field = models.TextField()
```

In `_settings.py`

```python
FEATUREFLAG_CLIENT_MODEL = "featureflag.DummyModel"
```

Once that has been created, you can make the migrations, as you usually would
```shell
python _manage.py makemigrations
```

You'll then just need to remove any references to the dummy model in your migrations file 
(and delete the dummy model itself)

```python
migrations.CreateModel(
    name='DummyModel',
    fields=[
        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('dummy_field', models.TextField()),
    ],
),
migrations.AlterField(
    model_name='clientflag',
    name='client',
    field=models.ManyToManyField(blank=True, help_text='Activate this flag for these sites.', to='featureflag.dummymodel'),
),
```