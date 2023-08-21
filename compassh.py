#!/usr/bin/env python3
#
# CompaSSH - OpenSSH Helper for VPN-like services
# Copyright (C) 2012-2023 Andrea Novara <tx0@strumentiresistenti.org>
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
import getopt
import yaml
import os
import subprocess
import re
import socket
import time

class Config:
	"""Manages CompaSSH configuration"""

	def __init__(self, argv):
		self.parse_config_files()
		self.parse_command_line(argv)
		self.exe_scan()
		self.execution_mode()
	
	def parse_command_line(self, argv):
		"""
		Parse the command line arguments
		
		h = Help
		v = Verbose
		c = Show config for a specific VPN
		H = Print the internal host table
		p = Print declared patterns
		l = List all the VPN (default behaviour)
		s = Start VPN
		S = Stop VPN
		r = Restart VPN
		R = Resolve a hostname like the CompaSSH proxy would do
		
		"""
		self.conf['args'] = {'action': 'show_vpn'}
		opts, args = getopt.getopt(argv, "hvc:Hls:S:r:R:p")
		for opt, arg in opts:
			if opt == '-h':
				self.print_help()
			elif opt == '-v':
				self.conf['args']['verbose'] = True
				print("Verbose logging enabled\n")
			elif opt == '-c':
				self.conf['args']['action'] = 'show_config'
				self.conf['args']['target'] = arg
			elif opt == '-H':
				self.conf['args']['action'] = 'show_hosts'
			elif opt == '-l':
				self.conf['args']['action'] = 'show_vpn'
			elif opt == '-p':
				self.conf['args']['action'] = 'show_patterns'
			elif opt == '-s':
				self.conf['args']['action'] = 'start_vpn'
				self.conf['args']['target'] = arg
			elif opt == '-S':
				self.conf['args']['action'] = 'stop_vpn'
				self.conf['args']['target'] = arg
			elif opt == '-r':
				self.conf['args']['action'] = 'restart_vpn'
				self.conf['args']['target'] = arg
			elif opt == '-R':
				self.conf['args']['action'] = 'resolve_host'
				self.conf['args']['target'] = arg

	def parse_config_files(self):
		""" Read configuration from the user home and from the system file """
		conf_yaml = self.conf_file_path()
		if os.path.exists(conf_yaml) and os.path.isfile(conf_yaml):
			with open(conf_yaml, "r") as ymlfile:
				self.conf = yaml.safe_load(ymlfile)
			if self.conf['verbose']:
				print("verbose enabled\n")

		else:
			print(f"Unable to read {conf} configuration file")
			sys.exit(1)
	
	def conf_file_path(self):
		"""
		Provide the path of the main config file
		"""
		home = os.path.expanduser('~')
		return f"{home}/.compassh.yaml"
	
	def vpn_conf_file_path(self, vpn):
		"""
		Provide the path of a VPN config file.
		If the file does not exist, the default path ~/.ssh/config.compassh is provided.
		If even that has not been created, /dev/null is returned.
		"""
		home = os.path.expanduser('~')
		conf_file = f"{home}/.ssh/config.{vpn}"
		default_conf_file = f"{home}/.ssh/config.compassh"
		if os.path.isfile(conf_file):
			return conf_file
		elif os.path.isfile(default_conf_file):
			return default_conf_file
		else:
			return "/dev/null"

	def arg(self, a):
		""" return a specific argument from the command line """
		return self.conf['args'][a]
	
	def action(self):
		""" return the requested action """
		return self.arg('action')

	def vpn(self, v):
		""" return the configuration of a specific VPN """
		return self.conf['VPN'][v]
	
	def pattern(self, p):
		""" return a configured proxy pattern """
		return self.conf['patterns'][p]
	
	def host(self, h):
		""" return a host from the internal host table """
		return self.conf['hosts'][h]

	def exe_scan(self):
		""" scan the filesystem to locate the executable CompaSSH uses """
		self.conf['cmd'] = dict()
		for exe in ['nc', 'ssh', 'kill', 'lsof']:
			# exe_path = subprocess.Popen(['/usr/bin/which', exe], stdout=subprocess.PIPE, shell=False)
			with os.popen(f"which {exe}") as which:
				option = which.readlines()
				if len(option) == 0:
					print(f"Unable to locate {exe}, aborting execution!")
					sys.exit(1)
				else:
					exe_path = option[0][:-1]
					self.conf['cmd'][exe] = exe_path
					# print(f"{exe} is located at [{exe_path}]")
	
	def execution_mode(self):
		""" guess if CompaSSH must operate in CLI or proxy mode """
		em = __file__.split("/")[-1]
		if em == 'compassh_proxy' or em == 'compassh_proxy.py':
			self.conf['args']['execution_mode'] = 'proxy'
		else:
			self.conf['args']['execution_mode'] = 'cli'
	
	def run_cli(self):
		""" Return true if CLI mode is requested """
		return self.conf['args']['execution_mode'] == 'cli'
	
	def run_proxy(self):
		""" Return true if proxy mode is requested """
		return not self.run_cli()
	
	def cmd(self, prg):
		""" Return the path of a specific executable """
		return self.conf['cmd'][prg]
	
	def target(self):
		""" return the target of the requested action (a VPN name, a host name, ...) """
		return self.arg('target')
	
	def parent(self, target):
		""" return the name of the VPN the target VPN depends on (if any), oherwise return None """
		if 'parent' in self.vpn(target):
			return self.vpn(target)['parent']
		else:
			return None

	def print_help(self):
		command = sys.argv[0]
		print(f"""
CompaSSH, the SSH VPN without the VPN.

  {command} -l
    Show CompaSSH status and active VPNs (default)

  {command} -s <VPN>
  {command} -S <VPN>
  {command} -r <VPN>
    Start, stop or restart the specified VPN

  {command} -c <VPN>
    Show a VPN config file

  {command} -H 
    Show internal hostname resolution map

  {command} -p
    Print the configured host-to-VPN mapping patterns 

  {command} -R <hostname>
    Resolve <hostname> using all the resolution strategies available
    <hostname> must match a VPN pattern to be resolved

  {command} -h
    Print this help screen
""")
		sys.exit(0)

