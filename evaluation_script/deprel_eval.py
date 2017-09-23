#!/usr/bin/env python

# Evaluaion for dependency relations mismatch.

import sys
import os
import argparse

from collections import defaultdict
from conll17_ud_eval import evaluate_wrapper


gold_root = "../../data/gold_files"
system_root = "../../data/filtered-conllu" #change this path


def main(system_gold_map):
    sys.argv = ['conll17_ud_eval.py', 'foo', 'bar']
    parser = argparse.ArgumentParser()
    parser.add_argument("gold_file", type=str,
                        help="Name of the CoNLL-U file with the gold data.")
    parser.add_argument("system_file", type=str,
                        help="Name of the CoNLL-U file with the predicted data.")
    parser.add_argument("--weights", "-w", type=argparse.FileType("r"), default=None,
                        metavar="deprel_weights_file",
                        help="Compute WeightedLAS using given weights for Universal Dependency Relations.")
    parser.add_argument("--verbose", "-v", default=0, action="count",
                        help="Print all metrics.")
    args = parser.parse_args()
    
    for team in system_gold_map:
        for lang in system_gold_map[team]:
            sys.argv = ['conll17_ud_eval.py', system_gold_map[team][lang], lang]
            args = parser.parse_args()
            evaluation, labels = evaluate_wrapper(args)
            print(labels)

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
    
    
    
