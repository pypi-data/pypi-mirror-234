#!/bin/bash

cd $(dirname $0)/..

function modules() {
  pushd jouets > /dev/null
  for dir in *
  do
    if [ ! -d $dir ]
    then
      continue
    fi
    if [[ $dir == __* ]] || [[ $dir == .* ]]
    then
      continue
    fi
    if [[ $dir == "utils" ]]
    then
      continue
    fi
    echo $dir
  done
  popd > /dev/null
}

function dernier_tag() {
  git tag | grep $1 | head -n 1
}

for mod in $(modules)
do
  git log $(dernier_tag $mod)..HEAD jouets/$mod doc/${mod}* | cat - changelogs/$mod.md | sponge changelogs/$mod.md
done
