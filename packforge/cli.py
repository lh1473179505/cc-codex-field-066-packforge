import argparse
def main(argv=None):
    p=argparse.ArgumentParser(prog="packforge")
    sub=p.add_subparsers(dest="cmd", required=True)
    s=sub.add_parser("site")
    s.add_argument("--port", type=int, default=8766)
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--skin", choices=["v1","v2"], default="v2")
    h=sub.add_parser("harvest")
    h.add_argument("--base", required=True)
    h.add_argument("--pack", required=True)
    h.add_argument("--out", required=True)
    h.add_argument("--checkpoint", required=True)
    v=sub.add_parser("verify")
    v.add_argument("--out", required=True)
    v.add_argument("--expect", required=True)
    args=p.parse_args(argv)
    if args.cmd=="site":
        from packforge.site import serve
        serve(args.host, args.port, args.skin); return 0
    if args.cmd=="harvest":
        from packforge.harvest import run_harvest
        return run_harvest(args)
    if args.cmd=="verify":
        from packforge.verify import run_verify
        return run_verify(args)
    return 2
if __name__=="__main__":
    raise SystemExit(main())
