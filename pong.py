# import dependencies
import pygame

# initialize pygame
pygame.init()


# create the game window
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong by LJD0")

FPS = 60


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCORE_FONT = pygame.font.SysFont("comicsans", 60)

WINNING_SCORE = 10

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 15

# define the game objects
class Ball:
    MAX_VEL = 10

    def __init__(self, x, y, radius):
        self.x = self.ORIGINAL_X = x
        self.y = self.ORIGINAL_Y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.ORIGINAL_X
        self.y = self.ORIGINAL_Y
        self.x_vel *= -1
        self.y_vel = 0


class Paddle:
    # define the paddle constants
    COLOR = WHITE
    VEL = 8

    def __init__(self, x, y, width, height):
        self.x = self.ORIGINAL_X = x
        self.y = self.ORIGINAL_Y = y
        self.width = width
        self.height= height
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    # define the paddle movement
    def move(self, up=True):
        if up:
            self.y -= self.VEL 
        else:
            self.y += self.VEL
    def reset(self):
        self.x = self.ORIGINAL_X
        self.y = self.ORIGINAL_Y

# define the game functions

def draw (win, paddles, ball, left_score, right_score):
    # draw the game window
    win.fill(BLACK)

    # draw the scores
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH *(3/4) - right_score_text.get_width()//2, 20))
    # draw the paddles
    for padd in paddles:
        padd.draw(win)

    # draw a dotted line in the middle of the screen
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2-10,i, 20, HEIGHT//20))

    # draw the ball
    ball.draw(win)

    pygame.display.update()


def move_paddles(keys, left_pad, right_pad):
    if keys[pygame.K_w] and (left_pad.y - left_pad.VEL >= 0):
        left_pad.move(up=True)
    if keys[pygame.K_s] and (left_pad.y + left_pad.height + left_pad.VEL <= HEIGHT):
        left_pad.move(up=False)
    if keys[pygame.K_UP] and (right_pad.y - right_pad.VEL >= 0):
        right_pad.move(up=True)
    if keys[pygame.K_DOWN] and (right_pad.y + right_pad.height + right_pad.VEL <= HEIGHT):
        right_pad.move(up=False)

# define collision functions
def paddle_collision(ball, left, right):
    # define up/down collisions
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y -ball.radius <=0:
        ball.y_vel *= -1
    # define left/right collisions
    if ball.x_vel <0:
        if ball.y >= left.y and ball.y <= left.y +left.height:
            if ball.x - ball.radius <= left.x + left.width:
                ball.x_vel *= -1

                middle_y = left.y + left.height//2
                y_diff = middle_y - ball.y
                reduction = (left.height/2)/ball.MAX_VEL
                y_vel = y_diff/reduction
                ball.y_vel = y_vel * -1
    else:
        if ball.y >= right.y and ball.y <= right.y +right.height:
            if ball.x + ball.radius >= right.x:
                ball.x_vel *= -1

                middle_y = right.y + right.height//2
                y_diff = middle_y - ball.y
                reduction = (right.height/2)/ball.MAX_VEL
                y_vel = y_diff/reduction
                ball.y_vel = y_vel * -1


# define main game loop
def main():
    run = True
    clock = pygame.time.Clock()

    # create the game objects
    left_paddle = Paddle(10,  HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH,  HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    # set scores
    left_score = 0
    right_score = 0


    while run:
        # set the FPS
        clock.tick(FPS)
        draw(
            WIN, 
            [left_paddle, right_paddle], 
            ball, 
            left_score, 
            right_score
            )

        # check for events in the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # check for key presses
        keys = pygame.key.get_pressed()
        move_paddles(keys, left_paddle, right_paddle)
        ball.move()
        paddle_collision(ball, left_paddle, right_paddle)

        if ball.x <0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        WON = False
        if left_score >= WINNING_SCORE:
            WON = True
            win_text ="LEFT PLAYER WON"
        elif right_score >= WINNING_SCORE:
            WON = True
            win_text = "RIGHT PLAYER WON"

        if WON:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

if __name__ == "__main__":
    main()
# close the game
