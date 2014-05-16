Setting up a VM using Vagrant, and getting Weather to run
=========================================================

Background
----------

We are trying not to have too many differences between production and
the Vagrant. Nevertheless, there are a couple. Out-of-the-box, the
code in Git should work with a Vagrant dev setup; there are a couple
changes needed for production deployment.

These differences:

 * file-based "email" backend (see bottom of weather/settings.py)
 * "weather.dev" as the URL (see weather/config/config.py)

Please note that the only thing you will have to do is edit your _/etc/hosts_
file accordingly to contain this line:

```sh
192.168.33.10 weather.dev
```

This will allow you to point your browser to "weather.dev"; this is
the hostname used by the Vagrant setup. So then visiting
"https://weather.dev" in your host's browser should be seeing the
Vagrant box.


Clone Weather Git repo
----------------------

https://gitweb.torproject.org/user/karsten/weather.git/shortlog/refs/heads/vagrant

This box uses Wheezy 7.3 (which is not the latest release), but comes with Puppet installed.  (See TODO below.)

Start VM using Vagrant
----------------------

```sh
vagrant up
vagrant ssh
```

TODO
----

 - clean up hostnames and network-config
 - huge TODO: can all these setup-shenanigans be handled via puppet?  Abhiram says: "Once the sym-links and directories are created, may be this task can be automated. Will think about this later."
 - Upgrade VM to latest Wheezy release.  We could ask Puppet to update the distro.  But that would mean everyone would have to download the new distro when starting the VM for the first time and whenever they run `vagrant provision`.  Maybe there are better ways.  Like, Puppet Labs releasing a new image.
 - Cron-tab with Puppet. Try to add the background task as a cron job using puppet.  Unless that's something we don't want in the development environment.  Let's postpone this.
