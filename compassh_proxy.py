#!/usr/bin/perl
#
# CompaSSH - OpenSSH Helper for VPN-like services
# Copyright (C) 2012-2013  Tx0 <tx0@strumentiresistenti.org>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

use strict;
use warnings;

do "$ENV{HOME}/.compassh.conf";
do "/usr/libexec/compassh/compassh.utils";

###
### -------- Do NOT even think to change anything below this line -------
###

our $bin;

#
# Fetch arguments from command line
#
my $host = $ARGV[0] || die("No hostname or IP provided");
my $port = (defined $ARGV[1] and length $ARGV[1]) ? $ARGV[1] : 22;

#
# Define global variables (ugly, I know, but that's just a hack, mate!)
#
our $proxy = undef;
our $local_port = undef;
our $vpn = undef;

#
# If the host is matched by something, than try to figure out the
# address and then connect.
#
if ($vpn = match_pattern($host)) {
	#
	# use a proxy
	#

	#
	# first resolve the remote address using proxy /etc/hosts,
	# proxy resolver, local /etc/hosts and local resolver.
	# If anything fails (?!?!?) just use the provided $host value.
	#
	my $IP = resolve($host, $vpn);

	#
	# If there's no VPN (wow, not a real VPN, just a tunnel), starts
	# one, running in the background for future connections
	#
	if (!vpn_running($vpn)) {
		start_vpn($vpn);
		sleep 3;
	}

	#
	# launch netcat to forward the connection through the proxy
	#
	dbg("$bin->{nc} -n -X 5 -x 127.0.0.1:$local_port $IP $port", 2);
	exec($bin->{nc} . " -n -X 5 -x 127.0.0.1:$local_port $IP $port");

} else {

	#
	# simply forward the connection
	#
	exec($bin->{nc} . " $host $port");
}

__END__

=pod

=head1 NAME

compassh_proxy - CompaSSH ssh proxy command

=head1 SYNOPSYS

ProxyCommand /usr/libexec/compassh/compassh_proxy %h %p

=head1 DESCRIPTION

CompaSSH enables OpenSSH to connect to a host inside a private network
using a publicly reachable OpenSSH gateway. CompaSSH manages port forwarding and
SOCKS proxying. CompaSSH does some name resolution too to make private names valid
outside of private networks.

=head1 USAGE

compassh_proxy is a helper for OpenSSH. It must be enabled in ~/.ssh/config file
adding a line to the "Host *" stanza:

 Host *
 	ProxyCommand /usr/libexec/compassh/compassh_proxy %h %p

=head1 FILES

~/.compassh.confE<10> E<8>
	Your CompaSSH configuration

=head1 SEE ALSO

compassh(1), compassh.conf(5)

=head1 AUTHOR

Tx0 <tx0@strumentiresistenti.org>
