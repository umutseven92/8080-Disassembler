# 8080-Disassembler
A simple disassembler for the Intel 8080, writen in Python.

## Usage
From the */src* folder, do;

```python
python dis.py path.to.rom
```
This will put the dissasembled file in the */roms* folder, with a *dis_* prefix.

*/roms* folder already contains the Space Invaders ROM, for testing purposes. To test it out;

```python
python dis.py roms/invaders
```





