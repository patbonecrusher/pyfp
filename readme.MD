# Purposes

Doing this class [class](https://egghead.io/lessons/javascript-refactoring-imperative-code-to-a-single-composed-expression-using-box) in python

## Terminology

### Functor

Functor is a type class that abstracts over type constructors that can be map‘ed over. Examples of such type constructors are List, Option, and Future.

A Functor instance must obey two laws:

* Composition: Mapping with f and then again with g is the same as mapping once with the composition of f and g
  fa.map(f).map(g) = fa.map(f.andThen(g))
* Identity: Mapping with the identity function is a no-op
  fa.map(x => x) = fa
