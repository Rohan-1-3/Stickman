import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val):
        self.x = x
        self.y = y
        self.width = width
        self.height = 10
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.handle_radius = 8
        self.dragging = False

    def handle_pos(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        return self.x + int(ratio * self.width)

    def draw(self, screen):
        # Line
        pygame.draw.line(screen, (100, 100, 100), (self.x, self.y), (self.x + self.width, self.y), 4)
        # Handle
        pygame.draw.circle(screen, (0, 0, 0), (self.handle_pos(), self.y), self.handle_radius)

        # Label
        font = pygame.font.SysFont("Arial", 16)
        label = font.render(f"Size: {self.value:.1f}x", True, (0, 0, 0))
        screen.blit(label, (self.x, self.y + 15))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if abs(mx - self.handle_pos()) < self.handle_radius * 2 and abs(my - self.y) < 20:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, _ = event.pos
            ratio = max(0, min(1, (mx - self.x) / self.width))
            self.value = self.min_val + ratio * (self.max_val - self.min_val)

class LabeledSlider(Slider):
    def __init__(self, name, x, y, width, min_val, max_val, initial_val):
        super().__init__(x, y, width, min_val, max_val, initial_val)
        self.name = name

    def draw(self, screen):
        super().draw(screen)
        font = pygame.font.SysFont("Arial", 16)
        label = font.render(f"{self.name}: {self.value:.1f}", True, (0, 0, 0))
        screen.blit(label, (self.x, self.y - 20))
