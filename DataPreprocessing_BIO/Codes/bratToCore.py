import csv

from pycorenlp import StanfordCoreNLP
import os
from os import listdir
from os.path import isfile, join

DEFAULT_OTHER_ANNO = 'O'
STANDOFF_ENTITY_PREFIX = 'T'
STANDOFF_RELATION_PREFIX = 'R'
DATA_DIRECTORY = 'TestingFiles'
OUTPUT_DIRECTORY = 'OutputTestTestingFiles'
count = 0
NER_TRAINING_DATA_OUTPUT_PATH = join(OUTPUT_DIRECTORY, 'ner-crf-training-data.csv')
RE_TRAINING_DATA_OUTPUT_PATH = join(OUTPUT_DIRECTORY, 're-training-data.corp')

if os.path.exists(OUTPUT_DIRECTORY):
	if os.path.exists(NER_TRAINING_DATA_OUTPUT_PATH):
		os.remove(NER_TRAINING_DATA_OUTPUT_PATH)
	if os.path.exists(RE_TRAINING_DATA_OUTPUT_PATH):
		os.remove(RE_TRAINING_DATA_OUTPUT_PATH)
else:
    os.makedirs(OUTPUT_DIRECTORY)

sentence_count = 0
nlp = StanfordCoreNLP('http://localhost:9000')

# looping through .ann files in the data directory
ann_data_files = [f for f in listdir(DATA_DIRECTORY) if isfile(join(DATA_DIRECTORY, f)) and f.split('.')[1] == 'ann']

for file in ann_data_files:
	entities = []
	relations = []

	# process .ann file - place entities and relations into 2 seperate lists of tuples
	with open(join(DATA_DIRECTORY, file), 'r') as document_anno_file:
		lines = document_anno_file.readlines()
		for line in lines:
			standoff_line = line.split()
			#print(standoff_line[0][0])
			#print(int(standoff_line[0][1:]))
			if standoff_line[0][0] == STANDOFF_ENTITY_PREFIX:
				entity = {}
				entity['standoff_id'] = int(standoff_line[0][1:])
				entity['entity_type'] = standoff_line[1].capitalize()
				entity['offset_start'] = int(standoff_line[2].strip())
				entity['offset_end'] = int(standoff_line[3].strip())
				entity['word'] = standoff_line[4:]
				entities.append(entity)
				#print(entity)

			elif standoff_line[0][0] == STANDOFF_RELATION_PREFIX:
				relation = {}
				relation['standoff_id'] = int(standoff_line[0][1:])
				relation['name'] = standoff_line[1]
				relation['standoff_entity1_id'] = int(standoff_line[2].split(':')[1][1:])
				relation['standoff_entity2_id'] = int(standoff_line[3].split(':')[1][1:])
				relations.append(relation)
				# relations.append((standoff_id, relation_name, standoff_entity1_id, standoff_entity2_id))

	# read the .ann's matching .txt file and tokenize its text using stanford corenlp
	with open(join(DATA_DIRECTORY, file.replace('.ann', '.txt')), 'r') as document_text_file:
		document_text = document_text_file.read()

	output = nlp.annotate(document_text, properties={
	  'annotators': 'tokenize,ssplit,pos',
	  'outputFormat': 'json'
	})
	#print(output)
	# write text and annotations into NER and RE output files
	with open(NER_TRAINING_DATA_OUTPUT_PATH, mode = 'a') as ner_training_data:
		#ner_training_data.write('\n')
		#ner_training_data.write('\n')
		fieldnames = ['x', 'y']
		writer = csv.DictWriter(ner_training_data, fieldnames=fieldnames)

		for sentence in output['sentences']:
			#print(len(sentence['tokens']))

			for token1 in sentence['tokens']:
					count+=1
					offset_start = int(token1['characterOffsetBegin'])
					offset_end = int(token1['characterOffsetEnd'])
					entity_found = False
					ner_anno = DEFAULT_OTHER_ANNO
					word = str(token1['word'])
					for entity in entities:
						#print(entity['word'])
						if offset_start >= entity['offset_start'] and offset_end <= entity['offset_end'] and word in entity['word']:
								ner_anno = entity['entity_type']
								if count>=75:
									writer.writerow({'x':"#",'y': "#"})
									count = 0
								writer.writerow({'x':str(token1['word']),'y': str(ner_anno)})
								entity_found = True
								break

					#ner_anno= DEFAULT_OTHER_ANNO
					if entity_found == False:
						if count >= 75:
							writer.writerow({'x': "#", 'y': "#"})
							count = 0
						writer.writerow({'x':str(token1['word']), 'y': "O"})


					entity_found = False
			count = 0
			writer.writerow({'x':"#",'y': "#"})



	#with open(NER_TRAINING_DATA_OUTPUT_PATH, 'r') as f:
	#	data = f.read()
	#	with open(NER_TRAINING_DATA_OUTPUT_PATH, 'w') as w:
	#		w.write(data[:-1])

	print('Processed file pair: {} and {}'.format(file, file.replace('.ann', '.txt')))