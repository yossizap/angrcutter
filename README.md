## AngrCutter

<p align="center">
    <img src="resources/angrcutter.png"/>
</p>

### About

Cutter debug session integration with [angr](https://github.com/angr/angr) using the [angrdbg](https://github.com/andreafioraldi/angrdbg)
API.

### Installation
Simply checkout or download the repository and copy the angrcutter folder to your cutter plugins directory ([locating the plugins directory](https://github.com/radareorg/cutter/blob/master/docs/source/plugins.rst#loading-and-overview)).

#### Dependencies

AngrCutter depends on [angr](https://github.com/angr/angr) and [angrdbg](https://github.com/andreafioraldi/angrdbg),
to install run:

```
python3 -m pip install angr
python3 -m pip install angrdbg
```

### Other Debuggers

If you want to use angr in other debuggers take a look at [angrdbg](https://github.com/andreafioraldi/angrdbg)
