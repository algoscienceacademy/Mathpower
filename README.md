# MathPower

![mathpower_pic_1](https://github.com/user-attachments/assets/cb9b5c18-fcb0-4934-aa4c-90309111b7cf)


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting Up the Environment](#setting-up-the-environment)
- [Usage](#usage)
- [Building the Executable](#building-the-executable)
  - [Using PyInstaller](#using-pyinstaller)
  - [Using cx_Freeze](#using-cx_freeze)
- [Showcase](#showcase)
- [Contributing](#contributing)
- [License](#license)
- [About AlgoScience Academy](#about-algoscience-academy)

## Introduction

MathPower is a comprehensive mathematical tool developed to assist students, educators, and professionals in performing complex mathematical computations with ease. Designed with a user-friendly interface, MathPower aims to make advanced mathematical operations accessible to everyone.

## Features

- **Comprehensive Calculations**: Perform a wide range of mathematical computations, from basic arithmetic to advanced calculus.
- **Graphical Representations**: Visualize functions and data through interactive graphs.
- **Equation Solvers**: Solve linear and nonlinear equations efficiently.
- **User-Friendly Interface**: Intuitive design for a seamless user experience.

## Installation

### Prerequisites

- **Python 3.8 or higher**: Ensure that Python is installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

### Cloning the Repository

Clone the MathPower repository to your local machine using the following command:

```bash
git clone https://github.com/algoscienceacademy/Mathpower.git
```

### Setting Up the Environment

Navigate to the project directory and install the required dependencies:

```bash
cd Mathpower
pip install -r requirements.txt
```

## Usage

To start using MathPower, run the main application script:

```bash
python main.py
```

This will launch the MathPower interface, allowing you to perform various mathematical operations.

## Building the Executable

To distribute MathPower as a standalone executable, you can use tools like PyInstaller or cx_Freeze.

### Using PyInstaller

1. **Install PyInstaller**:

   ```bash
   pip install pyinstaller
   ```

2. **Create the Executable**:

   Navigate to the project directory and run:

   ```bash
   pyinstaller --onefile main.py
   ```

   This will generate a `dist` folder containing the `main.exe` executable.

### Using cx_Freeze

1. **Install cx_Freeze**:

   ```bash
   pip install cx_Freeze
   ```

2. **Create a `setup.py` File**:

   ```python
   from cx_Freeze import setup, Executable

   setup(
       name="MathPower",
       version="1.0",
       description="A comprehensive mathematical tool",
       executables=[Executable("main.py")]
   )
   ```

3. **Build the Executable**:

   Run the following command:

   ```bash
   python setup.py build
   ```

   This will create a `build` directory containing the executable files.

## Showcase

Here are some screenshots showcasing MathPower's capabilities:

![mathpower_pic_1](https://github.com/user-attachments/assets/ceb5ac05-8700-4c15-9174-3a7cc4dbe656)
*The main interface of MathPower.*


*Visualizing functions through interactive graphs.*
![mathpwer_pic_2](https://github.com/user-attachments/assets/ab70e1b0-537e-45df-8796-981c7190a8e3)
![mathpower_pic_4](https://github.com/user-attachments/assets/f2d1e95a-5d85-4ecc-8743-b005f30f5ae2)
![mathpower_pic_3](https://github.com/user-attachments/assets/26b4c506-15aa-4bb3-995c-3e332fc16ba9)
![mathpower_pic_5](https://github.com/user-attachments/assets/39760a32-0f8c-469b-bf4a-d33f5e31e67c)
![mathpower_pic_6](https://github.com/user-attachments/assets/d3491ecd-f3a5-4fe6-a3cb-7d0790a67f34)

*Solving equations efficiently.*

## Contributing

We welcome contributions from the community. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with descriptive messages.
4. Push your branch and create a pull request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

MathPower is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## About AlgoScience Academy

AlgoScience Academy is a platform dedicated to combining free thought and technology, aiming to work out goals and objectives that foster innovation and learning.

For more information, visit our [SoundCloud page](https://soundcloud.com/algoscienceacademy) or our [YouTube channel](https://www.youtube.com/@algoscienceacademy). 
