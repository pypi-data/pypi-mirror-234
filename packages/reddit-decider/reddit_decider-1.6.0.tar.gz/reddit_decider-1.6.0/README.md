# rust_decider

Rust implementation of bucketing, targeting, overrides, and dynamic config logic.

# Usage

## class `Decider`

A class used to expose these APIs:

- ```
  choose(
     feature_name: str,
     context: Mapping[str, JsonValue]
  ) -> Decision
  ```
- ```
  choose_all(
     context: Mapping[str, JsonValue],
     bucketing_field_filter: Optional[str] = None
  ) -> Dict[str, Decision]
  ```

(dynamic configurations)

- ```
  get_bool(
    feature_name: str,
    context: Mapping[str, JsonValue],
  ) -> bool
  ```
- ```
  get_int(
    feature_name: str,
    context: Mapping[str, JsonValue],
  ) -> int
  ```
- ```
  get_float(
    feature_name: str,
    context: Mapping[str, JsonValue],
  ) -> float
  ```
- ```
  get_string(
    feature_name: str,
    context: Mapping[str, JsonValue],
  ) -> str
  ```
- ```
  get_map(
    feature_name: str,
    context: Mapping[str, JsonValue],
  ) -> Dict[str, Any]
  ```
- ```
  all_values(
     context: Mapping[str, JsonValue],
  ) -> Dict[str, Any]
  ```

misc:

- ```
  get_feature(
    feature_name: str,
  ) -> Feature
  ```

### `choose()` examples:

```python
from rust_decider import Decider
from rust_decider import DeciderException
from rust_decider import FeatureNotFoundException
from rust_decider import DeciderInitException
from rust_decider import PartialLoadException
from rust_decider import ValueTypeMismatchException

# initialize Decider instance
try:
    decider = Decider("../cfg.json")
except PartialLoadException as e:
    # log errors of misconfigured features
    print(f"{e.args[0]}: {e.args[2]}")

    # use partially initialized Decider instance
    decider = e.args[1]
except DeciderInitException as e:
    print(e)

# get a Decision for a feature via choose()
try:
    decision = decider.choose(feature_name="exp_1", context={"user_id": "3", "app_name": "ios"})
except DeciderException as e:
    print(e)

assert dict(decision) == {
    "variant": "variant_0",
    "value": None,
    "feature_id": 3246,
    "feature_name": "exp_1",
    "feature_version": 2,
    "events": [
      "0::::3246::::exp_1::::2::::variant_0::::3::::user_id::::37173982::::2147483648::::test"
    ]
}

# `user_id` targeting not satisfied so "variant" is `None` in the returned Decision
try:
    decision = decider.choose(feature_name="exp_1", context={"user_id": "1"})
except DeciderException as e:
    print(e)

assert dict(decision) == {
  "variant": None,
  "value": None,
  "feature_id": 3246,
  "feature_name": "exp_1",
  "feature_version": 2,
  "events": []
}

# handle "feature not found" exception
# (`FeatureNotFoundException` is a subclass of `DeciderException`)
try:
    decision = decider.choose(feature_name="not_here", context={"user_id": "1"})
except FeatureNotFoundException as e:
  print("handle feature not found exception:")
  print(e)
except DeciderException as e:
    print(e)
```

### `choose_all()` examples:

```python
# `decider` initialized same as above
decisions = decider.choose_all(context={"user_id": "3", "app_name": "ios"}, bucketing_field_filter="user_id")

assert dict(decisions["exp_67"]) == {
  "variant": "variant_0",
  "value": None,
  "feature_id": 3125,
  "feature_name": "exp_67",
  "feature_version": 4,
  "events": [
    "0::::3125::::exp_67::::4::::variant_0::::3::::user_id::::37173982::::2147483648::::test"
  ]
}
```

### Dynamic Configurations + misc. examples:

```python
# `decider` initialized same as above
try:
    dc_bool = decider.get_bool("dc_bool", context={})
    dc_int = decider.get_int("dc_int", context={})
    dc_float = decider.get_float("dc_float", context={})
    dc_string = decider.get_string("dc_string", context={})
    dc_map = decider.get_map("dc_map", context={})

    feature = decider.get_feature("dc_map")
except FeatureNotFoundException as e:
    print("handle feature not found exception:")
    print(e)
except ValueTypeMismatchException as e:
    print("handle type mismatch:")
    print(e)
except DeciderException as e:
    print(e)

assert dc_bool == True
assert dc_int == 99
assert dc_float == 3.0
assert dc_string == "some_string"
assert dc_map == {
  "v": {
      "nested_map": {
          "w": False,
          "x": 1,
          "y": "some_string",
          "z": 3.0
      }
  },
  "w": False,
  "x": 1,
  "y": "some_string",
  "z": 3.0
}

assert dict(feature) == {
  "id": 3393,
  "name": "dc_bool",
  "version": 2,
  "bucket_val": '',
  "start_ts": 0,
  "stop_ts": 0,
  "owner": "test",
  "emit_event": False
}
```

### Dynamic Configuration `all_values()` example:

```python
# `decider` initialized same as above
decisions = decider.all_values(context={})

assert decisions["dc_int"] == 99
```

## python bindings used in `Decider` class

```python
import rust_decider

# Init decider
decider = rust_decider.init("darkmode overrides targeting holdout mutex_group fractional_availability value", "../cfg.json")

# Bucketing needs a context
ctx = rust_decider.make_ctx({"user_id": "7"})

# Get a decision
choice = decider.choose("exp_1", ctx)
assert choice.err() is None # check for errors
choice.decision() # get the variant

# Get a dynamic config value
dc = decider.get_map("dc_map", ctx) # fetch a map DC
assert dc.err() is None # check for errors
dc.val() # get the actual map itself
```

# Development

## Updating package with latest `src/lib.rs` changes

```sh
# In a virtualenv, python >= 3.7
$ cd decider-py
$ pip install -r requirements-dev.txt
$ maturin develop
```

## Running tests

```sh
$ pytest decider-py/test/
```

## Publishing

Use [conventional commit format](https://www.conventionalcommits.org/en/v1.0.0/#summary) in PR titles to trigger releases via `release-please` task in drone pipeline.

- `chore:` & `build:` commits don't trigger releases (used for changes like updating config files or documentation)
- `fix:` bumps the patch version
- `feat:` bumps the minor version
- `feat!:` bumps the major version

## Cross-Compilation

We're [using](https://www.maturin.rs/distribution.html#use-zig) Zig for cross-compilation which is reflected in the switch from the "FLAVOR" approach to "TARGET". Cross-compilation is useful when we want to build code on one type of machine (like our CI server), but have it run on a different type of machine (like a server or user's machine with a different architecture).

To build wheels for multiple platforms more effectively, we use "TARGET" variable in the .drone.yml. This includes platforms like "linux-aarch64" and "linux-musl-x86_64".

# Formatting / Linting

```sh
$ cargo fmt    --manifest-path decider-py/test/Cargo.toml
$ cargo clippy --manifest-path decider-py/test/Cargo.toml
```
