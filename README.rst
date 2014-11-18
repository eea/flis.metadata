====================
Flis Metadata Client
====================

Client for Flis application that require common metadata

Quick start
-----------

1. Add "flis_metadata.common" and "flis_metadata.client"
   to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'flis_metadata.common',
          'flis_metadata.client',
      )

2. Add METADATA_REMOTE_HOST into your settings file::

     METADATA_REMOTE_HOST = 'http://localhost:8000'

3. Run `python manage.py syncdb` to create the metadata models.

4. Run `python manage.py migrate` to migrate the common app.
   Note:
    If you are using django below 1.7.0 run `pip install south` and add it to
    INSTALLED_APPS.

5. Run `python manage.py sync_remote_models` to sync the metadata models with
   the remote ones.

How to add a new model
----------------------
We want to move model `Foo` from `flis.someapp` to be
replicated in all flis apps

In the this app:
    1. Add the model in `common/models.py`. Make sure it extends ReplicatedModel

    2. Add urls views and templates to edit it.

    3. Add a fixture having all instances of `Foo` for every flis app.

    4. Update the pip package using `setup.py`.

In `flis.someapp` and other apps using this model
    1. Update `eaa.flis.metadata` package in requirements.txt and install it
    
    2. For every `x = models.ForeingKey(Foo)` and
       `y = models.ManyToManyField(Foo)` add a new fields:
       `fake_x = models.ForeingKey('common.Foo')` or
       `fake_y = models.ManyToManyField('common.Foo')` and generate a migration

    3. Create a datamigration that:
        1. Calls `load_metadata_fixtures`
        2. For every `x` copies the same information in `fake_x` using the
           instance found in `common.Foo`.
           e.g. `obj.fake_x = orm['common.Foo'].objects.get(title=obj.x.title)`

    4. Remove the Foo model and `x` fields from `flis.someapp`

    5. Create an automatic schemamigration 

    6. Rename `fake_x` fields to `x`

    7. In the migration generated at 5. rename the fields and M2M tables from
       `fake_x` to `x`

    8. Make sure you don't break anything
