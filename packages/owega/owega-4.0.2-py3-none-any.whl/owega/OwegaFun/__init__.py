from .utility import Utility
from . import longTermSouvenirs as lts
# from .longTermSouvenirs import LTS, setAdd, setDel, setEdit
from .functions import Functions

existingFunctions = Functions().append(Utility, 'utility').append(lts.LTS, 'lts')
existingFunctions.disableGroup('lts')


def connectLTS(addfun, delfun, editfun):
	lts.setAdd(addfun)
	lts.setDel(delfun)
	lts.setEdit(editfun)
	existingFunctions.enableGroup('lts')
