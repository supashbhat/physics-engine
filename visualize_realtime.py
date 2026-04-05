#!/usr/bin/env python3
from collections import deque
import math
import random
import sys
from dataclasses import dataclass, field
from enum import Enum

import pygame


class GravityDirection(Enum):
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3


class ScenePreset(Enum):
    RANDOM = 0
    CASCADE = 1
    ORBIT = 2


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    restitution: float
    radius: float
    color: tuple[int, int, int]
    mass: float = 1.0
    trail: list = field(default_factory=list)


WIDTH, HEIGHT = 1280, 760
GROUND_Y = HEIGHT - 66
BASE_GRAVITY = 520.0
BASE_DT = 1 / 60.0
DAMPING = 0.998
MAX_TRAIL = 24

BG_TOP = (10, 13, 22)
BG_BOTTOM = (17, 24, 37)
PANEL = (17, 22, 34, 196)
PANEL_STRONG = (14, 20, 31, 228)
PANEL_LINE = (255, 124, 120, 52)
TEXT = (238, 243, 250)
TEXT_SOFT = (190, 176, 182)
TEXT_FAINT = (126, 108, 112)
ACCENT = (255, 118, 112)
ACCENT_SOFT = (255, 190, 180)
ACCENT_MINT = (255, 224, 205)
GROUND_COLOR = (44, 30, 36)
GROUND_LINE = (255, 128, 122)
RIBBON_PRIMARY = (255, 152, 142)
RIBBON_SECONDARY = (255, 214, 198)


class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, label, fmt="{:.1f}"):
        self.rect = pygame.Rect(x, y, width, 10)
        self.handle_radius = 9
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.fmt = fmt
        self.dragging = False

    def get_handle_x(self):
        t = (self.value - self.min_val) / (self.max_val - self.min_val)
        return self.rect.x + t * self.rect.width

    def update(self, mx, my, pressed):
        handle_x = self.get_handle_x()
        handle_rect = pygame.Rect(handle_x - 10, self.rect.y - 10, 20, 20)

        if not self.dragging and pressed[0] and (handle_rect.collidepoint(mx, my) or self.rect.collidepoint(mx, my)):
            self.dragging = True

        if self.dragging:
            if not pressed[0]:
                self.dragging = False
            else:
                t = (mx - self.rect.x) / self.rect.width
                t = max(0, min(1, t))
                self.value = self.min_val + t * (self.max_val - self.min_val)

    def draw(self, screen, font):
        pygame.draw.rect(screen, (56, 42, 48), self.rect, border_radius=999)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, int(self.get_handle_x() - self.rect.x), self.rect.height)
        pygame.draw.rect(screen, ACCENT, fill_rect, border_radius=999)
        pygame.draw.circle(screen, ACCENT_MINT, (int(self.get_handle_x()), self.rect.centery), self.handle_radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.get_handle_x()), self.rect.centery), self.handle_radius, 2)
        txt = font.render(f"{self.label}: {self.fmt.format(self.value)}", True, TEXT_SOFT)
        screen.blit(txt, (self.rect.x, self.rect.y - 24))


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.clicked = False

    def update(self, mx, my, pressed):
        hover = self.rect.collidepoint(mx, my)
        if hover and pressed[0] and not self.clicked:
            self.clicked = True
            return True
        if not pressed[0]:
            self.clicked = False
        return False

    def draw(self, screen, font, mx, my, active=False):
        hover = self.rect.collidepoint(mx, my)
        bg = (54, 42, 48) if active else (34, 29, 40)
        line = ACCENT if active else (98, 68, 74)
        if hover:
            bg = (62, 46, 54)
        draw_card(screen, self.rect, bg + (255,), line)
        txt = font.render(self.text, True, TEXT if active else TEXT_SOFT)
        screen.blit(txt, txt.get_rect(center=self.rect.center))


def draw_vertical_gradient(surface, top_color, bottom_color):
    for y in range(HEIGHT):
        t = y / HEIGHT
        color = tuple(int(top_color[i] * (1.0 - t) + bottom_color[i] * t) for i in range(3))
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))


