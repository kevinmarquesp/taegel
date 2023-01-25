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
- [ ] **`controllers.youtube:`** create a separated function just to handle the
rename of the downloaded file (some times it download as *mp4* format)
- [ ] **`controllers.youtube:`** abstract the connection with youtbue api in a
function in  the `models` module
- [ ] **`perf:`** let the main process handle the views instead of creating a
whole new process for that
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
