from src.verifier import verify_all

BEFORE = """hostname OLD-NAME
ip domain-name old.local
line vty 0 4
 transport input telnet ssh
"""

def test_verify_finds_missing_things():
    desired = {
        "hostname": "CAMPUS-EDGE-1",
        "domain_name": "lab.local",
        "ntp_server": "192.0.2.10",
        "vty_ssh_only": True,
        "banner_motd": "Authorized access only",
    }
    res = verify_all(BEFORE, desired)
    assert res["hostname"] is False
    assert res["domain_name"] is False
    assert res["ntp_server"] is False
    assert res["vty_ssh_only"] is False
    assert res["banner_motd"] is False
    assert res["all_passed"] is False
