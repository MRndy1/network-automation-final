from src.changer import apply_changes
from src.verifier import verify_all

def test_apply_makes_config_pass():
    before = "hostname OLD\nline vty 0 4\n transport input telnet ssh\n"
    desired = {
        "hostname": "NEW",
        "domain_name": "lab.local",
        "ntp_server": "192.0.2.10",
        "vty_ssh_only": True,
        "banner_motd": "Authorized access only",
    }
    after = apply_changes(before, desired)
    res = verify_all(after, desired)
    assert res["all_passed"] is True
