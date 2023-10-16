============================================================
`paste2sms` 📲 Sends the content of your clipboard as a SMS.
============================================================

`paste2sms` is a small tool which send the content of your clipboard as a SMS: do you want to share that cool link you just found (on your computer) to your friend? Copy it, and run `paste2sms` to send it as a SMS.

A list of frequently asked questions is available :ref:`there <faq>`.

.. only:: html

  .. image:: /_static/screencast.gif

.. contents::
   :local:
   :depth: 2

Rationale
=========

Example 1
---------

I mainly use my computer to browse; my wife mainly uses her cell phone to browse. When I wanted to share an URL with her, I could:

- send her an email (too cumbersome for this task);
- copy the URL in a file, transfer it to my phone by Bluetooth, open it from my phone, copy the link and paste it in a SMS (even more cumbersome).

With `paste2sms`, I simply copy the link, run `paste2sms` (which send the content of the clipboard as an SMS to my phone), and transfer this SMS.

Example 2
---------

I suck at typing on a phone. Most of the time, when I want to send a SMS, I write it on my computer (with a real keyboard) using `paste2sms`, and, on my phone, I then forward it to its actual recipient.

Configuration file
==================

A ``paste2sms.conf`` (or ``toto2titi.conf``) :ref:`configuration file <configfile>` must exists on your computer. An example is:

.. code-block:: ini

  [general]
  provider = freemobile
  editor = gedit --wait --standalone {}

  [provider:freemobile]
  user = 12345678
  password = s3cr37

- Section ``general``:

  - ``editor``: Command line to be executed to edit the content of the SMS before sending it (where ``{}`` is replaced by a temporary file name). Can be ommited: in this case, a very simple text editor is used instead.
  - ``provider``: Provider used to send the SMS. See :ref:`smsprovider`.

- Section ``provider:FOO``:

  This section contains the options of cell phone provider `FOO`. Each provider has its own set of options. See :ref:`smsprovider`.

The list of available cell phone providers is available here: :ref:`smsprovider`.

.. _paste2sms_binaries:

Binaries
========

The `paste2sms` binary does not take any interesting arguments.
