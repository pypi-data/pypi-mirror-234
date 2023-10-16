
import pickle
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

def load_prior():

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    
    return pickle.load(open(filename,'rb'))

#print(load_prior())
#es_priors = load_prior()

#print('here')