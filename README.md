# Physics Engine

Physics Engine is a computational physics sandbox built around rigid-body simulation, numerical integration, and interactive visualization. It combines a C++ core with Python and browser-facing surfaces so the same physical ideas can be explored through benchmarks, local sandboxes, and public demos.

The project started as a way to compare integrators and collision handling in a more tangible setting. It now also includes the beginning of a Barnes-Hut workstream for many-body gravity and scaling experiments.

## Highlights

- C++ rigid-body core with Euler and RK4 integration
- Multi-body simulation with circle-circle and ground collision handling
- Benchmark tooling for energy drift and spring-system behavior
- Polished real-time Python sandbox with scene presets, pause/step controls, and live energy feedback
- Browser-facing 2D and 3D demo surfaces connected to the portfolio
- Barnes-Hut benchmark tooling for `O(N^2)` vs `O(N log N)` gravity comparison

## Quick Start

### Build the C++ engine

```bash
git clone https://github.com/supashbhat/physics-engine.git
cd physics-engine
cmake -S . -B build
cmake --build build
./build/physics_engine
```

### Run the real-time sandbox

```bash
pip install pygame
python3 visualize_realtime.py
```

### Run the analysis scripts

```bash
pip install numpy matplotlib
python3 energy_analysis.py
python3 spring_visualize.py
```

### Run the Barnes-Hut benchmark

```bash
python3 barnes_hut_benchmark.py --theta 0.6
```

Add `--write-summary` to save a benchmark snapshot into `docs/`.

## Main Components

### C++ core

- `RigidBody`, `Vec2`, and collision primitives
- Euler and RK4 integrators for direct numerical comparison
- Terminal-native simulation loop for fast iteration
- Benchmark programs that make the integrator tradeoff explicit

### Python sandbox

`visualize_realtime.py` is the most polished local surface in the repository.

- Drag-and-throw interaction
- Scene presets: `Random`, `Cascade`, `Orbit`
- Live gravity, time-scale, and trail controls
- Pause / step workflow
- HUD, help overlay, and energy-history display
- Atmospheric styling so the sandbox reads like a tool instead of a debug window

### Browser demos

- [2D demo](https://supashbhat.github.io/2d-physics.html)
- [3D demo](https://supashbhat.github.io/3d-physics.html)
- [Physics project page](https://supashbhat.github.io/physics-engine.html)

### Barnes-Hut workstream

The Barnes-Hut additions live in:

- `barnes_hut.py`
- `barnes_hut_benchmark.py`
- `docs/barnes_hut_notes.md`

This part of the repo is focused on scaling from small-body interaction toward large gravitational systems through spatial partitioning, center-of-mass approximation, and timing/error tradeoff analysis.

## Sandbox Controls

### Keyboard

- `W A S D` - redirect gravity
- `1 2 3` - switch scene preset
- `Space` - spawn one ball
- `B` - spawn a burst
- `R` - reset the current preset
- `C` - clear the scene
- `P` - pause / resume
- `.` - step one frame while paused
- `T` - toggle trails
- `H` - toggle HUD
- `I` - toggle help overlay

### Mouse

- Drag a ball to reposition and throw it
- Drag the window itself to inject a subtle global impulse

## Repository Map

- `src/` - C++ engine core, collisions, and benchmarks
- `visualize_realtime.py` - polished Pygame sandbox
- `visualize.py` - trajectory plotting
- `energy_analysis.py` - free-fall energy comparison
- `spring_visualize.py` - spring benchmark visualization
- `barnes_hut.py` - Barnes-Hut quadtree, exact gravity baseline, and stepping helpers
- `barnes_hut_benchmark.py` - timing/error comparison script for many-body gravity
- `docs/barnes_hut_notes.md` - Barnes-Hut implementation notes and next steps
- `ROADMAP.md` - project direction and future milestones

## Why This Project Exists

The aim is to make computational physics feel both rigorous and explorable: numerical methods that can be benchmarked seriously, but also interacted with directly. That same idea carries across the browser demos, the Python sandbox, and the newer Barnes-Hut scaling work.

## Roadmap

Current directions include:

- Barnes-Hut visualization and larger `N` benchmarking
- Broader collision and constraint systems
- More unified architecture between the C++ core and interactive surfaces
- Stronger browser-facing demos tied into the portfolio

More detail is available in [ROADMAP.md](ROADMAP.md).
