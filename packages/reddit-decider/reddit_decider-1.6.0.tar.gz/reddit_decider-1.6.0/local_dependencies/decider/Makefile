.DEFAULT: test

.PHONY: all
all: build test lint

.PHONY: build
build:
	cargo build --package decider

.PHONY: clean
clean:
	cargo clean --package decider

.PHONY: fmt
fmt:
	cargo fmt --package decider

.PHONY: lint
lint: fmt
	cargo clippy --package decider -- -D warnings

.PHONY: test
test:
	cargo test --package decider