def draw_card(screen, rect, fill_rgba, border_rgb, radius=20):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, fill_rgba, panel.get_rect(), border_radius=radius)
    pygame.draw.rect(panel, (*border_rgb, 255), panel.get_rect(), 1, border_radius=radius)
    screen.blit(panel, rect.topleft)


def draw_glow(screen, center, color, radius):
    glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*color, 36), (radius, radius), radius)
    pygame.draw.circle(glow, (*color, 18), (radius, radius), int(radius * 0.72))
    screen.blit(glow, (center[0] - radius, center[1] - radius), special_flags=pygame.BLEND_ALPHA_SDL2)


def make_ball_color():
    palette = [
        (255, 122, 115),
        (255, 172, 120),
        (255, 204, 158),
        (242, 209, 152),
        (255, 145, 136),
    ]
    return random.choice(palette)


def spawn_ball(x=None, y=None, vx=None, vy=None, restitution=None, radius=None, color=None):
    return Ball(
        x=x if x is not None else random.uniform(90, WIDTH - 90),
        y=y if y is not None else random.uniform(100, GROUND_Y - 120),
        vx=vx if vx is not None else random.uniform(-220, 220),
        vy=vy if vy is not None else random.uniform(-220, 40),
        restitution=restitution if restitution is not None else random.uniform(0.68, 0.95),
        radius=radius if radius is not None else random.uniform(10, 18),
        color=color if color is not None else make_ball_color(),
    )


def create_balls(preset):
    balls = []
    if preset == ScenePreset.CASCADE:
        for i in range(10):
            balls.append(
                spawn_ball(
                    x=130 + i * 92,
                    y=110 + i * 16,
                    vx=random.uniform(-30, 60),
                    vy=random.uniform(-30, 40),
                    restitution=0.78 + (i % 3) * 0.05,
                    radius=12 + (i % 3) * 2,
                )
            )
    elif preset == ScenePreset.ORBIT:
        cx = WIDTH * 0.5
        cy = GROUND_Y * 0.44
        for i in range(12):
            angle = (math.pi * 2.0 * i) / 12.0
            px = cx + math.cos(angle) * 190
            py = cy + math.sin(angle) * 120
            balls.append(
                spawn_ball(
                    x=px,
                    y=py,
                    vx=-math.sin(angle) * 180,
                    vy=math.cos(angle) * 140,
                    restitution=0.88,
                    radius=10 + (i % 2) * 2,
                )
            )
    else:
        for _ in range(12):
            balls.append(spawn_ball())

    balls.append(
        spawn_ball(
            x=WIDTH * 0.5,
            y=GROUND_Y - 120,
            vx=180,
            vy=-280,
            restitution=0.98,
            radius=22,
            color=(255, 215, 170),
        )
    )
    return balls


def apply_gravity(ball, direction, gravity, dt):
    if direction == GravityDirection.DOWN:
        ball.vy += gravity * dt
    elif direction == GravityDirection.UP:
        ball.vy -= gravity * dt
    elif direction == GravityDirection.LEFT:
        ball.vx -= gravity * dt
    elif direction == GravityDirection.RIGHT:
        ball.vx += gravity * dt


def check_bounds(ball):
    if ball.y + ball.radius > GROUND_Y:
        ball.y = GROUND_Y - ball.radius
        ball.vy = -ball.vy * ball.restitution
        if abs(ball.vy) < 18:
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
        return False

    nx, ny = dx / dist, dy / dist
    min_dist = a.radius + b.radius
    if dist < min_dist:
        overlap = min_dist - dist
        a.x += nx * overlap * 0.5
        a.y += ny * overlap * 0.5
        b.x -= nx * overlap * 0.5
        b.y -= ny * overlap * 0.5

        rvx = a.vx - b.vx
        rvy = a.vy - b.vy
        vel_along_normal = rvx * nx + rvy * ny
        if vel_along_normal > 0:
            return False

        restitution = (a.restitution + b.restitution) / 2.0
        impulse = -(1.0 + restitution) * vel_along_normal / (1 / a.mass + 1 / b.mass)

        a.vx += (impulse / a.mass) * nx
        a.vy += (impulse / a.mass) * ny
        b.vx -= (impulse / b.mass) * nx
        b.vy -= (impulse / b.mass) * ny

        return True

    return False


