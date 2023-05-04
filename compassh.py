#!/usr/bin/env python3
#
# CompaSSH - OpenSSH Helper for VPN-like services
# Copyright (C) 2012-2023  Andrea Novara <tx0@strumentiresistenti.org>
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

import sys
import compassh.config

if __name__ == "__main__":
	conf = compassh.config.Config(sys.argv[1:])

### if ($argv0 =~ /help/) {
### 	print qq(
###   CompaSSH, the SSH VPN without the VPN.
### 
###     $0 [show|list]
###       Show CompaSSH status and active VPNs
### 
###     $0 [start|stop|restart <VPN>]
###       Manages declared VPNs
###  
###     $0 [config <VPN>]
###       Show a VPN config file
### 
###     $0 [hosts [add|remove <host> <IP addr>]]
###       Show and manage internal hostname resolution map
### 
###   More information at http://strumentiresistenti.org/en/Compassh-introduction
### 
### );
### 	exit 0;
### }
### 
### if ($argv0 =~ /hosts/) {
### 	print qq(\n  Still to be implemented!\n\n);
### 	exit 1;
### }
### 
### if ($argv0 =~ /list|show/) {
### 	print "\n";
### 	print "   VPN name           SSH connection                                     Port  PID\n";
### 	print "-----------------------------------------------------------------------------------------\n";
### }
### 
### for my $vpn (sort keys %VPN) {
### 	if ($argv0 =~ /stop|restart/) {
### 		next if (($requested_vpn ne "") and ($requested_vpn ne $vpn));
### 		stop_vpn($vpn);
### 	}
### 
### 	if ($argv0 =~ /restart/) {
### 		sleep 2;
### 	}
### 
### 	if ($argv0 =~ /start|restart/) {
### 		next if (($requested_vpn ne "") and ($requested_vpn ne $vpn));
### 		start_vpn($vpn);
### 	}
### 	
### 	if ($argv0 =~ /show|list/) {
### 		show_running_vpn($vpn);
### 	}
### }
### 
### if ($argv0 =~ /config/) {
### 	unless (defined $requested_vpn and $requested_vpn) {
### 		print STDERR "No VPN provided after config\n";
### 		exit 1;
### 	}
### 
### 	my $vpn_config = $ENV{HOME} . "/.ssh/config.$requested_vpn";
### 
### 	unless (-f $vpn_config) {
### 		print STDERR "VPN $requested_vpn have no config file\n";
### 		exit 1;
### 	}
### 
### 	my $subcommand = $ARGV[2] || "show";
### 	if ($subcommand =~ /show|list|print/) {
### 		if (open(IN, $vpn_config)) {
### 			while (<IN>) { print $_; }
### 			close IN;
### 		} else {
### 			print STDERR "Unable to open $vpn_config\n";
### 		}
### 	}
### }
### 
### if ($argv0 !~ /restart|start|stop/) {
### 	print "\n";
### }
