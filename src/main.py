import argparse, yaml, sys
from pathlib import Path
from .verifier import verify_all
from .changer import apply_changes
from .diffutil import unified_diff_str

def read_text(p): return Path(p).read_text(encoding="utf-8")
def write_text(p, s): Path(p).write_text(s, encoding="utf-8")

def cmd_verify(args):
    cfg = read_text(args.config)
    desired = yaml.safe_load(Path(args.topology_or_changes).read_text()) if args.topology_or_changes else {}
    res = verify_all(cfg, desired or {})
    for k, v in res.items():
        if k != "all_passed":
            print(f"{k}: {'PASS' if v else 'FAIL'}")
    print("ALL PASSED" if res["all_passed"] else "SOME CHECKS FAILED")
    return 0 if res["all_passed"] else 1

def cmd_apply(args):
    cfg = read_text(args.config)
    desired = yaml.safe_load(Path(args.changes).read_text())
    new_cfg = apply_changes(cfg, desired)
    write_text(args.out, new_cfg)
    diff = unified_diff_str(cfg, new_cfg, args.config, args.out)
    write_text(args.out + ".diff.txt", diff)
    print(f"wrote: {args.out}\nwrote: {args.out}.diff.txt")
    return 0

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verify", help="verify a config against desired state")
    v.add_argument("--config", required=True)
    v.add_argument("--topology_or_changes", required=False, help="YAML with desired values")
    v.set_defaults(fn=cmd_verify)

    a = sub.add_parser("apply", help="apply 3+ config changes to a config file")
    a.add_argument("--config", required=True)
    a.add_argument("--changes", required=True)
    a.add_argument("--out", default="data/running_config_after.txt")
    a.set_defaults(fn=cmd_apply)

    args = p.parse_args()
    sys.exit(args.fn(args))

if __name__ == "__main__":
    main()