def compute_energy(balls, gravity):
    ke = sum(0.5 * b.mass * (b.vx ** 2 + b.vy ** 2) for b in balls)
    pe = sum(b.mass * gravity * (GROUND_Y - b.y) for b in balls if b.y < GROUND_Y)
    return ke, pe


def average_speed(balls):
    if not balls:
        return 0.0
    return sum(math.hypot(b.vx, b.vy) for b in balls) / len(balls)


def draw_motion_ribbons(screen, phase, direction):
    ribbon_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    direction_bias = {
        GravityDirection.DOWN: (0.0, 18.0),
        GravityDirection.UP: (0.0, -18.0),
        GravityDirection.LEFT: (-18.0, 0.0),
        GravityDirection.RIGHT: (18.0, 0.0),
    }[direction]

    for idx in range(5):
        points = []
        amplitude = 18 + idx * 7
        base_y = 128 + idx * 76
        for x in range(-60, WIDTH + 61, 26):
            normalized = x / WIDTH
            drift = phase * (0.62 + idx * 0.08)
            wave = math.sin(normalized * math.tau * (1.1 + idx * 0.14) + drift + idx * 0.65) * amplitude
            curl = math.cos(normalized * math.tau * 0.7 - drift * 0.42 + idx * 0.3) * (amplitude * 0.38)
            px = x + direction_bias[0] * 0.16 * idx
            py = base_y + wave + curl + direction_bias[1] * 0.18
            points.append((px, py))

        color = RIBBON_PRIMARY if idx % 2 == 0 else RIBBON_SECONDARY
        alpha = 12 + idx * 5
        pygame.draw.lines(ribbon_surface, (*color, alpha), False, points, 2 if idx == 2 else 1)

    screen.blit(ribbon_surface, (0, 0))


def draw_sparkline(screen, rect, values):
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(surface, (255, 255, 255, 10), surface.get_rect(), border_radius=14)
    pygame.draw.rect(surface, (*ACCENT_SOFT, 28), surface.get_rect(), 1, border_radius=14)

    values = list(values)
    if len(values) >= 2:
        low = min(values)
        high = max(values)
        span = max(high - low, 1.0)
        points = []
        for idx, value in enumerate(values):
            x = 8 + idx * (rect.width - 16) / max(1, len(values) - 1)
            normalized = (value - low) / span
            y = rect.height - 8 - normalized * (rect.height - 16)
            points.append((x, y))

        fill_points = [(points[0][0], rect.height - 8), *points, (points[-1][0], rect.height - 8)]
        pygame.draw.polygon(surface, (*ACCENT, 32), fill_points)
        pygame.draw.lines(surface, (*ACCENT_MINT, 255), False, points, 2)

    screen.blit(surface, rect.topleft)


def draw_help_overlay(screen, title_font, font, small_font):
    veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    veil.fill((4, 7, 12, 170))
    screen.blit(veil, (0, 0))

    panel_rect = pygame.Rect(WIDTH // 2 - 270, HEIGHT // 2 - 200, 540, 400)
    draw_card(screen, panel_rect, (11, 18, 28, 240), ACCENT_SOFT, radius=28)

    title = title_font.render("Sandbox Guide", True, TEXT)
    subtitle = font.render("Fast controls for exploring motion, energy, and collisions.", True, TEXT_SOFT)
    screen.blit(title, (panel_rect.x + 24, panel_rect.y + 22))
    screen.blit(subtitle, (panel_rect.x + 24, panel_rect.y + 68))

    left_column = [
        ("Drag", "Grab a ball and throw it back into the scene."),
        ("W A S D", "Change gravity direction on the fly."),
        ("1 / 2 / 3", "Swap between random, cascade, and orbit presets."),
        ("Space / B", "Spawn one ball or a whole burst."),
    ]
    right_column = [
        ("P / Step", "Pause and advance one simulation tick at a time."),
        ("T / Trails", "Toggle motion trails for a cleaner read."),
        ("H / HUD", "Show or hide the live stats panel."),
        ("I / Help", "Toggle this overlay whenever you need it."),
    ]

    def draw_help_column(items, start_x):
        y = panel_rect.y + 122
        for label, text in items:
            label_surface = font.render(label, True, ACCENT_MINT)
            desc_surface = small_font.render(text, True, TEXT_SOFT)
            screen.blit(label_surface, (start_x, y))
            screen.blit(desc_surface, (start_x, y + 24))
            y += 70

    draw_help_column(left_column, panel_rect.x + 24)
    draw_help_column(right_column, panel_rect.x + 278)

    footer = small_font.render("Drag the window itself to inject a subtle shake impulse into the system.", True, TEXT_FAINT)
    screen.blit(footer, (panel_rect.x + 24, panel_rect.bottom - 34))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Engine — Interactive Sandbox")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 20)
big_font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 54)

