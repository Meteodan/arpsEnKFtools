
import os
import subprocess
import time
import argparse
from math import ceil
from collections import defaultdict
import imp
from arpsenkftools.editNamelist import editNamelistFile
from arpsenkftools.batch import Batch


def import_all_from(module_path):
    """
    Modified from
    http://grokbase.com/t/python/python-list/1172ahxp0s/from-module-import-using-import
    Loads python file at "module_path" as module and adds contents to global namespace.
    """
    mod = imp.load_source('mod', module_path)
    return mod


def isDivisible(dividend, divisor):
    return float(dividend) / int(divisor) == int(dividend) / int(divisor)


def appendCommands(current_commands, commands):
    for e, cmd in commands.items():
        current_commands[e].extend(cmd)
    return current_commands


def doForEnsemble(commands, member_list, current_commands=None):

    if type(commands) not in [list, tuple]:
        commands = [commands]

    if current_commands is None:
        current_commands = defaultdict(list)

    for n_ens in member_list:
        key = "ena%03d" % (n_ens + 1)
        for cmd in commands:
            current_commands[key].append(cmd % {'ens': (n_ens + 1)})

    return current_commands


def doForMPIConfig(command, mpi_config):
    nproc_x, nproc_y = mpi_config

    commands = []

    for idx in range(nproc_x):
        for jdy in range(nproc_y):
            commands.append(command % {'x_proc': idx + 1, 'y_proc': jdy + 1, 'ens': '%(ens)03d'})

    return commands


def getPaths(base_path, job_name, **kwargs):
    paths = []
    default_paths = {
        'work': "%s/%s/" % (base_path, job_name),
        'input': "%s/input/" % base_path,
        'debug': "%s/debug/" % base_path,
        'batch': "%s/batch/" % base_path,
        'boundary': "%s/boundary/" % base_path,
        'hx': "%s/%s/" % (base_path, job_name),
    }
    for p in ['work', 'input', 'debug', 'batch', 'boundary', 'hx']:
        if p in kwargs and kwargs[p]:
            paths.append(default_paths[p])

    if len(paths) == 1:
        paths = paths[0]
    return paths

# def generateEnsembleIntegration(base_path, job_name, member_list,
# mpi_config, n_cores, start_time, end_time, dump_time,
# split_files='neither', move_for_assim=True, current_commands=None,
# input_file_name="arps.input"):


def generateEnsembleIntegration(cm_args, batch, start_time, end_time,
                                dump_time, split_files='neither', move_for_assim=True, **kwargs):
    work_path, input_path, debug_path, bc_path, hx_path = \
        getPaths(
            cm_args.base_path,
            cm_args.job_name,
            work=True,
            input=True,
            debug=True,
            boundary=True,
            hx=True)

    nproc_x, nproc_y = cm_args.mpi_config_model
    nproc_x_dump, nproc_y_dump = cm_args.mpi_config_dump
    nproc_x_enkf, nproc_y_enkf = cm_args.mpi_config_enkf

    extraneous_files = [
        "%s/%s.hdf%06d*.01" % (work_path, 'ena%(ens)03d', start_time),
        "%s/%s.hdfgrdbas*.01" % (work_path, 'ena%(ens)03d'),
        "%s/%s.log*" % (work_path, 'ena%(ens)03d'),
        "%s/%s.maxmin*" % (work_path, 'ena%(ens)03d'),
    ]

    read_split = split_files in ['read', 'both']
    dump_split = split_files in ['dump', 'both']
    print("dump_split = ", dump_split)

    if move_for_assim:
        if dump_split:
            epilogue = doForMPIConfig(
                "mv %s/%s/%s.hdf%06d_%s %s/%s/%s.hdf%06d_%s" %
                (work_path, 'EN%(ens)s', 'ena%(ens)s', end_time, '%(x_proc)03d%(y_proc)03d',
                 work_path, 'ENF%(ens)s', 'enf%(ens)s', end_time, '%(x_proc)03d%(y_proc)03d'),
                cm_args.mpi_config_dump
            )
        else:
            epilogue = [
                "mv %s/%s.hdf%06d %s/%s.hdf%06d" % (work_path,
                                                    'ena%(ens)03d',
                                                    end_time,
                                                    work_path,
                                                    'enf%(ens)03d',
                                                    end_time)
            ]
    else:
        epilogue = []

    # Move batch output files to a subdirectory to get them out of the way
    batch_output_dir = os.path.join(cm_args.base_path, 'batch_output')
    if not os.path.exists(batch_output_dir):
        os.makedirs(batch_output_dir)
    epilogue.extend([
        "mv *.e* {}/".format(batch_output_dir),
        "mv *.o* {}/".format(batch_output_dir)
    ])

    arps_input_file_name = "%s/%s.%d-%d.arps.input" % (
        input_path, 'ena%(ens)03d', start_time, end_time)
    arps_debug_file_name = "%s/%s.%d-%d.arps.debug" % (
        debug_path, 'ena%(ens)03d', start_time, end_time)
    if cm_args.algorithm == "4densrf":
        arpsenkf_input_file_name = "%s/%d.arpsenkf.input" % (input_path, end_time)

        epilogue.extend([
            "mv ????????????_%s.lso %s" % ('%(ens)03d', hx_path),
            "mv ????????????_%s.snd %s" % ('%(ens)03d', hx_path),
            "mv ????_*_??????_%s %s" % ('%(ens)03d', hx_path),
        ])

    for n_ens in cm_args.members:
        ens_member_name = "ena%03d" % (n_ens + 1)
        ens_member_directory = "EN%03d" % (n_ens + 1)

        ens_arps_file_name = arps_input_file_name % {'ens': (n_ens + 1)}

        if read_split:
            init_file = "%s/%s/%s.hdf%06d" % (work_path,
                                              ens_member_directory,
                                              ens_member_name,
                                              start_time),
            init_grdbas = "%s/%s/%s.hdfgrdbas" % (work_path,
                                                  ens_member_directory, ens_member_name),
        else:
            init_file = "%s/%s.hdf%06d" % (work_path, ens_member_name, start_time),
            init_grdbas = "%s/%s.hdfgrdbas" % (work_path, ens_member_name),

        if dump_split:
            out_dir = "%s/%s/" % (work_path, ens_member_directory)
        else:
            out_dir = "%s/" % work_path

        # kwargs = {'hxopt': 0, 'tstop': end_time}
        kwargs['hxopt'] = 0
        kwargs['tstop'] = end_time
        if cm_args.algorithm == '4densrf':
            kwargs['memid'] = n_ens + 1
            kwargs['hxopt'] = 1
            kwargs['tstop'] += 150

        editNamelistFile("%s/%s" % (cm_args.base_path, cm_args.arps_template),
                         ens_arps_file_name,
                         nproc_x=nproc_x,
                         nproc_y=nproc_y,
                         nproc_x_out=nproc_x_dump,
                         nproc_y_out=nproc_y_dump,
                         runname=ens_member_name,
                         initopt=3,
                         inifile=init_file,
                         inigbf=init_grdbas,
                         exbcname="%s/%s" % (bc_path, ens_member_name),
                         tstart=start_time,
                         tstrtdmp=start_time + dump_time,
                         thisdmp=dump_time,
                         dmp_out_joined=int(not dump_split),
                         inisplited=int(read_split),
                         dirname=out_dir,
                         **kwargs
                         )

    if cm_args.algorithm == 'ensrf':
        command = [
            "%s %s $base/arps %s > %s " % (batch.getMPIprogram(),
                                           batch.getMPIargs() % (nproc_x * nproc_y),
                                           arps_input_file_name,
                                           arps_debug_file_name),
            "rm %s" % (" ".join(extraneous_files))
        ]
        command.extend(epilogue)
    elif cm_args.algorithm == '4densrf':
        command = [
            "%s %s $base/arps %s %s > %s " % (batch.getMPIprogram(),
                                              batch.getMPIargs() % (nproc_x * nproc_y),
                                              arps_input_file_name,
                                              arpsenkf_input_file_name,
                                              arps_debug_file_name),
            "rm %s" % (" ".join(extraneous_files))
        ]
        command.extend(epilogue)

    command_lines = doForEnsemble(command, cm_args.members)

    return command_lines


