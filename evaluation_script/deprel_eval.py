#!/usr/bin/env python

# Evaluaion for dependency relations mismatch.

import sys
import os
import argparse
import json

from collections import defaultdict
from conll17_ud_eval import evaluate_wrapper

gold_root = "../../data/gold_files"
system_root = "../../data/system" #change this path
json_file_name = "all_data.json"
json_file_name_orphans = "orphans_data.json"

def main(gold_files_names):
    json_file = open(json_file_name, 'r', encoding='UTF-8')
    team_lang_statistics = json.load(json_file)

    json_file_orph = open(json_file_name_orphans, 'r', encoding='UTF-8')
    team_lang_correct_orph = json.load(json_file_orph)

    # Get statistics
    get_stats_by_team(team_lang_statistics, threshold=0, relation='orphan')
    get_laTex_table(team_lang_statistics, threshold=0, relation='orphan')
    correct_orphan_stats(team_lang_correct_orph)
    #get_stats(team_lang_statistics, gold_files_names, top=5, relation='all') #ToDo it's not working
    

def correct_orphan_stats(team_lang_correct_orph):
    correct_stats = {}
    for team in sorted(team_lang_correct_orph, key=lambda x: x.lower()):
        correct_stats[team] = ()
        # Get number of all orphans
        all_orph_num = 0
        for lang in sorted(team_lang_correct_orph[team], key=lambda x: x.lower()):
            for dep_pair in sorted(team_lang_correct_orph[team][lang], 
                                   key=lambda x: team_lang_correct_orph[team][lang][x], reverse=True):
                all_orph_num += team_lang_correct_orph[team][lang][dep_pair][0]
        correct_orph_num = 0
        correct_parent_num = 0
        for lang in sorted(team_lang_correct_orph[team], key=lambda x: x.lower()):
            for dep_pair in sorted(team_lang_correct_orph[team][lang], 
                                   key=lambda x: team_lang_correct_orph[team][lang][x], reverse=True):
                if dep_pair == 'orphan-orphan':
                    correct_orph_num += team_lang_correct_orph[team][lang][dep_pair][0]
                    correct_parent_num += team_lang_correct_orph[team][lang][dep_pair][0] - team_lang_correct_orph[team][lang][dep_pair][1]
        correct_stats[team] = (all_orph_num, correct_orph_num, correct_parent_num)

    outfile = open('correct_orphans.csv', 'w', encoding='UTF-8')
    outfile.write('\t'.join(['Parser', 'Aligned orphan number', 'Correct', 'Correct %', 'Correct parent', 'Correct parent %']) + '\n')
    for team in sorted(correct_stats, key=lambda x: x.lower()):
        try:
            outfile.write('\t'.join([team, str(correct_stats[team][0]), str(correct_stats[team][1]),
                                str(round(float(correct_stats[team][1])/float(correct_stats[team][0]) * 100, 2)) + '%',
                                str(correct_stats[team][2]), str(round(float(correct_stats[team][2])/float(correct_stats[team][1]) * 100, 2)) + '%']) + '\n')
        except ZeroDivisionError:
            outfile.write('\t'.join([team, str(correct_stats[team][0]), str(correct_stats[team][1]), '0%', str(correct_stats[team][2]), '0%']) + '\n')
    outfile.close()
        
    
def get_stats_by_team(team_lang_statistics, threshold, relation):
    temp_freq = {}
    for team in sorted(team_lang_statistics, key=lambda x: x.lower()):
        temp_freq[team] = {}
        for lang in sorted(team_lang_statistics[team], key=lambda x: x.lower()):
        
            for dep_pair in sorted(team_lang_statistics[team][lang], 
                                   key=lambda x: team_lang_statistics[team][lang][x], reverse=True):
                                   
                if team_lang_statistics[team][lang][dep_pair][0] > threshold:
                
                    if relation in dep_pair or relation == 'all':
                        if dep_pair not in temp_freq[team]:
                            temp_freq[team][dep_pair] = [0, 0]

                        temp_freq[team][dep_pair][0] += team_lang_statistics[team][lang][dep_pair][0]
                        temp_freq[team][dep_pair][1] += team_lang_statistics[team][lang][dep_pair][1]

    #Create table    
    longest_row = 0
    for team in temp_freq:
        if len(temp_freq[team]) > longest_row:
            longest_row = len(temp_freq[team])

    # Calculate number of errors and percentage
    for team in temp_freq:
        error_num = 0
        for pair in temp_freq[team]:
            error_num += temp_freq[team][pair][0]
        for rel_pair in temp_freq[team]:
            temp_freq[team][rel_pair][0] = (temp_freq[team][rel_pair][0], round(float(temp_freq[team][rel_pair][0]) / float(error_num) * 100, 2))

    list_of_lists = [[] for i in range(longest_row + 1)]
    
    for team in sorted(temp_freq, key=lambda x: x.lower()):
        list_of_lists[0].append(team)
        i = -1
        for i, pair in enumerate(sorted(temp_freq[team], key=lambda x: temp_freq[team][x], reverse=True)):
            list_of_lists[i+1].append(str(pair) + ' ' + str(temp_freq[team][pair][0][1]) +
                                      '% ' + str(temp_freq[team][pair][0][0]) + ' headness: ' +
                                      str(round(float(temp_freq[team][pair][1]) / float(temp_freq[team][pair][0][0]) * 100, 2)) + '% ' +
                                      str(temp_freq[team][pair][1]))
        for j in range(i+2, longest_row+1):
            list_of_lists[j].append('-')
        
    outfile = open(relation + '_gold-sys.csv', 'w', encoding='UTF-8')
    for line in list_of_lists:
        outfile.write('\t'.join(line) + '\n')
    outfile.close()
    
