FILE DESCRIPTIONS:

classes.py contains all the OOP classes used, namely detector & partition classes.
config.py is the parameter/input file. It contains all the user-parsed data, as well as the problem parameters.
dlpack.py contains an implementaion of the DLPack Packing Algorithm.
main.py is the command file that is to be used to run the system.
mmh.py contains an implementation of the MMH Reshaping Algorithm.
ryg.py contains an implementation of the RYG Reassignment Algorithm.
utils.py contains utility/helper functions used throughout.


INSTRUCTIONS FOR USE:
- enter configurable problem parameters into config.py, including source data filepaths. Run config.py by itself. 
  It has built-in assertion checks, so if it runs successfully, that is great!
- finally run main.py. This starts the optimization system, and outputs a 'move list' of where detectors should be moved.


