"""
The objective of this experiment is to calculate the interhemispheric
transmission time (IHTT) based on the difference of reation time between
the hand whose motor cortex is ipsilateral or contralateral to the visual
cortex of the eye receiving the stimulus. The procedure here is loosely
based on the set of studies described in Bashore (1981)

References
Bashore, T. R. (1981). Vocal and manual reaction time estimates of
interhemispheric transmission time. Psychological Bulletin, 89(2), 352.

Written by Diego Lima https://github.com/diegolimajti
"""

from expyriment import design, misc, control, io, stimuli
import random

exp = design.Experiment('interhemispheric reaction time',
background_colour = misc.constants.C_BLACK)

###Initializing experiment###
control.set_develop_mode(True)
control.defaults.fast_quit = True
control.initialize(exp)
exp.keyboard.set_quit_key(misc.constants.K_ESCAPE)

#Define messages
welcome = """Bem vindo ao experimento. Instrucoes: O programa pedira que voce mantenha o dedo indicador
de uma das maos repousado sobre a tecla B sem aperta-la. Mantenha seu olhar sempre dirigido para a regiao
central da tela, indicada por uma cruz branca. Nao desvie o olhar dessa posicao durante a apresentacao dos estimulos.
Quando notar um circulo branco, pressione a tecla B uma vez, e aguarde o aparecimento dos proximos
estimulos ou das proximas instrucoes"""

block_left_msg = """Mantenha o dedo indicador da sua mao ESQUERDA repousando sobre a tecla B sem aperta-la.
So aperte ela uma vez, o mais rapido possivel, sempre que notar um circulo branco. Pressione a tecla B uma vez agora
para comecar a apresentacao dos proximos estimulos."""

block_right_msg = """Mantenha o dedo indicador da sua mao DIREITA repousando sobre a tecla B sem aperta-la.
So aperte ela uma vez, o mais rapido possivel, sempre que notar um circulo branco. Pressione a tecla B uma vez agora
para comecar a apresentacao dos proximos estimulos."""


###Define structure of the experiment###
stim_cross = stimuli.FixCross(size = [30, 30], colour = misc.constants.C_WHITE)
circle = stimuli.Circle(radius = 50, colour = misc.constants.C_WHITE)
text_welcome = stimuli.TextBox(text = welcome, size = (600, 400), text_colour = misc.constants.C_WHITE)
text_block_left = stimuli.TextBox(text = block_left_msg, size = (600, 400), text_colour = misc.constants.C_WHITE)
text_block_right = stimuli.TextBox(text = block_right_msg, size = (600, 400), text_colour = misc.constants.C_WHITE)
blank = stimuli.BlankScreen()
stim_cross.preload()
circle.preload()
text_welcome.preload()
text_block_left.preload()
text_block_right.preload()

trial = design.Trial()
trial.add_stimulus(circle)

#LC - Left contralateral; LI - Left ipsilateral; RC - Right contralateral; RI - Right ipsilateral
factor_values = ['LC', 'LI', 'RC', 'RI']

for fv in factor_values:
    block = design.Block()
    block.set_factor('type', fv)
    block.add_trial(trial, copies = 10)
    exp.add_block(block, copies = 5)

    exp.shuffle_blocks()


###Start experiment###
control.start()

exp.data_variable_names = ['type_block','rt']

text_welcome.present()
exp.keyboard.wait()

for block in exp.blocks:

    if(block.get_factor('type') == 'LI'):
        circle.position = ( - exp.screen.window_size[0] * 0.4, 0)
        text_block_left.present()
        exp.keyboard.wait()
    elif(block.get_factor('type') == 'LC'):
        circle.position = (- exp.screen.window_size[0] * 0.4, 0)
        text_block_right.present()
        exp.keyboard.wait()
    elif(block.get_factor('type') == 'RI'):
        circle.position = (exp.screen.window_size[0] * 0.4, 0)
        text_block_right.present()
        exp.keyboard.wait()
    elif(block.get_factor('type') == 'RC'):
        circle.position = (exp.screen.window_size[0] * 0.4, 0)
        text_block_left.present()
        exp.keyboard.wait()
        
    for trial in block.trials:
        #Variable cross presentation time between 1-3 sec
        stim_cross.present()
        exp.clock.wait(1000 + random.random() * 2000)
        
        #Present circle
        circle.present()
        
        #Collect and save reponse
        key, rt = exp.keyboard.wait(misc.constants.K_b, duration = 500)
        exp.data.add([block.get_factor('type'), rt])
        exp.data.save()
        
        #Wait 3 sec to next trial
        blank.present()
        exp.clock.wait(3000)
        
        
control.end()
