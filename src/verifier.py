import re

def _get(pattern, text):
    m = re.search(pattern, text, re.M)
    return m.group(1) if m else None

def has_hostname(text, expected):
    name = _get(r'^hostname\s+(\S+)', text)
    return name == expected

def has_domain(text, expected):
    dom = _get(r'^ip domain-name\s+(\S+)', text)
    return dom == expected

def has_ntp_server(text, server):
    return bool(re.search(rf'(?m)^ntp server\s+{re.escape(server)}\b', text))

def vty_ssh_only(text):
    ssh = re.search(r'(?m)^\s*transport input\s+ssh\b', text)
    telnet = re.search(r'(?m)^\s*transport input\s+telnet\b', text)
    return bool(ssh) and not bool(telnet)

def has_banner(text, msg):
    return (msg is None) or (('banner motd' in text) and (msg in text))

def verify_all(text, desired):
    res = {
        "hostname":     has_hostname(text, desired.get("hostname")),
        "domain_name":  has_domain(text, desired.get("domain_name")),
        "ntp_server":   has_ntp_server(text, desired.get("ntp_server")),
        "vty_ssh_only": vty_ssh_only(text) if desired.get("vty_ssh_only") else True,
        "banner_motd":  has_banner(text, desired.get("banner_motd")),
    }
    res["all_passed"] = all(res.values())
    return res
