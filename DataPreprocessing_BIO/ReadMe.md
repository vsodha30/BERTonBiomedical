#Data Preprocessing and BIO Tagging to generate Train and Test Data for Bio-BERT Model

1) Install the pycorenlp, csv, os, pathlib, tqdm package
2) Run keepImpEntities.py for preprocessing the annotated file data and considering only rows which are required.
3) Preprocessed data is stored in "DataSet Folder"
2) Run CoreNLP server (Port No: 9000, Change the port number if required)
3) Place .ann and .txt files from brat in the location specified in DATA_DIRECTORY
4) Run BratToCore.py,finalPreprocessing.py in order. Train and Test files are stored in OutputTrain (train.tsv) and OutputTest (test.tsv) respectively and can be directly used for BertModel
