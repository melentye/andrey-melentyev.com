Title: Python environments and where to find them
Tags: python
Modified: 2017-11-26 23:39
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

`pip freeze` command exports the list of installed packages. The output of this command saved in a
[requirements.txt file](https://pip.pypa.io/en/stable/user_guide/#requirements-files) can be stored in a version
control system allowing multiple developers to keep their package versions in sync. Example:

    $ pip freeze
    matplotlib==2.1.0
    numpy==1.13.3
    pandas==0.21.0
    scipy==1.0.0
    seaborn==0.8.1

### virtualenv

> [virtualenv](https://virtualenv.pypa.io/en/stable/) is a tool to create isolated Python environments.

virtualenv can be installed with `pip install virtualenv`. Some things that virtualenv takes care of when a new
environment is created:

* `python` executable is copied to the `ENV/bin` directory.
* `ENV/lib` and `ENV/include` are populated with supporting files.
* `pip` is installed into `ENV/bin` and
   [it knows how to install packages in this virtualenv](https://stackoverflow.com/questions/27079235/how-does-pip-know-about-virtualenv-and-where-to-install-packages).

Sample usage:

    $ virtualenv ~/virtualenvs/pelican
    Using base prefix '/Users/andrey.melentyev/.pyenv/versions/3.6.3'
    New python executable in /Users/andrey.melentyev/virtualenvs/pelican/bin/python3.6
    Also creating executable in /Users/andrey.melentyev/virtualenvs/pelican/bin/python
    Installing setuptools, pip, wheel...done.elentyev/tmp/jenkins-jobs/bin/python
    Installing setuptools, pip, wheel...done.

    $ source ~/virtualenvs/pelican/bin/activate

    $ pip install pelican

after running the above, Pelican is installed in a virtual environment named "pelican" in the directory
`$HOME/virtualenvs/pelican`, leaving my other Python installations unchanged. A nice side effect of using virtualenv
like this is that super-user priveleges are no longer required in order to install packages.

To create a virtual environment with a specific Python version, use the `-p` argument:

    virtualenv -p /usr/local/bin/python3 ~/virtualenvs/yourenv

Virtual environments can be stored anywhere, one approach could be to store them in the `~/virtualenvs`, another
would be to put them in the directory of the projects where they are used.

### pyenv

> [pyenv](https://github.com/pyenv/pyenv) lets you easily switch between multiple versions of Python. It's simple,
> unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.

pyenv supports both Python 2.7.x and 3.x.
[Miniconda]({filename}/2017-11-26_python-environments-and-where-to-find-them.md#Miniconda) can be treated as yet
another Python version: it can be installed via pyenv with `pyenv install miniconda3-4.3.27` and then activated as
usual. Same goes for [Anaconda]({filename}/2017-11-26_python-environments-and-where-to-find-them.md#Anaconda).

pyenv enables switching between Python versions by using `PYENV_VERSION` environment variable or other means such as
placing a `.python-version` file in a project directory.

#### pyenv-virtualenv

> [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is a pyenv plugin that provides features to manage
> virtualenvs and conda environments for Python on UNIX-like systems.

Like pyenv allows installing Python versions, including Miniconda and Anaconda, pyenv-virtualenv helps manage virtual
environments within Python versions. For a "vanilla" Python distributions, virtualenv will be used, for Miniconda and
Anaconda, pyenv-virtualenv delegates to Conda for environment management.

Note that you don't need pyenv-virtualenv to use pyenv and virtualenv together, the plugin just makes it easier.

### Conda

[Conda](https://conda.io/docs/) is a package manager similar to pip. Unlike pip, Conda is not just for Python packages,
which turns out to be very useful for installing things like [MKL](https://docs.anaconda.com/mkl-optimizations/).

Conda packages are hosted on [Conda Forge](https://conda-forge.org/). In my experience, Conda Forge sometimes has
slightly outdated versions of some Python packages in comparison to PyPI, but it could also be a sampling error. That
is compensated by Conda's ability to install packages with pip.

An alternative to pip's `requirements.txt` file in Conda is `environment.yml` file:

    :::yaml
    name: my-env
    dependencies:
      - numpy
      - pandas
      - pip:
        - matplotlib
        - seaborn

in the example above, numpy and pandas will be installed from Conda Forge while matplotlib and seaborn will be fetched
by pip from PyPI.

Conda doesn't manage Python versions, meaning that you can't say "Hey, Conda, install me fresh Python". Conda
itself is distributed with a Python installation: as a part of Miniconda or Anaconda.

### Miniconda

As we briefly mentioned, [Miniconda](https://conda.io/docs/glossary.html#miniconda) is a Python distribution with Conda
and some useful packages.

### Anaconda

[Anaconda](https://www.anaconda.com/distribution/) is a Python distribution for data science. It comes with a
number of popular data analysis and machine learning packages pre-installed. It features a nice GUI for managing
libraries and environments and with useful tools like
[Jupyter notebook](https://jupyter-notebook.readthedocs.io/en/stable/) and
[Spyder IDE](https://pythonhosted.org/spyder/).

Anaconda allows installing different Python versions. For package management and virtual environments Anaconda uses Conda.

Note that if you use the graphical installer, it will update your `$HOME/.bash_profile` and prepend Anaconda
directory to your `PATH` (which you can of course later revert back if that's undesired). Installing with `brew cask`
is another option and then the `PATH` variable is not updated.

### Docker

Docker doesn't really belong in the list of Python environment management tools but it comes in handy to enable
reproducibility when it's not just Python packages play a role in the environment. An example could be a deep learning
setup where Keras uses Tensorflow which runs so much faster with GPU acceleration with CUDA. Keras and Tensorflow
can be installed as Python packages but not CUDA.

What about CUDA? Well, one way to solve it is to package CUDA Toolkit
and supporting libraries in a Docker image, which is exactly what [nvidia/cuda](https://hub.docker.com/r/nvidia/cuda/)
is about. And then build another Docker image on top of that, installing your favorite flavor of Python and
package management tools:

    :::Dockerfile
    FROM nvidia/cuda:9.0-cudnn7-devel

    # Setup build environment
    RUN apt-get update --fix-missing && \
        apt-get install -y build-essential cmake wget ca-certificates git

    # Install Miniconda
    RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
        wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
        /bin/bash ~/miniconda.sh -b -p /opt/conda && \
        rm ~/miniconda.sh

    ENV PATH /opt/conda/bin:$PATH

    # Install Python packages
    RUN conda install -y tensorflow-gpu keras-gpu ipython

    # A nicer Python REPL
    ENTRYPOINT ["ipython"]

In order for the resulting image to actually work with CUDA, it needs to be ran using
[nvidia-docker](https://github.com/NVIDIA/nvidia-docker). This `Dockerfile` is just an example, if it's reproducibility
that we care about, it also makes sense to pin the versions of the installed software packages.

## Putting it all together

Tool             | Manage Python versions | Install Python packages | Manage Python virtual environments
---------------- |:----------------------:|:-----------------------:|:---------------------------------:
pip              | No                     | Yes                     | No
virtualenv       | No                     | No                      | Yes
pyenv            | Yes                    | No                      | No
pyenv-virtualenv | No                     | No                      | Yes
Conda            | No                     | Yes                     | Yes
Anaconda         | Yes                    | Yes                     | Yes

## Practical advice

### How to find out what is currently being used

To find out which version of Python is currently active, one can use `python --version`:

    $ python --version
    Python 2.7.10

alternatively, if I activate one of my other environments:

    $ python --version
    Python 3.6.2 :: Continuum Analytics, Inc.

It's a start, but where does this version come from? [which](https://tldr.ostera.io/which) command comes to the rescue:

    $ which --all python
    /Users/andrey.melentyev/.pyenv/shims/python
    /usr/bin/python

the first line of the output is the full path to the executable that will be ran when I type `python` in the command
line. The subsequent lines are some other `python` executables that are shadowed by the first one. In this case we
notice that pyenv-managed Python is at the top. We can query pyenv to find out more:

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
* [Conda](https://conda.io/docs/user-guide/tasks/use-r-with-conda.html) (again!) for R
