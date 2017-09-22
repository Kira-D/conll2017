#!/usr/bin/env python

# Evaluaion for dependency relations mismatch.

import sys
import os

from collections import defaultdict
from conll17_ud_eval import evaluate


gold_root = "../../data/gold_files"
system_root = "../../data/filtered-conllu" #change this path


def main(system_gold_map):
    for team in system_gold_map:
        print(team)
        for lang in system_gold_map[team]:
            print(lang)
            #print(system_gold_map[team], lang)
            print(evaluate(system_gold_map[team], lang))

def get_paths(system_files, gold_files):
    gold_files_list = []
    system_files_dict = defaultdict(str) #this is a dict of lists
    system_gold_map = defaultdict(dict)

    team_names = os.listdir(system_files)
    for team in team_names:
        run_date = max(os.listdir(os.path.join(system_files, team)))
        team_langs_result = os.listdir(os.path.join(system_files, team, run_date, 'output'))
        system_files_list = [os.path.join(system_files, team, run_date, 'output', name) for name in team_langs_result]
        system_files_dict[team] = system_files_list

    gold_files_names = os.listdir(gold_files)
    gold_files_list = [os.path.join(gold_files, name) for name in gold_files_names]

    for parser in system_files_dict:
        for language in system_files_dict[parser]:
            if os.path.join(gold_files, os.path.basename(language)) in gold_files_list:
                system_gold_map[parser][language] = os.path.join(gold_files, os.path.basename(language)) #{sys_file:gold:file}
    return system_gold_map

if __name__ == "__main__":
    system_gold_map = get_paths(system_root, gold_root)
    main(system_gold_map)
    
    
    
