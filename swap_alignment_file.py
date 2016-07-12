import argparse


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("alignment_file", required=True)

args = arg_parser.parse_args()


outfile = open(args.alignment_file + ".swapped", "w")
with open(args.alignment_file, "r") as infile:
    for line in infile:
        als = [a.split("-") for a in line.split()]
        als = [a[1] + "-" + a[0] for a in als]
        outfile.write(" ".join(als) + "\n")

outfile.close()