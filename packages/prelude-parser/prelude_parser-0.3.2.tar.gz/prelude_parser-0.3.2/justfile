@develop:
  maturin develop -E all

@install: && develop
  pip install -r requirements-dev.txt

@lint:
  echo cargo check
  just --justfile {{justfile()}} check
  echo cargo clippy
  just --justfile {{justfile()}} clippy
  echo cargo fmt
  just --justfile {{justfile()}} fmt
  echo ruff
  just --justfile {{justfile()}} ruff
  echo black
  just --justfile {{justfile()}} black
  echo mypy
  just --justfile {{justfile()}} mypy

@check:
  cargo check

@clippy:
  cargo clippy

@fmt:
  cargo fmt

@black:
  black prelude_parser tests

@mypy:
  mypy .

@ruff:
  ruff check . --fix

@test:
  pytest