def generateEnsemblePerturbations(cm_args, batch, start_time):
    work_path, input_path, debug_path = \
        getPaths(cm_args.base_path, cm_args.job_name, work=True, input=True, debug=True)

    for n_ens in cm_args.members:
        ens_member_name = "ena%03d" % (n_ens + 1)

        arpsenkfic_input_file_name = "%s/%s.arpsenkfic.input" % (input_path, ens_member_name)

        editNamelistFile("%s/%s" % (cm_args.base_path, cm_args.arpsenkfic_template),
                         arpsenkfic_input_file_name,
                         seeds=-n_ens,
                         dirnamp="%s/" % work_path,
                         outdumpdir="%s/" % work_path,
                         outname=ens_member_name,
                         tfgs=start_time)

    arps_input_file_name = "%s/arps.input" % input_path
    arpsenkfic_input_file_name = "%s/%s.arpsenkfic.input" % (input_path, 'ena%(ens)03d')
    arpsenkfic_debug_file_name = "%s/%s.arpsenkfic.debug" % (debug_path, 'ena%(ens)03d')

    command = "%s -n 1 $base/arpsenkfic %s < %s > %s" % \
        (batch.getMPIprogram(),
         arps_input_file_name,
         arpsenkfic_input_file_name,
         arpsenkfic_debug_file_name)

    command_lines = doForEnsemble(command, cm_args.members)

    return command_lines


