# Lummao

[Lummao](https://github.com/SaladDais/Lummao) is a toolkit for compiling and executing the Linden Scripting Language as Python. 
It aims to ease testing of LSL code by leveraging Python's existing ecosystem for debugging and testing. Think of it as the less opinionated,
stupider cousin of [LSLForge's unit testing framework](https://github.com/raysilent/lslforge/blob/master/lslforge/eclipse/lslforge/html/unit-test.html).

The runtime is largely handled by the excellent implementation of LSL's basic operations and library functions
from Sei Lisa's [LSL-PyOptimizer](https://github.com/Sei-Lisa/LSL-PyOptimizer).
See [vendor/lslopt](https://github.com/SaladDais/Lummao/tree/master/lummao/vendor/lslopt) for Lummao's vendored copy of LSL-Pyoptimizer.

To see an example input script and its Python output, see the [`test_resources` directory](https://github.com/SaladDais/Lummao/tree/master/tests/test_resources).

## Setup

```bash
pip install --upgrade pip
pip install lummao
```

### From source

```bash
pip install -e .
```

## How

For a real-world example of local LSL testing with Lummao, see <https://github.com/SaladDais/SLGraphPather> or
<https://github.com/SaladDais/SickJoke>'s tests and test coverage reporting.

Along with the python API, a helper `lummao` script is provided that takes in an LSL file and outputs a python file.
It can be invoked like `lummao input.lsl output.py`.

If you just want to run an LSL script from the command-line, the `shellsl` command will be installed alongside `lummao`,
and can be run from the commandline like so:

```
$ shellsl tests/test_resources/lsl_conformance.lsl
All tests passed
```

## Why

If you've ever written a sufficiently complicated system in LSL, you know how annoying it is to debug your scripts
or be sure if they're even correct. Clearly the sanest way to bring sanity to your workflow is to convert your LSL
scripts to Python, so you can mock LSL library functions and use Python debuggers. Hence, the name "Lummao".

## TODO

* Symbol shadowing behavior is not correct. Python has very different shadowing rules.
* Provide mock helpers for: 
* * inter-script communication
* * auto-stubs for all functions

## License

GPLv3

### Licensing Clarifications

The output of the compiler necessarily links against the GPL-licensed runtime code from LSL-PyOptimizer for
functionality, and LSL-PyOptimizer does not provide a library exception in its license.
You should assume that any LSL converted to Python by the compiler and any testcases you write exercising
them must _also_ be distributable under the GPL.

In short: If or when you distribute your testcases, you must _also_ allow distribution of their direct
dependencies (your LSL scripts) under the terms of the GPL. This does not necessarily
change the license of your LSL scripts themselves, or require consumers of your scripts to license
their own scripts under the GPL. It is perfectly possible to have an otherwise MIT-licensed or proprietary
library with a GPL-licensed test suite. No distribution of testcases == no requirement to distribute under the GPL.

Suggested reading to understand your rights and obligations under the GPL when using a GPL-licensed test suite:

* https://www.gnu.org/licenses/gpl-3.0.html
* https://opensource.stackexchange.com/questions/7503/implications-of-using-gpl-licenced-code-only-during-testing
* https://opensource.stackexchange.com/questions/4112/using-gpl-library-in-unit-test-suite-of-open-source-library
