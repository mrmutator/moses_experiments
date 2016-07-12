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



def check_paths(params):
    check_list = ["e_file_gz", "f_file_gz", "target_dir", "alignment_file", "language_model", "moses_dir"]
    for c in check_list:
        if not os.path.exists(params[c]):
            raise Exception("Path does not exist for parameter %s: <%s>" % (c, params[c]))


def get_params(args):
    params = dict()
    params['e_file_gz'] = os.path.abspath(args.e_file_gz)
    params['f_file_gz'] = os.path.abspath(args.f_file_gz)
    params['target_dir'] = os.path.abspath(args.target_dir)
    params['alignment_file'] = os.path.abspath(args.alignment_file)
    params['language_model'] = os.path.abspath(args.language_model)
    params['job_file'] = params['target_dir'] + "/training.job"
    params['job_template_dir'] = os.path.dirname(os.path.realpath(__file__))
    params['wall_time'] = args.wall_time
    params['moses_dir'] = os.path.abspath(args.moses_dir)
    params['num_cores'] = args.num_cores

    return params


def generate_job(**params):
    with open(params['job_template_dir'] + "/train_moses.txt", "r") as infile:
        template = infile.read()
        job_file = template % params
    with open(params['job_file'], "w") as outfile:
        outfile.write(job_file)


def send_job(**params):
    proc = subprocess.Popen(['qsub', params['job_file']], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=params['target_dir'])
    stdout, stderr = proc.communicate()
    if stderr:
        raise Exception("Failed sending prepare_job: " + stderr)


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("-e_file_gz", required=True)
arg_parser.add_argument("-f_file_gz", required=True)
arg_parser.add_argument("-language_model", required=True)
arg_parser.add_argument("-alignment_file", required=True)
arg_parser.add_argument("-target_dir", required=True)
arg_parser.add_argument("-wall_time", required=False, default="05:00:00", type=str)
arg_parser.add_argument("-moses_dir", required=False, default=os.getenv("HOME") + "/mosesdecoder", type=str)
arg_parser.add_argument("-num_cores", required=False, default=16, type=int)
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