import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)

# Set up display
width, height = 600, 400
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Initialize clock
clock = pygame.time.Clock()

# Game parameters
snake_size = 10
snake_speed = 15

# Set up fonts
message_font = pygame.font.SysFont('ubuntu', 30)
score_font = pygame.font.SysFont('ubuntu', 25)

# Helper functions
def print_score(score):
    """Display the current score at the top of the screen"""
    text = score_font.render(f"Score: {str(score)}", True, orange)
    game_display.blit(text, [0, 0])

def draw_snake(snake_size, snake_pixels):
    """Render the snake body from the list of positions"""
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, white, [pixel[0], pixel[1], snake_size, snake_size])

def display_message(msg, color):
    """Display a message on the screen"""
    text = message_font.render(msg, True, color)
    text_rect = text.get_rect(center=(width/2, height/2))
    game_display.blit(text, text_rect)

# Main game function
def run_game():
    # Game state variables
    game_over = False
    game_close = False
    
    # Initial snake position (center of screen)
    x = width / 2
    y = height / 2
    
    # Initial movement
    x_speed = 0
    y_speed = 0
    
    # Snake body
    snake_pixels = []
    snake_length = 1
    
    # Initial food position
    target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
    target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
    
    # Main game loop
    while not game_over:
        
        # Game over state handling
        while game_close:
            game_display.fill(black)
            display_message("You Lost! Press Q-Quit or C-Play Again", red)
            print_score(snake_length - 1)
            pygame.display.update()
            
            # Wait for player decision
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            # Direction control
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_speed == 0:  # Prevent 180-degree turns
                    x_speed = -snake_size
                    y_speed = 0
                elif event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed = snake_size
                    y_speed = 0
                elif event.key == pygame.K_UP and y_speed == 0:
                    x_speed = 0
                    y_speed = -snake_size
                elif event.key == pygame.K_DOWN and y_speed == 0:
                    x_speed = 0
                    y_speed = snake_size
        
        # Check boundary collision
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True
        
        # Update position
        x += x_speed
        y += y_speed
        
        # Render background
        game_display.fill(black)
        
        # Render food
        pygame.draw.rect(game_display, orange, [target_x, target_y, snake_size, snake_size])
        
        # Update snake pixels
        snake_head = [x, y]
        snake_pixels.append(snake_head)
        
        # Remove tail if not growing
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]
        
        # Check self collision (game over if snake head hits its body)
        for pixel in snake_pixels[:-1]:
            if pixel == snake_head:
                game_close = True
        
        # Draw snake
        draw_snake(snake_size, snake_pixels)
        
        # Update score
        print_score(snake_length - 1)
        
        # Update display
        pygame.display.update()
        
        # Handle food collision
        if round(x) == round(target_x) and round(y) == round(target_y):
            # Generate new food position
            target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
            # Increase snake length
            snake_length += 1
        
        # Control game speed
        clock.tick(snake_speed)
    
    # Quit pygame
    pygame.quit()
    quit()

# Start the game
if __name__ == "__main__":
    run_game() 