from gwf import Workflow, AnonymousTarget
from scripts.modpath import modpath

gwf = Workflow()

# Chromosome and group to perform admixture analysis on
chr = 7
pop = 'females'
ks = range(4, 11)

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

def vcf2bed(chrom, pop):
    filtered_vcf = f'steps/recode_vcf/chr{chrom}_{pop}.recode.vcf'
    bed = f'steps/plink/chr{chrom}_{pop}.bed'
    base_name = modpath(bed, suffix=('.bed', ''))
    pruned_bed = f'steps/plink/chr{chrom}_{pop}.pruned.bed'
    
    inputs = [filtered_vcf]
    outputs = [pruned_bed]

    options = {
        'memory': '2g',
        'walltime': '02:00:00'
    }

    spec = f'''

    mkdir -p steps/plink

    plink --vcf {filtered_vcf} --make-bed --double-id --geno 0.025 --indep-pairwise 50 10 0.1 \
        --out {base_name}
    
    plink --bfile {base_name} --extract {base_name}.prune.in --make-bed --out {base_name}.pruned

 
    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


def admixture(k, chrom, pop):
    bedfile = f'steps/plink/chr{chrom}_{pop}.pruned.bed'
    outputq = f'results/admixture/chr{chrom}_{pop}.pruned.{k}.Q'
    outputp = f'results/admixture/chr{chrom}_{pop}.pruned.{k}.P'
    no_path = f'chr{chrom}_{pop}.pruned.{k}'

    inputs = [bedfile]
    outputs = [outputq, outputp]

    options = {
        'memory': '5g',
        'walltime': '8:00:00'
    }

    spec = f'''

    mkdir -p results/admixture

    admixture {bedfile} {k}

    mv {no_path}* results/admixture/

    '''
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

gwf.target_from_template(
    name='exctract_pop',
    template=vcf_filter(
        vcf_file='../../../../primatediversity/data/PG_baboons_pananu3_23_2_2021/output.filtered.snps.chr7.removed.AB.pass.vep.vcf.gz',
        chrom=chr,
        popfile='females_all.txt',
        pop=pop
    )
)


gwf.target_from_template(
    name='vcf2bed',
    template=vcf2bed(
        chrom=chr,
        pop=pop
    )
)

for k in ks:
    gwf.target_from_template(
        name=f'admixture_{k}',
        template=admixture(
            k=k,
            chrom=chr,
            pop=pop
        )
    )
