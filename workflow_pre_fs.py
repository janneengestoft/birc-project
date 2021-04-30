from gwf import Workflow, AnonymousTarget
from scripts.modpath import modpath

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

def vcf2plink(chrom, pop):
    filtered_vcf = f'steps/recode_vcf/chr{chrom}_{pop}.recode.vcf'
    ped_file = f'steps/plink/chr{chrom}_{pop}.ped'
    map_file = f'steps/plink/chr{chrom}_{pop}.map'
    base_name = modpath(ped_file, suffix=('.ped', ''))

    inputs = [filtered_vcf]
    outputs = [ped_file, map_file]
    options = {
        'memory': '2g',
        'walltime': '10:00:00'
    }
    
    spec = f''' 
    
    mkdir -p steps/plink

    plink --vcf {filtered_vcf} --recode12 --double-id --geno 0.025 --out {base_name}  

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def plink2finestructure(chrom, pop):
    ped_file = f'steps/plink/chr{chrom}_{pop}.ped'
    map_file = f'steps/plink/chr{chrom}_{pop}.map'
    id_file = f'steps/finestructure/chr{chrom}_{pop}.ids'
    phase_file = f'steps/finestructure/chr{chrom}_{pop}.phase'                              # Fix name

    inputs = [ped_file, map_file]
    outputs = [phase_file, id_file]
    options = {
        'memory': '2g',
        'walltime': '10:00:00'
    }
    
    spec = f''' 

    mkdir -p steps/finestructure
    
    ../../../software/fs_janne/plink2chromopainter.pl -p={ped_file} -m={map_file} \
        -d={id_file} -o={phase_file}   

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
    name='reformat2plink',
    template=vcf2plink(
        chrom=chrom,
        pop=pop
    )
)

gwf.target_from_template(
    name='reformat2finestructure',
    template=plink2finestructure(
        chrom=chrom,
        pop=pop
    )
)