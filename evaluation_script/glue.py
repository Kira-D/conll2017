#!/usr/bin/env python

# Glue for conllu files.

import sys
import os

from collections import defaultdict

system_root = "../../data/system" #change this path
postfix_gold = 'out_file_gold.conllu'
postfix_sys = 'out_file.conllu'
wr_folder = 'Results'

def main():
    if not os.path.exists(wr_folder):
        os.makedirs(wr_folder)
    conllu_to_merge = get_paths(system_root)

    for team in conllu_to_merge:
        write_me_gold = open('./' + wr_folder + '/' + team + '_gold.conllu', 'w', encoding='UTF-8')
        write_me_sys = open('./' + wr_folder + '/' + team + '.conllu', 'w', encoding='UTF-8')

        for g, s in zip(sorted(conllu_to_merge[team][0]), sorted(conllu_to_merge[team][1])):
            if os.stat(g).st_size == 0 or os.stat(s).st_size == 0:
                continue

            write_me_gold.write('#' + os.path.basename(g).split('.')[0] + '\n')
            write_me_sys.write('#' + os.path.basename(s).split('.')[0] + '\n')
            with open(g, 'r', encoding='utf-8') as g_infile, open(s, 'r', encoding='utf-8') as s_infile:
                for line in g_infile:
                    write_me_gold.write(line)
                for line in s_infile:
                    write_me_sys.write(line)
        
        write_me_gold.close()
        write_me_sys.close()
    
def get_paths(system_files):
    result = {}

    team_names = os.listdir(system_files)
    for team in team_names:
        run_date = max(os.listdir(os.path.join(system_files, team)))
        team_langs_result = os.listdir(os.path.join(system_files, team, run_date, 'output'))
        gold_out = [os.path.join(system_files, team, run_date, 'output', name) for name in team_langs_result if name.endswith(postfix_gold)]
        system_out = [os.path.join(system_files, team, run_date, 'output', name) for name in team_langs_result if name.endswith(postfix_sys)]
        result[team] = [gold_out, system_out]
                
    return result

if __name__ == "__main__":
    main()

