import os
import subprocess
from datetime import datetime

def parseQLineStampede(line):
    cols_order = ['id', 'name', 'username', 'state', 'ncores', 'timerem'] #, 'timestart']
    cols = dict([
        ('id',        slice(0,  9)),
        ('name',      slice(9,  20)),
        ('username',  slice(20, 34)),
        ('state',     slice(34, 42)),
        ('ncores',    slice(42, 50)),
        ('timerem',   slice(50, 61)),
        ('timestart', slice(61, None))
    ])

    line_dict = {}
    for name in cols_order:
        line_dict[name] = line[cols[name]].strip()

    try:
        line_dict['id'] = int(line_dict['id'])
        line_dict['ncores'] = int(line_dict['ncores'])
    except ValueError:
        return ""

    return line_dict

def parseQLineKraken(line):
    field_widths = []
    qstat = []
    for line in text:
        if line.startswith('---'):
            field_widths = [ len(f) for f in line.split() ]
            continue

        if field_widths != []:
            fields = []
            offset = 0
            for width in field_widths:
                fields.append(line[(offset):(offset + width)])
                offset += width + 1

#           print fields
            qstat.append(fields)
    return qstat


def parseQLineRice_PBS(line):
    cols_order = ['id', 'username', 'queue', 'name', 'sessid', 'nnodes', 'ncores', 'reqmem',
                  'reqtime', 'state', 'timeuse'] #, 'timestart']
    cols = dict([
        ('id',          slice(0,     8)),
        ('username',    slice(24,   35)),
        ('queue',       slice(36,   44)),
        ('name',        slice(45,   61)),
        ('sessid',      slice(62,   68)),
        ('nnodes',      slice(69,   74)),
        ('ncores',      slice(75,   81)),
        ('reqmem',      slice(82,   91)),
        ('reqtime',     slice(92,  101)),
        ('state',       slice(102, 103)),
        ('timeuse',     slice(104, None)),
    ])

    line_dict = {}
    for name in cols_order:
        line_dict[name] = line[cols[name]].strip()
    #print line_dict[name]
    try:
        line_dict['id'] = int(line_dict['id'])
        #print line_dict['id']
    except ValueError:
        return ""

    return line_dict


def parseQLineRice_old(line):
    cols_order = ['id', 'username', 'queue', 'name', 'nnodes', 'ncores', 'reqtime', 'state',
                  'timeuse']
    cols = dict([
        ('id',          slice(0,     5)),
        ('username',    slice(13,   21)),
        ('queue',       slice(23,   31)),
        ('name',        slice(36,   52)),
        ('nnodes',      slice(53,   58)),
        ('ncores',      slice(61,   65)),
        ('reqtime',     slice(66,  77)),
        ('state',       slice(78, 80)),
        ('timeuse',     slice(81, None)),
    ])

    line_dict = {}
    for name in cols_order:
        line_dict[name] = line[cols[name]].strip()
    #print line_dict[name]
    try:
        line_dict['id'] = int(line_dict['id'])
        #print line_dict['id']
    except ValueError:
        return ""

    return line_dict


def parseQLineRice(line):
    cols_order = ['id', 'username', 'queue', 'name', 'nnodes', 'ncores', 'reqtime', 'state',
                  'timeuse']
    line = line.strip().split()
    line_dict = {}

    for n, name in enumerate(cols_order):
        line_dict[name] = line[n].strip()
    #print line_dict[name]
    try:
        line_dict['id'] = int(line_dict['id'])
        #print line_dict['id']
    except ValueError:
        return ""

    return line_dict

def parseQLineBell(line):
    cols_order = ['id', 'username', 'queue', 'name', 'nnodes', 'ncores', 'reqtime', 'state',
                  'timeuse']
    line = line.strip().split()
    line_dict = {}

    for n, name in enumerate(cols_order):
        line_dict[name] = line[n].strip()
    #print line_dict[name]
    try:
        line_dict['id'] = int(line_dict['id'])
        #print line_dict['id']
    except ValueError:
        return ""

    return line_dict

