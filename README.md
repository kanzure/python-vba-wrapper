# python-vba-wrapper

**python-vba-wrapper** is a python ctypes wrapper for the VBA emulator.

## installing

Follow the build instructions in the README for
[vba-linux](https://github.com/kanzure/vba-linux). Future versions will be
included through setup.py by default, but for now this is a manual procedure. Continue installing by the following steps.

```bash
pip install -U vba-wrapper
```

or

```bash
git clone git://github.com/kanzure/python-vba-wrapper.git
cd python-vba-wrapper/
python setup.py install
```

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
