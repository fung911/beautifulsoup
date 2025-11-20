# Milestone-3

---

## Project Structure

```


├── apps   # Sample text file
    └── m3/
        └──README.md              # This file
        └── task7.py         
    └── bs4/
        └──tests              
            └── test_xformer.py        # Test cases  
        └── SoupReplace.py             # My customize class
     
```

---

## Part1

---

## Installation

### Requirements

- Python **3.10+**

---

## How to run

### Command Line Usage

Go to the /apps/m2 file

```
cd apps
cd m3
```

Run the program with an input file:

Make sure the html/xml file in the same file as the task.py does

```
python task7.py yourFile.xml
```

---

## Part2

---

### API Overview

Milestone3 extends the `SoupReplacer` mechanism to allow more flexible and powerful transformations on the parse tree
while BeautifulSoup is building it.
It supports dynamic renaming, attribute modification, and arbitrary tag-level transformations using transformer
functions.
---

### Why it works?

#### 1. Tag Detection:

Each time the parser reads a new start tag (e.g., `<b>`), it passes the tag name (`name = "b"`) to the `handle_starttag`
method inside BeautifulSoup.

#### 2. Replacement Check:

Inside this method, the code checks whether a SoupReplacer object is attached:

```python    
def transform(self, tag):
    # new Milestone3 transforms
    # ---  name_xformer ---
    if self.name_xformer is not None:
        try:
            original_tag_name = tag.name
            new_name = self.name_xformer(tag)
            if new_name is not None:
                if not isinstance(new_name, str):
                    raise TypeError(f"name_xformer must return a string or None, got {type(new_name)}")
                tag.name = new_name
                self.old_tag = original_tag_name
                self.new_tag = new_name
        except Exception as e:
            # print error
            print(f"[SoupReplacer Warning] name_xformer failed for <{tag.name}>: {e}")
```

- `self.replacer.name_xformer` → function that returns a new tag name for a given tag.

- `self.replacer.attrs_xformer` → function that returns a new attribute dictionary for a tag.
- `self.replacer.xformer` → function that can perform arbitrary modifications or side effects on the tag.

#### 3. Tree Integrity Maintained:

Because all transformations happen before the tag is pushed into the tree, the parse tree remains structurally
consistent, and all subsequent operations automatically reflect the modifications.

---

### How to Use

All three transformers (`name_xformer`, `attrs_xformer`, `xformer`) can be used simultaneously to apply complex
transformations during parsing.

```python
def uppercase_text(tag):
    if tag.string:
        tag.string = tag.string.upper()


text_upper = SoupReplacer(xformer=uppercase_text)
soup = BeautifulSoup(html_doc, "html.parser", replacer=text_upper)
```
