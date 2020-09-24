######
Deploy
######



***************
Clone this repo
***************

::

  [ziggy@stardust ~]$ git clone https://github.com/bwiessneth/flask_rest_api.git flask_rest_api/
  [ziggy@stardust ~]$



******************************************************
Setup python environment and install required packages
******************************************************

You definitely want to create a isolated python environment. That way the required packages you are going to install with ``pip`` are encapsulated form your systemwide python installation. For more info check https://virtualenv.pypa.io/en/latest/

::

  [ziggy@stardust ~]$ cd flask_rest_api
  [ziggy@stardust flask_rest_api]$ virtualenv -p python3 ENV
  [ziggy@stardust flask_rest_api]$ pip install -r deploy/requirements.txt
  [ziggy@stardust flask_rest_api]$ 


You can activate your new python environment like this:

::

  [ziggy@stardust flask_rest_api]$ source ENV/bin/activate
  (ENV) [ziggy@stardust flask_rest_api]$

Once you're done playing with it, deactivate it with the following command:

::
  
  (ENV) [ziggy@stardust flask_rest_api]$ deactivate
  [ziggy@stardust flask_rest_api]$ 



******************************************************
Setup nginx
******************************************************

Create an endpoint where the app will be served from. I chose that my application should be served using http under ``/flask_rest_api`` using port ``1025``.
That way your default web endpoint ``/`` will be served by apache and display what's inside ``~/html``. 

On uberspace you'll want to use the built-in ``uberspace`` tool.

:: 

  [ziggy@stardust ~]$ uberspace web backend set /flask_rest_api --http --port 1025 --remove-prefix



Start your application 
----------------------

Using Werkzeug for development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use Werkzeug which get's shipped with Flask to spin up a small development server. But be aware: **Do not use it in a production deployment.** For more info head to https://www.palletsprojects.com/p/werkzeug/.

To start Werkzeug execute ``run_werkzeug.sh`` from within the application directory.
It enables the virtual python environment and executes ``flask_rest_api.py``.

Once its running try to access it at ``/flask_rest_api/users``. Stop it by pressing ``Ctrl + C``.

::

  [ziggy@stardust flask_rest_api]$ ./run_werkzeug.sh
   ℹ * Serving Flask app "app" (lazy loading)
   ℹ * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
   ℹ * Debug mode: on
   ℹ * Running on http://0.0.0.0:1025/ (Press CTRL+C to quit)
   ℹ * Restarting with stat
   ℹ * Debugger is active!
   ℹ * Debugger PIN: 262-417-928
  [ziggy@stardust flask_rest_api]$ ^C
  [ziggy@stardust flask_rest_api]$




UWSGI
^^^^^

A more suited approach to serve your application would be to use uWSGI.
The uWSGI project aims at developing a full stack for building hosting services.  For more info head to https://uwsgi-docs.readthedocs.io/en/latest/.

To serve your application via uWSGI execute the ``run_uwsgi.sh`` script from within the application directory.

Once its running try to access it at https://ziggy.uber.space/flask_rest_api. Stop it by pressing ``Ctrl + C``.

::

  [ziggy@stardust flask_rest_api]$ ./run_uwsgi.sh
  [uWSGI] getting INI configuration from uwsgi.ini
  ℹ *** Starting uWSGI 2.0.18 (64bit) on [Tue Jan 21 15:47:41 2020] ***
  ℹ ...
  ℹ *** uWSGI is running in multiple interpreter mode ***
  ℹ spawned uWSGI master process (pid: 23422)
  ℹ spawned uWSGI worker 1 (pid: 23455, cores: 1)
  [ziggy@stardust flask_rest_api]$ ^C
  [ziggy@stardust flask_rest_api]$


Use supervisord to monitor and control your processes 
-----------------------------------------------------

Supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.
For more info head to http://supervisord.org.

Copy the configuration file somewhere supervisord can find it. After that we tell supervisord to reread and update the found configurations. After that you can use ``status``, ``start`` and ``stop`` to control your application process.

::

  [ziggy@stardust ~]$ cp flask_rest_api/deploy/flask_rest_api.ini ~/etc/services.d/
  [ziggy@stardust ~]$ supervisorctl reread
  [ziggy@stardust ~]$ supervisorctl update
  [ziggy@stardust ~]$ supervisorctl start flask_rest_api
  ℹ flask_rest_api: started
  [ziggy@stardust ~]$ supervisorctl status flask_rest_api  
  ℹ flask_rest_api             RUNNING   pid 30707, uptime 0:00:34
  [ziggy@stardust ~]$ supervisorctl stop flask_rest_api
  ℹ flask_rest_api: stopped
  [ziggy@stardust ~]$ 
