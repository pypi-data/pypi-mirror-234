#!/usr/bin/env python3

import math

import pandas as pd
from nucleodiver.params import Params
from nucleodiver.utils import read_vcf, time_stamp

pm = Params('nucleodiver')
args = pm.set_options()


from multiprocessing import Pool

class NucleoDiver_2(object):

    def __init__(self, args):
        self.args = args
        self.wind = self.args.window
        self.step = self.args.step
        self.output_1 = '{}_mutations.tsv'.format(args.name)
        self.output_2 = '{}_pie_values.tsv'.format(args.name)
        self.output_3 = '{}_list.tsv'.format(args.name)
        
        #Prepare chromosome information
        self.fai_data = []
        with open(self.args.fai, 'r') as f:
            for row in f:
                row = row.strip()
                self.fai_data.append(row.split('\t'))
        fai_col = ['chr', 'len', 'A', 'B', 'C']
        self.fai_data = pd.DataFrame(self.fai_data, columns=fai_col)
        self.fai_data['len'] = self.fai_data['len'].astype(int)

        #Read vcf file
        vcf_list = read_vcf(args.vcf)
        self.vcf_header = vcf_list[0]
        self.vcf_col = vcf_list[1]
        self.vcf_col[0] = 'CHROM'
        self.data = pd.DataFrame(vcf_list[2], columns=self.vcf_col)
        self.data['POS'] = self.data['POS'].astype(int)
        self.newdata = self.data.iloc[:, 0:9]

        #Making set of regions to focus.
        #[chr01, 1, 100000], [chr01, 10001, 110000]...
        self.loc = []
        for i in range(len(self.fai_data['chr'])):
            for j in range(math.ceil(self.fai_data['len'][i]/self.step)):
                c = self.fai_data['chr'][i]
                sta = 1 + self.step * j
                end = sta + self.wind - 1
                self.loc.append([c, sta, end])

    def run(self):
        #Make new DataFrame easy to parse.
        for i in range(9, len(self.data.columns)):
            newcol = []
            for j in range(len(self.data)):
                temp = self.data.iat[j, i]
                #ex. temp = "1/1:0,5:5:15:203,15,0"

                geno = temp.split(':')[0]
                #ex. geno = "1/1"
                
                hap = geno.split('/')
                #ex. hap = ["1", "1"]
                if len(hap) != 2:
                    newcol.append(-1)

                #Homo --> 0,1,2.... Hetero or missing --> -1
                check_list = (str.isdigit(hap[0])
                              and str.isdigit(hap[1])
                              and hap[0] == hap[1])
                if check_list:
                    newcol.append(int(hap[0]))
                else:
                    newcol.append(-1)
            self.newdata['{}'.format(self.data.columns[i])] = newcol
        print(time_stamp(), 'Extracting variants data has done.', flush=True)


        #Making list of 2 varieties set
        #If 100 varieties, 100*99/2=4550 sets
        set = []
        count = 0
        for i in range(9, len(self.vcf_col)-1):
            for j in range(i+1, len(self.vcf_col)):
                set.append([count, i, j])
                count = count + 1
        #set[0] = ID, set[1]=Column number of variety 1, set[2]=that of 2.

        with Pool(self.args.cpu) as p:
            results = p.map(self.parallel, set)

        #result is the list of [id, list of mutation number, list of pie value,
        #                       names of 2 varieties]
        #sort by id
        results.sort(reverse=False, key=lambda x:x[0])

        df_1 = pd.DataFrame(self.loc, columns=['chr','start','end'])
        df_2 = pd.DataFrame(self.loc, columns=['chr','start','end'])
        list_3 = self.vcf_col[9:]
        for i in range(len(results)):
            res = results[i]
            df_1['{}'.format(res[3])] = res[1]
            df_2['{}'.format(res[3])] = res[2]

        df_1.to_csv(self.output_1, sep='\t')
        df_2.to_csv(self.output_2, sep='\t')
        with open(self.output_3, 'w') as o:
            for h in list_3:
                o.write('{}\n'.format(h))
        
        
    def parallel(self, set):
        id = set[0]
        n1 = set[1]
        n2 = set[2]
        name_of_set = '{}_{}'.format(self.vcf_col[n1], self.vcf_col[n2])
        print(time_stamp(), 'Processing data of No. {}.'.format(id), flush=True)

        #Make DataFrame with 0 or 1 data according to mutation or not
        mut_data = self.newdata.iloc[:, 0:2] #only CHROM and POS
        mutcol = []
        for i in range(len(self.newdata)):
            val_1 = self.newdata.iat[i, n1]
            val_2 = self.newdata.iat[i, n2]

            check_list = (val_1 != -1
                          and val_2 != -1
                          and val_1 != val_2)
            if check_list:
                mutcol.append(1)
            else:
                mutcol.append(0)
        mut_data['mut'] = mutcol

        #Calculate mutation number and pie value
        mutations = []
        pie = []
        for i in range(len(self.loc)):
            temp_chr = self.loc[i][0]
            temp_sta = self.loc[i][1]
            temp_end = self.loc[i][2]
            sub_data = mut_data.query('CHROM == @temp_chr '
                                      'and POS >= @temp_sta '
                                      'and POS <= @temp_end')
            mut = sub_data['mut'].sum()
            mutations.append(mut)
            pie.append(mut / self.wind)

        return [id, mutations, pie, name_of_set]
        

def main():
    print(time_stamp(), 'nucleodiver started.', flush=True)

    prog = NucleoDiver_2(args)
    prog.run()    
    print(time_stamp(), 'nucleodiver successfully finished.\n', flush=True)

if __name__ == '__main__':
    main()
