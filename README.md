# Manim Videos

The code for generating my manim videos, as well as the mp4 outputs.

## Generating videos using Manim

First, install Manim:

```nix
{ pkgs, ... }:

{
  environment.systemPackages = [
    pkgs.manim
  ];
}
```

Then run manim, for example:

```sh
manim render -pqh hello-world/scene.py SquareToCircle
```
