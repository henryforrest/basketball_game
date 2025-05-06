import pygame
import math
import sys

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball Shot!")

# Colors
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()

# Gravity
gravity = 0.5

# Fonts
font = pygame.font.SysFont(None, 48)

# Basketball class
class Basketball:
    def __init__(self, x, y, radius=15):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.radius = radius
        self.color = ORANGE
        self.vel_x = 0
        self.vel_y = 0
        self.launched = False

    def launch(self, power, angle):
        self.vel_x = math.cos(angle) * power
        self.vel_y = math.sin(angle) * power
        self.launched = True

    def move(self):
        if self.launched:
            self.vel_y += gravity
            self.x += self.vel_x
            self.y += self.vel_y

            # Bounce on floor
            if self.y + self.radius > HEIGHT - 50:
                self.y = HEIGHT - 50 - self.radius
                self.vel_y *= -0.7
                self.vel_x *= 0.8

            # Roll
            if abs(self.vel_y) < 1 and self.y + self.radius >= HEIGHT - 50:
                self.vel_y = 0
                if self.vel_x > 0:
                    self.vel_x -= 0.2
                    if self.vel_x < 0:
                        self.vel_x = 0
                elif self.vel_x < 0:
                    self.vel_x += 0.2
                    if self.vel_x > 0:
                        self.vel_x = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vel_x = 0
        self.vel_y = 0
        self.launched = False

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

# Hoop class
class Hoop:
    def __init__(self, x, y):
        self.backboard = pygame.Rect(x, y, 10, 100)
        self.rim = pygame.Rect(x - 50, y + 50, 60, 10)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.backboard)
        pygame.draw.rect(screen, RED, self.rim)

    def check_score(self, ball):
        # Check if ball goes *through* rim
        if self.rim.colliderect(ball.get_rect()) and ball.vel_y > 0:
            return True
        return False

# Game Variables
basketball = Basketball(150, HEIGHT - 100)
hoop = Hoop(650, 200)

score = 0
start_pos = None
end_pos = None

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw ground
    pygame.draw.rect(screen, BROWN, (0, HEIGHT-50, WIDTH, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = pygame.mouse.get_pos()
            if start_pos and end_pos:
                dx = start_pos[0] - end_pos[0]
                dy = start_pos[1] - end_pos[1]
                angle = math.atan2(dy, dx)
                power = math.hypot(dx, dy) * 0.2
                basketball.launch(power, angle)
                start_pos = None
                end_pos = None

    # Draw aiming line if dragging
    if start_pos:
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, BLACK, start_pos, current_pos, 3)

    basketball.move()

    if hoop.check_score(basketball):
        score += 2
        basketball.reset()

    basketball.draw(screen)
    hoop.draw(screen)

    # Display Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 200, 30))

    pygame.display.flip()
    clock.tick(60)
