# {{cookiecutter.experiment_name}}

Author: {{cookiecutter.author}}

```
├── docs                    <- Testing related documents i.e. consent forms
├── instructions            <- Instructions in the experiment
│   ├── end_instr.txt       <- Ending message
│   └── instruction.txt     <- Starting message/instructions
├── references              <- References related to this experiment's design etc.
├── src                     <- Source code for use
│   ├── __init__.py         <- Make src a Python module
│   ├── experiment.py       <- Experiment related functions
│   ├── fileIO.py           <- File reading/writing related functions
│   └── trial_generator.py  <- Experiment trial generation functions (optional).
├── stimuli                 <- Experiment stimuli
│   └── trials.csv          <- Pregenerated trials (optional).
├── README.md               <- The README for people developing/using this experiment
└── run.py                  <- The main experiment code. The task is constructed here.

```


