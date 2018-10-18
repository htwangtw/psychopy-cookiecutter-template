# -*- coding: utf-8 -*-

'''experiment.py
experiemnt stimulus here
'''
from psychopy import core, data, gui, visual, event, logging
from pyglet.window import key

import os
from src.fileIO import create_dir, load_instruction
from random import uniform, shuffle

import numpy as np

# use the first font found on this list

sans = ['Arial', 'Gill Sans MT', 'Helvetica', 'Verdana']


class Paradigm(object):
    '''
    Study paradigm
    '''
    def __init__(self, escape_key='esc', window_size=(1280, 720), color=0, *args, **kwargs):
        self.escape_key = escape_key
        self.trials = []
        self.stims = {}

        if window_size =='full_screen':
            self.window = visual.Window(fullscr=True, color=color, units='pix', *args, **kwargs)
        else:
            self.window = visual.Window(size=window_size, color=color, allowGUI=True, units='pix', *args, **kwargs)


class Text(object):
    '''
    show text in the middle of the screen
    such as 'switch'
    '''
    def __init__(self, window, text, color, height=34):
        '''Initialize a text stimulus.
        Args:
        window - The window object
        text - text to display
        duration - the duration the text will appear
        keys - list of keys to press to continue to next stimulus. If None,
                will automatically go to the next stimulus.
        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.text = visual.TextStim(self.window, text=text, height=height, wrapWidth=1100, color=color, font=sans)

    def show(self, clock, duration):
        self.text.draw()
        self.window.flip()
        start_trial = clock.getTime()
        core.wait(duration)
        if event.getKeys(keyList=['escape']):
            print('user quit')
            core.quit()
        return start_trial


class Text_trial(object):
    '''
    show text-based trials in the middle of the screen
    receive responses
    '''
    def __init__(self, window, color, respkeylist, keyans=None, height=34):
        '''Initialize a text stimulus.
        Args:
        window - The window object
        text - text to display
        duration - the duration the text will appear
        respkeylist - list of keys to press to continue to next stimulus.
                        If None, will automatically go to the next stimulus.
        keyans - what each key in respkeylist actually means.
                If None, copy respkeylist
        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.text = visual.TextStim(self.window, text=None, height=height,
                                    wrapWidth=1100, color=color, font=sans)

        if keyans is None:
            self.respkeylist, self.keyans = respkeylist, respkeylist
        else:
            self.respkeylist, self.keyans = respkeylist, keyans

    def set_trial(self, trial):
        self.duration = trial['StimDuration']
        self.ans = trial['Ans']
        self.text.setText(trial['Item'])
        self.item = [trial['Item']]

    def show(self, clock):
        event.clearEvents()

        rt = np.nan
        correct = None
        KeyResp = None
        Resp = None
        KeyPressTime = np.nan

        self.text.draw()
        self.window.flip()
        start_trial = clock.getTime()
        trial_clock = core.Clock()
        if self.duration is None:
            # wait for certain key
            event.waitKeys(keyList=self.respkeylist)
        else:
            # answer in a time frame
            while KeyResp is None and (trial_clock.getTime() <= self.duration):
                # get key press and then disappear
                self.text.draw()
                self.window.flip()
                KeyResp, Resp, KeyPressTime = get_keyboard(
                    clock, self.respkeylist, self.keyans)
            # get reaction time and key press
            if not np.isnan(KeyPressTime):
                rt = KeyPressTime - start_trial
            else:
                KeyResp, Resp = 'None', 'None'

            # get correct trials
            if self.ans == 'NA':
                correct = None
            elif self.ans == Resp:
                correct = 1
            else:
                correct = 0

        return start_trial, KeyResp, Resp, rt, correct


