#!/bin/bash

rm -rf _main
curl -L https://github.com/deepset-ai/haystack/tarball/main -o main.tar
mkdir _main
tar xf main.tar -C _main --strip-components 1
rm -rf haystack/preview
cp -r _main/haystack/preview haystack
hatch clean
hatch build
