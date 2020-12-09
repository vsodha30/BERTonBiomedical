Once you extract the Zip folder:-

The main code is in biobert, go to biobert directory level

1) Run:- 
   pip install -r requirements.txt


    -- set the varaibles to following values--
    NER_OUTPUT_DIR = 'ner_outputs-BMI'
    DATASET_DIR = 'datasets/NER/APNA'

2) (Optional) If required to train
    run :-

python run_ner.py --do_train=true --do_eval=true --max_seq_length=200 --vocab_file=biobert_v1.1_pubmed/vocab.txt --bert_config_file=biobert_v1.1_pubmed/bert_config.json --init_checkpoint=biobert_v1.1_pubmed/model.ckpt-1000000 --num_train_epochs=10.0 --data_dir=$DATASET_DIR --output_dir=$NER_OUTPUT_DIR

3) (Optional) If required to predict
    run :-

python run_ner.py --do_train=false --do_predict=true --max_seq_length=200 --vocab_file=biobert_v1.1_pubmed/vocab.txt --bert_config_file=biobert_v1.1_pubmed/bert_config.json --init_checkpoint=biobert_v1.1_pubmed/model.ckpt-1000000 --num_train_epochs=10.0 --data_dir=$DATASET_DIR --output_dir=$NER_OUTPUT_DIR

4) (Optional) If requires to detokenize the tokens created after training and predicting

python biocodes/ner_detokenize.py --token_test_path=$NER_OUTPUT_DIR/token_test.txt --label_test_path=$NER_OUTPUT_DIR/label_test.txt --answer_path=$DATASET_DIR/test.tsv --output_dir=$NER_OUTPUT_DIR

5) For final evaluation results:-
!perl biocodes/conlleval.pl < $NER_OUTPUT_DIR/NER_result_conll.txt