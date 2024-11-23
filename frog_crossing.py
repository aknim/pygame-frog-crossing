import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

FROG_WIDTH = 40
FROG_HEIGHT = 40
frog_x = SCREEN_WIDTH // 2
frog_y = SCREEN_HEIGHT - FROG_HEIGHT
frog_speed = 10

# Road and vehicle properties
LANE_HEIGHT = 40
SAFE_ZONE_HEIGHT = 40
NUM_LANES = 3
vehicle_width = 60
vehicle_height = 40
vehicle_speed = 5

# Create lanes and vehicles
lanes = [SCREEN_HEIGHT - (i + 1) * (LANE_HEIGHT + SAFE_ZONE_HEIGHT) for i in range(NUM_LANES)]
vehicles = [
    {"x": random.randint(0, SCREEN_WIDTH), 
     "y": lanes[i],
     "speed": vehicle_speed + i * 2}
     for i in range(NUM_LANES)
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frog Crossing")

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    # Move frog
    if keys[pygame.K_LEFT] and frog_x > 0:
        frog_x -= frog_speed
    if keys[pygame.K_RIGHT] and frog_x < SCREEN_WIDTH - FROG_WIDTH:
        frog_x += frog_speed
    if keys[pygame.K_UP] and frog_y > 0:
        frog_y -= frog_speed
    if keys[pygame.K_DOWN] and frog_y < SCREEN_HEIGHT - FROG_HEIGHT:
        frog_y += frog_speed

    # Move vehicles
    for vehicle in vehicles:
        vehicle["x"] += vehicle["speed"]
        # Reset vehicle when it goes off screen
        if vehicle["x"] > SCREEN_WIDTH:
            vehicle["x"] = -vehicle_width

    # Check for collisions
    for vehicle in vehicles:
        if (
            frog_x < vehicle["x"] + vehicle_width
            and frog_x + FROG_WIDTH > vehicle["x"]
            and frog_y < vehicle["y"] + vehicle_height
            and frog_y + FROG_HEIGHT > vehicle["y"]
        ):
            print("Game Over! Frog hit an obstacle!")
            running = False

    # Check for win condition
    if frog_y <= 0:
        print("You Win!")
        running = False
    
    # Draw everything
    screen.fill(WHITE) # Clear the screen

    # Draw lanes and safe zones
    for i, lane_y in enumerate(lanes):
        # Draw road(lane)
        pygame.draw.rect(screen, GRAY, (0, lane_y, SCREEN_WIDTH, LANE_HEIGHT))
        # Draw safe zone
        if i < NUM_LANES - 1:
            pygame.draw.rect(screen, WHITE, (0, lane_y + LANE_HEIGHT, SCREEN_WIDTH, SAFE_ZONE_HEIGHT))

    # Draw vehicles
    for vehicle in vehicles:
        pygame.draw.rect(screen, RED, (vehicle["x"], vehicle["y"], vehicle_width, vehicle_height))

    # Draw the frog
    pygame.draw.rect(screen, GREEN, (frog_x, frog_y, FROG_WIDTH, FROG_HEIGHT))
    pygame.display.flip() 

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()