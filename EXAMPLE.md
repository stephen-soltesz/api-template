## junk

* The file `files/named.conf.local` contains private key data used to
  authenticate zone transfers from slave name servers.
* The deployed name server is BIND9. It is configured to run in a [chrooted
  environment](http://www.tldp.org/HOWTO/Chroot-BIND-HOWTO-1.html) to limit the
  risk exposure should someone compromise a vulnerability in BIND9.
* Be sure that the `hosts` file has the correct domain name for the VM before
  running any of the playbooks.
