#%%
from __future__ import print_function

import numpy as np
import tempfile
import tensorflow as tf

from tf_rl.frontend import pygame_front as frontend
from tf_rl.controller import DiscreteDeepQ, HumanController
from tf_rl.simulation import KarpathyGame
from tf_rl import simulate
from tf_rl.models import MLP
#%%
LOG_DIR = tempfile.mkdtemp()
print(LOG_DIR)
#%%
current_settings = {
    'objects': [
        'friend',
        'enemy',
        'boss',
    ],
    'colors': {
        'hero':   (255, 255, 0),
        'friend': (0, 255, 0),
        'enemy':  (255, 0, 0),
        'boss':   (255, 165, 0),
    },
    'object_reward': {
        'friend': 0.1,
        'enemy': -0.1,
        'boss': -0.5,
    },
    'hero_bounces_off_walls': False,
    'world_size': (640,480),
    'hero_initial_position': [400, 300],
    'hero_initial_speed':    [0,   0],
    "maximum_speed":         [50, 50],
    "object_radius": 10,
    "num_objects": {
        "friend" : 25,
        "enemy" :  25,
        "boss"  :  15,
    },
    "num_observation_lines" : 32,
    "observation_line_length": 120.,
    "tolerable_distance_to_wall": 50,
    "wall_distance_penalty":  -0.0,
    "delta_v": 50
}
#%%
# create the game simulator
scene = frontend.Scene((current_settings['world_size'][0]+20,
 current_settings['world_size'][1]+20))
g = KarpathyGame(scene, current_settings)
#%%
human_control = True

if human_control:
    current_controller = HumanController(scene) 
else:
    # Tensorflow business - it is always good to reset a graph before creating a new controller.
    tf.reset_default_graph()
    session = tf.InteractiveSession()

    # This little guy will let us run tensorboard
    #      tensorboard --logdir [LOG_DIR]
    journalist = tf.train.SummaryWriter(LOG_DIR)

    # Brain maps from observation to Q values for different actions.
    # Here it is a done using a multi layer perceptron with 2 hidden
    # layers
    brain = MLP([g.observation_size,], [200, 200, g.num_actions], 
                [tf.tanh, tf.tanh, tf.identity])
    
    # The optimizer to use. Here we use RMSProp as recommended
    # by the publication
    optimizer = tf.train.RMSPropOptimizer(learning_rate= 0.001, decay=0.9)

    # DiscreteDeepQ object
    current_controller = DiscreteDeepQ((g.observation_size,), g.num_actions, brain, optimizer, session,
                                       discount_rate=0.99, exploration_period=5000, max_experience=10000, 
                                       store_every_nth=4, train_every_nth=4,
                                       summary_writer=journalist)
    
    session.run(tf.initialize_all_variables())
    session.run(current_controller.target_network_update)
    # graph was not available when journalist was created  
    journalist.add_graph(session.graph)
#%%
FPS          = 60
ACTION_EVERY = 1
    
fast_mode = False
if fast_mode:
    WAIT, VISUALIZE_EVERY = False, 50
else:
    WAIT, VISUALIZE_EVERY = True, 1

    
try:
    with tf.device("/cpu:0"):
        simulate(simulation=g,
                 controller=current_controller,
                 fps=FPS,
                 visualize_every=VISUALIZE_EVERY,
                 action_every=ACTION_EVERY,
                 wait=WAIT,
                 disable_training=False,
                 simulation_resolution=0.001,
                 save_path=None)
except KeyboardInterrupt:
    print("Interrupted")