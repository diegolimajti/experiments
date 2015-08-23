# -*- encoding:utf-8 -*- #
import numpy as np
from expyriment import design, control, stimuli, misc, io


"""
This experiment aims to replicate the original study:
Money, E. A., Kirk, R. C., & McNaughton, N. (1992). Alzheimer's
dementia produces a loss of discrimination but no increase in
rate of memory decay in delayed matching to sample.
Neuropsychologia, 30(2), 133-143.

The study employed a match-to-sample task using 
circles of different diameters to study memory
retention over delays of 0, 2, 4, 6, 8, 16 and 32 seconds.

Number of blocks have been changed from 10 to 8
Number of trials per block have been changed from 12 to 14

Instead of using the 'Z' and 'M' keys, participants here
use a touchscreen monitor or the mouse.

Written by Diego Lima https://github.com/diegolimajti
"""


def get_stimuli_diameters():
    """
    In the original study, the comparison stimuli have a difference of 
    approximately 1cm. This method create stimuli with the same size 
    ratios as the original study. E.g. Stimuli 1 = 3.6cm, and is 
    measuring here 280px. Stimuli 2 = 3.8cm and is measuring here
    (280px + 14px), etc.
    """
    
    correct = np.random.randint(1,13)
    incorrect = int()
    
    if np.random.rand() > 0.5:
        incorrect = correct + 5 + np.random.randint(-1,1)
        if incorrect > 13:
            incorrect = correct - 5 + np.random.randint(-1,1)
    else:
        incorrect =  correct - 5 + np.random.randint(-1,1)
        if incorrect < 0:
            incorrect = correct + 5 + np.random.randint(-1,1)

    return 280 + (14 * correct), 280 + (14 * incorrect)


def organize_block():
    """
    Organize a block of trials according to the design of
    Money et. al. (1992)
    """

    #column 1 is a delay, column 2 is wether the correct stimuli will
    #be on left or right (-1 for left, 1 for right)
    order = np.array([[0,-1],[0,1],[2,-1],[2,1],[4,-1],[4,1],[6,-1],
    [6,1],[8,-1],[8,1],[16,-1],[16,1],[32,-1],[32,1]])

    #Verify if position didn't repeated more than twice.
    #If it did, shuffle array again
    repeats = False

    while repeats == False:
        np.random.shuffle(order)
        repeats = True
        for i in range(2, order.shape[0] - 1):
            if (order[i,1] == order[i-1, 1] == order[i-2, 1]):
                repeats = False

    return order


###Initializing experiment###
exp = design.Experiment("Circle diameter DMTS",
background_colour = misc.constants.C_WHITE)
control.initialize(exp)
exp.mouse.show_cursor()

###Define basic structure of the experiment###
for i in np.arange(8):
    block = design.Block(name=str(i+1))
    order = organize_block()

    for j in np.arange(14):
        trial = design.Trial()
        correct, incorrect = get_stimuli_diameters()
        
        #correct can be acessed with trial.stimuli[0],
        #incorrect can be acessed with trial.stimuli[1]
        trial.add_stimulus(stimuli.Circle(diameter = correct))
        trial.add_stimulus(stimuli.Circle(diameter = incorrect))

        trial.set_factor('delay',int(order[j,0]))
        trial.set_factor('position_correct',int(order[j,1]))

        block.add_trial(trial)

    exp.add_block(block)
    
    
#Change to False in the actual experimental session
control.defaults.window_mode = True

blank = stimuli.BlankScreen()

### Starting experiment ###
control.start()

exp.data_variable_names = ['correct_stimulus','incorrect_stimulus',
'correct_position','delay','response','latency']

#A welcome message in portuguese explaining the experimental procedure
welcome = stimuli.TextBox(text = 
u'''Você vai observar a breve apresentação de um círculo no centro da tela.
Depois de um tempo, dois círculos vão aparecer na tela. Sua tarefa é
tocar no círculo igual ao apresentado anteriormente.
Toque nesta mensagem para continuar.''', text_size = 30,
text_colour = (10,10,10), background_colour=(230,230,230),
size=(600,300))

touchbox_welcome = io.TouchScreenButtonBox(button_fields = welcome,
stimuli=[] ,background_stimulus=None)    
touchbox_welcome.show()
touchbox_welcome.wait()

for block in exp.blocks:

    order = organize_block()

    for trial in block.trials:
        #Present sample for 3s
        trial.stimuli[0].present()
        exp.clock.wait(3000)
        
        #Wait delay assigned to this trial
        blank.present()
        exp.clock.wait(trial.get_factor('delay') * 1)

        #Since stimuli[0] is the correct stimuli, if multiplied by
        #position_correct = - 1 it will go to the left, and multiplied by
        #position_correct = 1 it will go to the right. The incorrect
        # stimuli will always go to the opposite side of the
        #correct stimuli if multiplied by -1
        trial.stimuli[0].position = [exp.screen.size[0] * 0.33 *
        trial.get_factor('position_correct'), 0]
        
        trial.stimuli[1].position = [exp.screen.size[0] * 0.33 *
        trial.get_factor('position_correct') * -1, 0]
        
        touchbox_response = io.TouchScreenButtonBox(
        button_fields = [trial.stimuli[0], trial.stimuli[1]],
        stimuli=[] ,background_stimulus=None)
        touchbox_response.show()
        response, rt = touchbox_response.wait()
        
        blank.present()
        exp.clock.wait(2000)

        correct = int()
        if (response == trial.stimuli[0]):
            correct = 1
        else:
            correct = 0

        #The columns of data are organized as follows:
        #Size of the "right" stimuli, size o the "wrong" stimuli,
        #position of the "right" stimuli, delay of the particular
        #trial, correct response (1=yes,0=no), and the reaction 
        #time (since the presentation of the comparisons)
        exp.data.add([trial.stimuli[0].diameter, 
        trial.stimuli[1].diameter, trial.get_factor('position_correct'),
        trial.get_factor('delay'),correct,rt])
        exp.data.save()
    
    if block.name != '8':
        #A message in portuguese informing that the participant can 
        #rest for a little bit.
        rest = stimuli.TextBox(text= u'''Caso queira, você pode descansar
        um pouco. Toque nesta mensagem quando estiver preparado para recomeçar''',
        text_size = 30, text_colour = (10,10,10), 
        background_colour=(230,230,230), size=[600,300])
        
        touchbox_rest = io.TouchScreenButtonBox(button_fields = rest,
        stimuli=[], background_stimulus=None)    
        touchbox_rest.show()
        touchbox_rest.wait()

#A message in portuguese saying thank you to the participant
bye = stimuli.TextBox(text = u'''Obrigado pela sua participação!
Toque na mensagem para sair.''', text_size = 30, 
text_colour = (10,10,10), background_colour=(230,230,230),
size=[600,300])

touchbox_bye = io.TouchScreenButtonBox(button_fields = bye, 
stimuli=[] ,background_stimulus=None)    
touchbox_bye.show()
touchbox_bye.wait()

###End of experiment###
control.end()
