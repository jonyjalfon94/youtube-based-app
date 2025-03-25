# Snake Game Implementation Plan

## Overview
This document outlines the step-by-step implementation plan for creating a Snake game using Pygame, based on the tutorial video from NeuralNine.

## Prerequisites
- Python installed on your system
- Basic understanding of Python syntax
- Pygame library installed (`pip install pygame`)

## Project Structure
```
snake_game/
│
├── snake_game.py    # Main game file
└── README.md        # Project documentation
```

## Implementation Steps

### 1. Setting Up the Environment
- Import necessary libraries:
  - Pygame for game development
  - Time for controlling game speed
  - Random for generating food positions
- Initialize Pygame
- Set up the game window:
  - Define screen dimensions (600x400 pixels)
  - Create the game display
  - Set the window caption
  - Initialize the clock for controlling frame rate

### 2. Define Game Constants and Variables
- Colors (RGB values):
  - White (255, 255, 255) - Snake color
  - Black (0, 0, 0) - Background color
  - Red (255, 0, 0) - Game over message
  - Orange (255, 165, 0) - Food and score color
- Game parameters:
  - Snake size (10 pixels)
  - Snake speed (15 frames per second)
- Fonts for score display and messages:
  - Message font (Ubuntu, 30pt)
  - Score font (Ubuntu, 25pt)
- Initial game state:
  - Snake position (center of screen)
  - Snake direction (initially stationary)
  - Snake length (1 segment)
  - Food position (random)
  - Game state flags (game_over, game_close)

### 3. Create Helper Functions
- `print_score(score)`: Displays the current score at the top of the screen
- `draw_snake(snake_size, snake_pixels)`: Renders the snake body from the list of positions
- `run_game()`: Main game loop function

### 4. Main Game Loop Implementation
1. Initialize game variables
2. Start the main game loop (runs while game is not over)
3. Event handling:
   - Process window close events
   - Handle keyboard input for snake direction (arrow keys)
4. Movement and collision detection:
   - Update snake position based on current direction
   - Check for boundary collisions (walls)
   - Check for self-collisions (snake hitting itself)
5. Food interaction:
   - Detect if snake eats food
   - Increase snake length
   - Generate new food at random position
6. Rendering:
   - Fill background with black
   - Draw food
   - Draw snake
   - Display score
   - Update display
7. Game over conditions:
   - Display game over message when applicable
   - Option to restart or quit
8. Control game speed using the clock

### 5. Detailed Game Logic

#### Snake Movement
- Store snake body as a list of pixel coordinates
- Add new head position to the list based on current direction
- Remove the tail (first element) to create movement effect
- Keep tail when food is eaten to make the snake grow

#### Food Generation
- Use random coordinates within the game boundaries
- Round to nearest 10 to align with snake grid
- Regenerate when eaten by the snake

#### Collision Detection
- Wall collision: Check if snake head coordinates are outside screen boundaries
- Self collision: Check if head position matches any existing body segment

## Code Implementation

### Basic Structure
```python
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
    text = score_font.render(f"Score: {str(score)}", True, orange)
    game_display.blit(text, [0, 0])

def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, white, [pixel[0], pixel[1], snake_size, snake_size])

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
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            
            # Direction control
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -snake_size
                    y_speed = 0
                elif event.key == pygame.K_RIGHT:
                    x_speed = snake_size
                    y_speed = 0
                elif event.key == pygame.K_UP:
                    x_speed = 0
                    y_speed = -snake_size
                elif event.key == pygame.K_DOWN:
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
        snake_pixels.append([x, y])
        
        # Remove tail if not growing
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]
        
        # Check self collision
        for pixel in snake_pixels[:-1]:
            if pixel == [x, y]:
                game_close = True
        
        # Draw snake
        draw_snake(snake_size, snake_pixels)
        
        # Update score
        print_score(snake_length - 1)
        
        # Update display
        pygame.display.update()
        
        # Handle food collision
        if x == target_x and y == target_y:
            target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
            snake_length += 1
        
        # Game over message
        if game_close:
            game_display.blit(message_font.render("You Lost! Press Q to Quit or C to Play Again", True, red), [width/6, height/3])
            pygame.display.update()
            
            # Wait for quit or continue
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            waiting = False
                        if event.key == pygame.K_c:
                            run_game()
                    if event.type == pygame.QUIT:
                        game_over = True
                        waiting = False
        
        # Control game speed
        clock.tick(snake_speed)
    
    # Quit pygame
    pygame.quit()
    quit()

# Start the game
if __name__ == "__main__":
    run_game()
```

## Extension Ideas
1. Add sound effects for eating food and game over
2. Implement different difficulty levels (changing snake speed)
3. Add a high score system with persistent storage
4. Include obstacles or walls in the game area
5. Add special food items that give bonus points or abilities

## Troubleshooting
- If you encounter module not found errors, ensure Pygame is installed correctly
- Check for indentation errors in your code
- Verify that all variables are properly initialized
- Use an IDE with code completion (like VSCode with Tabnine) for easier development

## Resources
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Random Module Documentation](https://docs.python.org/3/library/random.html) 