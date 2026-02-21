import nmap

# 1. Initialize the 'Scanner' object (the brain)
nm = nmap.PortScanner()

# 2. Define the Target (Your home network)
# '192.168.1.0/24' tells the tool to look at all 254 possible spots on the network.
target = '127.0.0.1' # We use this for a safe 'self-test' first

print(f"--- AV-Sec Architect is scanning: {target} ---")

# 3. Perform the Scan
# '-sn' is a 'Ping Scan' - it just asks 'Are you there?' without being aggressive.
nm.scan(hosts=target, arguments='-sn')

# 4. Display the results in a List (Your Option 2)
for host in nm.all_hosts():
    # Retrieve the name of the device if available
    name = nm[host].hostname() if nm[host].hostname() else "Unknown Device"
    
    # Retrieve the status (Up/Down)
    status = nm[host].state()
    
    print(f"Found: {name} | IP: {host} | Status: {status}")

print("--- Scan Complete ---")
