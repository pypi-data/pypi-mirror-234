.DEFAULT: test

.PHONY: all
all: build test lint

.PHONY: build
build: build-rust build-python

.PHONY: build-python
build-python: install-python-deps
	maturin develop

.PHONY: build-rust
build-rust:
	cargo build --package reddit-decider

.PHONY: clean
clean:
	cargo clean --package reddit-decider

.PHONY: fmt
fmt:
	reddit-lint --mode fix
	cargo fmt --package reddit-decider

.PHONY: install-python-deps
install-python-deps:
	pip install -r requirements-dev.txt

.PHONY: lint
lint: fmt
	reddit-lint --mode enforce
	cargo clippy --package reddit-decider -- -D warnings

.PHONY: test
test: test-rust test-python

.PHONY: test-python
test-python: build-python
	pytest -vs -W ignore::DeprecationWarning --tb native ./test

.PHONY: test-rust
test-rust:
	cargo test --package reddit-decider