_environment = {
    'stampede': {
        'btmarker': "SBATCH",
        '-J': "%(jobname)s",
        '-o': "%(debugfile)s",
        '-n': "%(nmpi)d",
        '-N': "%(nnodes)d",
        '-p': "%(queue)s",
        '-t': "%(timereq)s",
        'queueprog': 'showq',   # Name of the program that gets the queue state
        'queueparse': parseQLineStampede,
        'submitprog': 'sbatch', # Name of the program submits the batch file
        'mpiprog': 'ibrun',     # Name of the program that runs MPI
        'n_cores_per_node': 16,
    },
    'kraken': {
        'btmarker': "PBS",
        'queueprog': 'qstat',
        'queueparse': parseQLineKraken,
        'submitprog': 'qsub',
        'mpiprog': 'aprun',
        'n_cores_per_node': 12,
    },
    'oscer': {
    },
    # 'rice': {
    #     'btmarker': "PBS",
    #     '-q': " %(queue)s",
    #     '-l nodes': "=%(nnodes)d:ppn=%(ppn)d",
    #     '-l walltime': "=%(timereq)s",
    #     '-N': " %(jobname)s",
    #     '-l naccesspolicy': "=singleuser", # '-n':"",
    #     'queueprog': 'qstat',
    #     'queueparse': parseQLineRice,
    #     'submitprog': 'qsub',
    #     'mpiprog': 'mpiexec',
    #     'mpiargs': '-n %d',
    #     'n_cores_per_node': 20,
    #     'running_state': 'R',
    #     'complete_state': 'C'
    # }
    'rcac': {
        'btmarker': "SBATCH",
        '-A': " %(queue)s",
        '-N': " %(nnodes)d",
        '--ntasks-per-node': " %(ppn)d",
        '-t': " %(timereq)s",
        '--job-name': "=%(jobname)s",
        # '--exclusive': "",
        'queueprog': 'squeue',
        'queueparse': parseQLineRice,
        'submitprog': 'sbatch',
        'mpiprog': 'mpiexec',
        'mpiargs': '-n %d',
        'n_cores_per_node': 20,
        'running_state': ' R',
        'complete_state': 'CD'
    },
    # NOTE: changed mpiprog to srun below, but in order to get it to work
    # I had to give it the --export=ALL argument in order to make sure
    # that the job inherited the user environment. Otherwise, I got
    # shared library object file missing errors when running arps_mpi or
    # arpsenkf_mpi (specifically the jpeg library). I think this is because
    # when originally compiling arps, I had the anaconda module loaded which
    # led to it pointing to the jpeg library in the anaconda distribution
    # instead of the system one. But when running srun, it seems to not
    # inherit the environment and can't find the jpeg library. It also
    # finds different locations for the other needed libraries.
    # For some reason, using mpiexec doesn't run into this problem.
    # Also added --mpi=pmi2 since I am using the Intel compilers for ARPS
    # right now until I can solve other issues with the GNU ones.
    'bell': {
        'btmarker': "SBATCH",
        '-A': " %(queue)s",
        '-N': " %(nnodes)d",
        '--ntasks-per-node': " %(ppn)d",
        '-t': " %(timereq)s",
        '--job-name': "=%(jobname)s",
        # '--exclusive': "",
        'queueprog': 'squeue',
        'queueparse': parseQLineBell,
        'submitprog': 'sbatch',
        'mpiprog': 'srun',
        'mpiargs': '--export=ALL --mpi=pmi2 -n %d',
        'n_cores_per_node': 128,
        'running_state': ' R',
        'complete_state': 'CD'
    }

}

_environment['rice'] = _environment['rcac'].copy()
_environment['rice']['n_cores_per_node'] = 20
_environment['brown'] = _environment['rcac'].copy()
_environment['brown']['n_cores_per_node'] = 24


class Batch(object):
    def __init__(self, environment, username="dawson29"):
        self._env = _environment[environment]
        self._username = username
        self._envname = environment
        return

    def gen(self, commands, **kwargs):
        env_dict = {}
        ppn = kwargs.get('ppn', 20)
        nnodes = kwargs.get('nnodes', 1)
        # if self._envname == 'rcac':
        #     ppn = ppn * nnodes  # Rice now needs the *total* nodes in the job specification
        # if ppn < 20 and nnodes > 1:
        #     # print(self._env.keys())
        #     try:
        #         self._env.pop('--exclusive')
        #     except (KeyError):
        #         pass
        for k, v in self._env.items():
            try:
                assert k[0] == '-'
                env_dict[k] = v % kwargs
            except (AssertionError, KeyError):
                pass

        text = "#!/bin/bash\n"
        for arg, val in env_dict.items():
            text += "#%s %s%s\n" % (self._env['btmarker'], arg, val)

        if(self._envname == 'bell'):
            commands.insert(0,"module load netcdf")
            #text += "\n" + "module load devel" + "\n"

        text += "\n" + "\n".join(commands) + "\n"
        return text

    def submit(self, text):
        echo = subprocess.Popen([ "echo", text ], stdout=subprocess.PIPE)
        subm = subprocess.Popen([ self._env['submitprog'] ], stdin=echo.stdout, stdout=subprocess.PIPE)
        echo.stdout.close()
        ret_value = subm.communicate()[0]
        print(ret_value.decode('utf-8').strip().split("\n")[-1])
        return

    def getQueueStatus(self, display=True):
        if self._env['queueprog'] == 'squeue':
            os.environ['SQUEUE_FORMAT'] = "%12i %9u %12a %70j %.5D %.6C %.11l %.2t %M"
        queue = subprocess.Popen([self._env['queueprog'], '-u', self._username], stdout=subprocess.PIPE)
        queue_text = queue.communicate()[0]
        lines = []
        for line in queue_text.decode('utf-8').strip().split("\n"):
            line_dict = self._env['queueparse'](line)
            if line_dict != "":
                lines.append(line_dict)

        if display:
            self.displayQueue(lines)
        return lines

    def displayQueue(self, queue):
        print("Queue State as of %s" % datetime.now().strftime("%H:%M:%S %d %b %Y"))
        for line in queue:
            # if line['state'].lower() == 'running':
            if line['state'] == self._env['running_state']:
                if self._envname == 'bell':
                    print("%(name)s (PID %(id)d): %(state)s (%(timeuse)s elapsed)" % line)
                else:
                    print("%(name)s (PID %(id)d): %(state)s (%(timerem)s remaining)" % line)
            else:
                print("%(name)s (PID %(id)d): %(state)s" % line)

        if len(queue) == 0:
            print("[ empty ]")
        return

    def getMPIprogram(self):
        return self._env['mpiprog']

    def getMPIargs(self):
        return self._env['mpiargs']

    def getNCoresPerNode(self):
        return self._env['n_cores_per_node']

    def getEnv(self):
        return self._envname

    def getQueueStateNames(self):
        return self._env['running_state'], self._env['complete_state']

if __name__ == "__main__":
    bt = Batch('bell')
#   bt_text = bt.gen(['ls $HOME', 'ls $WORK'], jobname='test', debugfile='test.debug', ncores=1, nnodes=1, queue='normal', timereq='00:05:00')
#   bt.submit(bt_text)
    bt.getQueueStatus()
