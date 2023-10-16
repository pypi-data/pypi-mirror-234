#!/bin/bash

cd $(dirname $0)
rm -fr html static index.html
mkdir html static

../../bin/evs cache clear evariste.setup
../../bin/evariste evariste.setup -v
