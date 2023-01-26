# `taegel` youtube audio downloader

## Installation
Manual installation:
```bash
git clone https://github.com/kevinmarquesp/taegel
cd taegel
python -m pip install .
```

## Roadmap
### todos
- [x] **`controllers.youtube:`** ~~create a separated function just to handle the~~
rename of the downloaded file (some times it download as *mp4* format)
- [x] **`controllers.youtube:`** ~~abstract the connection with youtbue api in a
function in  the `models` module~~
- [ ] **`ref:`** create an dict type for the download logging communication
- [ ] **`ci/cd:`** add type checking with `mypy` module
- [ ] **`controllers.data:`** use the number of processess specified by the
user to fetch the video urls from a playlist (which means: fetch more than one
playlist at the same time)
- [ ] **`app:`** handle the cache files and directories (without the reading
feature yet, be patient)
    - [ ] **`1:`** save the raw arguments into the cash directory
    - [ ] **`2:`** save the list of albums and delete the raw one
    - [ ] **`3:`** clear that directorie when finish
        - [ ] **`feat:`** function to delete the empty directories in the cache
    - [ ] **`4:`** create and update the *done list* file after each download
    (even if it fails)
- [ ] **`ci/cd:`** write tests for the most of the controllers functions
- [x] **`docs:`** ~~add a todo list~~
