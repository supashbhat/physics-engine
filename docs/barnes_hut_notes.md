# Barnes-Hut Notes

This workstream extends the physics engine from local rigid-body interaction into many-body gravity and scaling.

## Why Barnes-Hut

Direct gravity between `N` bodies is `O(N^2)`. That is fine for dozens or a few hundred particles, but it becomes expensive quickly. Barnes-Hut reduces the force pass by grouping distant regions of mass and approximating them with a single center-of-mass interaction, leading to roughly `O(N log N)` behavior.

## Current Implementation

- 2D quadtree with recursive subdivision
- Center-of-mass aggregation at each node
- Barnes-Hut force traversal with configurable `theta`
- Direct exact-force baseline for comparison
- Leapfrog-style stepping for simple multi-step timing comparisons
- Benchmark script that compares:
  - exact vs Barnes-Hut force-pass time
  - approximate vs exact integration-loop runtime
  - RMS acceleration error

## What To Look For

- smaller `theta` values improve accuracy but reduce speedup
- larger `theta` values improve speed but increase approximation error
- the useful range is where timing improves materially while force error remains interpretable

## Next Steps

- add a visual N-body sandbox rather than only benchmark output
- expose `theta` interactively
- benchmark larger particle counts and write results out as plots
- connect the Barnes-Hut work to a future browser-facing demo surface
