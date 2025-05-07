import pygame

# Initialize only display (minimal initialization)
pygame.display.init()

# Constants
WIDTH, HEIGHT = 640, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimal Test")
clock = pygame.time.Clock()

# Main game loop
def main():
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Drawing
        screen.fill(BLACK)
        
        # Draw a simple shape
        pygame.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), 50)
        
        # Draw text without font module
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 40))
        
        # Update display
        pygame.display.flip()
        clock.tick(30)

try:
    main()
except Exception as e:
    print(f"Error: {e}")
finally:
    pygame.quit() 