def generateEnKFAssimilation(cm_args, batch, assim_time, radar_data_flag=None):
    work_path, input_path, debug_path, batch_path = \
        getPaths(
            cm_args.base_path,
            cm_args.job_name,
            work=True,
            input=True,
            debug=True,
            batch=True)

    nproc_x, nproc_y = cm_args.mpi_config_enkf
    nproc_x_dump, nproc_y_dump = cm_args.mpi_config_dump

    arps_input_file_name = "%s/%d.arps.input" % (input_path, assim_time)
    enkf_input_file_name = "%s/%d.arpsenkf.input" % (input_path, assim_time)
    enkf_debug_file_name = "%s/%d.arpsenkf.debug" % (debug_path, assim_time)
    # batch_file_name = "%s/%d.sh" % (batch_path, assim_time)

    kwargs = {}

    # Figure out what conventional data we're assimilating (combine this with the next section!)
    cvn_data_flags = dict((k, getattr(cm_args, k))
                          for k in ['sndgflags', 'profflags', 'surfflags'])
    # assim_all = False
    if isDivisible(assim_time, 3600):
        print("Assimilate all data ...")
    else:
        cvn_data_flags['sndgflags'] = 'no'
        cvn_data_flags['profflags'] = 'no'

    # Conventional DA flags
    for cvn_flag, kw_flag in [('sndgflags', 'sndassim'), ('profflags',
                                                          'proassim'), ('surfflags', 'sfcassim')]:
        if cvn_flag in cvn_data_flags and cvn_data_flags[cvn_flag].lower() == 'yes':
            kwargs[kw_flag] = 1
        else:
            kwargs[kw_flag] = 0

    if cm_args.split_files:
        kwargs['nproc_x_in'] = nproc_x_dump
        kwargs['nproc_y_in'] = nproc_y_dump
        kwargs['inidirname'] = "%s/ENF%s" % (work_path, "%3N")
    else:
        kwargs['inidirname'] = work_path

    # Figure out what our covariance inflation will be (combine this with the next section!)
    for cov_infl in cm_args.cov_infl:
        if ':' in cov_infl:
            time, factors = cov_infl.split(':')
            if assim_time >= int(time):
                covariance_inflation = factors
        else:
            covariance_inflation = cov_infl

    print("Covariance inflation for this timestep is", covariance_inflation)

    # Covariance inflation flags
    kwargs['mult_inflat'] = 0
    kwargs['adapt_inflat'] = 0
    kwargs['relax_inflat'] = 0
    kwargs['add_inflat'] = 0

    try:
        covariance_inflation = covariance_inflation.split(',')
    except ValueError:
        covariance_inflation = [covariance_inflation]

    for cov_infl in covariance_inflation:
        if '=' in cov_infl:
            inflation_method, inflation_factor = cov_infl.split('=')
            inflation_factor = float(inflation_factor)

            if inflation_method == "mults":
                # Multiplicative inflation in the storm region only
                kwargs['mult_inflat'] = 1
                kwargs['cinf'] = inflation_factor

            elif inflation_method == "multd":
                # Multiplicative inflation over the entire domain
                kwargs['mult_inflat'] = 2
                kwargs['cinf'] = inflation_factor

            elif inflation_method == "adapt":
                # Relaxation to Prior Spread ("Adaptive") inflation
                kwargs['adapt_inflat'] = 1
                kwargs['rlxf'] = inflation_factor

            elif inflation_method == "adapt2":
                # Relaxation to Prior Spread ("Adaptive") inflation, version 2
                kwargs['adapt_inflat'] = 2
                kwargs['rlxf'] = inflation_factor

            elif inflation_method == "relax":
                # Relaxation to Prior Perturbation ("Relaxation") inflation
                kwargs['relax_inflat'] = 1
                kwargs['rlxf'] = inflation_factor
        else:
            inflation_method = cov_infl
            if inflation_method == "add":
                # Additive inflation. Perturbation standard deviations must be set up ahead of
                # time in the arpsenkf.input template file
                kwargs['add_inflat'] = 1

    if cm_args.algorithm == 'ensrf':
        kwargs['anaopt'] = 2
    elif cm_args.algorithm == '4densrf':
        kwargs['anaopt'] = 5

    # print len(radar_data_flag[True]) if True in radar_data_flag else 0
    try:
        n_radars = len(radar_data_flag[True]) if True in radar_data_flag else 0
    except BaseException:
        n_radars = 0
    radardaopt = 1 if n_radars > 0 else 0

    editNamelistFile("%s/%s" % (cm_args.base_path, cm_args.arpsenkf_template), enkf_input_file_name,
                     nen=cm_args.n_ens_members,
                     casenam=cm_args.job_name,
                     enkfdtadir="%s/" % work_path,
                     cvndatadir="%s/obs/" % cm_args.base_path,
                     assim_time=assim_time,
                     radardaopt=radardaopt,
                     nrdrused=n_radars,
                     rmsfcst=2,
                     hdmpfheader=cm_args.job_name,
                     **kwargs
                     )

    if cm_args.algorithm == '4densrf':
        # Hard-code the 4densrf assimilation window for now, change me later
        kwargs = {'hdmptim(1)': assim_time, 'tstop': assim_time + 150}
    else:
        kwargs = {}

    # DTD: arpsenkf needs to dump out to ensemble analysis subdirectories too, I think.
    # Next arps integration was trying to read from individual analysis subdirectories
    # but original code below was saving them to just work_path.
    if cm_args.split_files:
        kwargs['dirname'] = "%s/EN%s" % (work_path, "%3N")
    else:
        kwargs['dirname'] = work_path

    joined = 0 if cm_args.split_files else 1
    editNamelistFile("%s/%s" % (cm_args.base_path, cm_args.arps_template),
                     arps_input_file_name,
                     nproc_x=nproc_x,
                     nproc_y=nproc_y,
                     nproc_x_out=nproc_x_dump,
                     nproc_y_out=nproc_y_dump,
                     dmp_out_joined=joined,
                     inisplited=3 * (1 - joined),
                     sfcdat=3,
                     sv_lkup_tble=0,
                     rd_lkup_tble=1,
                     **kwargs
                     )

    # DTD: removed extra cd to work_path here, so that we are running job in same directory
    # (base_path) as ARPS jobs. This is so that relative paths that are set in arps.input work for
    # both ARPS and ARPSENKF
#    command_lines = [
#        "cd %s" % work_path,
#        "%s %s $base/arpsenkf %s < %s > %s" % (batch.getMPIprogram(),
#           batch.getMPIargs()%(nproc_x*nproc_y), arps_input_file_name, enkf_input_file_name,
#           enkf_debug_file_name),
#        "cd -",
#        "",
#    ]

    command_lines = [
        "%s %s $base/arpsenkf %s < %s > %s" % (batch.getMPIprogram(),
                                               batch.getMPIargs() % (nproc_x * nproc_y),
                                               arps_input_file_name,
                                               enkf_input_file_name,
                                               enkf_debug_file_name),
        "mv *hdfwgt* %s/%s/" % (work_path, "wgt"),
        "mv K* %s/%s/" % (work_path, "stats"),
        "rename .txt _%d.txt dif_*" % (assim_time),
        "mv dif_* {}/{}/".format(work_path, 'difobs'),
        "cd -",
        "",
    ]

    return command_lines


