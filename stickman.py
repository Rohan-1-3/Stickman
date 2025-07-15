import pygame
import math

class Stickman:
    def __init__(self, x, y, config):
        self.x = x
        self.y = y
        self.config = config
        self._parse_config()

    def _parse_config(self):
        self.head_radius = int(self.config.get("head_size", 25))
        self.eye_size = int(self.config.get("eye_size", 3))
        self.nose_size = int(self.config.get("nose_size", 4))
        self.mouth_size = int(self.config.get("mouth_size", 12))
        self.arm_length = int(self.config.get("arm_length", 40))
        self.arm_thickness = int(self.config.get("arm_thickness", 2))
        self.leg_length = int(self.config.get("leg_length", 50))
        self.torso_length = int(self.config.get("torso_length", 60))
        self.hair_color = self.config.get("hair_color", (0, 0, 0))
        self.skin_color = self.config.get("skin_color", (255, 224, 189))



    def draw(self, screen):
        # Head center
        head_x, head_y = self.x, self.y

        # Draw head
        pygame.draw.circle(screen, self.skin_color, (head_x, head_y), self.head_radius)

        # Hair
        num_spikes = 12
        spike_length = self.head_radius // 1.5  # relative to head size

        for i in range(num_spikes):
            angle = math.pi * (i / (num_spikes - 1))  # from 0 to pi (top arc)
            
            # Start point: on head edge
            x0 = head_x + math.cos(angle) * self.head_radius
            y0 = head_y - math.sin(angle) * self.head_radius

            # End point: extend outward
            x1 = head_x + math.cos(angle) * (self.head_radius + spike_length)
            y1 = head_y - math.sin(angle) * (self.head_radius + spike_length)

            pygame.draw.line(screen, self.hair_color, (x0, y0), (x1, y1), 2)

        # Eyes
        eye_offset = self.head_radius // 2
        pygame.draw.circle(screen, (0, 0, 0), (head_x - eye_offset, head_y - eye_offset), self.eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (head_x + eye_offset, head_y - eye_offset), self.eye_size)

        # Nose (line down)
        pygame.draw.line(screen, (120, 90, 90),
                         (head_x, head_y),
                         (head_x, head_y + self.nose_size), 2)

        # Mouth (horizontal line)
        pygame.draw.line(screen, (255, 0, 0),
                         (head_x - self.mouth_size // 2, head_y + self.head_radius // 2),
                         (head_x + self.mouth_size // 2, head_y + self.head_radius // 2), 2)

        # Torso (line down from head)
        torso_top = (head_x, head_y + self.head_radius)
        torso_bottom = (head_x, torso_top[1] + self.torso_length)
        pygame.draw.line(screen, self.skin_color, torso_top, torso_bottom, 3)

        # Arms
        arm_y = torso_top[1] + self.torso_length // 4
        pygame.draw.line(screen, self.skin_color,
                         (head_x - self.arm_length, arm_y),
                         (head_x + self.arm_length, arm_y),
                         self.arm_thickness)

        # Legs
        pygame.draw.line(screen, self.skin_color,
                         torso_bottom,
                         (head_x - self.leg_length // 2, torso_bottom[1] + self.leg_length),
                         3)

        pygame.draw.line(screen, self.skin_color,
                         torso_bottom,
                         (head_x + self.leg_length // 2, torso_bottom[1] + self.leg_length),
                         3)
