# f-Strings (Formatted String Literals) in Python

In Python, f-strings (formatted string literals) make it easy to insert variables and expressions directly into strings. They were introduced in Python 3.6 and are prefixed by an `f` (or `F`) before the string. With f-strings, you can easily include variables and expressions inside curly braces `{}` in a string, and Python will replace those with the actual values.

---

## Basic f-string Example

Here’s a simple example to get you started:

```python
name = "Alice"
age = 30
message = f"Hello, my name is {name} and I am {age} years old."
print(message)
```
#### Output:
```Hello, my name is Alice and I am 30 years old.```

Here, {name} is replaced by the value of name, and {age} by the value of age.

---

## Example with Expressions

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

## Formatting Numbers

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

## Formatting Dates

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

## Summary of Common Formatting Options
- {value:.2f}: Format as a float with 2 decimal places.
- {value:,.2f}: Add commas as thousands separators, with 2 decimal places.
- {date:%B %d, %Y}: Format a datetime object to display month, day, and year.

With f-strings, you can format values right in the string, making your code cleaner and easier to read!
