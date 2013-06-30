#!/usr/bin/env zsh
pandoc -t slidy python_tool_walkthrough.md --highlight-style pygments  --self-contained -o ptw.html
