# python-vba

**python-vba** is a python ctypes wrapper for the VBA emulator.

## installing

```bash
pip install -U vba
```

or

```bash
git clone git://github.com/kanzure/python-vba-wrapper.git
cd python-vba-wrapper/
python setup.py install
```

TODO: instructions for compiling the required version of libvba.

## testing

```bash
nosetests
```

## usage

```python
import vba_wrapper
vba = vba_wrapper.VBA("/home/kanzure/code/pokecrystal/pokecrystal.gbc")
vba.run() # press f12 to get back to python
```

## license

BSD
