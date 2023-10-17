#####
Setup
#####

#. Install.

   `Install Rspamd
   <https://rspamd.com/doc/quickstart.html#rspamd-installation>`_ on your server.
   It is advised to apply recommended changes to the Redis configuration.

   Then install kalabash-rspamd in you venv::

      sudo -u <kalabash_user> -i bash
      source <venv_path>/bin/activate
      pip install kalabash-rspamd

   You then need to add `kalabash_rspamd` to `KALABASH_APPS`::

      KALABASH_APPS = (
      ....
      # Kalabash extensions here.
      'kalabash_rspamd',
      )


#. Proxy setup.

   In order for rspamd to communicate with postfix, you must
   enable the `proxy worker <https://rspamd.com/doc/workers/rspamd_proxy.html>`_
   and perhaps disable the normal worker to save resources.

   Then you need to edit postfix configuration to re-route mails to rspamd milter.

   #. DKIM setup.

   It is recommended to create a "dkim" user and add it to both _rspamd and kalabash group.
   If you want to fine tune the permission, kalabash needs read/write and _rspamd only read.

   The map updating process is automatically done in the background using RQ (starting kalabash 2.2.0).
   Please take a look at the RQ instructions on kalabashs main documentation. You only need to change
   the user for the supervisord ini file.

   Then, go to the *Kalabash > Parameters > Rspamd* panel and edit the
   **Path map path** and **Selector map path** settings if necessary
   (an absolute path is required and kalabash user must have write permission on it).


   Then update Rspamd dkim signing configuration (should be here : /etc/rspamd/local.d/dkim_signing.conf):

      .. code :

      try_fallback = false;
      selector_map = "**Path map path** ";
      path_map = "**Selector map path**";


   When the configuration is done, Kalabash will completly handles the
   updates when DKIM is changed on a domain.


#. Other settings.

   You can take a look at the `configuration files
   <https://github.com/amonak/kinstaller/tree/master/kinstaller/scripts/files>`_
   available on `kinstaller <https://github.com/amonak/kinstaller>`_.
   Keep in mind, this is just a recommended configuration.
