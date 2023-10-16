toto2titi 🗔 A rag-bag of small desktop utilities
================================================

* `paste2file` 💾 Save clipboard content as a file.
* `paste2qrcode` 🔳 Display clipboard content as a QR code
* `wifi2qrcode` 🌐 Display wifi credentials as a QR code. Scanning this code with your smartphone will automatically connect it to this network.
* `paste2sms` 📲 Send clipboard content as a SMS

  `paste2sms` is a small tool which send the content of your clipboard as a SMS: do you want to share that cool link you just found (on your computer) to your friend? Copy it, and run `paste2sms` to send it as a SMS.

  .. image:: https://framagit.org/spalax/paste2sms/raw/main/doc/_static/screencast.gif

What's new?
-----------

See `changelog
<https://git.framasoft.org/spalax/paste2sms/blob/main/CHANGELOG.md>`_.

Download and install
--------------------

* From sources:

  * Download: https://pypi.python.org/pypi/toto2titi
  * Install::

        python3 -m pip install .

* From pip::

    pip install toto2titi

* Do-it-yourself Debian package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ (and `setuptools-scm <https://pypi.org/project/setuptools-scm/>`_) to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/toto2titi-<VERSION>_all.deb

  This will also install the launchers.


Documentation
-------------

* The compiled documentation is available on `readthedocs
  <http://paste2sms.readthedocs.io>`_

* To compile it from source, download and run::

      cd doc && make html
