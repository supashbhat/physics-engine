# Physics Engine

<div align="center">

**A high-performance rigid-body physics simulator with RK4 integration, real-time visualization, and full interactive features**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C++17](https://img.shields.io/badge/C%2B%2B-17-blue.svg)](https://isocpp.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-green.svg)](https://python.org)

</div>

---

## Overview

A complete rigid-body physics engine built from scratch in C++ with Python visualization. Demonstrates numerical integration methods, collision detection, and real-time interactive simulation.

**Live demos:** [supashbhat.github.io](https://supashbhat.github.io)

---

## Features

### Core Physics (C++)
- **RK4 Integration** — 4th-order Runge-Kutta for high accuracy
- **Euler Integration** — 1st-order method for comparison
- **Rigid Body Dynamics** — Mass, position, velocity, force accumulation
- **Sphere-Sphere Collision** — Impulse-based resolution with restitution
- **Ground Collision** — Plane collision with configurable bounciness
- **Multi-Body Simulation** — 10+ interacting objects

### Python Interactive Demo (Full Features)
- **Drag & Throw** — Click and drag balls, release to throw with velocity
- **Gravity Control** — WASD keys or slider to change gravity direction/strength
- **Window Shake** — Drag the window to apply inertia to all balls
- **Real-time Energy Display** — Kinetic, potential, and total energy tracking
- **Ball Trails** — Visual motion trails for each ball
- **Keyboard Controls** — SPACE (add), R (reset), C (clear), T (toggle display)

### Web Demos
- **2D** — Drag to throw, WASD gravity
- **3D** — Camera controls, 6-direction gravity (keys 1-6)

---

## Quick Start

### C++ Engine
```bash
git clone https://github.com/supashbhat/physics-engine.git
cd physics-engine
mkdir build && cd build
cmake ..
make
./physics_engine
```

### Python Interactive Demo (Full Features)
```bash
cd physics-engine
pip install pygame
python3 visualize_realtime.py
```

**Controls:** Click & drag to throw | WASD gravity | SPACE add | R reset | C clear | Drag window to shake

### Run Benchmarks
```bash
cd build
./benchmark          # Energy conservation (Euler vs RK4)
./spring_benchmark   # Spring-mass system comparison
```

---

## Project Structure

```
physics-engine/
├── src/
│   ├── main.cpp                 # C++ simulation
│   ├── benchmark.cpp            # Energy benchmark
│   ├── spring_benchmark.cpp     # Spring-mass benchmark
│   ├── core/
│   │   ├── Vec2.h/cpp           # 2D vector math
│   │   └── RigidBody.h/cpp      # Physics body
│   ├── dynamics/
│   │   └── Integrator.h/cpp     # Euler & RK4
│   └── collision/
│       └── CollisionDetector.h/cpp
├── visualize_realtime.py        # Full Python demo
├── energy_analysis.py           # Energy plots
├── spring_visualize.py          # Spring visualization
└── CMakeLists.txt
```

---

## Numerical Methods

| Method | Order | Error | Best For |
|--------|-------|-------|----------|
| Euler | 1st | O(dt) | Simple systems |
| RK4 | 4th | O(dt⁴) | High accuracy, oscillatory systems |

**Benchmark Results (Spring-Mass):**
- Euler error at 0.01s: 0.153
- RK4 error at 0.01s: 0.028
- **RK4 is ~100x more accurate**

---

## Why This Matters for Robotics

Modern robotics simulators (MuJoCo, Drake, Bullet) rely on the same concepts:
- Rigid body dynamics for robot arms and manipulators
- Collision detection for obstacle avoidance and grasping
- Numerical integration for stable simulation
- Contact resolution for realistic interactions

---

## Skills Demonstrated

- **C++17** — Object-oriented design, CMake, Git
- **Numerical Methods** — Euler, RK4, error analysis
- **Physics** — Newtonian mechanics, collisions, energy conservation
- **Python** — Pygame, matplotlib, real-time visualization

---

## Live Demos

| Platform | Link | Features |
|----------|------|----------|
| 🌐 2D Web | [supashbhat.github.io/2d-physics.html](https://supashbhat.github.io/2d-physics.html) | Drag to throw, WASD gravity |
| 🌐 3D Web | [supashbhat.github.io/3d-physics.html](https://supashbhat.github.io/3d-physics.html) | Camera controls, 6-direction gravity |
| 🐍 Python | `python3 visualize_realtime.py` | Window shake, energy display, trails |
| 💻 C++ | `./physics_engine` | Terminal simulation, benchmarks |

---

## Development Roadmap

See [ROADMAP.md](ROADMAP.md) for the complete project evolution.

---

## License

MIT License

---

## Author

**Supash Bhat** — UC Berkeley (Physics, Astrophysics, Music)  
[GitHub](https://github.com/supashbhat) | [Portfolio](https://supashbhat.github.io) | supash_bhat@berkeley.edu
```