HEADER_RECT = pygame.Rect(22, 20, 468, 176)
STATS_RECT = pygame.Rect(WIDTH - 324, 20, 302, 252)
CONTROLS_RECT = pygame.Rect(22, HEIGHT - 116, WIDTH - 44, 94)

gravity_slider = Slider(34, HEIGHT - 86, 240, 0, 1400, BASE_GRAVITY, "Gravity", "{:.0f}")
time_slider = Slider(310, HEIGHT - 86, 180, 0.35, 1.8, 1.0, "Time Scale", "{:.2f}x")
trail_slider = Slider(526, HEIGHT - 86, 180, 8, 36, MAX_TRAIL, "Trail", "{:.0f}")

scene_buttons = {
    ScenePreset.RANDOM: Button(HEADER_RECT.x + 18, HEADER_RECT.bottom - 44, 118, 32, "Random"),
    ScenePreset.CASCADE: Button(HEADER_RECT.x + 146, HEADER_RECT.bottom - 44, 118, 32, "Cascade"),
    ScenePreset.ORBIT: Button(HEADER_RECT.x + 274, HEADER_RECT.bottom - 44, 118, 32, "Orbit"),
}

burst_button = Button(744, HEIGHT - 78, 74, 40, "Burst")
step_button = Button(826, HEIGHT - 78, 68, 40, "Step")
pause_button = Button(902, HEIGHT - 78, 78, 40, "Pause")
trails_button = Button(988, HEIGHT - 78, 78, 40, "Trails")
hud_button = Button(1074, HEIGHT - 78, 64, 40, "HUD")
help_button = Button(1146, HEIGHT - 78, 94, 40, "Help")

current_preset = ScenePreset.RANDOM
balls = create_balls(current_preset)
direction = GravityDirection.DOWN
direction_names = ["DOWN", "UP", "LEFT", "RIGHT"]
direction_arrows = {
    GravityDirection.DOWN: "↓",
    GravityDirection.UP: "↑",
    GravityDirection.LEFT: "←",
    GravityDirection.RIGHT: "→",
}

show_hud = True
show_trails = True
show_help = False
paused = False
step_once = False

dragging_ball = None
drag_offset_x = 0.0
drag_offset_y = 0.0
drag_last_x = 0.0
drag_last_y = 0.0
throw_velocity = None

last_window_x, last_window_y = 0, 0
first_frame = True
visual_phase = 0.0
simulation_time = 0.0
collision_count = 0
energy_history = deque(maxlen=140)


def reset_scene():
    energy_history.clear()
    return create_balls(current_preset)


