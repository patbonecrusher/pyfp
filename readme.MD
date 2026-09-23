# Purposes

Doing this class [class](https://egghead.io/lessons/javascript-refactoring-imperative-code-to-a-single-composed-expression-using-box) in python

## Getting started

This project uses [uv](https://docs.astral.sh/uv/) to manage the Python
environment. Install uv (`brew install uv` or
`curl -LsSf https://astral.sh/uv/install.sh | sh`), then:

```sh
uv sync                       # create .venv and install dev dependencies
uv run pytest                 # run the test suite (src/function)
uv run pytest --cov=. --cov-report=xml   # tests with coverage
uv run ptw --delay 2 .        # watch mode (re-run tests on change)
```

The scratch files under `src/scratch/` and `types/` are runnable scripts that
print their output — run any of them directly:

```sh
uv run python src/scratch/either.py
uv run python types/functor.py
```

There are no runtime dependencies; everything runs on the standard library.

## Terminology

### Functor

Functor is a type class that abstracts over type constructors that can be map‘ed over. Examples of such type constructors are List, Option, and Future.

A Functor instance must obey two laws:

* Composition: Mapping with f and then again with g is the same as mapping once with the composition of f and g
  fa.map(f).map(g) = fa.map(f.andThen(g))
* Identity: Mapping with the identity function is a no-op
  fa.map(x => x) = fa
