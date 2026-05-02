import nmap

def scan(target: str = "127.0.0.1") -> list[dict]:
    """
    Ping-scan target, return list of discovered hosts.
    Each entry: {name, ip, status, device_type, room_sensitivity}
    """
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments="-sn")

    results = []
    for host in nm.all_hosts():
        name = nm[host].hostname() or "Unknown Device"
        results.append({
            "name": name,
            "ip": host,
            "status": nm[host].state(),
            # defaults — override with real inventory data
            "device_type": "Unknown",
            "room_sensitivity": "Low",
        })
    return results


if __name__ == "__main__":
    hosts = scan("127.0.0.1")
    for h in hosts:
        print(h)
