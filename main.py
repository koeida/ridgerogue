import curses
import display
from display import init_colors, display_news, display_stars, init_stars
from news import news
from random import randint
from itertools import combinations, permutations

score = 0


class Ship:
    pass

def keyboard_input(inp, player, ships):
    oldx = player.x
    oldy = player.y
    if inp == curses.KEY_DOWN:
        player.y = player.y + 1
    elif inp == curses.KEY_UP:
        player.y = player.y - 1
    elif inp == curses.KEY_LEFT:
        player.x = player.x - 1
    elif inp == curses.KEY_RIGHT:
        player.x = player.x + 1
    elif inp == ord('l') and player.laser_num != 0:
        player.laser_num -= 1
        l1 = Ship()
        l1.x = player.x
        l1.y = player.y
        l1.image = ["!"]
        l1.type = "laser"
        l1.dead = False
        l1.color = 1
        l2 = Ship()
        l2.x = player.x + 4
        l2.y = player.y
        l2.image = ["!"]
        l2.type = "laser"
        l2.dead = False
        l2.color = 1
        ships.append(l1)
        ships.append(l2)

    if  ((player.x + len(player.image[0]) > display.MAP_WIDTH) or
        (player.x < 0) or
        (player.y + len(player.image) - 1 == display.MAP_HEIGHT)):
        player.x = oldx
        player.y = oldy

def new_meteor():
    meteor = Ship()
    meteor.x = randint(0, display.MAP_WIDTH)
    meteor.y = 0
    meteor.color = 4
    meteor.dead = False
    meteor.type = "meteor"
    meteor.image = ["#"]
    return meteor

def new_UFO():
    UFO = Ship()
    UFO.x = randint(0, display.MAP_WIDTH)
    UFO.y = 0
    UFO.color = 2
    UFO.dead = False
    UFO.type = "UFO"
    UFO.image = ["0"]
    return UFO

def move_ufo(s,player, ships):
    global score
    if randint(1, 2) == 2:
        if player.y > s.y:
            s.y += 1
        if player.x > s.x:
            s.x += 1
        if player.x < s.x:
            s.x -= 1

    for s2 in ships:
        if s2.type == "laser" and is_colliding(s, s2):
            score += 2
            s.dead = True
            s2.dead = True
        if s2.type == "meteor" and is_colliding(s, s2):
            s.dead = True
            s2.dead = True
    if randint(1, 3) == 2:
        ul = Ship()
        ul.x = s.x
        ul.y = s.y + 1
        ul.image = ["|"]
        ul.type = "UFO laser"
        ul.dead = False
        ul.color = 3
        ships.append(ul)


def draw_ship(screen, img, x, y, color):
    ymod = 0
    for line in img:
        screen.addstr(y + ymod, x, line, curses.color_pair(color))
        ymod += 1

def display_screen(player, score, screen, ships, stars):
    display_stars(screen, stars, score)
    for s in ships:
        draw_ship(screen, s.image, s.x, s.y, s.color)
    # player display code
    if player.dead:
        p_width = len(player.image[0])
        middle_x = int((player.x + (player.x + p_width)) / 2)
        screen.addstr(player.y, middle_x, "O", curses.color_pair(1))
    display_news(screen, news)
    screen.addstr(1, 1, "power: " + ("!" * player.laser_num), curses.color_pair(1))
    screen.refresh()


def is_colliding(s1,s2):
    def check(m,p):
        p_width = len(p.image[0])
        p_height = len(p.image)

        if m.x >= p.x and m.x < p.x + p_width:
            if m.y >= p.y and m.y < p.y + p_height:
                return True

        if m.type == "laser" and m.x == p.x and m.y == p.y - 1:
            return True

        return False
    return check(s1,s2) or check(s2,s1)

def move_enemies(ships, player):
    for s in ships:
        if s.type == "meteor":
            s.y = s.y + 1
        elif s.type == "laser":
            s.y = s.y - 1
        elif s.type == "UFO":
            move_ufo(s, player, ships)
        elif s.type == "UFO laser":
            s.y += 1

def update_world(player, ships):
    move_enemies(ships, player)
    check_collisions(ships)
    for s in ships:
        if s.y >= display.MAP_HEIGHT:
            s.dead = True
        if s.y < 0:
            s.dead = True
    ships = filter(lambda s: s.dead != True, ships)
    return ships

def check_collisions(ships):
    global score

    ship_pairs = permutations(ships, 2)
    colliding_ships = filter(lambda pair: is_colliding(pair[0], pair[1]), ship_pairs)

    for s1, s2 in colliding_ships:
        types = (s1.type, s2.type)
        if types == ("laser", "meteor"):
            score += 1
            s1.dead = True
            s2.dead = True
        elif types == ("player", "UFO laser"):
            s1.dead = True
            s2.dead = True
        elif types == ("player", "meteor"):
            news.append("KABOOM! You died so hard...")
            s1.dead = True

def make_player():
    player = Ship()
    player.x = display.MAP_WIDTH / 2
    player.y = display.MAP_HEIGHT / 2
    player.dead = False
    player.type = "player"
    player.color = 0
    player.laser_num = 5
    player.image = [
        ' /@\\ ',
        '|<X>|',
        '  ^ '
    ]
    return player

def main(screen):
    global score

    curses.curs_set(False)  # Disable blinking cursor
    init_colors()

    stars = init_stars()
    player = make_player()
    ships = [player]
    for x in range(10):
        ships.append(new_meteor())

    inp = 0
    laser_timer = 3
    KEY_Q = 113

    news.append("WELCOME TO SPACE ATTACK!!!!")

    while (inp != KEY_Q):  # Quit game if player presses "q"
        screen.clear()

        #TIMERS
        laser_timer -= 1
        if laser_timer == 0:
            if player.laser_num <= 10:
                player.laser_num += 1
            laser_timer = 3

        #NEW ENEMIES
        for x in range(5):
            ships.append(new_meteor())
        for x in range(1):
            ships.append(new_UFO())

        #PLAYER INPUT
        if player.dead == False:
            keyboard_input(inp, player, ships)

        #MOVE ENEMIES/CHECK COLLISIONS/ETC
        ships = update_world(player, ships)

        #OUTPUT
        display_screen(player, score, screen, ships, stars)

        #GET KEYBOARD INPUT/END TURN
        inp = screen.getch()


curses.wrapper(main)