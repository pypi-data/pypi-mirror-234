# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biopipen',
 'biopipen.core',
 'biopipen.ns',
 'biopipen.scripts.bam',
 'biopipen.scripts.bcftools',
 'biopipen.scripts.bed',
 'biopipen.scripts.cnvkit',
 'biopipen.scripts.gene',
 'biopipen.scripts.misc',
 'biopipen.scripts.tcgamaf',
 'biopipen.scripts.tcr.GIANA',
 'biopipen.scripts.tcr.TESSA_source',
 'biopipen.scripts.vcf',
 'biopipen.scripts.web',
 'biopipen.utils']

package_data = \
{'': ['*'],
 'biopipen': ['reports/bam/*',
              'reports/cnv/*',
              'reports/cnvkit/*',
              'reports/delim/*',
              'reports/gsea/*',
              'reports/scrna/*',
              'reports/scrna_metabolic_landscape/*',
              'reports/tcr/*',
              'reports/utils/*',
              'reports/vcf/*',
              'scripts/cnv/*',
              'scripts/delim/*',
              'scripts/gsea/*',
              'scripts/plot/*',
              'scripts/rnaseq/*',
              'scripts/scrna/*',
              'scripts/scrna_metabolic_landscape/*',
              'scripts/tcr/*']}

install_requires = \
['datar[pandas]>=0.15.2,<0.16.0',
 'pipen-board[report]>=0.12,<0.13',
 'pipen-cli-run>=0.10,<0.11',
 'pipen-filters>=0.9,<0.10',
 'pipen-verbose>=0.8,<0.9',
 'pipen>=0.11,<0.12']

extras_require = \
{'runinfo': ['pipen-runinfo>=0.3,<0.4']}

entry_points = \
{'pipen_cli_run': ['bam = biopipen.ns.bam',
                   'bcftools = biopipen.ns.bcftools',
                   'bed = biopipen.ns.bed',
                   'cnv = biopipen.ns.cnv',
                   'cnvkit = biopipen.ns.cnvkit',
                   'cnvkit_pipeline = biopipen.ns.cnvkit_pipeline',
                   'delim = biopipen.ns.delim',
                   'gene = biopipen.ns.gene',
                   'gsea = biopipen.ns.gsea',
                   'misc = biopipen.ns.misc',
                   'plot = biopipen.ns.plot',
                   'rnaseq = biopipen.ns.rnaseq',
                   'scrna = biopipen.ns.scrna',
                   'scrna_basic = biopipen.ns.scrna_basic',
                   'scrna_metabolic_landscape = '
                   'biopipen.ns.scrna_metabolic_landscape',
                   'tcgamaf = biopipen.ns.tcgamaf',
                   'tcr = biopipen.ns.tcr',
                   'vcf = biopipen.ns.vcf',
                   'web = biopipen.ns.web']}

setup_kwargs = {
    'name': 'biopipen',
    'version': '0.18.0',
    'description': 'Bioinformatics processes/pipelines that can be run from `pipen run`',
    'long_description': 'None',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
