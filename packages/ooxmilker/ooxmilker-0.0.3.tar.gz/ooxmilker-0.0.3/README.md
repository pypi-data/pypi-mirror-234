OOXmilker is an Office Open XML parser that outputs HTML. It takes any Word (.docx, .docm), Excel (.xlsx, .xlsm), PowerPoint (pptx, pptm) or Visio (.vsdx, .vsdm)<sup>1</sup> file as an input. It returns every paragraphs from the file, one after the other.

## Installation:

This package can be installed using the following instruction in a console:
```bash
pip install ooxmilker
```

## Usage:

Once the package installed, the module can be imported like so:
```python
import ooxmilker
```

To use OOXmilker, make a call to `read()` function. This function takes a **string** representing the path to an Office Open XML file as argument. `read()` being a generator function, it must be part of some sort of loop. 

For example, the following script prints each paragraph from a Word file.
```python
file_path = "C:\\Documents and Settings\\Guest\\My Documents\\document.docx"
for p in ooxmilker.read(file_path):
    print(p[0])
    print(p[1])
```
Each iteration returns a **tuple** with 2 values. In the example above, value `p[0]` is a **string** containing a single paragraph from *document.docx* with some HTML tags. Value `p[1]` is a **dictionary** providing context information on the paragraph.

| Key | Possible Values | Description |
|---|---|---|
| tbl | `True`  `False` | If True, the content is located inside a table. Does not apply to Excel files. |
| chg | `True`  `False` | If True, the content contains changes (insertions or deletions). Applies to Word files only. |

Continuing with the same example, `p[1].get("tbl")` would either return a **boolean** `True` or `False`. If True, the paragraph is part of a table; if False, the paragraph is not part of a table.

## Compatibility

OOXmilker needs Python 3.6 to work.

Features from Office Open XML format and their respective compatibility when using OOXmilker will be listed in the near future.

1\. Visio is not part of the OOXML standard, but still close enough for OOXmilker.