def generateDomainSubset(cm_args, batch, src_path, start_time, end_time,
                         step_time, perturb_ic=True, copy_ic=False):
    work_path, input_path, debug_path, bc_path = \
        getPaths(
            cm_args.base_path,
            cm_args.job_name,
            work=True,
            input=True,
            debug=True,
            boundary=True)

    for n_ens in cm_args.members:
        ens_member_name = "ena%03d" % (n_ens + 1)

        interp_input_file_name = "%s/%s.arpsintrp.input" % (input_path, ens_member_name)
        arpsenkfic_input_file_name = "%s/%s.arpsenkfic.input" % (input_path, ens_member_name)
        arps_input_file_name = "%s/%s.arps.input" % (input_path, ens_member_name)

        editNamelistFile("%s/%s" % (cm_args.base_path, cm_args.arpsintrp_template),
                         interp_input_file_name,
                         runname="%s" % ens_member_name,
                         hdmpfheader="%s/%s" % (src_path, ens_member_name),
                         dirname=bc_path,
                         tbgn_dmpin=start_time,
                         tend_dmpin=end_time,
                         tintv_dmpin=step_time,
                         )

        editNamelistFile("%s/%s" % (cm_args.base_path, cm_args.arps_template),
                         arps_input_file_name,
                         runname="%s" % ens_member_name,
                         initopt=3,
                         inifile="%s/%s.hdf%06d" % (bc_path, ens_member_name, start_time),
                         inigbf="%s/%s.hdfgrdbas" % (bc_path, ens_member_name),
                         tstart=start_time,
                         tstop=end_time,
                         dirname="%s/" % work_path
                         )

        if perturb_ic:
            editNamelistFile("%s/%s" % (cm_args.base_path, cm_args.arpsenkfic_template),
                             arpsenkfic_input_file_name,
                             seeds=-n_ens,
                             dirnamp="%s/" % work_path,
                             outdumpdir="%s/" % work_path,
                             outname=ens_member_name,
                             tfgs=start_time
                             )

    interp_input_file_name = "%s/ena%s.arpsintrp.input" % (input_path, '%(ens)03d')
    interp_debug_file_name = "%s/ena%s.arpsintrp.debug" % (debug_path, '%(ens)03d')
    arps_input_file_name = "%s/ena%s.arps.input" % (input_path, '%(ens)03d')
    arpsenkfic_input_file_name = "%s/ena%s.arpsenkfic.input" % (input_path, '%(ens)03d')
    arpsenkfic_debug_file_name = "%s/ena%s.arpsenkfic.debug" % (debug_path, '%(ens)03d')

    commands = ["rm %s/%sicbc.*" % (bc_path, "ena%(ens)03d"), ""]
    if perturb_ic:
        command_template = ("%s -n 1 $base/arpsintrp %s/arps.input < %s > %s ;"
                            " %s -n 1 $base/arpsenkfic %s < %s > %s")
        commands.append(command_template % (batch.getMPIprogram(), input_path,
                                            interp_input_file_name, interp_debug_file_name,
                                            batch.getMPIprogram(), arps_input_file_name,
                                            arpsenkfic_input_file_name, arpsenkfic_debug_file_name))
    else:
        commands.append(
            "%s -n 1 $base/arpsintrp %s/arps.input < %s > %s" %
            (batch.getMPIprogram(),
             input_path,
             interp_input_file_name,
             interp_debug_file_name))
        if copy_ic:
            commands.extend([
                "cp %s/%s.hdf%06d %s" % (bc_path, 'ena%(ens)03d', start_time, work_path),
                "cp %s/%s.hdfgrdbas %s" % (bc_path, 'ena%(ens)03d', work_path),
                "cp %s/%s.hdfgrdbas %s/%s.hdfgrdbas" % (bc_path,
                                                        'ena%(ens)03d', work_path, 'enf%(ens)03d')
            ])

    command_lines = doForEnsemble(commands, cm_args.members)

    return command_lines


