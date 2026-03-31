#!/usr/bin/env python3
import pygame
import sys
import math
import random
from dataclasses import dataclass, field
from enum import Enum

class GravityDirection(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3

@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    restitution: float
    radius: float
    color: tuple
    mass: float = 1.0
    trail: list = field(default_factory=list)

# --- Simulation parameters ---
WIDTH, HEIGHT = 1200, 700
GROUND_Y = HEIGHT - 50
GRAVITY_STRENGTH = 500.0
DT = 1/60.0
DAMPING = 0.999

# --- Colors ---
BG_COLOR = (20, 20, 30)
GROUND_COLOR = (60, 60, 80)
TEXT_COLOR = (200, 200, 200)
BUTTON_COLOR = (80, 80, 100)
BUTTON_HOVER = (100, 100, 120)

# --- Slider ---
class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, 10)
        self.handle_radius = 8
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False

    def get_handle_x(self):
        t = (self.value - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + t * self.rect.width

    def update(self, mx, my, pressed):
        handle_x = self.get_handle_x()
        handle_rect = pygame.Rect(handle_x-8, self.rect.y-8, 16, 16)

        if not self.dragging and pressed[0] and handle_rect.collidepoint(mx, my):
            self.dragging = True

        if self.dragging:
            if not pressed[0]:
                self.dragging = False
            else:
                t = (mx - self.rect.x) / self.rect.width
                t = max(0, min(1, t))
                self.value = self.min_val + t*(self.max_val - self.min_val)

    def draw(self, screen, font):
        pygame.draw.rect(screen, (100,100,150), self.rect)
        pygame.draw.circle(screen, (200,200,250),
                           (int(self.get_handle_x()), self.rect.y+5), 8)
        txt = font.render(f"{self.label}: {self.value:.1f}", True, TEXT_COLOR)
        screen.blit(txt, (self.rect.x, self.rect.y-25))

# --- Button ---
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.clicked = False

    def update(self, mx, my, pressed):
        hover = self.rect.collidepoint(mx, my)
        if hover and pressed[0] and not self.clicked:
            self.clicked = True
            return True
        if not pressed[0]:
            self.clicked = False
        return False

    def draw(self, screen, font, mx, my):
        hover = self.rect.collidepoint(mx, my)
        color = self.hover_color if hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (150,150,170), self.rect, 2, border_radius=5)
        txt = font.render(self.text, True, TEXT_COLOR)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

# --- Init balls ---
def create_balls():
    balls = []
    for _ in range(12):
        balls.append(Ball(
            x=random.uniform(80, WIDTH-80),
            y=random.uniform(80, GROUND_Y-80),
            vx=random.uniform(-200, 200),
            vy=random.uniform(-200, 0),
            restitution=random.uniform(0.6, 0.95),
            radius=random.uniform(8, 16),
            color=(random.randint(100,255), random.randint(100,255), random.randint(100,255))
        ))
    # High-bounce ball
    balls.append(Ball(
        x=WIDTH//2, y=GROUND_Y-100,
        vx=150, vy=-300,
        restitution=0.98,
        radius=20,
        color=(255, 100, 100)
    ))
    return balls

# --- Physics ---
def apply_gravity(ball, direction, g, dt):
    if direction == GravityDirection.DOWN:
        ball.vy += g*dt
    elif direction == GravityDirection.UP:
        ball.vy -= g*dt
    elif direction == GravityDirection.LEFT:
        ball.vx -= g*dt
    elif direction == GravityDirection.RIGHT:
        ball.vx += g*dt

def check_bounds(ball):
    if ball.y + ball.radius > GROUND_Y:
        ball.y = GROUND_Y - ball.radius
        ball.vy = -ball.vy * ball.restitution
        if abs(ball.vy) < 15:
            ball.vy = 0

    if ball.x - ball.radius < 0:
        ball.x = ball.radius
        ball.vx *= -ball.restitution
    if ball.x + ball.radius > WIDTH:
        ball.x = WIDTH - ball.radius
        ball.vx *= -ball.restitution
    if ball.y - ball.radius < 0:
        ball.y = ball.radius
        ball.vy *= -ball.restitution

