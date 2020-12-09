from tqdm import tqdm
from pathlib import Path
def should_remove_line(line, stop_words):
    return any([word in line for word in stop_words])

def _edit_files(path):
    directory = Path(path)
    stop_words = ["Frequency", "Dosage", "Form", "Route", "Strength"]
    for f in tqdm(directory.glob('*.ann'), desc='Reading_files'):

        with open(f) as oldfile, open(f.name, 'w') as newfile:
            for line in oldfile:
                if not line.startswith('R') and not should_remove_line(line, stop_words):
                    #if ";" in line:
                    if line[3].find(';') != -1:
                        edit_line = line.split()
                        new_line = edit_line[:3] + edit_line[4:len(edit_line)]
                        newfile.write(" ".join(new_line)+"\n")
                    else:
                        newfile.write(line)

_edit_files("C:/Users/dhrit/Downloads/gold-standard-test-data/test")
