* mklog 1.3.0 (2023-10-07)

    * Python3.12 support.
    * Add one test.

    -- Louis Paternault <spalax@gresille.org>

* mklog 1.2.0 (2022-11-29)

    * Python3.11 support.

    -- Louis Paternault <spalax@gresille.org>

* mklog 1.1.0 (2021-11-25)

    * Python support
        * Drop python3.4 and python3.6 support.
        * Add python3.7 to python3.10 support.
    * Fix bug: Standard output and error is now preserved with option --command
    * Improve error messages.
    * [setup] Use setup.cfg

    -- Louis Paternault <spalax@gresille.org>

* mklog 1.0.0 (2018-03-05)

    * Add python3.6 support.
    * Script can now be called using `python -m mklog`.
    * Minor code and documentation improvements.

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.3.3 (2015-06-13)

    * Prevent encoding errors on string received from file or (standard or error)
      input.
    * Simplification of thread management (no visible effect).
    * Several minor improvements to setup, test and documentation.

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.3.2 (2015-03-15)

    * Ported to Python3
    * Changed project URL : is now http://git.framasoft.org/spalax/mklog
    * Changed default string formatting
    * Improved documentation

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.3.1 (2013-01-27)

    * Changed project URL

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.3.0 (2011-08-10)

    * Added option "--time-format".
    * Corrected bug: Arguments of "--command" containing quotation marks are
      handled well.
    * Corrected bug: Output is correctly flushed.
    * Improved man page.
    * Small internal improvements.

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.2.0 (2011-07-24)

    * Added option "--format", to set output format.

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.1.4 (2011-01-12)

    * Complex commands such as the following one are now accepted.
      mklog -c "cat file1 & tail file2"

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.1.3 (2011-01-10)

    * Corrected bug: Error if a non-existent file is given in argument.

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.1.2 (2010-08-19)

    * Keyboard interrupt (^C) are correctly handled.
    * With option -c, standard output and error are preserved.

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.1.1 (2010-07-24)

    * Changed details in release process. No incidence on final package.

    -- Louis Paternault <spalax@gresille.org>

* mklog 0.1.0 (2010-07-24)

    * Initial release.

    -- Louis Paternault <spalax@gresille.org>
