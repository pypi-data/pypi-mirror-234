* toto2titi 2.2.0 (2023-10-07)

    * Python3.12 support.

    -- Louis Paternault <spalax@gresille.org>

* toto2titi 2.1.0 (2022-11-29)

    * Python 3.10 and 3.11 support.

    -- Louis Paternault <spalax@gresille.org>

* toto2titi 2.0.2 (2022-02-15)

    * setup
      * Remove useless dependency.
      * Fix dependency names (again).
      * Fix `sendsms` setup.

    -- Louis Paternault <spalax@gresille.org>

* toto2titi 2.0.1 (2021-06-10)

    * [setup] Fix dependeny names.

    -- Louis Paternault <spalax@gresille.org>

* toto2titi 2.0.0 (2021-06-10)

    * Supported python versions
        * Add python3.9 support
        * Drop python3.7 support
    * Rename to toto2titi
    * Configuration options can be set either globally in `toto2titi.conf`, or per-project (for instance `paste2sms.conf`).
    * New tools:
        * paste2file
        * paste2qrcode
        * wifi2qrcode
    * paste2sms
        * If no editor is set in the configuration file, use a quick-and-dirty one instead.

    -- Louis Paternault <spalax@gresille.org>

* paste2sms 1.1.0 (2020-05-02)

    * Add a `sendsms` binary.
    * Document the library.
    * Message is saved (in temporary directory) if it could not be sent.

    -- Louis Paternault <spalax@gresille.org>

* paste2sms 1.0.0 (2020-01-26)

    * First published version.

    -- Louis Paternault <spalax@gresille.org>