class Actions:
	""" Holds all the actions the CLI performs """

	def show_hosts(conf):
		""" Show hosts from the internal host table """
		print("\n")
		print("       IP Address   Hostname                           ")
		print("-----------------------------------------------------------------------------------------")
		hosts = conf.conf['hosts']
		for h in hosts:
			print("  %15s   %s" % (hosts[h], h))
		print()
		sys.exit(0)
	
	def show_vpn(conf):
		""" Show the VPN with their status (default behaviour) """
		print("\n")
		print("    VPN name           SSH connection                                     Port   PID")
		print("----------------------------------------------------------------------------------------")
	
		vpn = conf.conf['VPN']
		for v in vpn:
			pid = Actions.vpn_running(conf, v)
			running = "   "
			if pid != 0:
				running = '-->'
			print("%s %-18s %-50s %-6d %s" % (running, v, vpn[v]['proxy'], vpn[v]['local_port'], pid))
		print()
		sys.exit(0)
	
	def show_patterns(conf):
		""" Show internal patterns used to guess which VPN a host should be routed through """
		print("\n")
		print("   Pattern                                  VPN                                     ")
		print("-----------------------------------------------------------------------------------------")
		patterns = conf.conf['patterns']
		for p in patterns:
			print("   %-40s %s" % (p, patterns[p],))
		print()
		sys.exit(0)
	
	def start_vpn(conf, target):
		""" Start a VPN """
		proxy = conf.vpn(target)['proxy']
		local_port = conf.vpn(target)['local_port']
	
		pid = Actions.vpn_running(conf, target)
		if (pid):
			print(f"VPN {target} #{local_port} already running on PID: {pid}")
		else:
			parent = conf.parent(target)
			if parent != None:
				start_vpn(conf, parent)
				ppid = Actions.vpn_running(conf, parent)
				if ppid == 0:
					print(f"Error starting parent VPN {parent} - Aborting VPN {target}")
					return
	
			profile = conf.vpn_conf_file_path(target)
		
			cmd = f"{conf.cmd('ssh')} -F {profile} -C -q -N -D0.0.0.0:{local_port} {proxy}".split(" ");
			print(f"Starting {cmd}");
			subprocess.Popen(cmd)
			time.sleep(2)
			Actions.show_vpn(conf)
	
	def stop_vpn(conf, target):
		""" Stop a VPN """
		proxy = conf.vpn(target)['proxy']
		local_port = conf.vpn(target)['local_port']
	
		pid = Actions.vpn_running(conf, target)
		if (pid):
			print(f"Killing VPN {target} #{local_port} (PID: {pid})")
			os.system(f"{conf.cmd('kill')} {pid}")
		else:
			print(f"VPN {target} #{local_port} NOT running")
	
	def restart_vpn(conf, target):
		""" Restart a VPN """
		Actions.stop_vpn(conf, target)
		Actions.start_vpn(conf, target)
	
	def vpn_running(conf, target):
		""" Check if a VPN is running and return its PID """
		local_port = conf.vpn(target)['local_port']
	
		def transform(line):
			return re.sub('^[^\s]+\s+([0-9]+)[^:]+:([0-9]+).*$', '\\2:\\1', line)
	
		def predicate(line):
			return re.match(f'^{local_port}:', line)
	
		entry = list(filter(predicate, map(transform, subprocess.getoutput(f"{conf.cmd('lsof')} -nP -iTCP -sTCP:LISTEN").split("\n")[1:])))
		if len(entry) == 0:
			return 0
	
		return entry[0].split(":")[1]
	
	def show_config(conf, vpn):
		""" Show SSH configuration used with a specific VPN """
		conf_file = conf.vpn_conf_file_path(vpn)
		if conf_file == "/dev/null":
			print(f"VPN {vpn} has no config file and no default config file has been created as ~/.ssh/config.compassh")
		else:
			with open(conf_file, "r") as f_in:
				print("")
				print(f"Showing config file {conf_file} for VPN {vpn}")
				print("")
				print("======================================================================")
				print(f_in.read())
				print("======================================================================")

	
	def match_pattern(conf, host):
		""" Match a host with all the patterns defined, returning the corresponding VPN if one exists """
		for key in conf.conf['patterns']:
			if re.match(key, host):
				vpn = conf.pattern(key)
				# avoid looping
				for v in conf.conf['VPN'].keys():
					if conf.vpn(v)['proxy'] == host:
						print(f"Direct connection to host {host} which is marked as proxy")
						return None
				proxy = conf.vpn(vpn)['proxy']
				local_port = conf.vpn(vpn)['local_port']
				print(f"Connections to host {host} use host {proxy} on port {local_port}")
				return vpn

		print(f"No profile found for host {host}")
		return None

	def resolve(conf, host, vpn):
		"""
		Resolve a hostname to its IP address using the internal host map and the local resolver.
		Further resolving strategies based on remote endpoints still have to be implemented.
		"""
		proxy = conf.vpn(vpn)['proxy']
		local_port = conf.vpn(vpn)['local_port']

		#
		# get the remote address from (customize the order to your needs):
		#
		# Missing options:
		#  * remote resolution
		#
		addr = ''
		if host in conf.conf['hosts'].keys():
			addr = conf.host(host)
		else:
			addr = socket.gethostbyname(host) or host

		print(f"{host} resolves to IP address {addr}")
		return addr
	
	def match_and_resolve(conf, host):
		""" Do both match and resolve like the proxy would do. Used by the -R option in CLI mode """
		vpn = Actions.match_pattern(conf, host)
		if vpn:
			Actions.resolve(conf, host, vpn)

