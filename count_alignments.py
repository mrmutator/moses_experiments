

if __name__ == "__main__":
    import argparse
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("alignment_file")

    args = arg_parser.parse_args()

    alignment_count = 0
    N = 0
    with open(args.alignment_file, "r") as infile:
        for line in infile:
            als = len(line.split())
            alignment_count += als
            N += 1

    print alignment_count
    print float(alignment_count) / N