def submit(cm_args, batch, command_lines, wall_time, n_cores,
           start_time, end_time, hybrid=False, squash_jobs=False):

    # TODO: Refactor this function!

    job_suffixes = []
    job_completed = []
    job_submit_count = []
    job_failed = []

    if hybrid:
        n_mpi = int(ceil(float(n_cores) / batch.getNCoresPerNode()))
    else:
        n_mpi = n_cores

    n_nodes = int(ceil(float(n_cores) / batch.getNCoresPerNode()))

    envname = batch.getEnv()
    if(envname == 'rice'):
        queuename = 'dawson29'
        if cm_args.ppn_req > 0:
            ppn = cm_args.ppn_req
        else:
            ppn = min(batch.getNCoresPerNode(), n_cores)
    else:
        queuename = 'normal'

    running_state, complete_state = batch.getQueueStateNames()

    work_path, debug_path, batch_path = getPaths(cm_args.base_path, cm_args.job_name, work=True,
                                                 debug=True, batch=True)

    nproc_x_mod, nproc_y_mod = cm_args.mpi_config_model
    cm_args.mpi_config_dump = cm_args.mpi_config_dump or cm_args.mpi_config_model
    cm_args.mpi_config_enkf = cm_args.mpi_config_enkf or cm_args.mpi_config_model

    nproc_x_dump, nproc_y_dump = cm_args.mpi_config_dump
    nproc_x_enkf, nproc_y_enkf = cm_args.mpi_config_enkf

    if type(command_lines) in [list, tuple]:
        command_lines = {'enkf': command_lines}

    written_example = False
    # DTD: Try to squash multiple runs into one job
    if(squash_jobs):
        runs_per_job = 4
        squashed_command_lines = defaultdict(list)
        count = 0
        for key, commands in command_lines.items():
            if(count % runs_per_job == 0):
                newkey = '%03d' % ((count + runs_per_job) / runs_per_job)
            for cmd in commands:
                squashed_command_lines[newkey].append(cmd)
            count += 1
        command_lines = squashed_command_lines

    for key, commands in command_lines.items():
        key = 'e' + key[-2:]

        if(key == 'ekf'):
            job_key = "%s-%s_%d" % (key, cm_args.job_name, end_time)
        else:
            job_key = "%s-%s_%d-%d" % (key, cm_args.job_name, start_time, end_time)
        if(envname == 'rice'):
            queuename = 'dawson29'
            file_text = batch.gen(
                commands,
                queue=queuename,
                nnodes=n_nodes,
                ppn=ppn,
                timereq=wall_time + ":00",
                jobname=job_key)
        else:
            queuename = 'normal'
            file_text = batch.gen(
                commands,
                jobname=job_key,
                debugfile="%s/%s.output" %
                (debug_path,
                 job_key),
                nmpi=n_mpi,
                nnodes=n_nodes,
                queue=queuename,
                timereq=wall_time +
                ":00")

        # Shouldn't this be called "job_prefixes"?
        job_suffixes.append(key)

        if not written_example or cm_args.save_batch:
            file = open("%s/%s.sh" % (batch_path, job_key), 'w', encoding='utf8')
            file.write(file_text)
            file.close()
            written_example = True

        if cm_args.submit:
            batch.submit(file_text)
        else:
            print("I would submit %s here ..." % job_key)
        job_completed.append(False)
        job_submit_count.append(1)
        job_failed.append(False)

    print("Done submitting ...")

    if not cm_args.submit:
        return

    batch.getQueueStatus()
    need_to_check = False

    while True:
        time.sleep(0.5 * 60)

        queue = batch.getQueueStatus()

        if len(queue) > 0:
            jobs_queued = [r['name'].strip() for r in queue]
            job_name_len = max(len(n) for n in jobs_queued)

            for idx, suffix in enumerate(job_suffixes):
                need_to_check = False
                if suffix == 'ekf':
                    job_key = "%s-%s_%d" % (suffix, cm_args.job_name, end_time)
                else:
                    job_key = "%s-%s_%d-%d" % (suffix, cm_args.job_name, start_time, end_time)
                if job_key[:job_name_len] in jobs_queued:
                    jdy = jobs_queued.index(job_key[:job_name_len])
                    if queue[jdy]['state'] == complete_state:
                        if cm_args.error_check:
                            need_to_check = True
                        else:
                            job_completed[idx] = True
                else:
                    if cm_args.error_check:
                        print("Check that job {} was successful".format(suffix))
                        need_to_check = True
                    else:
                        print("No error checking!")
                        job_completed[idx] = True
                if need_to_check and not job_completed[idx]:
                    # TODO: check to make sure a CFL violation did not occur

                    # Check to see if all the appropriate output files have been written
                    # by the job. If not, something went wrong (likely a lustre problem)
                    # Try resubmitting the job.
                    if suffix == 'ekf':
                        key = 'enkf'
                        path_template = "%s/EN%03d/ena%03d.hdf%06d_%03d%03d"
                        all_files_exist = [os.path.exists(path_template %
                                            (work_path, n_ens + 1, n_ens + 1, end_time,
                                            proc_x, proc_y)) for proc_y in
                                            range(1, nproc_y_enkf + 1)
                                            for proc_x in range(1, nproc_x_enkf + 1)
                                            for n_ens in cm_args.members]
                    else:
                        # Check for individual forecast member failure
                        key = 'ena{:03d}'.format(int(job_key[1:3]))
                        path_template = "%s/ENF%03d/enf%03d.hdf%06d_%03d%03d"
                        all_files_exist = [os.path.exists(path_template %
                                            (work_path, int(job_key[1:3]), int(job_key[1:3]), end_time,
                                            proc_x, proc_y)) for proc_y in
                                            range(1, nproc_y_dump + 1)
                                            for proc_x in range(1, nproc_x_dump + 1)]
                    if not all(all_files_exist):
                        print("Not all files exist for job {}!".format(suffix))
                        # Something went wrong! Resubmit the job if it's the first time it's
                        # happened. Otherwise quit after this cycle.
                        commands = command_lines[key]
                        if(envname == 'rice'):
                            queuename = 'dawson29'
                            file_text = batch.gen(
                                commands,
                                queue=queuename,
                                nnodes=n_nodes,
                                ppn=ppn,
                                timereq=wall_time + ":00",
                                jobname=job_key)
                            print(file_text)
                        else:
                            queuename = 'normal'
                            file_text = batch.gen(
                                commands,
                                jobname=job_key,
                                debugfile="%s/%s.output" %
                                (debug_path,
                                    job_key),
                                nmpi=n_mpi,
                                nnodes=n_nodes,
                                queue=queuename,
                                timereq=wall_time +
                                ":00")
                        if cm_args.submit:
                            if job_submit_count[idx] == 1:
                                print("Problem with {}! Resubmitting!".format(job_key))
                                batch.submit(file_text)
                                job_submit_count[idx] = 2
                            else:
                                print("Job {} failed a second time!".format(job_key),
                                        "You might want to check that out...",
                                        "Stopping after this cycle.")
                                job_failed[idx] = True
                        else:
                            print("I would submit %s here ..." % job_key)
                    else:
                        print("We are here! Had to check but everything's ok!")
                        print("Job {} completed successfully (I think)!".format(job_key))
                        job_completed[idx] = True
                        need_to_check = False
                elif job_completed[idx]:
                    print("Job {} completed successfully (I think)!".format(job_key))
        else:
            for idx in range(len(job_completed)):
                job_completed[idx] = True
        print("Member:    " + " ".join("{:02d}".format(idx+1) for idx, _ in enumerate(job_completed)))
        print("Completed: " + "  ".join("C" if c else "N" for c in job_completed))
        print("Failed:    " + "  ".join("{:d}".format(2) if job_failed[idx] else "{:d}".format(1)
                                        if job_submit_count[idx] == 2 else "{:d}".format(0) for
                                        idx, _ in enumerate(job_completed)))
        if any(job_failed):
            #     print("The following jobs failed twice. Check their output before trying again!")
            #     print("Failed jobs: ".join("{:02d}".format(idx+1) for idx, job in enumerate(job_failed)
            #                                if not job))
            exit()
        if all(job_completed):
            print("All jobs are completed, returning for the next step ...")
            return

    return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n-ens', dest='n_ens_members', default=4, type=int)
    ap.add_argument('--members', dest='members', nargs='+', default=[], type=int)
    ap.add_argument('--base-path', dest='base_path', default=os.getcwd())
    ap.add_argument('--job-name', dest='job_name', default="run_osse_test")
    ap.add_argument('--mpi-config-model', dest='mpi_config_model', nargs=2, default=(3, 4),
                    type=int)
    ap.add_argument('--mpi-config-dump', dest='mpi_config_dump', nargs=2, type=int)
    ap.add_argument('--mpi-config-enkf', dest='mpi_config_enkf', nargs=2, type=int)
    ap.add_argument('--algorithm', dest='algorithm', choices=['ensrf', '4densrf'], default='ensrf')

    ap.add_argument('--ens-start', dest='t_ens_start', default=1200, type=int)
    ap.add_argument('--ens-end', dest='t_ens_end', default=1500, type=int)
    ap.add_argument('--assim-step', dest='dt_assim_step', default=300, type=int)
    ap.add_argument('--ens-step', dest='dt_ens_step', default=300, type=int)

    ap.add_argument('--initial-conditions', dest='init_cond', default='')
    ap.add_argument('--boundary-conditions', dest='bound_cond', default='')
    ap.add_argument('--subset-ic', dest='subset', action='store_true')
    ap.add_argument('--free-forecast', dest='free_forecast', action='store_true')
    ap.add_argument('--covariance-inflation', dest='cov_infl', nargs='+', default=["mult=1.1"])

    ap.add_argument('--arps-template', dest='arps_template', default='arps.input')
    ap.add_argument('--arpsenkf-template', dest='arpsenkf_template', default='arpsenkf.input')
    ap.add_argument('--arpsenkfic-template', dest='arpsenkfic_template', default='arpsenkfic.input')

    ap.add_argument('--assim-radar', dest='radflags')
    ap.add_argument('--assim-sndg', dest='sndgflags', default='yes')
    ap.add_argument('--assim-prof', dest='profflags', default='yes')
    ap.add_argument('--assim-surf', dest='surfflags', default='yes')

    ap.add_argument('--init-fcst-req', dest='init_fcst_req', default='0:40')
    ap.add_argument('--fcst-req', dest='fcst_req', default='0:20')
    ap.add_argument('--init-free-fcst-req', dest='init_free_fcst_req', default='1:45')
    ap.add_argument('--free-fcst-req', dest='free_fcst_req', default='1:30')
    ap.add_argument('--assim-on-req', dest='assim_on_req', default='1:00')
    ap.add_argument('--assim-off-req', dest='assim_off_req', default='0:45')

    ap.add_argument('--chunk-size', dest='chunk_size', default=1200, type=int)
    ap.add_argument('--join-files', dest='split_files', action='store_false')
    # Whether or not the initialization is split.
    ap.add_argument('--split-init', dest='split_init', choices=['auto', 'yes', 'no'],
                    default='auto')
    ap.add_argument('--no-submit', dest='submit', action='store_false')
    ap.add_argument('--restart', dest='restart', action='store_true')
    ap.add_argument('--debug', dest='debug', action='store_true')
    ap.add_argument('--save-batch', dest='save_batch', action='store_true')
    ap.add_argument('--ppn', dest='ppn_req', default=-1, type=int)
    ap.add_argument('--error-check', dest='error_check', action='store_true')
    ap.add_argument('--user-name', dest='user_name', default='dawson29')
    ap.add_argument('--save-lookup', dest='save_lookup', action='store_true')

    args = ap.parse_args()
    batch = Batch('rice', username=args.user_name)  # stampede

