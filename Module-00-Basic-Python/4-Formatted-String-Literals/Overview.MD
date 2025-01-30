# f-Strings (Formatted String Literals) in Python

In Python, formatted string literals make it easy to insert variables and expressions directly into strings. They were introduced in Python 3.6 and are prefixed by an `f` (or `F`) before the string. With f-strings, you can easily include variables and expressions inside curly braces `{}` in a string, and Python will replace those with the actual values.

---

## 1. Basic f-string Example

Here’s a simple example to get you started:

```python
name = "Aarya"
age = 20
message = f"Hello, my name is {name} and I am {age} years old."
print(message)
```
#### Output:
```Hello, my name is Aarya and I am 20 years old.```

Here, {name} is replaced by the value of name, and {age} by the value of age.

---

## 2. Example with Expressions

You can even include expressions (like calculations) within the curly braces:
```python
width = 5
height = 10
area_message = f"The area of a {width}x{height} rectangle is {width * height}."
print(area_message)
```
#### Output:
```The area of a 5x10 rectangle is 50.```

---

## 3. Formatting Numbers

f-strings allow you to format numbers directly inside the string. For example, you can format a number with commas and set the number of decimal places.

Example with :,.2f
The format specifier :,.2f does the following:

- : signals that you’re starting a format specification.
- , adds comma separators for thousands.
- .2f formats the number as a floating point with 2 decimal places.

#### Example:
```python
price = 1234567.8912
formatted_price = f"The price is ${price:,.2f}"
print(formatted_price)
```
#### Output:
```The price is $1,234,567.89```
This formats the number to two decimal places and includes commas to make it more readable.

---

## 4. Formatting Dates

You can also use f-strings to format dates. For this, you’ll typically use the datetime module.

#### Example:
```python
from datetime import datetime

current_date = datetime.now()
formatted_date = f"Today’s date is {current_date:%B %d, %Y}."
print(formatted_date)
```
#### Output:
```Today’s date is January 23, 2025.```

Here’s what’s happening in {current_date:%B %d, %Y}:

- %B represents the full month name (e.g., "November").
- %d is the day of the month (with leading zero if necessary).
- %Y is the four-digit year.

---

## Summary

| **Feature**              | **Description**                                                                                                     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------|
| **Basic f-string Usage**  | Insert variables and expressions directly into strings using curly braces `{}`.                                     |
| **Expressions in f-strings** | Supports calculations and expressions directly within the curly braces (e.g., `{width * height}`).                  |
| **Number Formatting**     | Use format specifiers like `:,.2f` to add commas for thousands and specify decimal places.                          |
| **Date Formatting**       | Format `datetime` objects using specifiers such as `%B` for month, `%d` for day, and `%Y` for year.                 |
| **Advantages**            | Simplifies code by integrating variable values, expressions, and formatting directly into the string for better readability. |

