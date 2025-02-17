from gwf import Workflow, AnonymousTarget
import os

"""
This workflow is made to run fs in a slurm/gwf compliant way,
which means that all processes have to be defined before the code is run
"""

"""
By Erik Fogh Sørensen
"""

#
# Variable definitions
#

gwf = Workflow(defaults={"account": "baboondiversity"})
run_name = "test"
cp_dir = "steps/finestructure/"
os.makedirs(cp_dir+run_name, exist_ok=True)
idfile = "../../../data/haploidified_chrX_males/idfile.ids"
phasefile = "../../../data/haploidified_chrX_males/chrX_haploid.phase"
# recombfile = 'data/chrX.map'
recombfile = "../../../data/haploidified_chrX_males/approx_rec.recombfile" # Uniform recombination rate
s3iters = 100000
s4iters = 50000
s1minsnps = 1000
s1indfrac = 0.1

block_number_1 = 10
block_number_2 = 75

#
# Functions
#


def fs_start(cp_dir, run_name, idfile, phasefile, recombfile,
             s3iters, s4iters, s1minsnps, s1indfrac):

    """Function to initialize the fs run in hpc mode. If options should be added, they are defined here"""
    commandfile = f'{cp_dir}/{run_name}/commandfiles/commandfile1.txt'
    
    inputs = [idfile, phasefile, recombfile]
    outputs = [commandfile] #cp_dir+run_name+"/commandfiles/commandfile1.txt"
    
    options = {
        'cores': 1, 
        'memory': '8g', 
        'walltime': '01:00:00', 
        'account': 'baboondiversity'}

    spec = f'''
    
    cd {cp_dir}

    fs {run_name}.cp -hpc 1 -idfile ../../{idfile} -phasefiles ../../{phasefile} -recombfiles ../../{recombfile} \
        -s3iters {s3iters} -s4iters {s4iters} -s1minsnps {s1minsnps} -s1indfrac {s1indfrac} -go

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def fs_master(cp_dir, run_name, i, o):
    """Function to run the -go parts of fs"""
    
    inputs = i
    outputs = [cp_dir+run_name+o]
    
    options = {
        'cores': 2, 
        'memory': "8g", 
        'walltime': "01:00:00", 
        "account": 'baboondiversity'}

    spec = f'''

    cd {cp_dir}

    fs {run_name}.cp -go

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def command_files(block, block_number, cp_dir, run_name, cf, i):
    """Function to run the commandfiles generated"""
    
    inputs = i
    o_file = f'{run_name}/commandfiles/{cf[-5]}_{block}_{block_number}'
    outputs = cp_dir+o_file
    
    options = {
        'cores': 4, 
        'memory': "16g", 
        'walltime': "04:00:00", 
        "account": 'baboondiversity'}

    spec = f'''

    cd {cp_dir}
    file_length=$(wc -l < {run_name}/commandfiles/{cf})
    start=$((file_length*{block-1}/{block_number}+1))
    stop=$((file_length*{block}/{block_number}))
    sed -n "$start,$stop p" {run_name}/commandfiles/{cf} | bash
    touch {o_file}

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def command_files_single(cp_dir, run_name, cf, i):
    """Function to run the commandfiles generated"""
    inputs = i
    o_file = f'{run_name}/commandfiles/{cf[-5]}'
    outputs = cp_dir+o_file
    
    options = {
        'cores': 8, 
        'memory': "16g", 
        'walltime': "04:00:00", 
        "account": 'baboondiversity'}

    spec = f'''

    cd {cp_dir}

    cat {run_name}/commandfiles/{cf} | parallel

    touch {o_file}

    '''
    print(spec)
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


#
# Function calls
#
# Goal for the runtime/dataset:
# Optimized for 75-300 samples.
# TODO: Code might fail if more jobs are submitted than lines in commandfiles, investigate solutions.

fs1 = gwf.target_from_template('fs_start',
                               fs_start(cp_dir=cp_dir, run_name=run_name, idfile=idfile,
                                        phasefile=phasefile, recombfile=recombfile,
                                        s3iters=s3iters, s4iters=s4iters,
                                        s1minsnps=s1minsnps, s1indfrac=s1indfrac))
# Runnote: Very quick

block_list = list(range(1, block_number_1+1))
cf1 = gwf.map(command_files, block_list, name='c1',
              extra={'block_number': block_number_1, 'cp_dir': cp_dir,
                     'run_name': run_name, 'cf': 'commandfile1.txt', 'i': fs1.outputs
                     })
# Runnote: Roughly 15 for a single command, 31 for 2.

fs2 = gwf.target_from_template('fs2',
                               fs_master(cp_dir=cp_dir, run_name=run_name,
                                         i=cf1.outputs, o="/commandfiles/commandfile2.txt"))
# Runnote: Very quick

block_list = list(range(1, block_number_2+1))
cf2 = gwf.map(command_files, block_list, name='c2',
              extra={'block_number': block_number_2, 'cp_dir': cp_dir,
                     'run_name': run_name, 'cf': 'commandfile2.txt', 'i': fs2.outputs
                     })
# Runnote: Roughly 15 minutes for a single command, 30 for 2.

fs3 = gwf.target_from_template('fs3',
                               fs_master(cp_dir=cp_dir, run_name=run_name,
                                         i=cf2.outputs, o="/commandfiles/commandfile3.txt"))
# Runnote: Very quick

cf3 = gwf.target_from_template('cf3',
                               command_files_single(cp_dir=cp_dir, run_name=run_name,
                                                    cf='commandfile3.txt', i=fs3.outputs))
# Runnote: A bit over 1 hour

fs4 = gwf.target_from_template('fs4',
                               fs_master(cp_dir=cp_dir, run_name=run_name,
                                         i=cf3.outputs, o="/commandfiles/commandfile4.txt"))
# Runnote: Very quick

cf4 = gwf.target_from_template('cf4',
                               command_files_single(cp_dir=cp_dir, run_name=run_name,
                                                    cf='commandfile4.txt', i=fs4.outputs))
# Runnote: 2 minutes
