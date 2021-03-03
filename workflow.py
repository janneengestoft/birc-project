from gwf import Workflow, AnonymousTarget
from scripts.modpath import modpath

gwf = Workflow()

def vcf_filter(vcf_file):
    output_vcf = f'steps/vcf_filtered/.recode.vcf'
    
    inputs = [vcf_file]
    outputs = [output_vcf]
    options = {
        'memory': '1g',
        'walltime': '01:00:00'
    }
    
    spec = f'''

    vcftools --gzvcf {vcf_file} --keep  \
        --out {output_vcf}
    
    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def vcf2bed(filtered_vcf, chrom):
    bed = f'steps/plink/baboons.chr{chrom}.bed'
    base_name = modpath(bed, suffix=('.bed', ''))
    pruned_bed = f'steps/plink/baboons.chr{chrom}.pruned.bed'
    
    inputs = [filtered_vcf]
    outputs = [pruned_bed]

    options = {
        'memory': '2g',
        'walltime': '01:00:00'
    }

    spec = f'''

    mkdir -p steps/plink

    plink --vcf {filtered_vcf} --make-bed --double-id --geno 0.025 --indep-pairwise 50 10 0.1 \
        --out {base_name}
    
    plink --bfile {base_name} --extract {base_name}.prune.in --make-bed --out {base_name}.pruned

 
    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def admixture(k, chrom):
    bedfile = f'steps/plink/baboons.chr{chrom}.pruned.bed'
    outputq = f'steps/admixture/baboons.chr{chrom}.pruned.{k}.Q'
    outputp = f'steps/admixture/baboons.chr{chrom}.pruned.{k}.P'
    no_path = f'baboons.chr{chrom}.pruned.{k}'

    inputs = [bedfile]
    outputs = [outputq, outputp]

    options = {
        'memory': '5g',
        'walltime': '8:00:00'
    }

    spec = f'''

    mkdir -p steps/admixture

    admixture {bedfile} {k}

    mv {no_path}* steps/admixture/

    '''
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

"""
gwf.target_from_template(
    name='exctract_window',
    template=vcf_filter(
        vcf_file='../../../../primatediversity/people/kmt/baboon_flagship/steps/merged_vcfs/chr10.vcf.gz'
    )
)
"""

gwf.target_from_template(
    name='vcf2bed',
    template=vcf2bed(
        filtered_vcf='../../../../primatediversity/data/PG_baboons_pananu3_23_2_2021/output.filtered.snps.chr7.removed.AB.pass.vep.vcf.gz',
        chrom='7'
    )
)

gwf.target_from_template(
    name='admixture',
    template=admixture(
        k=6,
        chrom='7'
    )
)
