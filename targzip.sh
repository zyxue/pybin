#!/bin/bash

tar cfv - $1 | gzip -cv  > $1.tar.gz