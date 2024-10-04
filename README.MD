# LiteScript
my own interpreted scripted language focusing on simplicity and minimality.

## How to Use?

### Prerequisites
- Python 3.x installed on your machine.

### Setup
1. Clone the repository or download the source code.
2. Ensure you have the following files in the same directory:
   - `interpreter.py`
   - `code.ls`

### Writing LiteScript Code
1. Open `code.ls` in a text editor.
2. Write your LiteScript code. Here is an example:

    ```plaintext
    let a = 5
    let b = 10
    let c = 15
    let d = 20

    print(a)
    print(b)
    print(c)
    print(d)

    let sum = a + b + c + d
    print(sum)

    let product = a * b * c * d
    print(product)

    let average = (a + b + c + d) / 4
    print(average)

    let message = "The sum is: "
    print(message + sum)

    let greeting = "Hello, "
    let name = "World"
    print(greeting + name)

    let complex_expression = (a * b) + (c / d) - (a + b)
    print(complex_expression)

    let nested_expression = ((a + b) * (c - d)) / (a + b + c + d)
    print(nested_expression)
    ```

### Running the Interpreter
1. Open a terminal and navigate to the directory containing `interpreter.py` and `code.ls`.
2. Run the interpreter using Python:

    ```sh
    python interpreter.py
    ```

 ### Troubleshooting
- Ensure that `interpreter.py` and `code.ls` are in the same directory.
- Make sure you have Python 3.x installed and properly configured in your system's PATH.

Enjoy using LiteScript!