def resolve_collision(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        return

    nx, ny = dx/dist, dy/dist
    min_dist = a.radius + b.radius

    if dist < min_dist:
        overlap = min_dist - dist
        a.x += nx * overlap * 0.5
        a.y += ny * overlap * 0.5
        b.x -= nx * overlap * 0.5
        b.y -= ny * overlap * 0.5

        rvx = a.vx - b.vx
        rvy = a.vy - b.vy
        vel_along_normal = rvx*nx + rvy*ny

        if vel_along_normal > 0:
            return

        e = (a.restitution + b.restitution)/2
        j = -(1+e)*vel_along_normal / (1/a.mass + 1/b.mass)

        a.vx += (j/a.mass)*nx
        a.vy += (j/a.mass)*ny
        b.vx -= (j/b.mass)*nx
        b.vy -= (j/b.mass)*ny

# --- Energy ---
def compute_energy(balls, g):
    ke = sum(0.5*b.mass*(b.vx**2 + b.vy**2) for b in balls)
    pe = sum(b.mass*g*(GROUND_Y - b.y) for b in balls if b.y < GROUND_Y)
    return ke, pe

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Engine - Interactive Demo")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 32)

balls = create_balls()
gravity_slider = Slider(20, HEIGHT-80, 300, 0, 1200, GRAVITY_STRENGTH, "Gravity")
direction = GravityDirection.DOWN
direction_names = ["DOWN", "UP", "LEFT", "RIGHT"]

# UI state
show_energy = True
toggle_button = Button(WIDTH - 150, HEIGHT - 50, 120, 35, "Toggle Info", BUTTON_COLOR, BUTTON_HOVER)

# Mouse dragging with throw
dragging_ball = None
drag_offset_x = 0
drag_offset_y = 0
drag_last_x = 0
drag_last_y = 0
throw_velocity = None

# Window movement tracking
last_window_x, last_window_y = 0, 0
first_frame = True

running = True
while running:
    mx, my = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    # Track window position for shake effect
    try:
        import pygame._sdl2 as sdl2
        win = sdl2.Window.from_display_module()
        win_x, win_y = win.position
    except:
        win_x, win_y = 0, 0

    if not first_frame:
        delta_x = win_x - last_window_x
        delta_y = win_y - last_window_y
        if abs(delta_x) > 0 or abs(delta_y) > 0:
            for ball in balls:
                if ball is not dragging_ball:
                    ball.vx += delta_x * 1.5
                    ball.vy += delta_y * 1.5

    last_window_x, last_window_y = win_x, win_y
    first_frame = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                balls.append(Ball(
                    x=random.uniform(50, WIDTH-50),
                    y=random.uniform(50, GROUND_Y-50),
                    vx=random.uniform(-200, 200),
                    vy=random.uniform(-200, 0),
                    restitution=random.uniform(0.5, 0.95),
                    radius=random.uniform(8, 16),
                    color=(random.randint(100,255), random.randint(100,255), random.randint(100,255))
                ))
            elif event.key == pygame.K_r:
                balls = create_balls()
            elif event.key == pygame.K_c:
                balls.clear()
            # WASD gravity
            elif event.key == pygame.K_w:
                direction = GravityDirection.UP
            elif event.key == pygame.K_s:
                direction = GravityDirection.DOWN
            elif event.key == pygame.K_a:
                direction = GravityDirection.LEFT
            elif event.key == pygame.K_d:
                direction = GravityDirection.RIGHT
            elif event.key == pygame.K_t:
                show_energy = not show_energy

    GRAVITY_STRENGTH = gravity_slider.value

    # Handle button click
    if toggle_button.update(mx, my, pressed):
        show_energy = not show_energy

    # Mouse dragging with throw
    if pressed[0] and not gravity_slider.dragging and not toggle_button.rect.collidepoint(mx, my):
        if dragging_ball is None:
            for ball in balls:
                dx = ball.x - mx
                dy = ball.y - my
                if math.hypot(dx, dy) < ball.radius:
                    dragging_ball = ball
                    drag_offset_x = ball.x - mx
                    drag_offset_y = ball.y - my
                    drag_last_x = mx
                    drag_last_y = my
                    break
        else:
            mouse_dx = mx - drag_last_x
            mouse_dy = my - drag_last_y
            drag_last_x = mx
            drag_last_y = my

            dragging_ball.x = mx + drag_offset_x
            dragging_ball.y = my + drag_offset_y
            dragging_ball.vx = 0
            dragging_ball.vy = 0

            throw_velocity = (mouse_dx / DT, mouse_dy / DT)

            # Keep in bounds
            if dragging_ball.x - dragging_ball.radius < 0:
                dragging_ball.x = dragging_ball.radius
            if dragging_ball.x + dragging_ball.radius > WIDTH:
                dragging_ball.x = WIDTH - dragging_ball.radius
            if dragging_ball.y - dragging_ball.radius < 0:
                dragging_ball.y = dragging_ball.radius
            if dragging_ball.y + dragging_ball.radius > GROUND_Y:
                dragging_ball.y = GROUND_Y - dragging_ball.radius
    else:
        if dragging_ball is not None and throw_velocity is not None:
            dragging_ball.vx = throw_velocity[0]
            dragging_ball.vy = throw_velocity[1]
        dragging_ball = None
        throw_velocity = None

    gravity_slider.update(mx, my, pressed)

    # Physics update
    for b in balls:
        if b is dragging_ball:
            continue
        apply_gravity(b, direction, GRAVITY_STRENGTH, DT)
        b.x += b.vx * DT
        b.y += b.vy * DT
        b.vx *= DAMPING
        b.vy *= DAMPING
        check_bounds(b)

        # Trail
        b.trail.append((b.x, b.y))
        if len(b.trail) > 15:
            b.trail.pop(0)

    # Sphere collisions
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            resolve_collision(balls[i], balls[j])

    ke, pe = compute_energy(balls, GRAVITY_STRENGTH)

    # Draw
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

    for b in balls:
        # Trail
        for i, (tx, ty) in enumerate(b.trail):
            alpha = int(100 * i / len(b.trail))
            pygame.draw.circle(screen, b.color, (int(tx), int(ty)), max(1, int(b.radius * i / len(b.trail))))

        pygame.draw.circle(screen, b.color, (int(b.x), int(b.y)), int(b.radius))
        if b is dragging_ball:
            pygame.draw.circle(screen, (255,255,255), (int(b.x), int(b.y)), int(b.radius)+4, 3)
        elif b.restitution > 0.95:
            pygame.draw.circle(screen, (255,255,200), (int(b.x), int(b.y)), int(b.radius)+2, 2)

    gravity_slider.draw(screen, font)
    toggle_button.draw(screen, font, mx, my)

    # Info display - toggles between energy and controls
    if show_energy:
        info_lines = [
            f"Balls: {len(balls)}",
            f"KE: {ke:.0f}  PE: {pe:.0f}",
            f"Total: {ke+pe:.0f}",
            "",
            "Press T to toggle",
            "Drag window to shake"
        ]
    else:
        info_lines = [
            "CONTROLS:",
            "SPACE: Add ball",
            "R: Reset",
            "C: Clear all",
            "WASD: Gravity direction",
            "Click & drag: Throw balls",
            "Drag window: Shake",
            "Press T to toggle"
        ]

    for i, line in enumerate(info_lines):
        txt = font.render(line, True, TEXT_COLOR)
        screen.blit(txt, (WIDTH - 280, 10 + i * 22))

    # Gravity direction indicator
    dir_text = big_font.render(f"Gravity: {direction_names[direction.value]}", True, (150, 200, 255))
    screen.blit(dir_text, (WIDTH // 2 - 100, HEIGHT - 60))

    # Throw indicator
    if dragging_ball and throw_velocity:
        vel_text = font.render(f"Throw: ({throw_velocity[0]:.0f}, {throw_velocity[1]:.0f})", True, (255, 200, 100))
        screen.blit(vel_text, (mx + 20, my - 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
