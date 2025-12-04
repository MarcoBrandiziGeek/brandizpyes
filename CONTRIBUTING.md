# Contributing

Contributions are welcome!

## Types of Contributions

### Report Bugs

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

You can never have enough documentation! Please feel free to contribute to any
part of the documentation, such as the official docs, docstrings, or even
on the web in blog posts, articles, and such.

### Submit Feedback

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started with development

1. You need:
  * Git
  * Python
  * Poetry
  * Likely, Linux or macOS, possibly flavours like virtual machines, WSL, Docker (it should work on Windows too, but I have neither time, nor will to support it).

1. Fork https://github.com/marco-brandizi/brandizpyes.git

1. `git clone https://github.com/<your-username-or-organization>/brandizpyes.git` and `cd` into it.


1. Use `poetry`:

    ```console
    $ poetry install
    <Changes>
    $ poetry pytest [test files/functions]
    ```

1. Commit, push, and eventually send a pull request. 

## Best Practices

Please, try to follow these best practices.

### Software engineering

* [Clean Code][BEST10]
* [Solid Principles][BEST20]
* [Design Patterns][BEST30]
* [COSMIC Python][BEST40]
* [My Humble Opinions][BEST50] :-)

[BEST10]: https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29
[BEST20]: https://en.wikipedia.org/wiki/SOLID
[BEST30]: https://refactoring.guru/design-patterns
[BEST40]: https://cosmicpython.com
[BEST50]: https://marcobrandizi.info/a-few-notes-on-my-code-style

### Git and versioning

* [Conventional commits][BEST60]
* [CBEAMS article][BEST70]
* [My own notes][BEST80]

[BEST60]: https://www.conventionalcommits.org
[BEST70]: https://cbea.ms/git-commit
[BEST80]: https://marcobrandizi.info/some-tricks-and-tips-about-git


### Pull Requests

* Add tests to cover changes or new features
* Use enough comments and documentation
* Before creating a PR, merge your fork with the latest `main` branch and ensure it passes all the tests and builds.

## Code of Conduct

Yeah, [I have a doc for this too](./CONDUCT.md), which essentially, says be a decent person.

