pypimonitor 📈 Monitor your pypi packages
=========================================

    Unfortunately, due to a pypi bug, download statistics got from the json API are bogus. So some of the data displayed by this program (download badges, and line charts) are bogus too… This will be fixed when the pypi bug itself will be fixed.
    See for instance `#699 <https://github.com/pypa/warehouse/issues/699>`_ and `#787 <https://github.com/pypa/warehouse/issues/787>`_.
    
An HTML dashboard to monitor your `PyPI packages <http://pypi.python.org>`_. It
displays a line charts showing the evolution of downloads across versions, and
a set of badges (download statistics, `readthedocs <http://readthedocs.io>`__ badge,
continuous integration, etc.). See the example below.

|example|

.. |example| image:: http://pypimonitor.readthedocs.io/en/latest/_static/spalax.png
   :target: http://spalax.frama.io/pypimonitor

It is available as a `command line interface <http://pypimonitor.readthedocs.io/en/latest/module#pypimonitor-httpd>`_ that
generates the HTML code, and as a `web server <http://pypimonitor.readthedocs.io/en/latest/module#pypimonitor-httpd>`_, to
generate and serve this dashboard.

What's new?
-----------

See `changelog <http://framagit.org/spalax/pypimonitor/blob/main/CHANGELOG.md>`_.

What's next?
------------

This package replaces a static page that I manually updated from times to times. It does what I need, so there is little chance that I will develop it further. However, I see two directions this project could take:

- break everything, remove every single line of python code, and rewrite everything in javascript, so that this can be served as a static page (from the server point of view) that can be published using `gitlab pages <https://docs.gitlab.com/ee/pages/README.html>`_ or `github pages <https://pages.github.com/>`_, `readthedocs <http://readthedocs.io>`__, etc., and conquer the world;
- or replace this quick and dirty web server using `your favorite web framework <http://wiki.python.org/moin/WebFrameworks>`_, cache requests to the pypi API, publish it somewhere, and conquer the world.

I will do neither. But if you want to, you have my blessing… :)

Download and install
--------------------

* From sources:

  * Download: https://pypi.python.org/pypi/pypimonitor
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python3 setup.py install

* From pip::

    pip install pypimonitor

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/pypimonitor-<VERSION>_all.deb

Documentation
-------------

* The compiled documentation is available on `readthedocs <http://pypimonitor.readthedocs.io>`_

* To compile it from source, download and run::

      cd doc && make html
