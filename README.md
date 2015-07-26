# Compassh

the OpenSSH VPN, without the VPN. CompaSSH manages a set of preconfigured SSH tunnels and enables connecting to hosts on private networks by switching on a publicly reachable SSH gateway, using SSH `ProxyCommand` feature. The private host does not need to be publicly resolvable.

CompaSSH is configured by the `~/.compassh.conf` file:

    #!/usr/bin/perl

    our $debug = 1;

    #
    # Set a list of gateways to be used while forwarding connections
    # Each gateway has a label which is later pointed by %patterns hash.
    # Each gateway is formed by a proxy account (user@host:port) and
    # a local_port which will be used as argument for -D ssh switch.
    #
    our %VPN = (
        home => {
            proxy => 'root@ganimede.dontexist.net',
            local_port => "1090",
        },
        mycustomer => {
            proxy => 'root@1.2.3.4',
            local_port => "1082",
        },
        bigcorp => {
            proxy => 'jdoe@bigcorp.com',
            local_port => "1083",
        },
    );

    #
    # Each pattern here is a regular expression to be matched by
    # the host name the user is connecting to. Each pattern points
    # to a gateway listed in %gateways hash.
    #
    our %patterns = (
        '^customer-mail' => 'mycustomer',
        '^customer.*$' => 'mycustomer',
        '^jdoe-desktop$' => 'bigcorp',
    );

    #
    # /etc/hosts equivalent
    #
    our %hosts = (
        'jdoe-desktop' => '192.168.21.1',
        'customer-mail' => '172.20.107.32',
    );

VPNs can be started by `compassh start <VPN name>` and stopped by `compassh stop <VPN name>`. If a name is not provided, CompaSSH will start or stop all the VPNs. Configured VPNs can be listed by:

    $ compassh 
    
       VPN name               SSH connection                   Port  PID
    -----------------------------------------------------------------------
       bigcorp                jdoe@bigcorp.com                 1083  -
       home                   root@ganimede.dontexist.net      1090  -
     + mycustomer             root@1.2.3.4                     1082  1280 

Here *mycustomer* is running (see the `+` sign on the left and the assigned PID). Each VPN can have is SSH configuration file in the `~/.ssh` directory, with the VPN name appended. For example: `~/.ssh/config.bigcorp`. In this file a set of prefowarded ports can be specified.

After starting the *mycustomer* VPN, the user can:

 * connect to host **customer-mail** just by `ssh customer-mail`, even if the host is on a private remote network
 * connect to web resources inside the remote private network by setting up a SOCKS proxy in its browser at `localhost:1082` (the Port column reports the right port) and forwarding DNS requests across the SOCKS proxy

More information can be found at http://www.strumentiresistenti.org/en/labs/compassh

CompaSSH documentation can be read at http://github.com/StrumentiResistenti/Compassh/blob/master/docs/compassh.pdf
