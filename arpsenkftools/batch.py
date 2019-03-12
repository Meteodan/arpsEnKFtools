
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

def parseQLineRice(line):
    cols_order = ['id', 'username', 'queue', 'name', 'sessid', 'nnodes', 'ncores', 'reqmem', 'reqtime', 'state', 'timeuse'] #, 'timestart']
    cols = dict([
        ('id',          slice(0,  7)),
        ('username',    slice(24, 35)),
        ('queue',       slice(36, 44)),
        ('name',        slice(45, 61)),
        ('sessid',      slice(62, 68)),
        ('nnodes',      slice(69, 74)),
        ('ncores',      slice(75, 81)),
        ('reqmem',      slice(82, 88)),
        ('reqtime',     slice(90, 98)),
        ('state',       slice(99,100)),
        ('timeuse',     slice(101,None)),
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

_environment = {
    'stampede':{
        'btmarker':"SBATCH", 
        '-J':"%(jobname)s",
        '-o':"%(debugfile)s",
        '-n':"%(nmpi)d",
        '-N':"%(nnodes)d",
        '-p':"%(queue)s",
        '-t':"%(timereq)s",
        'queueprog':'showq',   # Name of the program that gets the queue state
        'queueparse':parseQLineStampede,
        'submitprog':'sbatch', # Name of the program submits the batch file
        'mpiprog':'ibrun',     # Name of the program that runs MPI
        'n_cores_per_node':16, 
    },
    'kraken':{ 
        'btmarker':"PBS",
        'queueprog':'qstat',
        'queueparse':parseQLineKraken,
        'submitprog':'qsub',
        'mpiprog':'aprun',
        'n_cores_per_node':12,
    },
    'oscer':{
    },
    'rice':{
        'btmarker':"PBS",
        '-q':" %(queue)s",
        '-l nodes':"=%(nnodes)d:ppn=%(ppn)d",
        '-l walltime':"=%(timereq)s",
        '-N':" %(jobname)s",
        '-l naccesspolicy':"=singleuser", # '-n':"",
        'queueprog':'qstat',
        'queueparse':parseQLineRice,
        'submitprog':'qsub',
        'mpiprog':'mpiexec',
        'mpiargs':'-n %d',
        'n_cores_per_node':20,
    }
}

class Batch(object):
    def __init__(self, environment, username="dawson29"):
        self._env = _environment[environment]
        self._username = username
        self._envname = environment
        return

    def gen(self, commands, **kwargs):
        env_dict = {}
        for k, v in self._env.items():
            try:
                assert k[0] == '-'
                env_dict[k] = v % kwargs
            except (AssertionError, KeyError):
                pass
            
        text = "#!/bin/csh\n"
        for arg, val in env_dict.items():
            text += "#%s %s%s\n" % (self._env['btmarker'], arg, val)

        if(self._envname == 'rice'):
            commands.insert(0,"module load devel")
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
            if line['state'].lower() == 'running':
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

if __name__ == "__main__":
    bt = Batch('rice')
#   bt_text = bt.gen(['ls $HOME', 'ls $WORK'], jobname='test', debugfile='test.debug', ncores=1, nnodes=1, queue='normal', timereq='00:05:00')
#   bt.submit(bt_text)
    bt.getQueueStatus()
