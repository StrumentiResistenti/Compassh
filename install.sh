#!/bin/sh
#
# CompaSSH - OpenVPN Helper for VPN-like services
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

#
# This is a quick and dirt installation script. CompaSSH is
# composed by three files. A Makefile would be just overkill
#

if [ "$(id -u)" -ne 0 ]; then
	echo "This script must be run as root" 1>&2
	exit 1
fi

echo ""
echo "  #####                                   #####   #####  #     #"
echo " #     #   ####   #    #  #####     ##   #     # #     # #     #"
echo " #        #    #  ##  ##  #    #   #  #  #       #       #     #"
echo " #        #    #  # ## #  #    #  #    #  #####   #####  #######"
echo " #        #    #  #    #  #####   ######       #       # #     #"
echo " #     #  #    #  #    #  #       #    # #     # #     # #     #"
echo "  #####    ####   #    #  #       #    #  #####   #####  #     #"
echo ""

echo
echo " Installing CompaSSH, the OpenSSH helper for VPN-like services."
echo

#
# Create /usr/libexec/compassh directory
#
echo -n " 1. Creating /usr/libexec/compassh directory: "
mkdir -p /usr/libexec/compassh
chmod 755 /usr/libexec/compassh
echo "done!"
echo

#
# Copy compassh_proxy and the compassh.utils library
#
echo -n " 2. Installing compassh_proxy and compassh.utils: "
cp compassh_proxy /usr/libexec/compassh
cp compassh.utils /usr/libexec/compassh
chown -R root.root /usr/libexec/compassh
chmod 755 /usr/libexec/compassh/compassh_proxy
chmod 644 /usr/libexec/compassh/compassh.utils
echo "done!"
echo

#
# Install compassh command in /usr/bin
#
echo -n " 3. Installing /usr/bin/compassh: "
cp compassh /usr/bin
chown root.root /usr/bin/compassh
chmod 755 /usr/bin/compassh
echo "done!"
echo
echo " Now create your custom ~/.compassh.conf file, "
echo " and add to ~/.ssh/config the following lines:"
echo
echo "   Host *"
echo "     ProxyCommand /usr/libexec/compassh/compassh_proxy %h %p"
echo
echo " Full documentation is available at:"
echo "   http://www.strumentiresistenti.org/en/labs/compassh"
echo

exit 0
