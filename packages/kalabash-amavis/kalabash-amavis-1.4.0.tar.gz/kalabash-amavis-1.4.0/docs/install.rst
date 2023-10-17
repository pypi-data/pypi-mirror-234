#######
Install
#######

Install this extension system-wide or inside a virtual environment by
running the following command::

  $ pip install kalabash-amavis

Edit the settings.py file of your kalabash instance and add
``kalabash_amavis`` inside the ``KALABASH_APPS`` variable like this::

    KALABASH_APPS = (
        'kalabash',
        'kalabash.core',
        'kalabash.lib',
        'kalabash.admin',
        'kalabash.relaydomains',
        'kalabash.limits',
        'kalabash.parameters',
        # Extensions here
        # ...
        'kalabash_amavis',
    )

Then, add the following at the end of the file::

  from kalabash_amavis.settings import *      

Run the following commands to setup the database tables::

  $ cd <kalabash_instance_dir>
  $ python manage.py migrate
  $ python manage.py collectstatic
  $ python manage.py load_initial_data
  $ python manage.py check --deploy
Finally, restart the python process running kalabash (uwsgi, gunicorn,
apache, whatever).
