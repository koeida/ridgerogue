import curses
import display
from display import init_colors, display_news, display_stars, init_stars
from news import news
from random import randint, choice
from itertools import combinations, permutations

score = 0


class Ship:
    pass

def first(f,l):
    for x in l:
        if f(x):
            return x
    return None


def make_explosions(ships,bomb):
    cmods = [(-1,-1), (0,-1), (1,-1),
             (-1, 0), (0, 0), (1, 0),
             (-1, 1), (0, 1), (1, 1)]
    for cm in cmods:
        bx = bomb.x
        by = bomb.y
        mx = cm[0]
        my = cm[1]
        ex = bx + mx
        ey = by + my
        e = make_explosion(ex,ey)
        ships.append (e)


def make_explosion(x,y):
    explosion = Ship()
    explosion.x = x
    explosion.y = y
    explosion.color = choice([1, 3])
    explosion.dead = False
    explosion.type = "explosion"
    img = choice("0oO")
    explosion.image = [img]
    return explosion


def create_shield(x, y):
    shield = Ship()
    shield.x = x
    shield.y = y
    shield.color = 4
    shield.dead = False
    shield.type = "shield"
    img = ["_____"]
    shield.image = img
    return shield
    


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
    elif inp == ord('b') and player.energy_num >= 2:
        b = make_bomb(player.x +2, player.y)
        ships.insert(0,b)
        player.energy_num -= 2
    elif inp == ord('d'):
        bomb = first(lambda s: s.type == "bomb", ships)
        if bomb != None:
            ships.remove(bomb)
            make_explosions(ships, bomb)
    elif inp == ord('s'):
        shield = first(lambda s: s.type == "shield", ships)
        if shield != None:
            ships.remove(shield)
        else:
            shield = create_shield(player.x + 1, player.y - 1)
            ships.insert(0,shield)
            news.append("shield made")
    elif inp == ord('l') and player.energy_num != 0:
        player.energy_num -= 1
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
        ships.insert(0,l1)
        ships.insert(0,l2)

    if  ((player.x + len(player.image[0]) > display.MAP_WIDTH) or
        (player.x < 0) or
        (player.y + len(player.image) - 1 == display.MAP_HEIGHT)):
        player.x = oldx
        player.y = oldy
        
def new_item(x,y):
    item = Ship()
    item.x = x
    item.y = y
    item.color = 0
    item.dead = False
    item.type = "item"
    item.image = ["|"]
    item.animation = "|/-\\"
    item.frame = 0
    return item


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
    screen.addstr(1, 1, "power: " + ("!" * player.energy_num), curses.color_pair(1))
    screen.refresh()


def is_colliding(s1,s2):
    def check(m,p):
        p_width = len(p.image[0])
        p_height = len(p.image)

        if m.x >= p.x and m.x < p.x + p_width:
            if m.y >= p.y and m.y < p.y + p_height:
                return True

        #if m.type == "laser" and m.x == p.x and m.y == p.y - 1:
        #    return True

        return False
    return check(s1,s2) or check(s2,s1)

def move_ship(s, ships, player):
    if s.type == "meteor":
        s.y = s.y + 1
    elif s.type == "laser":
        s.y = s.y - 1
    elif s.type == "UFO":
        move_ufo(s, player, ships)
    elif s.type == "UFO laser":
        s.y += 1
    elif s.type == "bomb":
        s.y -= 1
    elif s.type == "shield":
        s.y = player.y - 1
        s.x = player.x


def make_bomb(x, y):
    bomb = Ship()
    bomb.x = x
    bomb.y = y
    bomb.color = 4
    bomb.dead = False
    bomb.type = "bomb"
    bomb.image = ["o"]
    return bomb

def update_world(player, ships):
    # Filter ship list to get items only
    animate_items(ships)
    for s in ships:
        move_ship(s, ships, player)
        check_collisions(s, ships)

    ships = filter(lambda s: s.y <= display.MAP_HEIGHT and s.y >= 0, ships)
    return ships

def saferemove(i,l):
    if i in l:
        l.remove(i)

def check_collisions(s1, ships):
    global score

    colliding_ships = filter(lambda sb: s1 != sb and is_colliding(s1, sb), ships)


    for s2 in colliding_ships:
        types = (s1.type, s2.type)
        if set(types) == set(["laser", "meteor"]) :
            score += 1
            saferemove(s1, ships)
            saferemove(s2, ships)
        elif set(types) == set(["meteor","meteor"]):
            saferemove(s1, ships)
            saferemove(s2, ships)
        elif set(types) == set(["player", "UFO laser"]):
            saferemove(s1, ships)
            saferemove(s2, ships)
        elif set(types) == set(["player", "meteor"]):
            news.append("KABOOM! You died so hard...")
            saferemove(s1, ships)
            saferemove(s2, ships)
        elif set(types) == set(["laser","UFO"]):
            score += 2
            saferemove(s1, ships)
            saferemove(s2, ships)
            ships.append(new_item(s1.x, s1.y))
        elif types == ("item","player"):
            score += 9999999999
            saferemove(s1, ships)
        elif s1.type == "explosion":
            saferemove(s2, ships)
        elif s2.type == "explosion":
            saferemove(s1, ships)
        elif s1.type == "shield":
            news.append("shield collide")
            saferemove(s2, ships)
        elif s2.type == "shield":
            news.append("shield collide")
            saferemove(s1, ships)


def make_player():
    player = Ship()
    player.x = display.MAP_WIDTH / 2
    player.y = display.MAP_HEIGHT / 2
    player.dead = False
    player.type = "player"
    player.color = 0
    player.energy_num = 5
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

    news.append("WELCOME TO SPACE ATTACK!!!")

    while (inp != KEY_Q):  # Quit game if player presses "q"
        screen.clear()

        #TIMERS
        laser_timer -= 1
        if laser_timer == 0:
            if player.energy_num <= 10:
                player.energy_num += 1
            laser_timer = 3

        # Filter ships list to only include non-explosions
        ships = filter(lambda s:s.type != "explosion", ships)

        #NEW ENEMIES

        for x in range(3):
            ships.append(new_meteor())
        for x in range(randint(0, 1)):
            ships.append(new_UFO())


        #PLAYER INPUT
        if player in ships:
            keyboard_input(inp, player, ships)

        # If there a shield on
        #   remove some power



        #MOVE ENEMIES/CHECK COLLISIONS/ETC...
        ships = update_world(player, ships)
        
        shield = first(lambda s: s.type == "shield", ships)
        if shield != None:
            player.energy_num -= 2
        if player.energy_num <= 0 and shield != None:
            ships.remove(shield)
        if player not in ships and shield != None:
            ships.remove(shield)

        #OUTPUT
        display_screen(player, score, screen, ships, stars)

        #GET KEYBOARD INPUT/END TURN
        inp = screen.getch()


def animate_items(ships):
    items = filter(lambda s: s.type == "item", ships)
    # Loop over items
    for i in items:
        # Increase frame by one
        i.frame += 1
        # If the frame value is higher than the max animation index, reset it to 0
        if i.frame > 3:
            i.frame = 0
        # Change image to be the character in the animation string at that frame
        i.image = i.animation[i.frame]


curses.wrapper(main)