# CachiPy: A Caching Library for FastAPI

CachiPy is a caching library specially designed for use with FastAPI. It allows you to easily cache API responses and improve the performance of your FastAPI applications.

![CachiPy Logo](https://raw.githubusercontent.com/Ambar-06/CachiPy/main/CachiPy/CachiPy.png)

## Features

- Simple and efficient caching for FastAPI applications.
- Support for caching API responses and function results.
- Easy integration with FastAPI routes.
- Customizable cache size and eviction policies.
- Automatic cache clearing.

## Installation

You can install CachiPy using pip:

```bash
pip install CachiPy
```
## Usage
```python
from fastapi import FastAPI
from CachiPy import cacheit
import time

app = FastAPI()

@cacheit
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

# ... define FastAPI routes and route handlers ...

# Use @cacheit decorator to cache results within your route handlers.
```
Example usage:
```python
@app.get("/factorial/{n}")
def calculate_factorial(n: int):
    result = factorial(n)
    return {
        "result": result,
        "execution_time": end_time - start_time
    }
```

## Screenshots
### Before Caching
<img src='https://raw.githubusercontent.com/Ambar-06/CachiPy/main/screenshots/uncached_fibonacci_20.png'>
<img src='https://raw.githubusercontent.com/Ambar-06/CachiPy/main/screenshots/uncached_fibonacci_20_second.png'>
<img src='https://raw.githubusercontent.com/Ambar-06/CachiPy/main/screenshots/uncached_fibonacci_25.png'>

### After Caching
<img src='https://raw.githubusercontent.com/Ambar-06/CachiPy/main/screenshots/cached_factorial_250.png'>
<img src='https://raw.githubusercontent.com/Ambar-06/CachiPy/main/screenshots/cached_factorial_250_second.png'>
<img src='https://raw.githubusercontent.com/Ambar-06/CachiPy/main/screenshots/cached_fibonacci_300.png'>
<img src='https://raw.githubusercontent.com/Ambar-06/CachiPy/main/screenshots/cached_fibonacci_20.png'>

## License
This library is released under the MIT License. See LICENSE for details.

## Contributing
Contributions are welcome! Please read our Contribution Guidelines for more details.

## Support
If you encounter any issues or have questions, please open an issue on GitHub.

## Acknowledgments
Thank you to the FastAPI community for inspiration and support.