running = True
while running:
    dt = BASE_DT * time_slider.value
    gravity_strength = gravity_slider.value
    trail_limit = int(trail_slider.value)
    mx, my = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    visual_phase += BASE_DT * 0.9

    try:
        import pygame._sdl2 as sdl2

        win = sdl2.Window.from_display_module()
        win_x, win_y = win.position
    except Exception:
        win_x, win_y = 0, 0

    if not first_frame:
        delta_x = win_x - last_window_x
        delta_y = win_y - last_window_y
        if abs(delta_x) > 0 or abs(delta_y) > 0:
            for ball in balls:
                if ball is not dragging_ball:
                    ball.vx += delta_x * 1.4
                    ball.vy += delta_y * 1.4

    last_window_x, last_window_y = win_x, win_y
    first_frame = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                balls.append(spawn_ball())
            elif event.key == pygame.K_b:
                for _ in range(4):
                    balls.append(spawn_ball())
            elif event.key == pygame.K_r:
                balls = reset_scene()
            elif event.key == pygame.K_c:
                balls.clear()
                energy_history.clear()
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_h:
                show_hud = not show_hud
            elif event.key == pygame.K_t:
                show_trails = not show_trails
            elif event.key == pygame.K_i:
                show_help = not show_help
            elif event.key == pygame.K_PERIOD:
                step_once = True
            elif event.key == pygame.K_1:
                current_preset = ScenePreset.RANDOM
                balls = reset_scene()
            elif event.key == pygame.K_2:
                current_preset = ScenePreset.CASCADE
                balls = reset_scene()
            elif event.key == pygame.K_3:
                current_preset = ScenePreset.ORBIT
                balls = reset_scene()
            elif event.key == pygame.K_w:
                direction = GravityDirection.UP
            elif event.key == pygame.K_s:
                direction = GravityDirection.DOWN
            elif event.key == pygame.K_a:
                direction = GravityDirection.LEFT
            elif event.key == pygame.K_d:
                direction = GravityDirection.RIGHT

    for preset, button in scene_buttons.items():
        if button.update(mx, my, pressed):
            current_preset = preset
            balls = reset_scene()

    if burst_button.update(mx, my, pressed):
        for _ in range(4):
            balls.append(spawn_ball())
    if step_button.update(mx, my, pressed):
        step_once = True
    if pause_button.update(mx, my, pressed):
        paused = not paused
    if trails_button.update(mx, my, pressed):
        show_trails = not show_trails
    if hud_button.update(mx, my, pressed):
        show_hud = not show_hud
    if help_button.update(mx, my, pressed):
        show_help = not show_help

    gravity_slider.update(mx, my, pressed)
    time_slider.update(mx, my, pressed)
    trail_slider.update(mx, my, pressed)

    if not show_trails:
        for ball in balls:
            ball.trail.clear()

    interactive_rects = [
        gravity_slider.dragging,
        time_slider.dragging,
        trail_slider.dragging,
        burst_button.rect.collidepoint(mx, my),
        step_button.rect.collidepoint(mx, my),
        pause_button.rect.collidepoint(mx, my),
        trails_button.rect.collidepoint(mx, my),
        hud_button.rect.collidepoint(mx, my),
        help_button.rect.collidepoint(mx, my),
    ]
    interactive_rects.extend(button.rect.collidepoint(mx, my) for button in scene_buttons.values())

    if pressed[0] and not any(interactive_rects):
        if dragging_ball is None:
            for ball in reversed(balls):
                if math.hypot(ball.x - mx, ball.y - my) < ball.radius:
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
            throw_velocity = (mouse_dx / BASE_DT, mouse_dy / BASE_DT)

            dragging_ball.x = max(dragging_ball.radius, min(WIDTH - dragging_ball.radius, dragging_ball.x))
            dragging_ball.y = max(dragging_ball.radius, min(GROUND_Y - dragging_ball.radius, dragging_ball.y))
    else:
        if dragging_ball is not None and throw_velocity is not None:
            dragging_ball.vx = throw_velocity[0]
            dragging_ball.vy = throw_velocity[1]
        dragging_ball = None
        throw_velocity = None

    simulate_frame = (not paused) or step_once
    collision_count = 0
    if simulate_frame:
        simulation_time += dt
        for ball in balls:
            if ball is dragging_ball:
                continue
            apply_gravity(ball, direction, gravity_strength, dt)
            ball.x += ball.vx * dt
            ball.y += ball.vy * dt
            ball.vx *= DAMPING
            ball.vy *= DAMPING
            check_bounds(ball)

            if show_trails:
                ball.trail.append((ball.x, ball.y))
                if len(ball.trail) > trail_limit:
                    ball.trail.pop(0)
            else:
                ball.trail.clear()

        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if resolve_collision(balls[i], balls[j]):
                    collision_count += 1

        step_once = False

    ke, pe = compute_energy(balls, gravity_strength)
    total_energy = ke + pe
    avg_speed = average_speed(balls)
    if simulate_frame or not energy_history:
        energy_history.append(total_energy)

    draw_vertical_gradient(screen, BG_TOP, BG_BOTTOM)
    draw_motion_ribbons(screen, visual_phase, direction)
    draw_glow(screen, (WIDTH * 0.2, HEIGHT * 0.18), ACCENT, 140)
    draw_glow(screen, (WIDTH * 0.82, HEIGHT * 0.28), ACCENT_SOFT, 110)
    draw_glow(screen, (WIDTH * 0.5, HEIGHT * 0.78), (242, 209, 152), 90)

    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.line(screen, GROUND_LINE, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    for ball in balls:
        if show_trails and ball.trail:
            for idx, (tx, ty) in enumerate(ball.trail):
                alpha_t = (idx + 1) / max(1, len(ball.trail))
                radius = max(2, int(ball.radius * alpha_t * 0.9))
                trail_surface = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(
                    trail_surface,
                    (*ball.color, int(120 * alpha_t)),
                    (trail_surface.get_width() // 2, trail_surface.get_height() // 2),
                    radius,
                )
                screen.blit(trail_surface, (tx - trail_surface.get_width() / 2, ty - trail_surface.get_height() / 2))

        shadow = pygame.Surface((int(ball.radius * 3), int(ball.radius)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 32), shadow.get_rect())
        screen.blit(shadow, (ball.x - shadow.get_width() / 2, GROUND_Y - shadow.get_height() / 2))

        draw_glow(screen, (int(ball.x), int(ball.y)), ball.color, int(ball.radius * 2.4))
        pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), int(ball.radius))
        pygame.draw.circle(screen, (255, 245, 240), (int(ball.x - ball.radius * 0.25), int(ball.y - ball.radius * 0.28)), max(2, int(ball.radius * 0.22)))
        pygame.draw.circle(screen, (255, 255, 255), (int(ball.x), int(ball.y)), int(ball.radius), 2)

        if ball is dragging_ball:
            pygame.draw.circle(screen, ACCENT_MINT, (int(ball.x), int(ball.y)), int(ball.radius) + 5, 3)
        elif ball.restitution > 0.95:
            pygame.draw.circle(screen, (255, 224, 180), (int(ball.x), int(ball.y)), int(ball.radius) + 3, 2)

    if dragging_ball:
        anchor = (int(dragging_ball.x), int(dragging_ball.y))
        pygame.draw.line(screen, ACCENT_SOFT, anchor, (mx, my), 2)
        pygame.draw.circle(screen, ACCENT_MINT, (mx, my), 5)
        if throw_velocity:
            throw_text = font.render(f"Throw {throw_velocity[0]:.0f}, {throw_velocity[1]:.0f}", True, ACCENT_SOFT)
            screen.blit(throw_text, (mx + 20, my - 24))

    draw_card(screen, HEADER_RECT, PANEL, ACCENT)
    title = title_font.render("Physics Engine", True, TEXT)
    subtitle = font.render("Interactive simulation sandbox", True, TEXT_SOFT)
    blurb = small_font.render("Rigid bodies, scene presets, and energy-aware motion in one sleek loop.", True, TEXT_FAINT)
    screen.blit(title, (HEADER_RECT.x + 18, HEADER_RECT.y + 16))
    screen.blit(subtitle, (HEADER_RECT.x + 20, HEADER_RECT.y + 66))
    screen.blit(blurb, (HEADER_RECT.x + 20, HEADER_RECT.y + 95))
    screen.blit(small_font.render("Scene presets", True, TEXT_SOFT), (HEADER_RECT.x + 18, HEADER_RECT.bottom - 67))
    for preset, button in scene_buttons.items():
        button.draw(screen, small_font, mx, my, active=(current_preset == preset))

    if show_hud:
        draw_card(screen, STATS_RECT, PANEL_STRONG, ACCENT_SOFT)

        lines = [
            ("Scene", current_preset.name.title()),
            ("Time", f"{simulation_time:4.1f}s"),
            ("Balls", str(len(balls))),
            ("Gravity", direction_names[direction.value]),
            ("Average Speed", f"{avg_speed:5.1f}"),
            ("Collisions", str(collision_count)),
            ("Total Energy", f"{total_energy:7.0f}"),
        ]
        label_y = STATS_RECT.y + 18
        for label, value in lines:
            screen.blit(small_font.render(label.upper(), True, TEXT_FAINT), (STATS_RECT.x + 18, label_y))
            value_surface = font.render(value, True, TEXT if label != "Total Energy" else ACCENT_MINT)
            screen.blit(value_surface, (STATS_RECT.right - 18 - value_surface.get_width(), label_y - 2))
            label_y += 26

        meter_rect = pygame.Rect(STATS_RECT.x + 18, STATS_RECT.y + 206, STATS_RECT.width - 36, 14)
        pygame.draw.rect(screen, (54, 40, 44), meter_rect, border_radius=999)
        if total_energy > 0:
            ke_ratio = ke / total_energy
            ke_rect = pygame.Rect(meter_rect.x, meter_rect.y, int(meter_rect.width * ke_ratio), meter_rect.height)
            pygame.draw.rect(screen, ACCENT, ke_rect, border_radius=999)
            pe_rect = pygame.Rect(ke_rect.right, meter_rect.y, meter_rect.width - ke_rect.width, meter_rect.height)
            pygame.draw.rect(screen, ACCENT_MINT, pe_rect, border_radius=999)
        screen.blit(small_font.render("Energy Mix", True, TEXT_SOFT), (meter_rect.x, meter_rect.y - 20))

        spark_rect = pygame.Rect(STATS_RECT.x + 18, STATS_RECT.bottom - 58, STATS_RECT.width - 36, 36)
        screen.blit(small_font.render("Energy History", True, TEXT_SOFT), (spark_rect.x, spark_rect.y - 20))
        draw_sparkline(screen, spark_rect, energy_history)

    draw_card(screen, CONTROLS_RECT, PANEL_STRONG, ACCENT)
    gravity_slider.draw(screen, small_font)
    time_slider.draw(screen, small_font)
    trail_slider.draw(screen, small_font)
    burst_button.draw(screen, small_font, mx, my)
    step_button.draw(screen, small_font, mx, my, active=paused)
    pause_button.draw(screen, small_font, mx, my, active=paused)
    trails_button.draw(screen, small_font, mx, my, active=show_trails)
    hud_button.draw(screen, small_font, mx, my, active=show_hud)
    help_button.draw(screen, small_font, mx, my, active=show_help)

    controls_text = small_font.render("WASD gravity  •  1/2/3 scene presets  •  Space add ball  •  R reset  •  C clear  •  I help", True, TEXT_SOFT)
    screen.blit(controls_text, (CONTROLS_RECT.x + 18, CONTROLS_RECT.y + 16))

    gravity_label = big_font.render(f"{direction_arrows[direction]} {direction_names[direction.value]}", True, ACCENT_MINT)
    screen.blit(gravity_label, (WIDTH * 0.5 - gravity_label.get_width() / 2, 28))

    if paused:
        pause_surface = pygame.Surface((190, 58), pygame.SRCALPHA)
        pygame.draw.rect(pause_surface, (14, 20, 31, 220), pause_surface.get_rect(), border_radius=16)
        pygame.draw.rect(pause_surface, (*ACCENT, 255), pause_surface.get_rect(), 1, border_radius=16)
        pause_label = big_font.render("Paused", True, TEXT)
        pause_surface.blit(pause_label, pause_label.get_rect(center=pause_surface.get_rect().center))
        screen.blit(pause_surface, (WIDTH / 2 - pause_surface.get_width() / 2, HEIGHT / 2 - 34))

    if show_help:
        draw_help_overlay(screen, big_font, font, small_font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
