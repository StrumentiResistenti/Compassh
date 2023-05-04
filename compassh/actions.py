import sys

def show_hosts(conf):
	print("\n")
	print("       IP Address   Hostname                           ")
	print("-----------------------------------------------------------------------------------------")
	hosts = conf.conf['hosts']
	for h in hosts:
		print("  %15s   %s" % (hosts[h], h))
	sys.exit(0)

def show_vpn(conf):
	print("\n")
	print("   VPN name           SSH connection                                     Port  PID")
	print("-----------------------------------------------------------------------------------------")

	vpn = conf.conf['VPN']
	for v in vpn:
		pid = 0 # this should call an internal function to retrieve the PID of the VPN
		running = "?" # this should be a star only if the VPN is running
		print("%s  %-18s %-50s %-5d %d" % (running, v, vpn[v]['proxy'], vpn[v]['local_port'], pid))
	sys.exit(0)

def show_patterns(conf):
	print("   Pattern                                  VPN                                     ")
	print("-----------------------------------------------------------------------------------------")
	patterns = conf.conf['patterns']
	for p in patterns:
		print("   %-40s %s" % (p, patterns[p],))
