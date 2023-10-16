import argparse
import sys
from nucleodiver.__init__ import __version__

class Params(object):

    def __init__(self, program_name):
        self.program_name = program_name

    def set_options(self):
        if self.program_name == 'nucleodiver':
            parser = self.ncd_options()
        elif self.program_name == 'calcpie':
            parser = self.calcpie_options()

        if len(sys.argv) == 1:
            args = parser.parse_args(['-h'])
        else:
            args = parser.parse_args()
        return args
    
    def ncd_options(self):
        parser = argparse.ArgumentParser(description='NucleoDiver version {}'.format(__version__),
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('nucleodiver --fai <FASTA Index file> \n'
                        '            [--vcf <VCF> OR --geno <geno>]\n'
                        '            -n <name> --window <INT> --step <INT>\n')

        # set options
        parser.add_argument('-I', '--fai',
                            action='store',
                            required=True,
                            type=str,
                            help='Fasta index file.',
                            metavar='')

        parser.add_argument('-V', '--vcf',
                            action='store',
                            default='x',
                            type=str,
                            help=('VCF file for calculating nucleotide diversity.\n'),
                            metavar='')
        
        parser.add_argument('-G', '--geno',
                            action='store',
                            default='x',
                            type=str,
                            help=('geno file instead of VCF.\n'),
                            metavar='')
        
        parser.add_argument('-n', '--name',
                            action='store',
                            required=True,
                            type=str,
                            help=('Output file name.\n'),
                            metavar='')
                            
        parser.add_argument('--window',
                            action='store',
                            default=100000,
                            type=int,
                            help=('Window size where nucleotide diversity is calculated.\n'),
                            metavar='')
        
        parser.add_argument('--step',
                            action='store',
                            default=10000,
                            type=int,
                            help=('Number of CPUs to use.\n'),
                            metavar='')
        
        parser.add_argument('--cpu',
                            action='store',
                            default=2,
                            type=int,
                            help=('Number of CPUs to use.\n'),
                            metavar='')
        
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser
        
    def calcpie_options(self):
        parser = argparse.ArgumentParser(description='NucleoDiver version {}'.format(__version__),
                                         formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('calcpie --pie_values <xxx_pie_values.tsv> \n'
                        '        --list <.list file>\n')

        # set options
        parser.add_argument('-P', '--pie_values',
                            action='store',
                            required=True,
                            type=str,
                            help=('<xxx_pie_values.tsv>.\n'
                                  'which is the output of "nucleodiver"'),
                            metavar='')

        parser.add_argument('-L', '--list',
                            action='store',
                            required=True,
                            type=str,
                            help=('LIST file with designated format.\n'
                                  'Choose varieties for calculating pie'),
                            metavar='')
        
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))
        return parser
        
