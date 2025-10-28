# Milestone-2

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
cd m2
```
Run the program with an input file:

Make sure the html/xml file in the same file as the task.py does
```
python task2.py yourFile.xml
```
---

## Part2

---
| API Function | Source File     | Line Number |
|------------|-----------------|-------------|
| BeautifulSoup | bs4/__init__.py | 133         |
| prettify   | bs4/element.py  | 2601        |
| find_all   | bs4/element.py  | 2715        |
| find_parent | bs4/element.py  | 992         |
| new_tag      | bs4/__init__.py | 687         |
| insert_after  | bs4/element.py  | 716         |
| SoupStrainer  | bs4/filter.py   | 313         |
---

## Part3

---

### API Overview

The replacer mechanism is designed to dynamically modify specific HTML tags while BeautifulSoup is building the parse tree.

---
### Why it works?


#### 1. Tag Detection:
Each time the parser reads a new start tag (e.g., `<b>`), it passes the tag name (`name = "b"`) to the `handle_starttag` method inside BeautifulSoup.

#### 2. Replacement Check:
Inside this method, the code checks whether a SoupReplacer object is attached:
```
if self.replacer is not None and name == self.replacer.old_tag:
    name = self.replacer.replace(name)

```
- self.replacer.old_tag → the original tag name that should be replaced (e.g., `"b"`)

- self.replacer.replace(name) → returns the new tag name (e.g., `"blockquote"`)

#### 3. Tag Object Construction:
After the potential rename, the parser proceeds to create a Tag object using the modified name:
```
tag = tag_class(
    self,
    self.builder,
    name,
    ...)
```
#### 4. Tree Integrity Maintained:
Because the name is updated before the tag is added to the tree, all subsequent tree operations (child insertion, parent linkage, closing tag matching) automatically use the new tag name, ensuring structural consistency.

#### 5. End Tag Handling:
The same replacement logic can also be applied in the `handle_endtag()` method, so when the parser encounters a closing tag like `</b>`, it correctly maps it to the new tag name (`</blockquote>`).

---
### How to Use

Instantiate the `SoupReplacer` class, passing the tag you wish to modify and the new tag to its constructor. Then, pass this replacer class as a parameter when instantiating the `BeautifulSoup` class.
```
replacer = SoupReplacer(old_tag="b", new_tag="blockquote")
soup = BeautifulSoup(html, "html.parser", replacer=replacer)
```
