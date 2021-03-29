from gwf import Workflow, AnonymousTarget
from scripts.modpath import modpath
import scripts.vcf2haps

gwf = Workflow()

vcffile = '../../../../primatediversity/data/PG_baboons_pananu3_23_2_2021/output.filtered.snps.chrX.removed.AB.pass.vep.vcf.gz'
chrom = 'X'
pop = 'males'
popfile = 'males.txt'

def vcf_filter(vcf_file, chrom, popfile, pop):
    output_vcf = f'steps/recode_vcf/chr{chrom}_{pop}.recode.vcf'
    base_name = modpath(output_vcf, suffix=('.recode.vcf', ''))
    
    inputs = [vcf_file]
    outputs = [output_vcf]
    options = {
        'memory': '2g',
        'walltime': '02:00:00'
    }
    
    spec = f'''

    mkdir -p steps/recode_vcf

    vcftools --gzvcf {vcf_file} --recode --keep data/{popfile} \
        --out {base_name}
    
    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def vcf2chromopainter(chrom, pop):
    recoded_vcf = f'steps/recode_vcf/chr{chrom}_{pop}.recode.vcf'
    phase_file = f'steps/chromopainter/phase_{chrom}_{pop}.haps'

    inputs = [recoded_vcf]
    outputs = [phase_file]
    options = {
        'memory': '2g',
        'walltime': '03:00:00'
    }

    spec = f'''

    mkdir -p steps/chromopainter

    scripts/vcf2haps.py {recoded_vcf} {phase_file}

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def chromopainter(chrom, pop):
    phase_file = f'steps/chromopainter/phase_{chrom}_{pop}.haps'
    recomb_file = f'data/{chrom}_{pop}.recomrates'                                          # Not the right name
    output = f'steps/chromopainter/something_{chrom}_{pop}.'                                # Not right yet either

    inputs = [phase_file, recomb_file]
    outputs = [output]
    options = {
        'memory': '2g',
        'walltime': '10:00:00'
    }
    
    spec = f'''

    ~/baboondiversity/software/chromopainter-0.0.4/chromopainter -g {phase_file} -r {recomb_file} -a 0 0 -j -o {output}

    
    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def finestructure():
    inputs = []
    outputs = []
    options = {
        'memory': '2g',
        'walltime': '10:00:00'
    }
    
    spec = f''' 
    
    ~/baboondiversity/software/finestructure-0.0.5/finestructure 

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


gwf.target_from_template(
    name='exctract_pop',
    template=vcf_filter(
        vcf_file=vcffile,
        chrom=chrom,
        popfile=popfile,
        pop=pop
    )
)

gwf.target_from_template(
    name='reformat_plink',
    template=vcf2chromopainter(
        chrom=chrom,
        pop=pop
    )
)
