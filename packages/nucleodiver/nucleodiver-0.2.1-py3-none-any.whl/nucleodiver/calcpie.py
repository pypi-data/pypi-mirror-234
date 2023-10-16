#!/usr/bin/env python3

import sys
import pandas as pd
from nucleodiver.params import Params
from nucleodiver.utils import time_stamp

pm = Params('calcpie')
args = pm.set_options()

class CalcPie(object):

    def __init__(self, args):
        self.args = args

        self.pie_values = pd.read_csv(self.args.pie_values, sep='\t', 
                                      index_col=0)
        with open(self.args.list, 'r') as input:
            temp_list = input.readlines()
        self.list = list(map(lambda s:s.rstrip("\n"), temp_list))

        self.output = '{}_calculated_pie.tsv'.format(self.args.list.split('.')[0])
        
    def run(self):
        use = [False, False, False] #List of boolean
        count = 0
        all_columns = self.pie_values.columns.values #all colnames
        for i in range(3, len(all_columns)):
            two = all_columns[i].split('_')
            flag = [False, False]
            for j in range(len(self.list)):
                if two[0] == self.list[j]:
                    flag[0] = True
                if two[1] == self.list[j]:
                    flag[1] = True
            if flag[0] and flag[1]:
                use.append(True)
                count = count + 1
            else:
                use.append(False)


        pie_select = self.pie_values.loc[:, use]
        print(time_stamp(), 'Using {} columns.'.format(count), flush=True)

        #Checking whether enough colmuns are selected
        #expected_ncol = nC2
        expected_ncol = len(self.list) * (len(self.list) - 1) / 2
        if len(pie_select.columns) != expected_ncol:
            print(time_stamp(), 'Error! Not Enough number of columns are found.\n', flush=True)
            sys.exit(1)

        #Sum of pie values for each row / number of varieties = pie
        result_table = self.pie_values.iloc[:, 1:3]
        result_table['pie'] = pie_select.sum(axis=1) / len(pie_select.columns)
        
        result_table.to_csv(self.output, sep='\t')
            

def main():
    print(time_stamp(), 'calcpie started.', flush=True)

    prog = CalcPie(args)
    prog.run()    
    print(time_stamp(), 'calcpie successfully finished.\n', flush=True)

if __name__ == '__main__':
    main()