#   work_path = "%s/%s" % (args.base_path, args.job_name)
#   input_path = "%s/input" % args.base_path
#   boundary_path = "%s/boundary/" % args.base_path

    work_path, input_path, debug_path, batch_path, boundary_path, hx_path =\
        getPaths(
            args.base_path,
            args.job_name,
            work=True,
            input=True,
            debug=True,
            batch=True,
            boundary=True,
            hx=True)

    if not os.path.exists(work_path):
        os.mkdir(work_path, 0o755)
    if not os.path.exists(input_path):
        os.mkdir(input_path, 0o755)
    if not os.path.exists(debug_path):
        os.mkdir(debug_path, 0o755)
    if not os.path.exists(batch_path):
        os.mkdir(batch_path, 0o755)
    if not os.path.exists(hx_path):
        os.mkdir(hx_path, 0o755)
    if not os.path.exists(work_path + '/wgt'):
        os.mkdir(work_path + '/wgt')
    if not os.path.exists(work_path + '/stats'):
        os.mkdir(work_path + '/stats')
    if not os.path.exists(work_path + '/difobs'):
        os.mkdir(work_path + '/difobs')


    member_list = [m - 1 for m in args.members]
    if member_list == []:
        member_list = list(range(args.n_ens_members))
    args.members = member_list

    nproc_x_mod, nproc_y_mod = args.mpi_config_model
    args.mpi_config_dump = args.mpi_config_dump or args.mpi_config_model
    args.mpi_config_enkf = args.mpi_config_enkf or args.mpi_config_model

    nproc_x_dump, nproc_y_dump = args.mpi_config_dump
    nproc_x_enkf, nproc_y_enkf = args.mpi_config_enkf

    prologue = [
        "echo \"\" > %s/debug/ena%s-%s.output" % (args.base_path, '%(ens)03d', args.job_name),
        "",
    ]

    command_lines = doForEnsemble(prologue, member_list)
    command = ["base=%s" % args.base_path, "cd $base", ""]
    appendCommands(command_lines,
                   doForEnsemble(command, member_list)
                   )

    joined = 0 if args.split_files else 1

    editNamelistFile("%s/%s" % (args.base_path, args.arps_template),
                     "%s/arps.input" % input_path,
                     nproc_x=nproc_x_mod,
                     nproc_y=nproc_y_mod,
                     nproc_x_out=nproc_x_dump,
                     nproc_y_out=nproc_y_dump,
                     dmp_out_joined=joined,
                     inisplited=3 * (1 - joined),
                     sfcdat=3,
                     dirname=work_path
                     )

    do_first_integration = True
    ens_chunk_start = args.t_ens_start

    if not args.free_forecast and args.chunk_size > args.dt_assim_step:
        args.chunk_size = args.dt_assim_step

    if args.dt_ens_step > args.chunk_size:
        args.dt_ens_step = args.chunk_size
        print("Warning: resetting dt_ens_step to be chunk_size (%d)" % args.dt_ens_step)

    if not args.free_forecast:
        try:
            rd = import_all_from("%s/%s" % (args.base_path, args.radflags))
            radar_data_flag = rd.radar_data_flag
            print(radar_data_flag)
        except BaseException:
            radar_data_flag = None
