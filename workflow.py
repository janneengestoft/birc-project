from gwf import Workflow, AnonymousTarget

gwf = Workflow()

def vcf_filter(vcf_file, pop):
    output_vcf = f'steps/vcf_filtered/{pop}.recode.vcf'
    
    inputs = [vcf_file]
    outputs = [output_vcf]
    options = {
        'memory': '1g',
        'walltime': '01:00:00'
    }
    
    spec = f'''

    vcftools --gzvcf {vcf_file} --recode --keep {pop} \
        --out {output_vcf}
    
    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def admixture(vcf):
    inputs = []
    outputs = []

    options = {
        'memory': '5g',
        'walltime': '08:00:00'
    }

    spec = f'''

    admixture 

    '''
    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)


gwf.target_from_template(
    name='exctract_window',
    template=vcf_filter(
        vcf_file='../../../../primatediversity/people/kmt/baboon_flagship/steps/merged_vcfs/chr10.vcf.gz',
        pop=''
    )
)

gwf.target_from_template(
    name='admixture',
    template=admixture(
        vcf=''
    )
)