import curses
from random import randint

MAP_WIDTH = 80
MAP_HEIGHT = 30

def init_stars():
    results = [[0 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]
    for x in range(100):
        rx = randint(0, MAP_WIDTH - 1)
        ry = randint(0, MAP_HEIGHT - 1)

        results[ry][rx] = randint(5,10)
    return results

def display_stars(screen, stars, score):
    for y in range(len(stars)):
        for x in range(len(stars[0])):
            color = stars[y][x]
            if color != 0:
                screen.addstr(y, x, ".", curses.color_pair(color))
    screen.addstr(0, 1, "your score is " + str(score))

def limit(foo,limit, bottom=0):
    if foo <= limit and foo >= bottom:
        return foo
    elif foo <= limit and foo <= bottom:
        return bottom
    else:
        return limit

def winit_color(cn, r, g, b):
    nr = limit(r,1000)
    ng = limit(g,1000)
    nb = limit(b,1000)
    curses.init_color(cn, nr, ng, nb)

def init_colors(mod=0):
    # Shades of grey for news
    winit_color(5, 800, 800, 800)
    winit_color(6, 800, 800, 800)
    winit_color(7, 600, 600, 600)
    winit_color(8, 400, 400, 400)
    winit_color(9, 300, 300, 300)
    # News fadeout
    curses.init_pair(6, 6, curses.COLOR_BLACK)
    curses.init_pair(7, 7, curses.COLOR_BLACK)
    curses.init_pair(8, 8, curses.COLOR_BLACK)
    curses.init_pair(9, 9, curses.COLOR_BLACK)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK)  # walls, brown on black
    curses.init_pair(3, 3, curses.COLOR_BLACK)
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    curses.init_pair(5, 5, curses.COLOR_BLACK)


def display_news(screen, news):
    top_news = news[-5:]
    top_news.reverse()
    cn = 0
    for n in top_news:
        screen.addstr(MAP_HEIGHT + cn, 0, " " * MAP_WIDTH, curses.color_pair(5 + cn)),
        screen.addstr(MAP_HEIGHT + cn, 0, n, curses.color_pair(5 + cn))
        cn += 1