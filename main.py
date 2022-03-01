import pygame
import random
pygame.init()
pygame.font.init()
WIDTH = 480
HEIGHT = 570
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("TETRIS")
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
my_font = pygame.font.SysFont("comicsans",20)
over_font = pygame.font.SysFont("arial",25)
timer = pygame.time.Clock()
FPS = 30
TILE_SIZE = 30
colors = [
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Figure:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0,len(self.figures)-1)
        self.color = colors[random.randint(0,len(colors)-1)]
        self.rotation = 0
        self.disabled = False
    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

class Grid:
    def __init__(self):
        self.grid = []
        self.figure = None
        self.lost = False
        self.pressed = False
        for i in range(HEIGHT//TILE_SIZE):
            self.grid.append(WIDTH//TILE_SIZE*[0])

    def new_figure(self):
        self.figure = Figure(random.randint(3,6),0)
        if self.intersection(self.figure.x,self.figure.y):
            self.lost = True
            for p in self.figure.image():
                row = self.figure.y + p//4
                col = self.figure.x + p%4
                self.grid[row][col] = self.figure.color
    def check_grid(self):
        global score
        r = len(self.grid)-1
        for row in reversed(range(len(self.grid))):
            is_filled = True
            for col in range(len(self.grid[row])):
                if self.grid[row][col]==0:
                    is_filled=False
            if is_filled:
                score+=5
                for col in range(len(self.grid[row])):
                    self.grid[row][col] = 0
                for row in (range(r,1,-1)):
                    for col in range(len(self.grid[row])):
                        self.grid[row][col]=0
                        self.grid[row][col]=self.grid[row-1][col]
            r-=1

    def intersection(self,x,y):
       for p in self.figure.image():
           row = y + p // 4
           col = x + p % 4
           if TILE_SIZE+col*TILE_SIZE<=0 or TILE_SIZE + col * TILE_SIZE > WIDTH or TILE_SIZE + row * TILE_SIZE>=HEIGHT or self.grid[row][col]!=0:
               if TILE_SIZE + row * TILE_SIZE>=HEIGHT:
                   self.figure.disabled=True
               return True
       return False

    def right(self):
        if self.intersection(self.figure.x+1,self.figure.y)==False:
            self.figure.x += 1

    def left(self):
        if self.intersection(self.figure.x - 1, self.figure.y) == False:
            self.figure.x -= 1

    def down(self):
        if self.intersection(self.figure.x , self.figure.y+1) == False:
            self.figure.y += 1
        else:
            for p in self.figure.image():
                row = self.figure.y + p//4
                col = self.figure.x + p%4
                self.grid[row][col]=self.figure.color
            self.figure = None
            self.new_figure()

    def rotate(self):
        self.figure.rotate()
        l = 0
        while self.intersection(self.figure.x,self.figure.y) == True and l<=8:
            self.figure.rotate()
            l+=1


    def draw_grid(self,screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col]!=0:
                    pygame.draw.rect(screen, self.grid[row][col], (col * TILE_SIZE, TILE_SIZE * (row + 1), TILE_SIZE, TILE_SIZE))

    def fall(self):
        if self.pressed:
            while self.intersection(self.figure.x, self.figure.y + 1) == False:
                self.figure.y += 1
            self.pressed = False
            self.figure.disabled = True
def draw_screen(screen,score,game_state):
    text = my_font.render(f'Score : {score}',1,RED)
    screen.blit(text,(WIDTH/2-text.get_width()/2,5))
    #we will draw horizontal and vertical lines

    for y in range(30,HEIGHT,TILE_SIZE):
        for x in range(0,WIDTH,TILE_SIZE):
            pygame.draw.line(screen,BLACK,(x,TILE_SIZE),(x,HEIGHT))
        pygame.draw.line(screen,BLACK,(0,y),(WIDTH,y))

    if game_state == False:
        over = over_font.render("YOU HAVE LOST,PRESS ENTER TO RESTART",1,RED)
        screen.blit(over,(WIDTH//2-over.get_width()/2,HEIGHT//2-20))
def main():
    global score
    run = True
    score = 0
    pressing_down = False
    game_state = True
    g = Grid()
    counter = 0
    g.new_figure()
    while run:
        if g.lost == True:
            game_state = False
        counter += 1
        if counter > 2500:
            counter = 0

        if counter % (5) == 0 or pressing_down:
            if game_state == True:
                g.down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and g.figure.disabled == False:
                if event.key == pygame.K_UP:
                    g.rotate()
                if event.key == pygame.K_LEFT:
                    g.left()
                if event.key == pygame.K_RIGHT:
                    g.right()
                if event.key == pygame.K_SPACE:
                    g.pressed = True
                    g.fall()
            if event.type==pygame.KEYDOWN:
                if game_state == False and event.key == pygame.K_RETURN:
                    main()

        screen.fill(WHITE)
        if game_state == True:
            if g.figure.image()!=None:
                for p in g.figure.image():
                    row = g.figure.y+p//4
                    col = g.figure.x+p%4
                    pygame.draw.rect(screen,g.figure.color,(col*TILE_SIZE,TILE_SIZE*(row+1),TILE_SIZE,TILE_SIZE))
        g.check_grid()
        g.draw_grid(screen)
        draw_screen(screen, score,game_state)
        pygame.display.update()
        timer.tick(FPS)
main()
