# CompaSSH

Claiming to be the OpenSSH VPN, but without the VPN, CompaSSH manages a set of preconfigured SSH tunnels and enables connecting to hosts on private networks by switching on a publicly reachable SSH gateway, using the SSH `ProxyCommand` feature. The private host name does not need to be publicly resolvable.

## Setting up and enabling

To setup CompaSSH, all you need to do is:

1. Copy compassh.py in a directory within your shell path
2. Link compassh.py as compassh_proxy.py too:

	$ ln -s compassh.py compassh_proxy.py

CompaSSH acts in proxy mode if invoked like this
3. Edit your ~/.ssh/config file (create one if you haven't) and set this two lines:

	Host *
		ProxyCommand /path/to/compassh_proxy.py %h %p

The third point just instructs OpenSSH to use CompaSSH as a proxy whenever a new SSH connection is started. CompaSSH will receive the remote hostname and port you want to connect (by the %h and %p macros) and will do its black magic behind the scenes to setup the required VPN (if not running yet) and will the forward all the trafic through that VPN.

## Configuring CompaSSH

CompaSSH is configured by the `~/.compassh.yaml` file:

	verbose: False
    #
    # Set a list of gateways to be used while forwarding connections
    # Each gateway has a label which is later pointed by %patterns hash.
    # Each gateway is formed by a proxy account (user@host:port) and
    # a local_port which will be used as argument for -D ssh switch.
    #
	VPN:
	    home:
	        proxy: 'root@ganimede.dontexist.net'
	        local_port: 1090
	    mycustomer:
	        proxy: root@1.2.3.4
	        local_port: 1082
	    bigcorp:
	        proxy: jdoe@bigcorp.com
	        local_port: 1083
    #
    # Each pattern here is a regular expression to be matched by
    # the host name the user is connecting to. Each pattern points
    # to a VPN listed in the VPN: section
    #
	patterns:
	    ^customer-mail: mycustomer
	    ^customer.*$: mycustomer
	    ^jdoe-desktop$: bigcorp
    #
    # /etc/hosts equivalent: basically maps a bunch of hostnames to
	# their corresponding IP addresses
    #
	hosts:
	    jdoe-desktop: 192.168.21.1
	    customer-mail: 172.20.107.32

VPNs can be started by `compassh -s <VPN name>` and stopped by `compassh -S <VPN name>`. Configured VPNs can be listed by:

    $ compassh 
    
         VPN name               SSH connection                   Port  PID
    -------------------------------------------------------------------------
         bigcorp                jdoe@bigcorp.com                 1083  -
         home                   root@ganimede.dontexist.net      1090  -
     --> mycustomer             root@1.2.3.4                     1082  1280 

Here *mycustomer* is running (see the `-->` sign on the left and the assigned PID). Each VPN can have its SSH configuration file in the `~/.ssh` directory, with the VPN name appended. For example: `~/.ssh/config.bigcorp` is the configuration file used when SSH routes the connection through the mycustomer VPN. In this file a set of prefowarded ports can be specified.

After starting the *mycustomer* VPN, the user can:

 * connect to host **customer-mail** just by `ssh customer-mail`, even if the host is on a private remote network to where no direct routing is provided
 * connect to web resources inside the remote private network by setting up a SOCKS proxy in its browser at `localhost:1082` (the Port column reports the right port) and forwarding DNS requests across the SOCKS proxy
