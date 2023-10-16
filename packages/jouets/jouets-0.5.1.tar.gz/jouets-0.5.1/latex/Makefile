TEX := $(wildcard *tex)
SVG := $(TEX:.tex=-01.svg)

all: ${SVG} ${PNG}

%-01.svg: %.pdf
	pdf2svg $*.pdf $*-%02d.svg all

%.pdf: %.tex
	lualatex $<
