# MinCfg

![Tests/Pylint/Mypy](https://github.com/pjz/mincfg/actions/workflows/python-test.yml/badge.svg)

## the Minimum Configuration Handling System

There are many configuration management/definition systems.  This one is mine.
This is an overview.  There are also more formal [docs](https://pjz.github.io/mincfg/).

A set of simple tools to build a configuration system with

The first set are 'sources':
  - DictSource, which takes values from a python dict and is useful for defaults
  - SubsetSource, which returns a subset of another source, to help with merge precedence
  - OSEnvironSource, which parses config values from os.environ into hierarchical dictionaries
  - YamlFileSource, which parses a yaml file into hierarchical dictionaires (`pip install mincfg[yaml]` for support) 
  - INIFileSource, which understands INI files (based on configobj) (`pip install mincfg[ini]` for support)
  - DotEnvSouce, which understands .env files (based on python-dotenv) (`pip install mincfg[env]` for support)
  
The second tool is:
  - MergedConfiguration: which merges multiple configuration sources into a coherent whole

Yes, much more could be done:
  - required keys
  - value validation
  - default parsers
  - default default values (that .get() without a default would default to)
  - more file types (json, ... xml?)
  - sphinx/rtd docs

... PRs accepted!

Much inspiration - and the .get() signature - is taken from everett, but the
implementation is all mine.

### To install

```pip install mincfg```
