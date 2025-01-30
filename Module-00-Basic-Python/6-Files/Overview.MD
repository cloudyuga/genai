# Working with Files

Python makes it easy to work with files for reading and writing. We will cover how to use the open() function, handle encoding (important for Windows users), and utilize context managers. We'll also touch on handling file paths in a platform-independent way and list files with glob.

## 1. Using the open() Function
The open() function is used to open a file for reading, writing, or other operations. Its basic syntax is:

```python
file = open('filename', mode, encoding='optional')
```
#### Common Modes:
- 'r' (read): Default mode. Opens the file for reading. File must exist.
- 'w' (write): Opens the file for writing. Overwrites if the file exists, creates a new one if it doesn’t.
- 'a' (append): Opens the file to append data. Creates a new file if it doesn’t exist.
- 'x' (exclusive creation): Creates a new file. Fails if the file exists.

#### Specifying Encoding:
Windows often uses a different default encoding (e.g., cp1252) than many other systems (utf-8). To ensure compatibility, specify the encoding:
```python
file = open('filename.txt', 'r', encoding='utf-8')
```
---
## 2. Using Context Managers
The best practice for working with files in Python is to use a context manager with the with statement. It automatically closes the file when you're done.

#### Example: Writing to a File
```python
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write("Hello, World!")
```

#### Example: Reading a File
```python
with open('output.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)
```

#### Example: Appending to a File
```python
with open('output.txt', 'a', encoding='utf-8') as file:
    file.write("\nThis is an appended line.")
```
---
## 3. Reading Line by Line
If the file is large, you may want to read it line by line instead of loading the entire file into memory:

```python
with open('example.txt', 'r', encoding='utf-8') as file:
    for line in file:
        print(line.strip())  # Strip removes newline characters
```
---
## 4. Handling Paths
Paths can vary depending on the operating system (Windows uses \, while Linux/Mac use /). Python's os and pathlib libraries make handling paths platform-independent.
### Using os.path
```python
import os

# Construct a file path
file_path = os.path.join('folder', 'subfolder', 'example.txt')
print(file_path)
```
### Using pathlib
The pathlib library (introduced in Python 3.4) offers an object-oriented approach:
```python
from pathlib import Path

# Construct a file path
file_path = Path('folder') / 'subfolder' / 'example.txt'
print(file_path)

# Check if a file exists
if file_path.exists():
    print(f"{file_path} exists!")
```
---
## 5. Listing Files in a Directory
To list files matching a pattern (e.g., all .txt files), use glob.glob:
```python
import glob

# List all .txt files in the current directory
txt_files = glob.glob('*.txt')
print(txt_files)
```
For subdirectories, use the ** wildcard with the recursive=True argument:

```python
# List all .txt files in current directory and subdirectories
all_txt_files = glob.glob('**/*.txt', recursive=True)
print(all_txt_files)
```
---
## 6. Putting It All Together

Here’s a complete example that:

- Reads a file line by line.
- Writes new content to another file.
- Uses platform-independent paths and lists files in a directory.

```python
from pathlib import Path
import glob

# Define file paths using pathlib
input_file = Path('data') / 'input.txt'
output_file = Path('data') / 'output.txt'

# Ensure the directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Read the input file and write to the output file
if input_file.exists():
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            outfile.write(line.upper())  # Example: Write uppercase content
else:
    print(f"File {input_file} not found.")

# List all text files in the directory
txt_files = glob.glob(str(Path('data') / '*.txt'))
print("Text files in the 'data' directory:", txt_files)
```
---
## Summary
- Use open() with appropriate modes for reading, writing, or appending files.
- Always specify encoding='utf-8' for cross-platform compatibility.
- Use with for safer file handling.
- Utilize os or pathlib for platform-independent paths.
- Use glob for listing files matching patterns.
These basics will get you started on working with files effectively in Python!
