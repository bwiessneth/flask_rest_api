#########
Flask
#########

Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.

----

License
=======

All relevant legal information can be found here

* https://www.palletsprojects.com/governance/licenses-and-copyright/



Installation
============

The name of the application you are going to set up is called **basic_flask_template**.
If you wish to use another name make sure to replace **basic_flask_template** in all of the following steps with the name of your choice.



Clone the template application
------------------------------

::

  [isabell@stardust ~]$ mkdir basic_flask_template
  [isabell@stardust ~]$ git clone https://github.com/bwiessneth/basic_flask_template.git basic_flask_template/
  [isabell@stardust ~]$

This repository comes with all the files you need for this tutorial.
Alternatively download the repository as a ZIP and extract it.



Setup python environment and install required packages
------------------------------------------------------

You definitely want to create a isolated python environment. That way the required packages you are going to install with ``pip`` are encapsulated form your systemwide python installation. For more info check https://virtualenv.pypa.io/en/latest/

::

  [isabell@stardust ~]$ cd basic_flask_template
  [isabell@stardust basic_flask_template]$ virtualenv -p python3 ENV
  [isabell@stardust basic_flask_template]$ pip install -r deploy/requirements.txt
  [isabell@stardust basic_flask_template]$ 

You can activate your new python environment like this:

::

  [isabell@stardust basic_flask_template]$ source ENV/bin/activate
  (ENV) [isabell@stardust basic_flask_template]$

Once you're done playing with it, deactivate it with the following command:

::
  
  (ENV) [isabell@stardust basic_flask_template]$ deactivate
  [isabell@stardust basic_flask_template]$ 



Setup nginx
-----------

Create an endpoint where the app will be served from. I chose that my application should be served using http under ``/basic_flask_template`` using port ``1024``.
That way your default web endpoint ``/`` will be served by apache and display what's inside ``~/html``. 

On uberspace you'll want to use the built-in ``uberspace`` tool.

:: 

  [isabell@stardust ~]$ uberspace web backend set /basic_flask_template --http --port 1024



Start your application 
----------------------

Using Werkzeug for development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use Werkzeug which get's shipped with Flask to spin up a small development server. But be aware: **Do not use it in a production deployment.** For more info head to https://www.palletsprojects.com/p/werkzeug/.

To start Werkzeug execute ``run_werkzeug.sh`` from within the application directory.
It enables the virtual python environment and uses executes ``app.py``.

Once its running try to access it at https://isabell.uber.space/basic_flask_template. Stop it by pressing ``Ctrl + C``.

::

  [isabell@stardust basic_flask_template]$ ./run_werkzeug.sh
   ℹ * Serving Flask app "app" (lazy loading)
   ℹ * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
   ℹ * Debug mode: on
   ℹ * Running on http://0.0.0.0:1024/ (Press CTRL+C to quit)
   ℹ * Restarting with stat
   ℹ * Debugger is active!
   ℹ * Debugger PIN: 262-417-928
  [isabell@stardust basic_flask_template]$ ^C
  [isabell@stardust basic_flask_template]$




UWSGI
^^^^^

A more suited approach to serve your application would be to use uWSGI.
The uWSGI project aims at developing a full stack for building hosting services.  For more info head to https://uwsgi-docs.readthedocs.io/en/latest/.

To serve your application via uWSGI execute the ``run_uwsgi.sh`` script from within the application directory.
It enables the virtual python environment and uses the configuration parameter found in ``uwsgi.ini``.
The application is loaded from ``uwsgi_app.py``, which justs imports the ``app`` object from ``app.py``.

Once its running try to access it at https://isabell.uber.space/basic_flask_template. Stop it by pressing ``Ctrl + C``.

::

  [isabell@stardust basic_flask_template]$ ./run_uwsgi.sh
  [uWSGI] getting INI configuration from uwsgi.ini
  ℹ *** Starting uWSGI 2.0.18 (64bit) on [Tue Jan 21 15:47:41 2020] ***
  ℹ ...
  ℹ *** uWSGI is running in multiple interpreter mode ***
  ℹ spawned uWSGI master process (pid: 23422)
  ℹ spawned uWSGI worker 1 (pid: 23455, cores: 1)
  [isabell@stardust basic_flask_template]$ ^C
  [isabell@stardust basic_flask_template]$


Use supervisord to monitor and control your processes 
-----------------------------------------------------

Supervisor is a client/server system that allows its users to monitor and control a number of processes on UNIX-like operating systems.
For more info head to http://supervisord.org.

Copy the configuration file somewhere supervisord can find it. After that we tell supervisord to reread and update the found configurations. After that you can use ``status``, ``start`` and ``stop`` to control your application process.

::

  [isabell@stardust ~]$ cp basic_flask_template/deploy/basic_flask_template.ini ~/etc/services.d/
  [isabell@stardust ~]$ supervisorctl reread
  [isabell@stardust ~]$ supervisorctl update
  [isabell@stardust ~]$ supervisorctl start basic_flask_template
  ℹ basic_flask_template: started
  [isabell@stardust ~]$ supervisorctl status basic_flask_template  
  ℹ basic_flask_template             RUNNING   pid 30707, uptime 0:00:34
  [isabell@stardust ~]$ supervisorctl stop basic_flask_template
  ℹ basic_flask_template: stopped
  [isabell@stardust ~]$ 
