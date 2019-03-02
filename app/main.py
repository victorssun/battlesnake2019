import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

#os.path('C:/Users/A/Desktop/K/Projects/battlesnake/snake/app/')
#import snake_functions
import numpy as np
import pandas as pd

# snake joke #battlesnake2019
# player.battlesnake.io: register with name, story, github, 
# how do i know i will respond within 250 ms round trip?
# 0 --> 14
# |
# |
# v
# 14
'''
http://localhost:8080
'''
@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = '#aacbff'
    headtype = 'sand-worm'
    tailtype = 'pixel'

    return start_response(color, headtype, tailtype)

@bottle.post('/move')
def move():
    data = bottle.request.json
    
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

#    data['board']['height'] # bottom
#    data['board']['width'] # right
#    data['you']['health'] # health
#    data['you']['body'][0] # head
#    head = np.array([[0,0,0], [0,1,0], [0,0,0]])

    not_directions = []
    if data['you']['body'][0]['y'] == data['board']['height'] - 1: # if head is at bottom, don't go down
        not_directions.append('down')
    elif data['you']['body'][0]['y'] == 0: # if head is at top, don't go up
        not_directions.append('up')
        
    if data['you']['body'][0]['x'] == data['board']['width'] - 1: # if head is at right, don't go right
        not_directions.append('right')
    elif data['you']['body'][0]['x'] == 0: # if head is at left, don't go left
        not_directions.append('left')
        
    # convert snake to array
    snake = pd.DataFrame(data['you']['body'])
    snake_diff = snake - snake.loc[0]
    snake_diff = snake_diff.isin([-1, 0, 1])

    x = []
    y = []
    for i in range(len(snake_diff)):
        if snake_diff.loc[i].sum() == 2:
            x_temp, y_temp = snake.loc[i]['x'], snake.loc[i]['y']
            x.append(x_temp)
            y.append(y_temp)
#    snake_diff = np.array([x,y])
    
    for j in range(len(data['board']['snakes'])):
        snake_enem = pd.DataFrame(data['board']['snakes'][j]['body'])
        snake_diff = snake_enem - snake.loc[0]
        snake_diff = snake_diff.isin([-1, 0, 1])
    
        for i in range(len(snake_diff)):
            if snake_diff.loc[i].sum() == 2:
                x_temp, y_temp = snake.loc[i]['x'], snake.loc[i]['y']
                x.append(x_temp)
                y.append(y_temp)
        snake_diff = np.array([x,y])
    snake_diff_final = np.array([x, y])
        
    if sum(data['you']['body'][0]['x'] + 1 == snake_diff_final[0]) != 0: # move to right and true then don't move right
        not_directions.append('right')
    elif sum(data['you']['body'][0]['x'] - 1 == snake_diff_final[0]) != 0: # move to left and true then don't move left
        not_directions.append('left')
        
    if sum(data['you']['body'][0]['y'] + 1 == snake_diff_final[1]) != 0: # move to down and true then don't move down
        not_directions.append('down')
    elif sum(data['you']['body'][0]['y'] - 1 == snake_diff_final[1]) != 0: # move to up and true then don't move up
        not_directions.append('up')        

    directions = ['up', 'down', 'left', 'right']
    
    for each in not_directions:
        directions.remove(each)
    
    direction = random.choice(directions)

#    print(ms)
    return move_response(direction)

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    # if being ran directly
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
    
data = bottle.request.json
print 'END'
