# Physics Engine Development Roadmap

## Project Evolution

This document traces the development journey from a simple kinematics calculator to a full 3D interactive physics engine.

---

## Phase 1: Kinematics Calculator
**Goal:** Build a simple 2D projectile motion simulator

- Basic velocity/position calculations
- Euler integration
- Gravity as a constant force
- Terminal output only

**Status:** ✅ Complete

---

## Phase 2: 2D Physics Engine
**Goal:** Add collision detection and multi-body dynamics

- Rigid body dynamics with mass and restitution
- Ground plane collisions
- Sphere-sphere collision detection
- RK4 integration for higher accuracy
- Energy conservation benchmarks

**Status:** ✅ Complete

---

## Phase 3: Interactive Visualization
**Goal:** Make it visual and interactive

- Pygame real-time visualization
- Mouse dragging to throw balls
- WASD gravity direction control
- Window drag inertia (shake effect)
- Energy display and trails

**Status:** ✅ Complete

---

## Phase 4: Web-Based Demo
**Goal:** Deploy to web for instant access

- JavaScript/Canvas implementation
- Live demo on portfolio site
- Click and drag interaction
- Mobile-responsive design

**Status:** ✅ Complete

---

## Phase 5: 3D Physics Engine
**Goal:** Upgrade to full 3D with intuitive controls

### Planned Features:

| Feature | Description | Status |
|---------|-------------|--------|
| 3D Rendering | Three.js with WebGL | 🔄 In Progress |
| 3D Spheres | Realistic ball rendering with lighting | 🔄 In Progress |
| Rotation Controls | WASD rotates the camera/view | 🔄 In Progress |
| Gravity Vector | 3D gravity (X, Y, Z components) | 🔄 In Progress |
| Window Shake | Detect window movement for inertia | 🔄 In Progress |
| Separate Demo Page | Full-screen interactive experience | 🔄 In Progress |

### Technical Implementation

**3D Environment:**
- Use Three.js for WebGL rendering
- Perspective camera with orbital controls
- Point lights and ambient lighting for realism

**Physics in 3D:**
- Extend 2D physics to 3D vectors (x, y, z)
- Sphere-sphere collision in 3D
- Ground plane at y = -5
- Walls at x = ±8, z = ±8

**Controls:**
- WASD: Rotate view around scene
- Shift/Ctrl: Move camera up/down
- Mouse drag: Throw balls in 3D space
- Number keys: Change gravity direction (1=down, 2=up, 3=left, 4=right, 5=forward, 6=back)

**Window Shake:**
- Track window position via requestAnimationFrame
- Apply impulse to all balls based on window movement delta
- Same physics as 2D version but in 3D

---

## Phase 6: CUDA GPU Acceleration (Future)
**Goal:** Scale to 10,000+ particles

- Parallel collision detection
- GPU-based integration
- Real-time performance metrics

---

## How to View the Project

| Version | Link |
|---------|------|
| C++ Engine | [GitHub Repo](https://github.com/supashbhat/physics-engine) |
| Python Demo | Run `python3 visualize_realtime.py` |
| Web Demo (2D) | [Portfolio Site](https://supashbhat.github.io) |
| Web Demo (3D) | Coming soon: `/3d-physics.html` |

---

## Development Timeline

| Phase | Started | Completed |
|-------|---------|-----------|
| Phase 1 | March 30, 2026 | March 30, 2026 |
| Phase 2 | March 30, 2026 | March 30, 2026 |
| Phase 3 | March 30, 2026 | March 30, 2026 |
| Phase 4 | March 30, 2026 | March 30, 2026 |
| Phase 5 | March 30, 2026 | March 31, 2026 |
| Phase 6 | TBD | TBD |

---

*This project is part of an ongoing exploration into computational physics, numerical methods, and interactive simulation.*
