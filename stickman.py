import pygame
import math

class Stickman:
    def __init__(self, x, y, config):
        self.x = x
        self.y = y
        self.config = config
        self._parse_config()

        # Movement and simulation state
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.is_simulating = False
        self.dead = False

    def _parse_config(self):
        self.head_radius = int(self.config.get("head_size", 25))
        self.eye_size = int(self.config.get("eye_size", 3))
        self.nose_size = int(self.config.get("nose_size", 4))
        self.mouth_size = int(self.config.get("mouth_size", 12))
        self.mouth_curve = self.config.get("mouth_curve", 0.0)
        self.arm_length = int(self.config.get("arm_length", 40))
        self.arm_thickness = int(self.config.get("arm_thickness", 2))
        self.leg_length = int(self.config.get("leg_length", 50))
        self.torso_length = int(self.config.get("torso_length", 60))
        self.hair_color = self.config.get("hair_color", (0, 0, 0))
        self.skin_color = self.config.get("skin_color", (255, 224, 189))

    def update(self, screen_width, screen_height):
        if not self.is_simulating or self.dead:
            return

        self.x += self.velocity_x
        self.y += self.velocity_y

        half_width = self.head_radius + self.arm_length // 2
        total_height = self.head_radius + self.torso_length + self.leg_length

        self.x = max(half_width, min(screen_width - half_width, self.x))
        self.y = max(total_height, min(screen_height - total_height, self.y))

    def draw(self, screen):
        head_x, head_y = int(self.x), int(self.y)

        # --- Head ---
        pygame.draw.circle(screen, self.skin_color, (head_x, head_y), self.head_radius)

        # --- Hair ---
        num_spikes = 100
        spike_length = self.head_radius // 1.5
        arc_span = math.pi * 0.8
        start_angle = math.pi / 2 - arc_span / 2

        for i in range(num_spikes):
            angle = start_angle + arc_span * (i / (num_spikes - 1))
            x0 = head_x + math.cos(angle) * self.head_radius
            y0 = head_y - math.sin(angle) * self.head_radius
            x1 = head_x + math.cos(angle) * (self.head_radius + spike_length)
            y1 = head_y - math.sin(angle) * (self.head_radius + spike_length)
            pygame.draw.line(screen, self.hair_color, (x0, y0), (x1, y1), 2)

        # --- Eyes ---
        eye_gap = self.head_radius // 2
        eye_y = head_y - self.head_radius // 3
        eye_radius = max(2, self.eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (head_x - eye_gap, eye_y), eye_radius)
        pygame.draw.circle(screen, (0, 0, 0), (head_x + eye_gap, eye_y), eye_radius)

        # --- Nose (angled) ---
        nose_top = (head_x, eye_y + eye_radius + 4)
        nose_bottom = (head_x + self.nose_size // 2, nose_top[1] + self.nose_size)
        pygame.draw.line(screen, (120, 90, 90), nose_top, nose_bottom, 2)

        # --- Mouth ---
        mouth_top_y = head_y + self.head_radius // 2
        mid_y = mouth_top_y + int(self.mouth_curve * 10)
        start_x = head_x - self.mouth_size // 2
        end_x = head_x + self.mouth_size // 2
        pygame.draw.lines(screen, (255, 0, 0), False, [
            (start_x, mouth_top_y),
            (head_x, mid_y),
            (end_x, mouth_top_y)
        ], 2)

        # --- Torso ---
        torso_top = (head_x, head_y + self.head_radius)
        torso_bottom = (head_x, torso_top[1] + self.torso_length)
        pygame.draw.line(screen, self.skin_color, torso_top, torso_bottom, 3)

        # --- Arms ---
        arm_start_y = head_y + self.head_radius + 5
        left_hand = (head_x - self.arm_length // 2, arm_start_y + self.arm_length)
        right_hand = (head_x + self.arm_length // 2, arm_start_y + self.arm_length)
        pygame.draw.line(screen, self.skin_color, (head_x, arm_start_y), left_hand, self.arm_thickness)
        pygame.draw.line(screen, self.skin_color, (head_x, arm_start_y), right_hand, self.arm_thickness)

        # --- Legs ---
        pygame.draw.line(screen, self.skin_color,
                         torso_bottom,
                         (head_x - self.leg_length // 2, torso_bottom[1] + self.leg_length), 3)
        pygame.draw.line(screen, self.skin_color,
                         torso_bottom,
                         (head_x + self.leg_length // 2, torso_bottom[1] + self.leg_length), 3)
