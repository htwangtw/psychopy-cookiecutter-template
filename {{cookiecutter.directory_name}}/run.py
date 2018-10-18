#!/usr/bin/python
# -*- coding: utf-8 -*-

'''run.py
build and run the main program here
'''

import os
import sys

from psychopy import core, event, logging, visual
from random import shuffle
from src.experiment import subject_info, event_logger, Paradigm, Text, Text_trial, Img_trial, instructions
from src.fileIO import load_conditions_dict, write_csv



# settings
INFO = {
    'Experiment': ['{{cookiecutter.experiment_name}}'],  # compulsory
    'Subject': '',# compulsory
    'Session': '',# compulsory
    }

settings = {
    'window_size': 'full_screen',
#    'window_size': [800, 600],
    'mouse_visible': False,
    'logging_level': logging.INFO,
    'MRI': False # set to true to allow trigger wait and dummy volume time
}

# MRI related settings
fmri_setting = {'trigger': '5',
                'dummy_vol': 3,
                'tr': 3,
                'slice_per_vol': 60
                }

keys = ['1', '2', '3', '4']

# instructions
exp_txt = './instructions/instruction.txt'
end_txt = './instructions/end_instr.txt'
trials_file = './stimuli/trials.csv'



def run_experiment(experiment_info, trials):

    # create experiment
    Experiment = Paradigm(escape_key='esc', color=0,
                          window_size=settings['window_size'])
    fixation = Text(window=Experiment.window, text='+', color='white', height=font_size)
    trigger = visual.TextStim(
                Experiment.window, text='Waiting for scanner.',
                name='trigger',
                pos=[-50,0], height=48, wrapWidth=1100,
                color='white',
                )


    startexp = instructions(window=Experiment.window, instruction_txt=exp_txt, color='white')
    endexp = instructions(window=Experiment.window, instruction_txt=end_txt, color='white')

    # hide mouse
    event.Mouse(visible=settings['mouse_visible'])

    # task instruction
    startexp.show(duration=None)


    if settings['MRI']==True:

        # wait trigger
        trigger.draw()
        Experiment.window.flip()
        event.waitKeys(keyList=fmri_setting['trigger'])

        # dummy volumes
        timer = core.Clock()
        fixation.show(timer, fmri_setting['tr'] * fmri_setting['dummy_vol'])

    # start the clock
    timer = core.Clock()

    for trial in trials:
        # write your task here


    # quit
    endexp.show(fmri_setting['tr'])
    Experiment.window.close()
    core.quit()



# now run this thing
if __name__ == "__main__":

    # set working directory as the location of this file
    _thisDir = os.path.dirname(os.path.abspath(__file__)
                               ).decode(sys.getfilesystemencoding())
    os.chdir(_thisDir)

    # load your experiment trials
    trials = load_conditions_dict(trials_file)
    shuffle(trials)

    # collect participant info
    experiment_info = subject_info(INFO)

    # set log file
    event_logger(settings['logging_level'], experiment_info['LogFile'])

    # run
    run_experiment(experiment_info, trials)


