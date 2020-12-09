import csv
from os.path import join

import pandas
import pandas as pd

def bio_tagger():
    bio_tagged = []
    prev_tag = "O"
    OUTPUT_DIRECTORY = 'OutputTest'
    NER_TRAINING_DATA_OUTPUT_PATH = join(OUTPUT_DIRECTORY, 'ner-crf-training-data-ARD.tsv')
    NER_TRAINING_DATA_OUTPUT_PATH_CSV = join(OUTPUT_DIRECTORY, 'ner-crf-training-data-ARD.csv')
    csv_file = open("C:/Users/dhrit/PycharmProjects/BIOTagging/OutputTest/ner-crf-training-data.csv")
    #read_tsv = csv.reader(tsv_file, delimiter="\t")
    read_csv =csv.reader(csv_file)
    for line in read_csv:
        #print(line)

        if len(line)==0:
            continue
        elif line[1]=="#":
            bio_tagged.append((" ", " "))
        else:
            line[0] = ''.join(e for e in line[0] if e.isalnum())
            if line[0] == "":
                prev_tag = line[1]
                continue
            if line[1] !="Ade" and line[1]!="Reason" and line[1]!="Drug" and line[1]!="O":
                bio_tagged.append((line[0],"O"))
                prev_tag = "O"
                continue

            if line[1] == "O":  # O
                bio_tagged.append((line[0], line[1]))
                prev_tag = line[1]
                continue
            if line[1] != "O" and prev_tag == "O":  # Begin NE
                bio_tagged.append((line[0], "B-" + line[1]))
                prev_tag = line[1]
            elif prev_tag != "O" and prev_tag == line[1]:  # Inside NE
                bio_tagged.append((line[0], "I-" + line[1]))
                prev_tag = line[1]
            elif prev_tag != "O" and prev_tag != line[1]:  # Adjacent NE
                bio_tagged.append((line[0], "B-" + line[1]))
                prev_tag = line[1]
    for x in bio_tagged:
        with open(NER_TRAINING_DATA_OUTPUT_PATH, 'a') as ner_training_data:
            ner_training_data.write('{}\t{}'.format(x[0], x[1]))
            ner_training_data.write('\n')



bio_tagger()