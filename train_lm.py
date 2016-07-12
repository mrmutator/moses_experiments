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
    check_list = ["e_file_gz", "moses_dir"]
    for c in check_list:
        if not os.path.exists(params[c]):
            raise Exception("Path does not exist for parameter %s: <%s>" % (c, params[c]))


def get_params(args):
    params = dict()
    params['e_file_gz'] = os.path.abspath(args.e_file_gz)
    params['target_file'] = os.path.abspath(args.target_file)
    params['job_file'] = params['target_file'] + ".job"
    params['job_template_dir'] = os.path.dirname(os.path.realpath(__file__))
    params['wall_time'] = args.wall_time
    params['job_dir'] = os.path.dirname(os.path.realpath(params['target_file']))
    params['moses_dir'] = os.path.abspath(args.moses_dir)

    return params


def generate_job(**params):
    with open(params['job_template_dir'] + "/train_lm.txt", "r") as infile:
        template = infile.read()
        job_file = template % params
    with open(params['job_file'], "w") as outfile:
        outfile.write(job_file)


def send_job(**params):
    proc = subprocess.Popen(['qsub', params['job_file']], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=params['job_dir'])
    stdout, stderr = proc.communicate()
    if stderr:
        raise Exception("Failed sending prepare_job: " + stderr)


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("-e_file_gz", required=True)
arg_parser.add_argument("-target_file", required=True)
arg_parser.add_argument("-wall_time", required=False, default="01:00:00", type=str)
arg_parser.add_argument("-moses_dir", required=False, default=os.getenv("HOME") + "/mosesdecoder", type=str)
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