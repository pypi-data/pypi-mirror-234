# ufo_draw

Allows you to quickly draw feynman diagrams from ufo model files.

## Installation

```bash
pip install ufo_draw # Install it
```
with optional `--user` or `--break-system-packages`. 
However due to the amount of dependencies it might be better to install it using pipx to have dependencies in isolated versions

```bash
pipx install ufo_draw
```

## Example

```
ufo_draw --initial "nu_e nu_e_bar" --final "nu_e nu_e_bar" -o diagram -m ufo_sm
```
creates following diagrams via [pyfeyn2](https://github.com/APN-Pucky/pyfeyn2) from the [ufo_sm](https://github.com/APN-Pucky/ufo_sm) model using [pyqgraf](https://github.com/APN-Pucky/pyqgraf).

![diag0](./img/diagram_0.png)
![diag1](./img/diagram_1.png)
