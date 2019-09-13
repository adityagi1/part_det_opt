# part_det_opt
Python implementation of algorithm(s) I designed to solve a variant of the bin-packing problem faced by the Cloud DLP Team.
Consists of the following algorithms:
- DLPACK - A Packing Heuristic Algorithm
- MMH - A Reshaping Algorithm
- RYG - A Reassignment Algorithm

Brief Description: Symantec's cloud operations require fitting detectors (representing customer instances) into partitions (Amazon EC2
instances). A natural goal is to minimize the total number of partitions used, leading to a variant of the classic bin-packing problem
studied in combinatorial optimization. The above algorithms produce an assignment subject to various application-specific constraints.

Following files are included:
- main.py : driver file
- utils.py: helper functions 
- classes.py: object-oriented classes used throughout program
- config.py: configuration file to be used by user to input problem parameters
- dlpack.py: implementation of dlpack algorithm
- mmh.py: implementation of mmh (meet-me-halfway) algorithm 
- ryg.py: implementation of ryg (red-yellow-green) algorithm

