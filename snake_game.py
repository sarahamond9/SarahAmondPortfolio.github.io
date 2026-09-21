#Sarah Amond
import pygame
import random
import sys

# Initialize Pygame
pygame.init()
# Game Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10
# Colors (RGB)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_SNAKE = (46, 204, 113)
COLOR_FOOD = (231, 76, 60)
COLOR_TEXT = (255, 255, 255)
# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Classic Snake Arcade")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.reset_game()
    def reset_game(self):
        # Start in the middle of the screen
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.spawn_food()
        self.game_over = False
    def spawn_food(self):
        while True:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            # Ensure food doesn't spawn inside the snake's body
            if self.food not in self.snake:
                break
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    # Prevent the snake from reversing directly into itself
                    #CONTROLS FOR THE GAME 
                    if event.key == pygame.K_UP and self.direction != DOWN:
                        self.direction = UP
                    elif event.key == pygame.K_DOWN and self.direction != UP:
                        self.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                        self.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                        self.direction = RIGHT

    def update(self):
        if self.game_over:
            return

        # Calculate new head position
        cur_head = self.snake[0]
        dx, dy = self.direction
        new_head = (cur_head[0] + dx, cur_head[1] + dy)

        # Collision Check: Walls
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return

        # Collision Check: Self
        if new_head in self.snake:
            self.game_over = True
            return

        # Move snake by inserting the new head location
        self.snake.insert(0, new_head)

        # Collision Check: Food
        if new_head == self.food:
            self.score += 10
            self.spawn_food()
        else:
            # Remove the tail segment if no food was eaten
            self.snake.pop()

    def draw(self):
        self.screen.fill(COLOR_BACKGROUND)

        # Draw Snake
        for segment in self.snake:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(self.screen, COLOR_SNAKE, rect)

        # Draw Food
        food_rect = pygame.Rect(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(self.screen, COLOR_FOOD, food_rect)

        # Draw Score
        score_surface = self.font.render(f"Score: {self.score}", True, COLOR_TEXT)
        self.screen.blit(score_surface, (10, 10))

        # Game Over Screen Overlay
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            go_surface = self.font.render("GAME OVER", True, COLOR_FOOD)
            restart_surface = self.font.render("Press SPACE to Restart or ESC to Quit", True, COLOR_TEXT)
            
            self.screen.blit(go_surface, (WIDTH // 2 - go_surface.get_width() // 2, HEIGHT // 2 - 40))
            self.screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