def get_laTex_table(team_lang_statistics, threshold, relation):
    temp_freq = {}
    for team in sorted(team_lang_statistics, key=lambda x: x.lower()):
        temp_freq[team] = {}
        for lang in sorted(team_lang_statistics[team], key=lambda x: x.lower()):
        
            for dep_pair in sorted(team_lang_statistics[team][lang], 
                                   key=lambda x: team_lang_statistics[team][lang][x], reverse=True):
                                   
                if team_lang_statistics[team][lang][dep_pair][0] > threshold:
                
                    if relation in dep_pair or relation == 'all':
                        if dep_pair not in temp_freq[team]:
                            temp_freq[team][dep_pair] = [0, 0]

                        temp_freq[team][dep_pair][0] += team_lang_statistics[team][lang][dep_pair][0]
                        temp_freq[team][dep_pair][1] += team_lang_statistics[team][lang][dep_pair][1]

    #Create table    
    longest_row = 0
    for team in temp_freq:
        if len(temp_freq[team]) > longest_row:
            longest_row = len(temp_freq[team])

    # Calculate number of errors and percentage
    for team in temp_freq:
        error_num = 0
        for pair in temp_freq[team]:
            error_num += temp_freq[team][pair][0]
        for rel_pair in temp_freq[team]:
            temp_freq[team][rel_pair][0] = (temp_freq[team][rel_pair][0], round(float(temp_freq[team][rel_pair][0]) / float(error_num) * 100, 2))

    list_of_lists = [[] for i in range(longest_row + 1)]
    
    for team in sorted(temp_freq, key=lambda x: x.lower()):
        list_of_lists[0].append(team)
        i = -1
        for i, pair in enumerate(sorted(temp_freq[team], key=lambda x: temp_freq[team][x], reverse=True)):
            list_of_lists[i+1].append(str(pair) + ' ' + str(temp_freq[team][pair][0][1]) +
                                      '% ' + str(temp_freq[team][pair][0][0]) + ' headness: ' +
                                      str(round(float(temp_freq[team][pair][1]) / float(temp_freq[team][pair][0][0]) * 100, 2)) + '% ' +
                                      str(temp_freq[team][pair][1]))
        for j in range(i+2, longest_row+1):
            list_of_lists[j].append('-')
        
    outfile = open(relation + '_gold-sys.txt', 'w', encoding='UTF-8')
    outfile.write('\\begin{table*}[ht]\n\\begin{center}\n\\begin{tabular}{|' + 'c|'*len(list_of_lists[0]) + '}\n\\hline\n')
    for line in list_of_lists:
        outfile.write(' & '.join(line) + ' \\\\\n')
        outfile.write('\\hline\n')
    outfile.write('\\end{tabular}\n\\caption{The caption of the big table}\n\\end{center}\n\\end{table*}')
    outfile.close()

def get_stats(team_lang_statistics, gold_files_names, top, relation):
    sorted_teams = sorted(team_lang_statistics, key=lambda x: x.lower())
    length_langs = len(gold_files_names) + 1
    list_of_lists = [[''] + sorted_teams]
    for lang in sorted(gold_files_names):
        lang_by_team = [lang]
        for team in sorted_teams:
            if lang in team_lang_statistics[team]:
                lang_by_team.append([(dep_pair, team_lang_statistics[team][lang][dep_pair][0])
                                        for dep_pair
                                            in sorted(team_lang_statistics[team][lang], 
                                                      key=lambda x: team_lang_statistics[team][lang][x],
                                                      reverse=True)][:top])
            else:
                lang_by_team.append([])
        list_of_lists.append(lang_by_team)

    outfile = open('somebigmatrix.csv', 'w', encoding='UTF-8')
    outfile.write('\t'.join(list_of_lists[0]) + '\n')
    for line in list_of_lists[1:]:
        for entry in line:
            if type(entry) is str:
                outfile.write(entry + '\t')
            else:
                for pair in entry:
                    pass
                    
    outfile.close()

    print(*list_of_lists, sep='\n')


def data_to_json(system_gold_map):
    # Send paits to evaluate_wrapper funcion from conll17_ud_eval
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
    
    team_lang_statistics = defaultdict(dict)
    team_lang_orphan_statistics = defaultdict(dict)

    for team in system_gold_map:
        for lang in system_gold_map[team]:
            sys.argv = ['conll17_ud_eval.py', system_gold_map[team][lang], lang]
            args = parser.parse_args()
            evaluation, labels, eval_orph = evaluate_wrapper(args)
            lang = os.path.basename(lang)
            team_lang_statistics[team][lang] = labels
            team_lang_orphan_statistics[team][lang] = eval_orph

    file_temp = open(json_file_name, 'w', encoding='UTF-8')
    file_temp.write(json.dumps(team_lang_statistics))

    file_temp = open(json_file_name_orphans, 'w', encoding='UTF-8')
    file_temp.write(json.dumps(team_lang_orphan_statistics))

def get_paths(system_files, gold_files):
    # Collect paths to gold and system files.
    # Output format: Dictionary {'Team': {system_parsed_file:corresponding_gold_file}, {}}
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
                
    return system_gold_map, gold_files_names

if __name__ == "__main__":
    system_gold_map, gold_files_names = get_paths(system_root, gold_root)
    data_to_json(system_gold_map)
    main(gold_files_names)
        
