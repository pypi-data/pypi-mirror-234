# lst-pressure

Python module for calculating LST pressure based on scheduled observations

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Contents**

- [Motivation](#motivation)
- [Quick start](#quick-start)
- [Local development](#local-development)
  - [Testing](#testing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Motivation
Observation blocks encompass various time-related constraints, notably the Local Sidereal Time (LST) and solar time windows. As LST and solar time can diverge over a year, there arises a need to query intersecting intervals between them. This library offers a mechanism to index and search these intervals. Additionally, it includes helper functions to normalize LST to solar times, and vice versa.

# Quick start
This will be usage instructions

# Local development
Ensure that you have Python v3.8.10 installed on your system, and then initiate the repository for local development with the following commands:

```sh
source env.sh
pipenv install
```

## Testing

To test the codebase, run `pytest` in the terminal. For live testing, use the [`chomp`](https://github.com/guybedford/chomp#install) task runner. Install either via Cargo (Rust), or via NPM (Node.js)

```sh
source env.sh
chomp --watch
```
