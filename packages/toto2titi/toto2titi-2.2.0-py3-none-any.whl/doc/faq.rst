.. _faq:

Frequently Asked Versions
=========================

.. contents::
   :local:
   :depth: 2

paste2sms
---------

How can I send a SMS to someone else?
"""""""""""""""""""""""""""""""""""""

You cannot. I did not bother implementing this because my cell phone provider provides an API to send free SMS to myself. Then, on my smarthone, I copy-paste SMS to its recipient.

`Patches <https://framagit.org/spalax/paste2sms/issues>`_ are welcome to fix this.

Can I send images as MMS?
"""""""""""""""""""""""""

No. My phone provider provides a free API to send SMS, but not MMS, so I did not bother implementing it.

`Patches <https://framagit.org/spalax/paste2sms/issues>`_ are welcome to fix this.

Common
------

.. _configfile:

Where are the configuration files located?
""""""""""""""""""""""""""""""""""""""""""

The configuration files may be located in any directory of ``XDG_CONFIG_DIRS`` (typically ``~/.config/toto2titi.conf``). Options can be stored in the configuration file of their own application (``paste2sms.conf``, ``paste2file.conf``, etc.) or in a common configuration file: ``toto2titi.conf``.

Does it work on Windows or MacOS?
"""""""""""""""""""""""""""""""""

I don't know. Most of ``toto2titi`` should be portable:
`pull requets <https://framagit.org/spalax/paste2sms/issues>`_ are welcome…

Do you really consider the icons beautiful?
"""""""""""""""""""""""""""""""""""""""""""

Not really. But I suck at drawing…
`Patches <https://framagit.org/spalax/paste2sms/issues>`_ are welcome…
