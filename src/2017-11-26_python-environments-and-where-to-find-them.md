Title: Python environments and where to find them
Tags: python
Modified: 2017-11-26 14:29
Status: draft
Summary: Taking care of Python environments can be hard and the variety of tools overwhelming. But it doesn't have to be!

Books, tutorials and online courses often make suggestions on how to set up a Python environment. Some recommend using
[conda](https://conda.io/docs/), some [virtualenv](https://virtualenv.pypa.io/en/stable/) or
[pyenv](https://github.com/pyenv/pyenv). Which one to choose? Is the system Python installation that most of the modern
operating systems have useless? The post unravels the mystery neat Python environments and teaches us to take care of
them.

One way to introduce some structure into the variety of the Python environment management tools is
to categorize them by the use case they are trying to solve:

* Installing Python packages.
* Managing Python versions, making it possible, for example, to have Python 3.5 installed at the same time as
  Python 3.6.
* Maintaining isolated Python environments, each environment having their own set of packages and allowing to use
  different versions of libraries in different projects.

### pip

[PyPA](https://www.pypa.io/en/latest/) is the Python Packaging Authority,
[PyPI](https://pypi.python.org/pypi) is the official Python Package Index and [pip](https://pip.pypa.io/en/stable/) is
the PyPA-recommended tool to install packages from PyPI. It is shipped with modern versions of Python and installed by
default when virtualenv is used.

pip can export the list of installed packages into a
[requirements.txt file](https://pip.pypa.io/en/stable/user_guide/#requirements-files) which can be stored in a version
control system allowing multiple developers to keep their package versions in sync.

### virtualenv

Allows to maintain Python *environments* where each environment has a dedicated set of installed packages.

Some things that `virtualenv` does when a new environment is created:

* Current `python` executable is copied to the `ENV/bin` directory.
* `ENV/lib` and `ENV/include` are populated with supporting files.
* `pip` is installed into `ENV/bin` and
   [it knows how to install packages in the right place](https://stackoverflow.com/questions/27079235/how-does-pip-know-about-virtualenv-and-where-to-install-packages).

### pyenv

**pyenv**

[Miniconda]({filename}/2017-11-26_python-environments-and-where-to-find-them.md#Miniconda) can be treated as yet
another Python version: it can be installed via pyenv with `pyenv install miniconda3-4.3.27` and then activated as
usual. Same applies to [Miniconda]({filename}/2017-11-26_python-environments-and-where-to-find-them.md#Anaconda)

#### pyenv virtualenv

### Conda

[**Conda**](https://conda.io/docs/) is a package manager for Python similar to pip. Unlike pip, Conda can also install
other software which turns out to be very useful for things like [MKL](https://docs.anaconda.com/mkl-optimizations/).

Conda packages are hosted on [Conda Forge](https://conda-forge.org/). In my experience, Conda Forge sometimes has
slightly outdated versions of some Python packages in comparison to PyPI, but it could also be a sampling error.

Conda doesn't manage Python versions, meaning that you can't say "Hey, Conda, install me fresh Python". Conda
itself is distributed with a Python installation: as a part of Miniconda or Anaconda.

### Miniconda

As we briefly mentioned, [Miniconda](https://conda.io/docs/glossary.html#miniconda) is a Python distribution with Conda
and some useful packages.

### Anaconda

[Anaconda](https://www.anaconda.com/distribution/) is a Python distribution for data science. It comes with a
number of popular data analysis and machine learning packages pre-installed (others can be added with Conda).
Anaconda features a nice GUI for managing libraries and environments and with useful tools like
[Jupyter notebook](https://jupyter-notebook.readthedocs.io/en/stable/) and
[Spyder IDE](https://pythonhosted.org/spyder/).

Anaconda supports environments, allowing to have different Python versions and isolated package environments too.
For package management Anaconda uses Conda

Note that if you use the graphical installer, it will update your `$HOME/.bash_profile` and prepend Anaconda
directory to your `PATH` (which you can of course later revert back if that's undesired). Installing with `brew cask`
is another option and then the `PATH` variable is not updated.

### Docker

## Comparison table

Tool             | Manage Python versions | Install Python packages | Manage Python package environments
---------------- | ---------------------- | ----------------------- | ----------------------------------
pip              | No                     | Yes                     | No
virtualenv       | No                     | No                      | Yes
pyenv            | Yes                    | No                      | No
pyenv-virtualenv | No                     | No                      | Yes
Conda            | No                     | Yes                     | Yes
Anaconda         | Yes                    | Yes                     | Yes

## Practical advice

### How to find out what is currently being used

To find out which version of Python is currently active, one can use `python --version`:

    :::shell
    $ python --version
    Python 2.7.10

alternatively, if I activate one of my other environments:

    :::shell
    $ python --version
    Python 3.6.2 :: Continuum Analytics, Inc.

It's a start, but where does this version come from? [which](https://tldr.ostera.io/which) command comes to the rescue:

    :::shell
    $ which --all python
    /Users/andrey.melentyev/.pyenv/shims/python
    /usr/bin/python

the first line of the output is the full path to the executable that will be ran when I type `python` in the command
line. The subsequent lines are some other `python` executables that are shadowed by the first one. In this case we
notice that pyenv-managed Python is at the top. We can query pyenv to find out more:

    :::shell
    $ pyenv version
    some-env-name (set by PYENV_VERSION environment variable)

    $ echo $PYENV_VERSION
    some-env-name

    $ pyenv which python
    /Users/andrey.melentyev/.pyenv/versions/some-env-name/bin/python

### Which one to use

As it happens with software, *it depends*:

* If you do a lot of data science / machine learning type of projects and not that much other Python development,
  Anaconda can be a good start. It has most of the things out of the box and doesn't require learning a new
  command-line tool.
* If you have Python projects with different requirements for Python and packages, go for pyenv or Conda.
* Finally, if you don't program Python, I'm surprised you've made it this far!

### What is the system Python good for

Gosh, I really don't know... on macOS High Sierra in 2017 it's still Python 2.7, same applies to large Linux
distributives like CentOS or Debian. I'd recommend leaving it alone and using a sane Python version with pyenv
or Conda for development.

## Environment management tools for other languages

* [rbenv](https://github.com/rbenv/rbenv) for Ruby
* [scalaenv](https://github.com/scalaenv/scalaenv) for Scala and [sbtenv](https://github.com/sbtenv/sbtenv) for SBT
* [jEnv](http://www.jenv.be/) for Java
* [Stack](https://docs.haskellstack.org/en/stable/README/) for Haskell (it does more than environment management)
* [kerl](https://github.com/kerl/kerl) for Erlang
* [Conda](https://conda.io/docs/user-guide/tasks/use-r-with-conda.html) (again!) for R.
