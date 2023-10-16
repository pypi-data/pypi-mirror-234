mklog 📆 Convert any output into a log (date and time prepended to each line)
=============================================================================

`mklog` is a python program that converts standard input, content of files, or
output of a command in a log-like format, i.e. current date and time is
prepended to each line.

Run `mklog --help` for the list of available options; see examples below.

Example
-------

Download using wget:

.. code-block:: python

    $ mklog  -c wget https://archive.org/download/Popeye_Nearlyweds/Popeye_Nearlyweds.ogv
    2015-02-05 13:13:41 --2015-02-05 13:13:41--  http://t/
    2015-02-05 13:13:41 Résolution de t (t)… échec : Nom ou service inconnu.
    2015-02-05 13:13:41 wget : impossible de résoudre l'adresse de l'hôte « t »
    2015-02-05 13:13:41 --2015-02-05 13:13:41--  https://archive.org/download/Popeye_Nearlyweds/Popeye_Nearlyweds.ogv
    2015-02-05 13:13:41 Résolution de archive.org (archive.org)… 207.241.224.2
    2015-02-05 13:13:41 Connexion à archive.org (archive.org)|207.241.224.2|:443… connecté.
    2015-02-05 13:13:42 requête HTTP transmise, en attente de la réponse… 302 Moved Temporarily
    2015-02-05 13:13:42 Emplacement : https://ia700502.us.archive.org/6/items/Popeye_Nearlyweds/Popeye_Nearlyweds.ogv [suivant]
    2015-02-05 13:13:42 --2015-02-05 13:13:42--  https://ia700502.us.archive.org/6/items/Popeye_Nearlyweds/Popeye_Nearlyweds.ogv
    2015-02-05 13:13:42 Résolution de ia700502.us.archive.org (ia700502.us.archive.org)… 207.241.237.122
    2015-02-05 13:13:42 Connexion à ia700502.us.archive.org (ia700502.us.archive.org)|207.241.237.122|:443… connecté.
    2015-02-05 13:13:43 requête HTTP transmise, en attente de la réponse… 200 OK
    2015-02-05 13:13:43 Taille : 26698780 (25M) [video/ogg]
    2015-02-05 13:13:43 Sauvegarde en : « Popeye_Nearlyweds.ogv »
    2015-02-05 13:13:43
    2015-02-05 13:13:44      0K .......... .......... .......... .......... ..........  0%  126K 3m26s
    [...]
    2015-02-05 13:14:18  26000K .......... .......... .......... .......... .......... 99%  541K 0s
    2015-02-05 13:14:18  26050K .......... .......... ...                             100% 5,80M=34s
    2015-02-05 13:14:18
    2015-02-05 13:14:18 2015-02-05 13:14:18 (762 KB/s) — « Popeye_Nearlyweds.ogv » sauvegardé [26698780/26698780]
    2015-02-05 13:14:18
    2015-02-05 13:14:18 Terminé — 2015-02-05 13:14:18 —
    2015-02-05 13:14:18 Temps total effectif : 37s
    2015-02-05 13:14:18 Téléchargés : 1 fichiers, 25M en 34s (762 KB/s)

Monitor logs (which are not dated)::

    $ tail -f /var/log/gdm3/\:0.log | mklog

What's new?
-----------

See `changelog <https://git.framasoft.org/spalax/mklog/blob/main/CHANGELOG.md>`_.

Download and install
--------------------

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/mklog
  * Install (in a `virtualenv`, not to mess with your distribution installation system)::

      python3 setup.py install

* With pip::

    pip install mklog

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/mklog-<VERSION>_all.deb

See also
--------

See also (other program with the same purpose):

* `ts <http://joeyh.name/code/moreutils/>`_
