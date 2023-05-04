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
	# l = List VPN (default behaviour)
	# s = Start VPN
	# S = Stop VPN
	# r = Restart VPN
	# V = The selected VPN
	#
	def parse_command_line(self, argv):
		self.conf['args'] = {'action': 'show_vpn'}
		opts, args = getopt.getopt(argv, "hvcHlsSrV:")
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
			elif opt == '-s':
				self.conf['args']['action'] = 'start_vpn'
			elif opt == '-S':
				self.conf['args']['action'] = 'stop_vpn'
			elif opt == '-R':
				self.conf['args']['action'] = 'restart_vpn'
			elif opt == '-V':
				self.conf['args']['vpn'] = arg
				print(f"Operating on VPN {self.conf['args']['vpn']}")

		print(f"Action requested: {self.conf['args']['action']}")

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

			VPN = self.conf['VPN']
			for vpn in VPN:
				print(f"VPN {vpn} // proxy: {VPN[vpn]['proxy']} // local_port: {VPN[vpn]['local_port']}")

			patterns = self.conf['patterns']
			for p in patterns:
				print(f"Pattern {p} points to vpn {patterns[p]}")

			hosts = self.conf['hosts']
			for h in hosts:
				print(f"Host {h} has address {hosts[h]}")
		else:
			print(f"Unable to read {conf} configuration file")
			sys.exit(1)
	
	#
	# Provide the path of the main config file
	#
	def conf_file_path(self):
		home = os.path.expanduser('~')
		return f"{home}/.compassh.conf"


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
