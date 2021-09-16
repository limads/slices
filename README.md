# About

This package helps building Rust extensions based on `ctypes` by exporting
a single class Slice which is FFI-compatible with function signatures
such as:

```rust
extern "C" fn receive_slice(a : &[f64]) { /*..*/ }

extern "C" fn return_slice() -> Box<[f64]> { /*..*/ }
```

Which are then compiled to a `.so`  to be loaded by Python `ctypes` module.
This minimizes the use of ```rust unsafe { }``` blocks when building Rust APIs to be
consumed by Python programs directly. It might help if Python is park of your
workflow, but you aren't really building a Python package with native extensions.


