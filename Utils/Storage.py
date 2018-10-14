from Model.AIML import AIML
import pickle

def save(filename,aiml):
    with open(filename+'.aib', 'wb') as output:
        pickle.dump(aiml, output, pickle.HIGHEST_PROTOCOL)

def restore(filename) -> AIML:
    with open('test.aib', 'rb') as input:
       aiml2 = pickle.load(input)
    return aiml2

def export(filename, aiml):
    with open(filename+'.aiml', 'w') as output:
        output.write(str(aiml))