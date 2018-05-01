Title: First impressions of Haskell
Tags: haskell, functional programming, rant
Summary: Observations I've made while trying to write my first non-trivial Haskell program.

## Learning curve

My journey into Haskell started with a book by Miran Lipovača titled
"Learn You a Haskell for Great Good". The book is [available online](http://learnyouahaskell.com/)
for free and I highly recommend it - the author does a great job explaining complicated concepts
in a beginner-friendly way. While reading it, I tried writing simple programs in Haskell and it
appeared to be very hard as if the compiler was inventing new rules on the way to make sure my
code never compiles.

The book is an introduction to the language and after finishing it (and making those small
programs compile) I realised that I still have no idea how to *build* anything in Haskell.
Definitely not something that has configuration, logging or persistent state. I had no idea how to
structure the code in a good way, when to use certain language features and when not to.

So I started a pet project, a personalised news feed delivered to the email address with data
sources being RSS and Atom, to begin with. Yes, I know there are news readers and other tools that do
this already. Later I may write a post describing the rationale for inventing the wheel, for now
here are some keywords: *private yet personalised reading list*.

The first attempt was not great: it was both spaghetti-like and, at the same time, had a
shape of a star with every module importing `Types.hs`, where the data model lived. I sensed the smell
but didn't really know how to get rid of it.

Then I stumbled upon [a talk](https://www.youtube.com/watch?v=-X1vrxQUETM) by
[Jasper Van der Jeugt](https://jaspervdj.be/), titled "Getting things done in Haskell" and it was an
eye-opener (thanks Jasper!). With the new energy I have gotten from the talk, I carry on implementing
my pet project, this time with more success. After a couple of iterations of refactoring, the tiny code
base started to have a much better shape. I'll make sure to share it when it's functionally complete
and not too ugly.

## Rant

I don't think this section is much news to anyone who's programmed in Haskell, most of the points
have already been posted online by other fools.

### Graphical syntax

There's widespread use or even abuse of **graphical syntax** for infix operators. I appreciate that
in some case it may make the code look more concise and elegant. But most of the time they are just
hard to google and impossible to pronounce. Okay, maybe
[not impossible](https://wiki.haskell.org/Pronunciation) but definitely hard.

Here's what I'm talking about:

```Haskell
atTag tag = deep (isElem >>> hasName tag)

text = getChildren >>> getText

getGuest2 = atTag "guest" >>>
  proc x -> do
    fname <- text <<< atTag "fname" -< x
    lname <- text <<< atTag "lname" -< x
    returnA -< Guest { firstName = fname, lastName = lname }
```

this is an example from the XML processing library HXT documentation. I count four
different types of infix operators here. I think `->` is not an infix operator but
I'm actually not sure!

It is not unlikely I will change my mind on the usefulness of [Arrows](https://en.wikibooks.org/wiki/Haskell/Understanding_arrows)
and [Lens](https://en.wikibooks.org/wiki/Haskell/Lenses_and_functional_references)
after learning more about them, we'll see.

### Records

Haskell records seem nice at first, they definitely do after reading about them in a book.
But after using records for longer than 10 minutes you may become disenchanted, for example,
the following code does not compile:

```Haskell
data Person  = MkPerson  { personId :: Int, name :: String }
data Address = MkAddress { personId :: Int, address :: String }
```

because both `Person` and `Address` have a field with label `personId`. It can be worked around
by a GHC extension
[DuplicateRecordFields](https://ghc.haskell.org/trac/ghc/wiki/Records/OverloadedRecordFields/DuplicateRecordFields).
It's nice but sometimes requires hints to disambiguate record usages.

Here's [another take on fixing the records](https://gist.github.com/patrickt/d43031e3b69f1a4ff8c9).
The author basically suggests using [Lens](https://en.wikibooks.org/wiki/Haskell/Lenses_and_functional_references)
instead which brings me back to the part of the rant on
[graphical syntax]({filename}/2018-04-30_first-impressions-of-haskell.md#graphical-syntax).

### Libraries

Quality of the **libraries** varies. For my simple use case, I've explored libraries for XML
processing and HTTP clients. In Java and Python world there are good libraries for everything
and basic HTTP or XML processing tools are a part of the language's standard library. In
Haskell, not so much: you get to choose between a small number of pet projects that sometimes
look like they were abandoned soon after being published. People on Twitter came up with a
word for it, *thesis-ware*.

I have another problem with Haskell libraries: **documentation** (or, rather, lack of thereof).
[Hspec]({filename}/2018-05-01_haskell-tools.md#hspec-testing-framework), which is arguably not
a library, is an example of Haskell software with good documentation: it has a website with a
getting started guide, examples with different levels of complexity, links to additional resources.
Otherwise, it's not uncommon for a Haskell package from Hackage to have very sparse documentation
consisting of generated [Haddock]({filename}/2018-05-01_haskell-tools.md#haddock) module
structure with little to none explanation of what functions, data types and other components
are supposed to do and how to use them together. I don't remember ever seeing a usage example in
Haddock generated documentation.

### Integrated development environments (IDEs)

Coming from the JVM world, I am spoiled by good **IDEs**. I like it when there's smart and fast
auto-complete which actually understands the language. When the IDE looks up the documentation
for me and doesn't ask me to re-generate hoogle database or perform another made-up action.
When it's possible to navigate to the source code of the library function directly from its use.

<figure>
  <img src="{attach}static/images/haskell-ide.png" alt="Haskero screenshot"/>
  <figcaption>
  Visual Studio Code with Haskero plugin showing a tooltip for a library
  function 'filter', yet no documentation is displayed.
  </figcaption>
</figure>

Full disclosure, I'm not a huge fan of using Vim or Emacs, maybe the grass is greener on the
other side, but the experience that the best VS Code plugin gives me is limited to syntax
highlighting, code formatting and showing compiler error messages inline.

### Small things

* People are using a lot of GHC extensions, not sure if that is necessarily a bad thing but it
  doesn't make the learning curve any lower.
* GHC is not super fast and it takes a few seconds before I can run the tests on the tiny project.
* There's a `String` type in the standard library that nobody uses because of its
  performance? Uh-oh!

## The good stuff

It would be unfair to waste so much space on the rants without expressing at least a little
gratitude to the good parts of the language.

* Pure functions, recursion, higher order functions and other aspects of FP are fun to learn and
  when applied feel like brain teasers.
* Once the code starts to compile, there's a good chance it also works as expected! I remember
  feeling the same when programming Scala, that's what a type-safe language does to you. That
  being said, having at least some tests is always a good idea.
* I loved the idea of all functions being [curried](https://wiki.haskell.org/Currying), awesome!
* I'm sure there will be time to change my mind later but so far isolating I/O operations using a
  special `IO` monad looks like a sensible thing to do.
* My experience with [Stack]({filename}/2018-05-01_haskell-tools.md#stack-build-tool) and
  [Hspec]({filename}/2018-05-01_haskell-tools.md#hspec-testing-framework) has been mostly positive
  so far.

I wanted to write more about Haskell tools, so here's another, more objective,
[post on Haskell tools]({filename}/2018-05-01_haskell-tools.md).
