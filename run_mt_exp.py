import argparse
import os

class TestReturn(object):

    def __init__(self, job_id):
        self.job_id = job_id

    def communicate(self):
        return str(self.job_id) + ".testjob", None

class Test(object):

    def __init__(self):
        self.i = 0
        self.PIPE = None

    def Popen(self, args, stderr=None, stdout=None, cwd=None):
        self.i += 1
        print self.i, " ".join(args)
        return TestReturn(self.i)

subprocess = Test()


def check_paths(params):
    check_list = ["e_train_gz", "f_train_gz", "e_dev_gz", "f_dev_gz", "e_test_gz", "f_test_gz", "result_dir",
                  "alignment_file", "language_model", "moses_dir"]
    for c in check_list:
        if not os.path.exists(params[c]):
            raise Exception("Path does not exist for parameter %s: <%s>" % (c, params[c]))


def get_params(args):
    params = dict()
    params['e_train_gz'] = os.path.join(os.path.abspath(args.corpus_dir), "training." + args.e + ".gz")
    params['f_train_gz'] = os.path.join(os.path.abspath(args.corpus_dir), "training." + args.f + ".gz")
    params['e_dev_gz'] = os.path.join(os.path.abspath(args.corpus_dir), "dev." + args.e + ".gz")
    params['f_dev_gz'] = os.path.join(os.path.abspath(args.corpus_dir), "dev." + args.f + ".gz")
    params['e_test_gz'] = os.path.join(os.path.abspath(args.corpus_dir), "test." + args.e + ".gz")
    params['f_test_gz'] = os.path.join(os.path.abspath(args.corpus_dir), "test." + args.f + ".gz")
    params['result_dir'] = os.path.abspath(args.result_dir)
    params['alignment_file'] = os.path.abspath(args.alignment_file)
    params['language_model'] = os.path.join(os.path.abspath(args.corpus_dir), "lm.blm." + args.e)
    params['job_file'] = os.path.join(params['result_dir'], "mt_exp.job")
    params['job_template_dir'] = os.path.dirname(os.path.realpath(__file__))
    params['wall_time'] = args.wall_time
    params['moses_dir'] = os.path.abspath(args.moses_dir)
    params['num_cores'] = args.num_cores
    params['num_mert'] = args.num_mert
    if args.reverse:
        params["reverse"] = "python " + os.path.join(params["job_template_dir"], "swap_alignment_file.py") + " aligned.grow-diag-final\nmv aligned.grow-diag-final.swapped aligned.grow-diag-final"
        params["job_file"] = params["job_file"][:-3] + "reverse.job"
        params["rev_prefix"] = "rev."
    else:
        params["reverse"] = ""
        params["rev_prefix"] = ""

    return params


def generate_job(**params):
    with open(params['job_template_dir'] + "/mt_exp.txt", "r") as infile:
        template = infile.read()
        job_file = template % params
    with open(params['job_file'], "w") as outfile:
        outfile.write(job_file)


def send_job(**params):
    proc = subprocess.Popen(['qsub', params['job_file']], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=params['result_dir'])
    stdout, stderr = proc.communicate()
    if stderr:
        raise Exception("Failed sending prepare_job: " + stderr)


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("-corpus_dir", required=True)
arg_parser.add_argument("-f", required=True)
arg_parser.add_argument("-e", required=True)
arg_parser.add_argument("-alignment_file", required=True)
arg_parser.add_argument("-result_dir", required=True)
arg_parser.add_argument("-num_mert", required=False, default=5, type=int)
arg_parser.add_argument("-wall_time", required=False, default="05:00:00", type=str)
arg_parser.add_argument("-moses_dir", required=False, default=os.getenv("HOME") + "/mosesdecoder", type=str)
arg_parser.add_argument("-num_cores", required=False, default=16, type=int)
arg_parser.add_argument("-reverse", required=False, dest="reverse", action='store_true')
arg_parser.add_argument('-no_sub', dest='no_sub', action='store_true', required=False)
arg_parser.set_defaults(no_sub=False)
args = arg_parser.parse_args()
params = get_params(args)

check_paths(params)



generate_job(**params)


if not args.no_sub:
    import subprocess
    send_job(**params)
    print "Jobs sent."
else:
    subprocess = Test()
    send_job(**params)
    print "Jobs prepared, but not sent."