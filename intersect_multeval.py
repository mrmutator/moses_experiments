import argparse
import os
import subprocess
import sys
import re





def evaluate(ref, baseline, hyps, prefix, multeval_path, lang):
    hyps_args = []
    for i, ha in enumerate(hyps):
        hyps_args.append("--hyps-sys" + str(i+1))
        hyps_args.append(os.path.join(ha, prefix))
    cmd = " ".join(["./multeval.sh", "eval", "--refs", ref, "--hyps-baseline", os.path.join(baseline, prefix)] + hyps_args + ["--meteor.language", lang])
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=multeval_path, shell=True)
    stdout, stderr = proc.communicate()
    print >> sys.stderr, stderr

    res = re.sub("baseline\s*", "", stdout)
    res = re.sub("system \d+\s*", "", res)
    res = re.sub("\s*\n", ",\n", res)
    res = re.sub("\s\s+", ",", res)
    print stdout
    print

    print res
    print args.bl, args.hyps




if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("hyps", nargs='+')
    arg_parser.add_argument("-ref", required=True)
    arg_parser.add_argument("-bl", required=True)
    arg_parser.add_argument("-lang", required=True)
    arg_parser.add_argument('-multeval_path', default=os.getenv("HOME") + "/multeval-0.5.1", required=False)

    args = arg_parser.parse_args()
    prefix = args.lang + ".translated.*"

    evaluate(os.path.abspath(args.ref), os.path.abspath(args.bl), map(os.path.abspath, args.hyps), prefix, os.path.abspath(args.multeval_path), args.lang)
