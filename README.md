# CompaSSH

Claiming to be the OpenSSH VPN, but without the VPN, CompaSSH manages a set of preconfigured SSH tunnels and enables connecting to hosts on private networks by switching on a publicly reachable SSH gateway, using the SSH `ProxyCommand` feature. The private host name does not need to be publicly resolvable.

## Setting up and enabling

Setting up CompaSSH is as easy as following this 1-2-3:

1. Copy compassh.py in a directory within your shell path. I have a ~/bin folder in my home dir that I use for my personal tools and scripts, but you can pick the one you prefer, as long as it's inside your $PATH:

```
$ cp compassh.py ~/bin
```

2. Inside that path, link compassh.py as compassh_proxy.py too, this will tell CompaSSH to act in proxy mode when invoked like this:

```
$ ln -s compassh.py compassh_proxy.py
```

3. Edit your ~/.ssh/config file (create one if you haven't) and set this two lines:

```
Host *
	ProxyCommand /path/to/compassh_proxy.py %h %p
```

The third point just instructs OpenSSH to use CompaSSH as a proxy whenever a new SSH connection is started. CompaSSH will receive the remote hostname and port you want to connect (by the %h and %p macros) and will do its black magic behind the scenes to setup the required VPN (if not running yet) and will then forward all the trafic through that VPN.

## Configuring CompaSSH

After setting up CompaSSH to work with OpenSSH, you still need to declare the VPNs and the rules to use them. This is done by writing a file named `~/.compassh.yaml`:

```
verbose: False

#
# Set a list of VPNs to be used while forwarding connections
# Each VPN has a label which is later pointed by the patterns section.
# Each VPN is formed by a proxy account (user@host:port) and
# a local_port which will be used as argument for -D ssh switch.
# The local port must be unique among the VPNs.
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
# to a VPN listed in the VPN section
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
```

## Command line interface 

VPNs can be started by `compassh -s <VPN name>` and stopped by `compassh -S <VPN name>`. 

Configured VPNs can be listed by:

    $ compassh 
    
         VPN name               SSH connection                   Port  PID
    -------------------------------------------------------------------------
         bigcorp                jdoe@bigcorp.com                 1083  -
         home                   root@ganimede.dontexist.net      1090  -
     --> mycustomer             root@1.2.3.4                     1082  1280 

Here *mycustomer* is running (see the `-->` sign on the left and the assigned PID). 

The internal hostname resolution can be tested by `compassh.py -R <hostname>`. Please note that <hostname> must match a host-to-VPN pattern to be resolved, otherwise the request will not be honoured.

## Configuring VPN port forwarding

Each VPN can have its own SSH configuration file in the `~/.ssh` directory, with the VPN name appended. For example: `~/.ssh/config.bigcorp` is the configuration file used when bigcorp VPN is activated. In this file a set of prefowarded ports can be specified, like in the example below:

```
Host *
        LocalForward 10001 localhost:10001
        LocalForward 8080 192.168.1.20:8080
```

With this file named `~/.ssh/conf.bigcorp` and after starting the bigcorp VPN with `compassh -s bigcorp`, the local port 10001 will be forwarded on port 10001 of the remote host, while 8080 will be forwarded on port 8080 of host 192.168.1.20, which is identified by a private address and is then reachable thanks to the proxy started on bigcorp' gateway. Thanks to this port forwarding you can reach the application server located at 192.168.1.20 (8080 is usually assigned to application servers) which is not publicly exposed.

## CompaSSH automatic routing

The most interesting feature of CompaSSH is the routing of SSH connections without requiring any other step. Let's suppose you are the owner of jdoe-desktop which is privately addressable on the bigcorp intranet. Let's also suppose you're moving and have only access to bigcorp public SSH gateway. Let's then focus on this subset of the YAML configuration:

```
VPN:
  bigcorp:
    proxy: jdoe@bigcorp.com
    local_port: 1083
patterns:
  ^jdoe-desktop$: bigcorp
hosts:
  jdoe-desktop: 192.168.21.1
```

This YAML states that:

1. It is possible to establish a VPN connection named bigcorp by connecting with SSH to host bigcorp.com as jdoe (private key credentials are assumed here)
2. Any SSH connection to host jdoe-desktop can be routed through that bigcorp VPN
3. Since the jdoe-desktop host has only a privately resolvable address, the conf suggest the resolution to 192.168.21.1

With this YAML in place as `~/.compassh.yaml`, right after powering up your PC and connecting to the Internet, without any other intermediate step, wherever you are, you can SSH straight to jdoe-desktop by just entering on your terminal:

```
$ ssh jdoe-desktop
```

OpenSSH will use compassh_proxy.py as its ProxyCommand, which in turn will decide to first power up the bigcorp VPN and route through it the connection to jdoe-desktop, using address 192.168.21.1 as its final destination.

Since the VPN is now active: 
* any SOCKS connection routed through port 1083 will be established from within bigcorp' network 
* any port forwardings possibly defined in a file named `~/.ssh/config.bigcorp` will be available as well
