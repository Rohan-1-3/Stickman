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
        self.speed = 10
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

        # Horizontal wrap
        if self.x < -self.head_radius:
            self.x = screen_width + self.head_radius
        elif self.x > screen_width + self.head_radius:
            self.x = -self.head_radius

        # Vertical wrap (optional)
        head_height = int(self.head_radius * 2.4)
        bottom_buffer = head_height // 2 + self.torso_length + self.leg_length

        if self.y < -bottom_buffer:
            self.y = screen_height + bottom_buffer
        elif self.y > screen_height + bottom_buffer:
            self.y = -bottom_buffer

    def draw(self, screen):
        head_x, head_y = int(self.x), int(self.y)

        # --- Head (oval instead of circle) ---
        head_width = self.head_radius * 1.5
        head_height = int(self.head_radius * 1.7)
        head_rect = pygame.Rect(head_x - head_width // 2, head_y - head_height // 2, head_width, head_height)
        pygame.draw.ellipse(screen, self.skin_color, head_rect)

        # --- Hair ---
        num_spikes = 100
        spike_length = self.head_radius // 1.5
        arc_span = math.pi * 0.8
        start_angle = math.pi / 2 - arc_span / 2

        for i in range(num_spikes):
            angle = start_angle + arc_span * (i / (num_spikes - 1))
            x0 = head_x + math.cos(angle) * (head_width // 2)
            y0 = head_y - math.sin(angle) * (head_height // 2)
            x1 = head_x + math.cos(angle) * ((head_width // 2) + spike_length)
            y1 = head_y - math.sin(angle) * ((head_height // 2) + spike_length)
            pygame.draw.line(screen, self.hair_color, (x0, y0), (x1, y1), 2)

        # --- Eyes (white, pupil, highlight) ---
        eye_gap = self.head_radius * 0.25
        eye_y = head_y - head_height // 4
        eye_white_radius = max(3, self.eye_size * 1.5)
        pupil_radius = max(2, self.eye_size * .8)
        highlight_radius = 2

        for offset in [-eye_gap, eye_gap]:
            eye_center = (int(head_x + offset), int(eye_y))
            pygame.draw.circle(screen, (255, 255, 255), eye_center, eye_white_radius)   # white part
            pygame.draw.circle(screen, (0, 0, 0), eye_center, pupil_radius)             # pupil
            pygame.draw.circle(screen, (255, 255, 255), 
                            (eye_center[0] - 2, eye_center[1] - 2), highlight_radius) # highlight

        # --- Nose ---
        nose_top = (head_x, int(eye_y + eye_white_radius + 4))
        nose_bottom = (head_x + self.nose_size // 2, nose_top[1] + self.nose_size)
        pygame.draw.line(screen, (120, 90, 90), nose_top, nose_bottom, 2)

        # --- Mouth ---
        mouth_top_y = head_y + head_height // 4
        mid_y = mouth_top_y + int(self.mouth_curve * 10)
        start_x = head_x - self.mouth_size // 2
        end_x = head_x + self.mouth_size // 2
        pygame.draw.lines(screen, (255, 0, 0), False, [
            (start_x, mouth_top_y),
            (head_x, mid_y),
            (end_x, mouth_top_y)
        ], 2)

        # --- Torso ---
        torso_top = (head_x, head_y + head_height // 2)
        torso_bottom = (head_x, torso_top[1] + self.torso_length)
        pygame.draw.line(screen, self.skin_color, torso_top, torso_bottom, 3)

        # --- Arms ---
        arm_start_y = torso_top[1] + 5
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
