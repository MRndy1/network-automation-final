import re

def _set_or_replace(pattern, replacement, text, flags=re.M):
    if re.search(pattern, text, flags):
        return re.sub(pattern, replacement, text, count=1, flags=flags)
    return replacement + "\n" + text

def _ensure_line(line, text):
    return text if re.search(rf'(?m)^{re.escape(line)}$', text) else (text.rstrip() + "\n" + line + "\n")

def apply_changes(text, desired):
    if desired.get("hostname"):
        text = _set_or_replace(r'^hostname\s+\S+', f'hostname {desired["hostname"]}', text)

    if desired.get("domain_name"):
        text = _set_or_replace(r'^ip domain-name\s+\S+', f'ip domain-name {desired["domain_name"]}', text)

    if desired.get("ntp_server"):
        text = _ensure_line(f'ntp server {desired["ntp_server"]}', text)

    if desired.get("vty_ssh_only"):
        def replace_vty(block):
            block = re.sub(r'(?m)^\s*transport input.*$', ' transport input ssh', block)
            if not re.search(r'(?m)^\s*transport input\s+ssh\b', block):
                block += '\n transport input ssh'
            block = re.sub(r'(?m)^\s*transport input\s+telnet.*\n?', '', block)
            return block
        text, n = re.subn(r'(?ms)^line vty [^\n]*\n(?: .*\n)*', lambda m: replace_vty(m.group(0)), text)
        if n == 0:
            text += '\nline vty 0 4\n transport input ssh\n'

    if desired.get("banner_motd"):
        text = _set_or_replace(r'^banner motd .+$', f'banner motd {desired["banner_motd"]}', text)

    return text