class Img_trial(object):
    '''
    show image-based trials in the middle of the screen
    receive responses
    '''
    def __init__(self, window, respkeylist, keyans=None):
        '''Initialize a text stimulus.
        Args:
        window - The window object        duration - the duration the text will appear
        respkeylist - list of keys to press to continue to next stimulus.
                        If None, will automatically go to the next stimulus.
        keyans - what each key in respkeylist actually means.
                If None, copy respkeylist
        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.img = visual.ImageStim(self.window, image=None)

        if keyans is None:
            self.respkeylist, self.keyans = respkeylist, respkeylist
        else:
            self.respkeylist, self.keyans = respkeylist, keyans

    def set_trial(self, trial):
        self.duration = trial['StimDuration']
        self.ans = trial['Ans']
        self.img.setImage(trial['Item'])
        self.item = [trial['Item']]

    def show(self, clock):
        event.clearEvents()

        rt = np.nan
        correct = None
        KeyResp = None
        Resp = None
        KeyPressTime = np.nan

        self.img.draw()
        self.window.flip()
        start_trial = clock.getTime()
        trial_clock = core.Clock()
        if self.duration is None:
            # wait for certain key
            event.waitKeys(keyList=self.respkeylist)
        else:
            # answer in a time frame
            while KeyResp is None and (trial_clock.getTime() <= self.duration):
                # get key press and then disappear
                self.img.draw()
                self.window.flip()
                KeyResp, Resp, KeyPressTime = get_keyboard(
                    clock, self.respkeylist, self.keyans)
            # get reaction time and key press
            if not np.isnan(KeyPressTime):
                rt = KeyPressTime - start_trial
            else:
                KeyResp, Resp = 'None', 'None'

            # get correct trials
            if self.ans == 'NA':
                correct = None
            elif self.ans == Resp:
                correct = 1
            else:
                correct = 0

        return start_trial, KeyResp, Resp, rt, correct


class Question(object):
    '''
    collect mind wandering report
    '''
    def __init__(self, window, questions, color):
        '''Initialize a question stimulus.
        Args:
        window - The window object
        questions - a list of dictionaries
        keys - list of keys to press to continue to next stimulus. If None,
                will automatically go to the next stimulus.
        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.description = visual.TextStim(
                self.window, text=None, height=34,
                wrapWidth=1100, color=color, font=sans)
        self.scale_lh = visual.TextStim(
                self.window, text=None, height=34, wrapWidth=1100,
                pos=[0, -150],
                color=color, font=sans)
        self.questions = questions
        self.rating = visual.RatingScale(self.window, low=1, high=10, markerStart=4.5,
                precision=10, tickMarks=[1, 10],
                leftKeys='1', rightKeys='2', acceptKeys='4')

    def set(self, trial):
        self.description.setText(trial['Item'])
        self.scale_lh.setText(trial['Scale_low'] + ' ' * 40 + trial['Scale_high'])
        if trial['StimDuration']:
            self.scale_max_time = trial['StimDuration']
        else:
            self.scale_max_time = 90


    def show(self, clock):
        keyState=key.KeyStateHandler()
        self.window.winHandle.push_handlers(keyState)
        self.description.draw()
        self.scale_lh.draw()
        self.rating.draw()
        self.window.flip()
        start_trial = clock.getTime()

        pos = self.rating.markerStart
        inc = 0.1

        while (self.rating.noResponse
               and clock.getTime() - start_trial < self.scale_max_time):
            if event.getKeys(keyList=['escape']):
                print('user quit')
                core.quit()

            if keyState[key._1] is True:
                pos -= inc
            elif keyState[key._2] is True:
                pos += inc

            if pos > 9:
                pos = 9
            elif pos < 0:
                pos = 0

            self.rating.setMarkerPos(pos)
            self.scale_lh.draw()
            self.description.draw()
            self.rating.draw()
            self.window.flip()

        score = self.rating.getRating()
        rt = self.rating.getRT()
        self.rating.reset()
        return start_trial, score, rt


class instructions(object):
    '''
    show instruction
    '''
    def __init__(self, window, instruction_txt, color):
        self.window = window
        self.instruction_txt = load_instruction(instruction_txt)

        self.display = visual.TextStim(
                window, text='default text', font=sans,
                name='instruction',
                pos=[-50,0], height=48, wrapWidth=1500,
                color=color,
                ) #object to display instructions

    def show(self, duration=None):
        # get instruction
        for i, cur in enumerate(self.instruction_txt):
            self.display.setText(cur)
            self.display.draw()
            self.window.flip()
            if duration:
                core.wait(duration)
            else:
                event.waitKeys(keyList=['1'])


def get_keyboard(timer, respkeylist, keyans):
    '''
    Get key board response
    Args:

        timer : obj
            the timer for the experiment

        respkeylist : list str
            a list of key names you whish to capture

        keyans : list str
            what each key in respkeylist means.
            The length of this list should be the same to respkeylist.
            type check yet to be implimented


    Return:
        KeyResp : str
            the name of the key being pressed

        Resp : str
            what KeyResp actually means

        KeyPressTime : float
            The clock time when the key press occurred
    '''

    Resp = None
    KeyResp = None
    KeyPressTime = np.nan
    keylist = ['escape'] + respkeylist

    for key, time in event.getKeys(keyList=keylist, timeStamped=timer):
        if key in ['escape']:
            core.quit()
        else:
            KeyResp, KeyPressTime = key, time
    # get what the key press means
    if KeyResp:
        Resp = keyans[respkeylist.index(KeyResp)]
    return KeyResp, Resp, KeyPressTime


def subject_info(experiment_info):
    '''
    get subject information
    return a dictionary
    '''
    dlg_title = '{} subject details:'.format(experiment_info['Experiment'])
    infoDlg = gui.DlgFromDict(experiment_info, title=dlg_title)

    experiment_info['Date'] = data.getDateStr()

    file_root = ('_').join([experiment_info['Subject'],
                            experiment_info['Experiment'],
                            experiment_info['Session']
                            ])

    experiment_info['DataFile'] = 'data' + os.path.sep + file_root + '_data_'  + experiment_info['Date'] + '.csv'
    experiment_info['LogFile'] = 'data' + os.path.sep + file_root + '_logs_'  + experiment_info['Date']+ '.log'

    if infoDlg.OK:
        return experiment_info
    else:
        core.quit()
        print('User cancelled')


def event_logger(logging_level, LogFile):
    '''
    log events
    '''
    directory = os.path.dirname(LogFile)
    create_dir(directory)

    logging.console.setLevel(logging.WARNING)
    logging.LogFile(LogFile, level=logging_level)
