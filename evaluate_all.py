import argparse
import os


job_header = """#PBS -S /bin/bash
#PBS -lnodes=1:cores16
#PBS -lwalltime=00:05:00"""


cmd = "python ~/moses_experiments/multeval.py "




if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("dir_file")
    arg_parser.add_argument("dir")
    arg_parser.add_argument("ref")
    arg_parser.add_argument("lang")
    arg_parser.add_argument('-reverse', dest='reverse', action='store_true', required=False)
    arg_parser.add_argument("-n", type=int, default=5)

    args = arg_parser.parse_args()

    target_dir = os.path.abspath(args.dir)
    ref_dir = os.path.abspath(args.ref)



    with open(args.dir_file, "r") as infile:
        bl = os.path.join(target_dir, infile.readline().strip())

        hyps = [os.path.join(target_dir, l.strip()) for l in infile.readlines()]



    c = 1
    while hyps:

        job_file = "eval." + args.lang + "." + ("%03d" % c)
        with open(job_file, "w") as outfile:
            outfile.write(job_header + "\n\n")

            outfile.write(cmd)
            if args.reverse:
                outfile.write(" -reverse ")
            outfile.write(" -ref " + ref_dir)
            outfile.write(" -lang " + args.lang)
            outfile.write(" -bl " + bl)

            i = 0
            while hyps and i < args.n:
                d = hyps.pop(0)
                outfile.write(" " + d + " ")
                i += 1

        c += 1











