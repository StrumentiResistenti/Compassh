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

import getopt, yaml, os, sys

class Config:
	"""Manages CompaSSH configuration"""

	def __init__(self, argv):
		self.parse_config_files()
		self.parse_command_line(argv)
	
	#
	# Parse the command line arguments
	#
	# h = Help
	# v = Verbose
	# c = Show config
	# H = Show internal host table
	# p = Show declared patterns
	# l = List VPN (default behaviour)
	# s = Start VPN
	# S = Stop VPN
	# r = Restart VPN
	# V = The selected VPN
	#
	def parse_command_line(self, argv):
		self.conf['args'] = {'action': 'show_vpn'}
		opts, args = getopt.getopt(argv, "hvcHlsSrpV:")
		for opt, arg in opts:
			if opt == '-h':
				self.print_help()
			elif opt == '-v':
				self.conf['args']['verbose'] = True
				print("Verbose logging enabled\n")
			elif opt == '-c':
				self.conf['args']['action'] = 'show_config'
			elif opt == '-H':
				self.conf['args']['action'] = 'show_hosts'
			elif opt == '-l':
				self.conf['args']['action'] = 'show_vpn'
			elif opt == '-p':
				self.conf['args']['action'] = 'show_patterns'
			elif opt == '-s':
				self.conf['args']['action'] = 'start_vpn'
			elif opt == '-S':
				self.conf['args']['action'] = 'stop_vpn'
			elif opt == '-R':
				self.conf['args']['action'] = 'restart_vpn'
			elif opt == '-V':
				self.conf['args']['vpn'] = arg
				print(f"Operating on VPN {self.conf['args']['vpn']}")

	#
	# Read configuration from the user home and from the system file
	#
	def parse_config_files(self):
		conf_yaml = self.conf_file_path()
		if os.path.exists(conf_yaml) and os.path.isfile(conf_yaml):
			with open(conf_yaml, "r") as ymlfile:
				self.conf = yaml.safe_load(ymlfile)
			if self.conf['verbose']:
				print("verbose enabled\n")

		else:
			print(f"Unable to read {conf} configuration file")
			sys.exit(1)
	
	#
	# Provide the path of the main config file
	#
	def conf_file_path(self):
		home = os.path.expanduser('~')
		return f"{home}/.compassh.conf"

	def arg(self, a):
		return self.conf['args'][a]
	
	def action(self):
		return self.arg('action')

	def vpn(self, v):
		return self.conf['VPN'][v]
	
	def pattern(self, p):
		return self.conf['patterns'][p]
	
	def host(self, h):
		return self.conf['hosts'][h]

	def print_help(self):
		command = sys.argv[0]
		print(f"""
CompaSSH, the SSH VPN without the VPN.

  {command} -l
    Show CompaSSH status and active VPNs

  {command} -s -V <VPN>
  {command} -S -V <VPN>
  {command} -r -V <VPN>
    Start, stop or restart the specified VPN

  {command} -c -V <VPN>
    Show a VPN config file

  {command} -H 
    Show internal hostname resolution map

More information at http://strumentiresistenti.org/en/Compassh-introduction
""")