def cli(conf):
	action = conf.action()
	if action == 'show_vpn':
		Actions.show_vpn(conf)
	elif action == 'show_hosts':
		Actions.show_hosts(conf)	
	elif action == 'show_patterns':
		Actions.show_patterns(conf)
	elif action == 'start_vpn':
		Actions.start_vpn(conf, conf.target())
	elif action == 'stop_vpn':
		Actions.stop_vpn(conf, conf.target())
	elif action == 'restart_vpn':
		Actions.restart_vpn(conf, conf.target())
	elif action == 'show_config':
		Actions.show_config(conf, conf.target())
	elif action == 'resolve_host':
		Actions.match_and_resolve(conf, conf.target())

def proxy(conf):
	if len(sys.argv) < 2:
		print(f"Can't run compassh in proxy mode without a host name")
	else:
		# first argument must be the remote host to be reached
		host = sys.argv[1]

		# second optional argument is the remote port, which defaults to 22
		port = 22
		if len(sys.argv) > 2:
			port = sys.argv[2]

		# try to guess a VPN to use as a rely
		vpn = Actions.match_pattern(conf, host)
		if vpn == None:
			print(f"No VPN found for hostname {host}, sending trafic to {host}")
			subprocess.Popen(f"{conf.cmd('nc')} {host} {port}".split(" "));
		else:
			# check if the VPN is running and start it if it isn't, then start the netcat tool
			print(f"{host} goes through VPN {vpn}, starting netcat")
			IP = Actions.resolve(conf, host, vpn)
			pid = Actions.vpn_running(conf, vpn)
			if pid == 0:
				Actions.start_vpn(conf, vpn)

			local_port = conf.vpn(vpn)['local_port']
			subprocess.Popen(f"{conf.cmd('nc')} -n -X 5 -x 127.0.0.1:{local_port} {IP} {port}".split(" "))

if __name__ == "__main__":
	conf = Config(sys.argv[1:])
	if conf.run_cli():
		cli(conf)
	else:
		proxy(conf)