#       args.radar_data_flags = radar_data_flag
    exp_start = args.t_ens_start

    # Copy the configuration information to the working directory, so we'll
    # **ALWAYS HAVE IT IF WE NEED TO GO BACK AND LOOK AT IT**
    config_files = [
        "%s/%s" %
        (args.base_path,
         f) for f in [
            args.arps_template,
            args.arpsenkf_template,
            args.arpsenkfic_template]]
    config_files.extend(['run_real_data_case.py', 'run_real_data_case.sh'])

    for file in config_files:
        subprocess.Popen(['cp', file, "%s/." % work_path])

    if args.restart:
        for t_ens in range(args.t_ens_start, args.t_ens_end +
                           args.dt_assim_step, args.dt_assim_step):

            if args.split_files and args.split_init != 'no':
                ena_exist = [
                    os.path.exists(
                        "%s/EN%03d/ena%03d.hdf%06d_001001" %
                        (work_path, n_ens + 1, n_ens + 1, t_ens)) for n_ens in member_list]
                enf_exist = [
                    os.path.exists(
                        "%s/ENF%03d/enf%03d.hdf%06d_001001" %
                        (work_path, n_ens + 1, n_ens + 1, t_ens)) for n_ens in member_list]
            else:
                ena_exist = [
                    os.path.exists(
                        "%s/ena%03d.hdf%06d" %
                        (work_path, n_ens + 1, t_ens)) for n_ens in member_list]
                enf_exist = [
                    os.path.exists(
                        "%s/enf%03d.hdf%06d" %
                        (work_path, n_ens + 1, t_ens)) for n_ens in member_list]

            all_ena_exist = all(ena_exist)
            all_enf_exist = all(enf_exist)

            if all_ena_exist and not args.free_forecast:
                args.t_ens_start = t_ens
                ens_chunk_start = t_ens
            elif all_enf_exist and not all_ena_exist:
                args.t_ens_start = t_ens - args.dt_assim_step
                do_first_integration = False

            for t_chunk in range(t_ens, t_ens + args.dt_assim_step, args.chunk_size):
                if args.split_files and args.split_init != 'no':
                    ena_exist = [
                        os.path.exists(
                            "%s/EN%03d/ena%03d.hdf%06d_001001" %
                            (work_path, n_ens + 1, n_ens + 1, t_chunk)) for n_ens in member_list]
                else:
                    ena_exist = [
                        os.path.exists(
                            "%s/ena%03d.hdf%06d" %
                            (work_path, n_ens + 1, t_chunk)) for n_ens in member_list]

                if all(ena_exist) and not args.free_forecast:
                    ens_chunk_start = t_chunk

        if do_first_integration:
            print("Restarting from time %d (with integration) ..." % (args.t_ens_start))
        else:
            print("Restarting from time %d (no integration) ..." %
                  (args.t_ens_start + args.dt_assim_step))

    else:
        print("New experiment ...")

        if args.split_files:
            command = "mkdir %s/%s ; mkdir %s/%s" % (work_path,
                                                     'EN%(ens)03d', work_path, 'ENF%(ens)03d')
            appendCommands(command_lines,
                           doForEnsemble(command, member_list)
                           )

        if args.init_cond == "":
            print("Generate random initial conditions ...")
            appendCommands(command_lines,
                           generateEnsemblePerturbations(args, batch, args.t_ens_start)
                           )

            command = "cp %s/%s.hdfgrdbas %s/%s.hdfgrdbas" % (
                work_path, 'ena%(ens)03d', work_path, 'enf%(ens)03d')
            appendCommands(command_lines,
                           doForEnsemble(command, member_list)
                           )
        elif args.init_cond != "restart":
            print("Use supplied initial conditions ...")
            if args.subset:
                print("Subset and perturb the domain ...")
                appendCommands(command_lines,
                               generateDomainSubset(
                                   args,
                                   batch,
                                   args.init_cond,
                                   args.t_ens_start,
                                   args.t_ens_end,
                                   args.dt_ens_step,
                                   perturb_ic=True)
                               )

                command = "cp %s/%s.hdfgrdbas %s/%s.hdfgrdbas" % (
                    boundary_path, 'ena%(ens)03d', work_path, 'enf%(ens)03d')
                appendCommands(command_lines,
                               doForEnsemble(command, member_list)
                               )

            else:
                print("No domain subset ...")
                command = [
                    "cp %s/%s.hdf%06d %s" % (boundary_path, 'ena%(ens)03d',
                                             args.t_ens_start, work_path),
                    "cp %s/%s.hdfgrdbas %s" % (boundary_path, 'ena%(ens)03d', work_path),
                    "cp %s/%s.hdfgrdbas %s/%s.hdfgrdbas" % (boundary_path,
                                                            'ena%(ens)03d', work_path,
                                                            'enf%(ens)03d')
                ]
                appendCommands(command_lines,
                               doForEnsemble(command, member_list)
                               )
        else:
            print("Random initial conditions already computed. I hope you know what you are doing!")

    if args.free_forecast:
        if args.subset and args.t_ens_start == exp_start:
            print("Subset the boundary conditions ...")
            appendCommands(command_lines,
                           generateDomainSubset(
                               args,
                               batch,
                               args.bound_cond,
                               args.t_ens_start,
                               args.t_ens_end,
                               args.dt_ens_step,
                               perturb_ic=False,
                               copy_ic=False)
                           )

            command = "cp %s/%s.hdfgrdbas %s/%s.hdfgrdbas" % (
                boundary_path, 'ena%(ens)03d', work_path, 'enf%(ens)03d')
            appendCommands(command_lines,
                           doForEnsemble(command, member_list)
                           )

        n_chunks = int(ceil(float(args.t_ens_end - args.t_ens_start) / args.chunk_size))
        n_chunk_start = 0

        n_chunk_start = (ens_chunk_start - args.t_ens_start) / args.chunk_size

        # TODO: insert logic to generate lookup tables if needed at the beginning of an
        # experiment. For now, just manually do so.
        if t_ens == args.t_ens_start and not args.restart and args.save_lookup:
            print("This is the beginning of the experiment, we need to generate lookup"
                  "tables for rfopt = 3!")
            kwargs = {
                'sv_lkup_tble': 1,
                'rd_lkup_tble': 0
            }
        else:
            kwargs = {
                'sv_lkup_tble': 0,
                'rd_lkup_tble': 1
            }
        for n_chunk, t_chunk in enumerate(range(ens_chunk_start, args.t_ens_end, args.chunk_size)):
            print("Generating free forecast from %d to %d (chunk %d of %d) ..." %
                  (args.t_ens_start, args.t_ens_end, n_chunk + n_chunk_start + 1, n_chunks))
            chunk_start = t_chunk
            chunk_end = t_chunk + args.chunk_size

            which_split = 'neither'
            if args.split_files and (args.split_init == 'auto' or args.split_init == 'yes'):
                which_split = 'both'
            elif args.split_files and args.split_init == 'no':
                which_split = 'dump'

            if chunk_end > args.t_ens_end:
                chunk_end = args.t_ens_end

            appendCommands(command_lines,
                           generateEnsembleIntegration(
                               args,
                               batch,
                               chunk_start,
                               chunk_end,
                               args.dt_ens_step,
                               split_files=which_split,
                               move_for_assim=False,
                               **kwargs)
                           )

            req_time = args.free_fcst_req
            if args.subset and t_chunk == exp_start:
                req_time = args.init_free_fcst_req

            submit(
                args,
                batch,
                command_lines,
                req_time,
                nproc_x_mod *
                nproc_y_mod,
                chunk_start,
                chunk_end,
                hybrid=False)
            command_lines.clear()

            command = ["base=%s" % args.base_path, "cd $base", ""]
            appendCommands(command_lines,
                           doForEnsemble(command, member_list)
                           )

    else:
        for t_ens in range(args.t_ens_start, args.t_ens_end, args.dt_assim_step):
            print("Generating timestep %d ..." % t_ens)

            # TODO: insert logic to generate lookup tables if needed at the beginning of an
            # experiment. For now, just manually do so.
            if t_ens == args.t_ens_start and not args.restart and args.save_lookup:
                print("This is the beginning of the experiment, we need to generate lookup"
                      "tables for rfopt = 3!")
                kwargs = {
                    'sv_lkup_tble': 1,
                    'rd_lkup_tble': 0
                    }
            else:
                kwargs = {
                    'sv_lkup_tble': 0,
                    'rd_lkup_tble': 1
                }

            start_time = t_ens
            end_time = t_ens + args.dt_assim_step

            if do_first_integration or t_ens > args.t_ens_start:
                n_chunks = int(ceil(float(end_time - start_time) / args.chunk_size))
                n_chunk_start = 0

                if start_time == args.t_ens_start:
                    n_chunk_start = (ens_chunk_start - start_time) / args.chunk_size
                    start_time = ens_chunk_start

                for n_chunk, t_chunk in enumerate(range(start_time, end_time, args.chunk_size)):
                    print(
                        "Submitting ensemble integration for timestep %d (chunk %d of %d) ..." %
                        (t_ens, n_chunk + n_chunk_start + 1, n_chunks))

                    chunk_start = t_chunk
                    chunk_end = t_chunk + args.chunk_size
                    if chunk_end > end_time:
                        chunk_end = end_time

                    which_split = 'neither'
                    if args.split_files:
                        if chunk_start == exp_start:
                            # For the first chunk
                            if args.restart:
                                # We're restarting
                                if args.split_init == 'auto' or args.split_init == 'yes':
                                    which_split = 'both'
                                elif args.split_init == 'no':
                                    which_split = 'dump'
                            else:
                                # No restart
                                if args.split_init == 'auto' or args.split_init == 'no':
                                    which_split = 'dump'
                                elif args.split_init == 'yes':
                                    which_split = 'both'
                        else:
                            # Everything after the first chunk
                            which_split = 'both'

                    if args.algorithm == '4densrf':
                        # ARPS for the 4DEnSRF wants an EnKF input file, too.
                        try:
                            radar_data_flag_sngltime = radar_data_flag[end_time]
                        except KeyError:
                            radar_data_flag_sngltime = None
                        generateEnKFAssimilation(args, batch, chunk_end, radar_data_flag_sngltime)

                    appendCommands(command_lines,
                                   generateEnsembleIntegration(
                                       args,
                                       batch,
                                       chunk_start,
                                       chunk_end,
                                       args.dt_ens_step,
                                       split_files=which_split,
                                       move_for_assim=(
                                           chunk_end == end_time),
                                       **kwargs)
                                   )

                    if args.split_files and t_chunk == exp_start:
                        command_template = "cp %s/%s/%s/%s.hdfgrdbas_%s %s/%s/%s/%s.hdfgrdbas_%s"
                        command = doForMPIConfig(command_template % (args.base_path, args.job_name,
                                                                     'EN%(ens)s', 'ena%(ens)s',
                                                                     '%(x_proc)03d%(y_proc)03d',
                                                                     args.base_path, args.job_name,
                                                                     'ENF%(ens)s', 'enf%(ens)s',
                                                                     '%(x_proc)03d%(y_proc)03d'),
                                                 args.mpi_config_dump)

                        appendCommands(command_lines,
                                       doForEnsemble(command, member_list)
                                       )

                    req_time = args.fcst_req
                    if (args.subset or not args.restart) and t_chunk == exp_start:
                        req_time = args.init_fcst_req

                    submit(
                        args,
                        batch,
                        command_lines,
                        req_time,
                        nproc_x_mod *
                        nproc_y_mod,
                        chunk_start,
                        chunk_end,
                        hybrid=False,
                        squash_jobs=False)
                    command_lines.clear()

                    command = ["base=%s" % args.base_path, "cd $base", ""]
                    appendCommands(command_lines,
                                   doForEnsemble(command, member_list)
                                   )

            req_time = args.assim_off_req
            if isDivisible(end_time, 3600):
                req_time = args.assim_on_req

            # Ask Tim about rationale for using hybrid with so many total cores...
            # assimilation_lines = [ "set base=%s" % args.base_path, "cd $base", "",
            # "setenv OMP_NUM_THREADS %d" % batch.getNCoresPerNode(), "" ]
            assimilation_lines = ["base=%s" % args.base_path, "cd $base", ""]
            try:
                radar_data_flag_sngltime = radar_data_flag[end_time]
            except KeyError:
                radar_data_flag_sngltime = None
            assimilation_lines.extend(
                generateEnKFAssimilation(args, batch, end_time, radar_data_flag_sngltime)
            )
            print("Submitting assimilation for timestep %d ..." % t_ens)
            # submit(args, batch, assimilation_lines, req_time, nproc_x * nproc_y *
            # batch.getNCoresPerNode(), hybrid=True) # Will have to ask Tim about
            # this...
            submit(
                args,
                batch,
                assimilation_lines,
                req_time,
                nproc_x_enkf *
                nproc_y_enkf,
                start_time,
                end_time,
                hybrid=False)
        print("Experiment complete!")
    return


if __name__ == "__main__":
    main()
