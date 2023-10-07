import os

__version__ = "0.1.12"

# Workaround for issues in the cargo dependency resolver:
#
# https://github.com/rust-lang/cargo/issues/10801
# https://github.com/rust-lang/cargo/issues/11698
#
# Feature dependencies that are "weak dependency features" need to be treated as
# hard dependencies until this is resolved.
CARGO_BUGGY_RESOLVER = True

# if the "CARGO" environment variable is not defined, fall back to "cargo"
if _cargo := os.environ.get("CARGO"):
    CARGO = _cargo
else:
    CARGO = "cargo"
