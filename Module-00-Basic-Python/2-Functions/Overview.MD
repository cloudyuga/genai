# Python Functions: An Overview

A function is a block of code that performs a specific task. Functions allow us to reuse code, making it cleaner and more efficient.

## Defining a Function

To define a function in Python, we use the `def` keyword followed by the function's name, parentheses `()`, and a colon `:`. Inside the parentheses, we can specify parameters (inputs the function can accept). The function's code should be indented.

Here’s an example of a simple function:

#### Example:
```python
def greet():
    print("Welcome to Python programming!")
```

This function greet doesn't take any arguments and simply prints a greeting. To use this function, call its name followed by parentheses:

```python
greet()
```
#### Output:
```
Welcome to Python programming!
```
---

## 2. Function With Arguments

Functions can accept parameters (inputs) which allow you to pass specific values to customize its behavior.

#### Example:
```python
def greet(name):
    print("Hello, " + name + "!")
```

Calling this function with an argument will greet the person whose name is provided.
```python
greet("Alice")  # Output: Hello, Alice!
```

#### Advantages:
- Flexible and customizable.
- Allows for repeated tasks with different inputs.
---

## 3. Function That Returns a Value

Instead of just performing an action, a function can also return a result that can be used elsewhere in the program.

#### Example:
```python
def add(a, b):
    return a + b
```

This function adds two numbers and returns their sum.

```python
result = add(5, 10)
print(result)  # Output: 15
```
#### Advantages:
- Useful when you need to perform a calculation and use the result later.
- Keeps your code modular and clean by separating logic.
- Allows the result to be used in further operations.
---
