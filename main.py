#!/usr/bin/env python3
import pygame
import random
pygame.init()
grid = (50, 50)
player_height = 10
player_width = 10
hud = 100
HEIGHT = grid[1] * player_height + hud
WIDTH = grid[0] * player_width
fps = 10
ded = 0
win = pygame.display.set_mode((WIDTH+ player_width, HEIGHT+ player_height))
pygame.display.set_caption("snake")
clock = pygame.time.Clock()
img = pygame.image.load("image.png").convert()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
font2 = pygame.font.SysFont('Comic Sans MS', 20)

class Snake:
    def __init__(self):
        self.korv_arr = [(2, 3)]
        self.beginlen = 3
        self.dir = "right"
        self.score = 0
        self.namelist = []
        with open("highscore.txt", "r") as f:
            self.scorelist = f.readlines()
            for i, line in enumerate(self.scorelist):
                self.scorelist[i] = line.split("\t")
                self.scorelist[i][0] = int(self.scorelist[i][0])
            self.scorelist.sort(key=lambda x:x[0], reverse=True)
            for i, line in enumerate(self.scorelist):
                self.namelist.append(line[1])

    def checkDie(self):
        global grid
        if self.korv_arr[-1][0] > grid[0] or self.korv_arr[-1][0] < 0:
            self.die()
        if self.korv_arr[-1][1] > grid[1] or self.korv_arr[-1][1] < 0:
            self.die()

        for korv in range(len(self.korv_arr)-2):
            if self.korv_arr[-1] == self.korv_arr[korv]:
                self.die()

    def die(self):
        global ded
        ded = 1

    def checkHighscore(self):
        global ded
        with open("highscore.txt", "r") as f:
            lines = f.readlines()
            scr = []
            for i, line in enumerate(lines):
                lines[i] = line.split("\t")
                scr.append(int(lines[i][0]))

        if ded != 1:
            return
        if len(scr) == 0:
            ded = 2
            return
        if self.score > max(scr):
            ded = 2
            return

    def drawHud(self):
        pygame.draw.rect(win, (40,40,40), pygame.Rect(0, HEIGHT+player_height-hud, WIDTH+player_width, hud))
        for i, names in enumerate(self.namelist):
            if i >= 3:
                break
            self.high_score = font2.render(str(self.scorelist[i][0])+", "+str(self.namelist[i])[:-1], False, (255,255,255))
            win.blit(self.high_score, (WIDTH-200, HEIGHT-90+ i*20))
        self.your_score = font.render("Din poäng: "+ str(self.score), False, (255,255,255))
        win.blit(self.your_score, (20,HEIGHT-70))

    def move(self):
        if self.dir == "right":
            self.korv_arr.append((self.korv_arr[-1][0]+1, self.korv_arr[-1][1]))
        if self.dir == "left":
            self.korv_arr.append((self.korv_arr[-1][0]-1, self.korv_arr[-1][1]))
        if self.dir == "up":
            self.korv_arr.append((self.korv_arr[-1][0], self.korv_arr[-1][1]-1))
        if self.dir == "down":
            self.korv_arr.append((self.korv_arr[-1][0], self.korv_arr[-1][1]+1))
        if len(self.korv_arr) > self.score + self.beginlen:
            del self.korv_arr[0]

    def draw(self):
        global player_width, player_height
        for makaroner in self.korv_arr:
            pygame.draw.rect(win, (255,255,255), pygame.Rect(makaroner[0]*player_width, makaroner[1]*player_height, player_width, player_height))

class Fruit(Snake):
    def __init__(self, snake):
        self.k = snake.korv_arr
        self.pos = (random.randint(0, grid[0]), random.randint(0, grid[1]))

    def spawn(self):
        self.pos = (random.randint(0, grid[0]), random.randint(0, grid[1]))
        for korv in self.k:
            if self.pos == korv:
                self.spawn()

    def det_spawn(self, snake):
        if self.k[-1] == self.pos:
            self.spawn()
            snake.score += 1

    def drawFruit(self):
        pygame.draw.rect(win, (255,255,255), pygame.Rect(self.pos[0]*player_width, self.pos[1]*player_height, player_width, player_height))

def save(score, name):
    with open("highscore.txt", "a") as f:
        f.write(str(score)+"\t"+name+"\n")

def main():
    global ded
    pressed = False
    s = Snake()
    f = Fruit(s)
    running = True
    name = ""
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    ded = False
                    s.__init__()
                    f.__init__(s)
                if event.key == pygame.K_d and s.dir != "left" and not pressed:
                    s.dir = "right"
                    pressed = True
                if event.key == pygame.K_a and s.dir != "right"and not pressed:
                    s.dir = "left"
                    pressed = True
                if event.key == pygame.K_w and s.dir != "down"and not pressed:
                    s.dir = "up"
                    pressed = True
                if event.key == pygame.K_s and s.dir != "up"and not pressed:
                    s.dir = "down"
                    pressed = True
                if ded == 2:
                    if event.key == pygame.K_RETURN:
                        save(s.score, name)
                        ded = 1
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                        continue
                    name += str(pygame.key.name(event.key))

                pressed = False
            if event.type == pygame.QUIT:
                running = False

        if ded == 0:
            win.fill((0,0,0))
            s.move()
            s.draw()
            s.drawHud()
            s.checkDie()
            s.checkHighscore()
            f.det_spawn(s)
            f.drawFruit()
            if name != "":
                name = ""

        if ded == 1:
            s.score_text = font.render("Du fick: "+str(s.score)+" poäng!", False, (255, 255, 255))
            win.blit(img, (-300,0))
            win.blit(s.score_text, (100,100))

        if ded == 2:
            s.score_text = font.render("Du fick: "+str(s.score)+" poäng! Nytt rekord!!!", False, (255, 255, 255))
            win.blit(img, (-300,0))
            win.blit(s.score_text, (20,100))
            s.namn_text = font.render("Skriv ditt namn: "+name, False, (255,255,255))
            win.blit(s.namn_text, (20,130))

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    quit()
main()
