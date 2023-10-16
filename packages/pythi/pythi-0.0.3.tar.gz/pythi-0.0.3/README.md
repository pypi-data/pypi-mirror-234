# Pythi, Python Projects Helper

This module contains basic function that help you with your python/jupyter projects.

## Project Root CWD Unifier

This Python function `unify_cwd()` helps you navigate to the project's root folder that contains the `.git` subfolder. It is particularly useful when you are working in a deep directory structure and want to ensure that your current working directory (CWD) is set to the root of the project for consistent and reliable file access. It is also useful with jupyter notebooks, as their CWD is always their own folder, and this function can be used to set the CWD to the project root.

### How to Use

1. Install and import the module `pythi` into your Python code.

2. Simply call the `unify_cwd()` function wherever you need to set your CWD to the project's root directory containing the `.git` subfolder.

3. Upon calling the function, it will traverse upwards in the directory hierarchy starting from the current CWD. It will stop as soon as it finds the `.git` subfolder, indicating the project root.

4. The function will change the CWD to the project root, ensuring that any subsequent file operations or imports are correctly relative to the root directory.

### Example Usage

```python
import os
from pythi import unify_cwd

def main():
    # the place where you are in the directory hierarchy
    print("Before unify_cwd():", os.getcwd())
    unify_cwd()
    # the git project root
    print("After unify_cwd():", os.getcwd())

if __name__ == "__main__":
    main()
```

In this example, calling `unify_cwd()` inside the `main()` function will change the CWD to the project root, and you will see the updated CWD printed in the console.

### Note

- Make sure that the function is used in a Python script that is part of the project and has access to the `.git` subfolder. Otherwise, it will not work as expected.

- Be cautious while using this function in modules or libraries intended for distribution, as it modifies the CWD globally. It is recommended to use this function mainly in scripts used during development or personal projects.

- Always remember to save your changes before executing the script using this function, as the CWD change may lead to unexpected behavior if other parts of your code rely on a specific directory structure.

### Build and upload

- Change version in setup.py
- Run the following commands
```
python setup.py sdist bdist_wheel
twine upload dist/*
```

