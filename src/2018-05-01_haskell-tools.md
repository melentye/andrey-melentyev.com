Title: Haskell tools
Tags: haskell, tools
Summary: A very brief description of Haskell tools I've encountered so far.

## GHC, the Glasgow Haskell Compiler

[GHC](https://www.haskell.org/ghc/) is the most popular Haskell compiler. Like with other
languages, when it comes to building a program consisting of more than a single source file,
invoking the compiler directly becomes unfeasible. In any case, it's good to know that `ghc` is
the compiler executable name and `ghci` is the interactive read-eval-print loop (REPL).

    $ ghci
    GHCi, version 8.2.2: http://www.haskell.org/ghc/  :? for help
    Prelude> print "Hello, World!"
    "Hello, World!"

As a side note, I initially found GHC error messages intractable. After some practice, I still do.
Hope it'll change over time.

## Cabal build tool

[Cabal](https://www.haskell.org/cabal/) is a build tool with dependency management for Haskell.
It uses [Hackage](http://hackage.haskell.org/) package archive. Build configuration is stored in
files with `.cabal` extension, its content is common sense for a build configuration:
module description, dependencies, etc.

Cabal users may end up in [Cabal Hell](https://en.wikipedia.org/wiki/Cabal_(software)#Criticism)
and even though there is official [survival guide](https://wiki.haskell.org/Cabal/Survival), I found
Stack to be a good solution.

## Stack build tool

[Stack](https://docs.haskellstack.org/en/stable/README/) is a user-friendly build and dependency system,
it uses Cabal under the hood but fixes the *Cabal Hell* problem by introducing 
[Stackage](https://www.stackage.org/) - a versioned collection of Haskell packages where packages in 
each Stackage release are known to compile well together. As long as you stick to the default version of
the package from the Stackage when adding a new dependency to your package, you're guaranteed to avoid
going to hell.

Stack features a set of subcommands you'd expect a build tool to have: `build`, `test`,
`exec`. It can also start an interactive GHC REPL with all your project packages and dependencies
available with `stack ghci`. There's Docker support, or even two! Firstly, you can
[run Stack inside Docker](https://docs.haskellstack.org/en/stable/docker_integration/), secondly,
it's possible to [generate Docker images with your freshly built Haskell programs](https://docs.haskellstack.org/en/stable/GUIDE/#docker),
handy!

Stack introduces two more build config files:

* `stack.yaml` is a project-level configuration file. It defines the Stackage release to be used
  across the project, meaning that all packages will share the settings.
* `package.yaml` is an [hpack](https://github.com/sol/hpack) package description, contains the
  configuration of the package(s): metadata, internal and external dependencies. That sounds familiar and
  indeed this is the same kind of information as Cabal build configuration has. In fact, `package.yaml`
  can be used to generate the `.cabal` configurations.

Does it mean that Stack requires you to write and support three config files? No and no; you can get
default configs when creating a project with `stack new`, and the Cabal files don't need to be supported
because they are auto-generated. It turns out you don't need to work with Cabal directly if you use Stack.
Using `stack new` is a great way to get a new Haskell project started because it creates a solid directory
structure for you with an entry-point into the program, a library package and an [Hspec](TODO) unit test
skeleton.

For my Python colleagues, one way to think of Stack is that it's similar to Conda:

* Isolated project settings for the compiler and dependencies.
* Multiple versions of the compiler can co-exist.

## Hspec testing framework

[Hspec](https://hspec.github.io/) is a testing framework for Haskell, I found it to be easy to learn
and intuitive to use. Hspec with [Quickcheck](https://hspec.github.io/quickcheck.html) is a recipe
for [property-based testing](http://blog.jessitron.com/2013/04/property-based-testing-what-is-it.html).

## Brittany code formatter

[Brittany](https://github.com/lspitzner/brittany) is a Haskell source code formatter. I like my code
formatted.

Before:

```Haskell
data Channel = Channel { title :: Maybe T.Text, link :: Maybe T.Text
    , description :: Maybe T.Text, items :: [I.Item], categories :: [T.Text]
    , image :: Maybe T.Text } deriving (Show, Eq)
```

After:

```Haskell
data Channel = Channel
    { title :: Maybe T.Text
    , link :: Maybe T.Text
    , description :: Maybe T.Text
    , items :: [I.Item]
    , categories :: [T.Text]
    , image :: Maybe T.Text
    } deriving (Show, Eq)
```

Britanny seems nice.

## Hlint linter

[Hlint](https://github.com/ndmitchell/hlint) is, as the name suggests, a linting tool for Haskell. I
find it helpful to make my code style more Haskell-y.

## Haddock

[Haddock](https://www.haskell.org/haddock/) is a tool for generating documentation from annotated
source code (similar to Javadoc in Java world or Pydoc in Python).

## IDE support

I normally use IntelliJ for larger projects and Visual Studio Code for smaller things. There's a
plugin for IntelliJ which is somewhat unstable and has an intrusive approach to using the notification
area.

For VS Code we get to chose between [Haskell Language Server](https://github.com/alanz/vscode-hie-server)
and [Haskero](https://github.com/commercialhaskell/intero). I found the former to be extremely CPU-heavy,
to a degree where it becomes unusable. Haskero seems to work fine. There are also plugins for Brittany and
Hlint for VS Code.

My subjective opinion is that Haskell ecosystem is lacking the most when it comes to a good IDE experience.
This is something you may not notice coming from C++, but for a person familiar with first-class support
modern editors and IDEs provide for Java or Python, it's quite clear.
