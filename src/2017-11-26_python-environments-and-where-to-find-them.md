Title: Python environments and where to find them
Tags: python
Modified: 2017-11-27 23:08
Summary: Taking care of Python environments can be hard and the variety of tools overwhelming. But it doesn't have to be!

Books, tutorials and online courses often make suggestions on how to set up a Python environment. Some recommend using
[Conda](https://conda.io/docs/), some [virtualenv](https://virtualenv.pypa.io/en/stable/) or
[pyenv](https://github.com/pyenv/pyenv). Which one to choose? Why not use the system Python installation that most of
the modern operating systems have?

One way to introduce some structure into the variety of the Python environment management tools is
to categorize them by the use case they are trying to solve:

* Installing Python packages.
* Managing Python versions, making it possible, for example, to have Python 3.5 installed at the same time as
  Python 3.6.
* Maintaining isolated Python environments, each environment having their own set of packages and allowing to use
  different versions of libraries in different projects.

The post walks through some of the popular tools that help create a friendly environment for your Python. The goal is not
to go into the details of how to install and operate each tool but rather to explain when to use it.

[TOC]

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

pip is extremely popular and nearly all major Python libraries and frameworks are published to PyPI.

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
is that super-user privileges are no longer required in order to install packages. This is not a unique feature of
virtualenv, we will get that for free with any of the other tools below.

To create an environment with a specific Python version (which has to be installed first), use the `-p` argument:

    virtualenv -p /usr/local/bin/python3 ~/virtualenvs/yourenv

Virtual environments can be stored anywhere, one approach is to store them in the `~/virtualenvs`, another
is to put the environment in the same directory as the project that uses it.

Refer to the [Getting started](TODO: add link) for more information.

### pyenv

> [pyenv](https://github.com/pyenv/pyenv) lets you easily switch between multiple versions of Python. It's simple,
> unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.

pyenv supports both Python 2.7.x and 3.x.
[Miniconda]({filename}/2017-11-26_python-environments-and-where-to-find-them.md#miniconda) can be treated as yet
another Python version: it can be installed via pyenv with `pyenv install miniconda3-latest` and then activated as
usual. Same goes for [Anaconda]({filename}/2017-11-26_python-environments-and-where-to-find-them.md#anaconda).

Usage:

    $ pyenv install 3.6.0
    Downloading Python-3.6.0.tar.xz...
    -> https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz
    Installing Python-3.6.0...
    Installed Python-3.6.0 to /Users/andrey.melentyev/.pyenv/versions/3.6.0

If you get "ERROR: The Python ssl extension was not compiled. Missing the OpenSSL lib?" under macOS, see
[Github issue](https://github.com/pyenv/pyenv/issues/950#issuecomment-333114076).

    $ pyenv versions
    system
    2.7.10
    3.5.1
    * 3.5.2 (set by /Users/andrey.melentyev/.pyenv/version)
    3.6.0
    3.6.3
    3.6.3/envs/moto

pyenv enables switching between Python versions by using `PYENV_VERSION` environment variable or other means such as
placing a `.python-version` file in a project directory:

    $ PYENV_VERSION=3.6.0 python --version
    Python 3.6.0

### pyenv-virtualenv

> [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is a pyenv plugin that provides features to manage
> virtualenvs and conda environments for Python on UNIX-like systems.

Like pyenv allows installing Python versions, pyenv-virtualenv helps manage virtual environments within Python
versions. For a "vanilla" Python distribution, virtualenv will be used, for Miniconda and Anaconda,
pyenv-virtualenv delegates to Conda.

Note that you don't need pyenv-virtualenv to use pyenv and virtualenv together, the plugin just makes it easier.

### Conda

[Conda](https://conda.io/docs/) is a package manager similar to pip. Unlike pip, Conda is not just for Python packages,
which turns out to be very useful for installing things like [MKL](https://docs.anaconda.com/mkl-optimizations/).

Conda packages are hosted on [Conda Forge](https://conda-forge.org/). In my experience, Conda Forge sometimes has
slightly outdated versions of some Python packages in comparison to PyPI, but it could also be a sampling error. That
is compensated by Conda's ability to install packages with pip.

An alternative to pip's `requirements.txt` file in Conda is the `environment.yml` file:

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

Conda treats Python as any other package, so it's possible to create an environment with an arbitrary Python version:

    $ conda create --name my-friends-env --yes --quiet python=2.7.14

    Package plan for installation in environment /Users/andrey.melentyev/anaconda3/envs/my-friends-env:

    The following NEW packages will be INSTALLED:

        ca-certificates: 2017.08.26-ha1e5d58_0
        certifi:         2017.11.5-py27hfa9a1c4_0
        libcxx:          4.0.1-h579ed51_0
        libcxxabi:       4.0.1-hebd6815_0
        libedit:         3.1-hb4e282d_0
        libffi:          3.2.1-h475c297_4
        ncurses:         6.0-hd04f020_2
        openssl:         1.0.2m-h86d3e6a_1
        pip:             9.0.1-py27h1567d89_4
        python:          2.7.14-h001abdc_23
        readline:        7.0-hc1231fa_4
        setuptools:      36.5.0-py27h2a45cec_0
        sqlite:          3.20.1-h7e4c145_2
        tk:              8.6.7-h35a86e2_3
        wheel:           0.30.0-py27h677a027_1
        zlib:            1.2.11-hf3cbc9b_2

    $ source activate my-friends-env
    $ which python
    /Users/andrey.melentyev/anaconda3/envs/my-friends-env/bin/python
    $ source activate my-friends-env
    $ python --version
    Python 2.7.14 :: Anaconda, Inc.

AWS [has recently announced a new version of the AWS Deep Learning AMI](https://aws.amazon.com/blogs/ai/new-aws-deep-learning-amis-for-machine-learning-practitioners)
where each deep learning framework resides in its own Conda environment. Neat!

### Miniconda

As we briefly mentioned, [Miniconda](https://conda.io/docs/glossary.html#miniconda) is a Python distribution with Conda
and some useful packages. If you liked the movie "Inception", you might also want to install Miniconda using pyenv.

### Anaconda

[Anaconda](https://www.anaconda.com/distribution/) is a Python distribution for data science. It comes with a
number of popular data analysis and machine learning packages pre-installed. It features a nice GUI for managing
libraries and environments and with useful tools like
[Jupyter notebook](https://jupyter-notebook.readthedocs.io/en/stable/) and
[Spyder IDE](https://pythonhosted.org/spyder/).

Anaconda uses Conda to manage Python versions, virtual environments and to install packages.

Note that if you use the graphical installer, it will update your `$HOME/.bash_profile` and prepend Anaconda
directory to your `PATH` (which you can of course later revert back if that's undesired). Installing with `brew cask`
is another option and then the `PATH` variable is not updated.

Refer to the [Installation guide](TODO: add link) and [Getting started](TODO: add link) for more information.

### Docker

Docker doesn't really belong in the list of Python environment management tools but it comes in handy to enable
reproducibility when not only Python packages play a role in the environment. An example could be a deep learning
setup where Keras uses Tensorflow which runs so much faster with GPU acceleration with CUDA. Keras and Tensorflow
can be installed as Python packages but not CUDA.

What about CUDA? Well, one way to solve it is to package CUDA Toolkit
and supporting libraries in a Docker image, which is exactly what [nvidia/cuda](https://hub.docker.com/r/nvidia/cuda/)
is about. And then build another Docker image on top of that, installing your favourite flavour of Python and
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

For the resulting image to actually work with CUDA, it needs to be ran using
[nvidia-docker](https://github.com/NVIDIA/nvidia-docker).

For improved reproducibility, it also makes sense to pin the versions of the software packages installed in the Docker
image. CUDA driver is on the host OS, outside of the Docker container and it's version needs to be managed separately.

The combination of nvidia-docker and cloud infrastructure as code deserves a dedicated article, the takeaway
for this post is that Docker images can be used to fix an environment with a specific Python version and dependencies
as well as non-Python software packages.

## Putting it all together

Tool             | Manage Python versions | Install Python packages | Manage Python virtual environments
---------------- |:----------------------:|:-----------------------:|:---------------------------------:
pip              | No                     | **Yes**                 | No
virtualenv       | No                     | No                      | **Yes**
pyenv            | **Yes**                | No                      | No
pyenv-virtualenv | No                     | No                      | **Yes**
Conda            | **Yes**                | **Yes**                 | **Yes**

From the table it becomes clear that there is more than one way to cover all three main use cases:

* Combination of pyenv, pyenv-virtualenv and pip.
* Conda installed with Miniconda or Anaconda.

## How to find out what is currently being used

### Example 1 - pyenv

To find out which version of Python is currently active, use `python --version`:

    $ python --version
    Python 3.6.3

It's a start, but where does this version come from? [which](https://tldr.ostera.io/which) command comes to the rescue:

    $ which --all python
    /Users/andrey.melentyev/.pyenv/shims/python
    /usr/bin/python

the first line of the output is the full path to the executable that will be run when I type `python` into the command
line. The subsequent lines are some other `python` executables that are shadowed by the first one. In this case, we
notice that pyenv-managed Python is at the top. We can query pyenv to find out more:

    $ pyenv version
    my-fresh-vanilla-python (set by PYENV_VERSION environment variable)

    $ echo $PYENV_VERSION
    my-fresh-vanilla-python

    $ pyenv which python
    /Users/andrey.melentyev/.pyenv/versions/my-fresh-vanilla-python/bin/python

### Example 2 - Anaconda

Check out Python version

    $ python --version
    Python 3.6.3 :: Anaconda, Inc.

Aha, it's an Anaconda. Where is it from?

    $ which python
    /Users/andrey.melentyev/anaconda3/bin/python

What other Conda environments do I have?

    $ conda env list
    # conda environments:
    #
    my-friends-env           /Users/andrey.melentyev/anaconda3/envs/my-friends-env
    root                  *  /Users/andrey.melentyev/anaconda3

### Example 3 - system Python

    $ python --version
    Python 2.7.10

    $ which python
    /usr/bin/python

this may not be the best choice but at least it is a clean slate!

### Some other places to look for snakes

* It's good to check your `$PATH` variable for Python-related things, just run `echo $PATH` and see if something pops up.
* The source of the `$PATH` is most likely in the `$HOME/.bash_profile` file, it's a go-to place if some cleanup is required.

## Which tool to use

As it happens with software, *it depends*:

* If you do a lot of data science, machine learning type of projects and not that much other Python development,
  Anaconda can be a good start. It has most of the things out of the box and doesn't require learning a new
  command-line tool (while still offering one).
* If you have Python projects with different requirements for Python and packages, consider using Conda or pyenv.
* Finally, if you don't program Python, I'm surprised you've made it this far!

It is easier to say which tools not to use together:

* If you decided to use Conda, using virtualenv is unnecessary and will only introduce confusion. Conda manages virtual
  environments for you already.
* Even though pyenv supports Miniconda and Anaconda and pyenv-virtualenv can handle Conda environments, the benefits
  may not outweigh the additional complexity. I would recommend having only one tool.

## What is the system Python good for

Gosh, I really don't know... on macOS High Sierra in 2017 it's still Python 2.7, same applies to large Linux
distributives like CentOS or Debian. I'd recommend leaving it alone and using a sane Python version with Conda or pyenv
for development.

Some exceptions are Amazon Linux 2017.09.1 having Python 3.6 and AWS Deep Learning AMIs which does a decent job keeping
Python and packages up-to-date.

## Environment management tools for other languages

* [rbenv](https://github.com/rbenv/rbenv) for Ruby
* [scalaenv](https://github.com/scalaenv/scalaenv) for Scala and [sbtenv](https://github.com/sbtenv/sbtenv) for SBT
* [jEnv](http://www.jenv.be/) for Java
* [Stack](https://docs.haskellstack.org/en/stable/README/) for Haskell (it does more than environment management)
* [kerl](https://github.com/kerl/kerl) for Erlang
* [Conda](https://conda.io/docs/user-guide/tasks/use-r-with-conda.html) (again!) for R
