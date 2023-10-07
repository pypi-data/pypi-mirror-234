# Rethink

A note-taking app dependent on python.

## Installation

```shell
pip install rethink-note
```

## Usage

```python
import rethink_note

rethink_note.run()
```

```python
import rethink_note

rethink_note.run(
    host='localhost',
    port=8080,
    reload=True,
    workers=1,
)
```
