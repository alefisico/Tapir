#!/bin/bash
curl -X POST \
     -F token=cd66d59113d4a8a220575341e88201 \
     -F ref=meanalysis-80x-V25 \
     https://gitlab.cern.ch/api/v3/projects/15324/trigger/builds
