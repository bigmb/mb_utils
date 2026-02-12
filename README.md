# MB Utils

[![Python Version](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/bigmb/mb_utils/graphs/commit-activity)
[![Downloads](https://static.pepy.tech/badge/mb_utils)](https://pepy.tech/project/mb_utils)

A collection of utility functions and tools to simplify common Python development tasks. Part of the `mb` namespace — install as `mb_utils`, import as `mb.utils`.

## Features

- **Logging**: Easy-to-use logging with colored console output, rotating file handlers, and a safe `LoggerWrapper` (`logg`) that skips logging when no logger is provided
- **File Operations**: Concurrent path checking and validation
- **Decorators**: Deprecation warnings and retry logic
- **Image Verification**: Validate image files (path, type, shape) with multithreading
- **S3 Integration**: Simplified AWS S3 file and directory operations
- **Profiling**: Function profiling with SnakeViz, line-by-line profiling
- **Utilities**: Timer decorator, batch creation

## Installation

```bash
pip install mb_utils
# or
uv pip install mb_utils
```

This installs under the `mb` namespace. Import everything via `mb.utils.*`.

## Usage

### Logging

```python
from mb.utils.logging import make_logger, logg

# Create a logger with colored console + rotating file output
logger = make_logger('myapp')
logger.info("Direct logger usage")

# Safe logging wrapper — no need for `if logger:` checks
logg.info("This message logs", logger)      # logs normally
logg.info("This is silenced", None)          # does nothing

# Set a default logger so you don't have to pass it every time
logg.set_default(logger)
logg.info("Uses default logger")             # logs via default
logg.warning("Also works")
```

### Path Checking

```python
from mb.utils.path_checker import check_path

# Check a list of paths concurrently (returns list of bools)
results = check_path(['/path/to/file1', '/path/to/file2'], max_threads=16)
```

### Retry Decorator

```python
from mb.utils.retry_decorator import retry

@retry(times=3, exceptions=(ValueError, TypeError))
def might_fail():
    pass
```

### Deprecation Decorator

```python
from mb.utils.deprecated import deprecated_func

@deprecated_func(deprecated_version="1.0", suggested_func="new_func", removed_version="3.0")
def old_function():
    pass
```

### S3 Operations

```python
from mb.utils.s3 import upload_file, download_file, upload_dir, download_dir, list_objects

# Upload / download a single file
upload_file('bucket-name', 'remote_key.txt', 'local_file.txt')
download_file('bucket-name', 'remote_key.txt', 'local_file.txt')

# Upload / download entire directories
upload_dir('bucket-name', 's3/prefix', '/local/dir')
download_dir('bucket-name', 's3/prefix', '/local/dir')

# List objects
list_objects('bucket-name')
```

### Timer & Batch Utilities

```python
from mb.utils.extra import timer, batch_generator, batch_create

@timer
def slow_function():
    pass

# Generator-based batching
for batch in batch_generator(range(100), batch_size=10):
    process(batch)

# List-based batching
batches = batch_create(my_list, n=10)
```

### Image Verification

```python
from mb.utils.verify_image import verify_image

results = verify_image(
    image_paths=['/path/img1.jpg', '/path/img2.png'],
    image_type='JPEG',           # optional: check format
    image_shape=(1920, 1080),    # optional: check dimensions (width, height)
    max_workers=16
)
# Returns list: True, False, 'image_type_mismatch', 'image_shape_mismatch', 'unknown_image_format'
```

### Profiling

```python
from mb.utils.profiler import run_with_snakeviz, line_profile

# Profile and visualize with SnakeViz
@run_with_snakeviz
def process_data(data):
    pass

# Save profile without opening SnakeViz
run_with_snakeviz(my_func, arg1, arg2, save_only=True, file_path="output.prof")

# Line-by-line profiling
@line_profile
def process_item(item):
    result = item * 2
    return result
```

## Available Modules

| Module | Description | Import Path |
|--------|-------------|-------------|
| logging | Logger with colored output, file rotation, safe wrapper | `from mb.utils.logging import make_logger, logg` |
| path_checker | Concurrent path validation | `from mb.utils.path_checker import check_path` |
| deprecated | Function deprecation decorator | `from mb.utils.deprecated import deprecated_func` |
| verify_image | Image verification (path, type, shape) | `from mb.utils.verify_image import verify_image` |
| retry_decorator | Retry mechanism for functions | `from mb.utils.retry_decorator import retry` |
| s3 | AWS S3 upload/download/list operations | `from mb.utils.s3 import *` |
| extra | Timer decorator, batch utilities | `from mb.utils.extra import *` |
| profiler | SnakeViz and line profiling | `from mb.utils.profiler import *` |
| terminal | Terminal size utilities | `from mb.utils.terminal import stty_size` |
| version | Package version info | `from mb.utils.version import version` |

## Included Scripts

- `verify_images_script`: Utility script for batch image verification
