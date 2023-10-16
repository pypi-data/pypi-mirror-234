all: ../../logo.png logo.pdf

logo.pdf: logo.svg
	rsvg-convert --zoom=.05 --format=pdf --output=$@ $<

../../logo.png: logo.svg
	inkscape --export-height 1000 --export-filename temp.png $<
	convert temp.png -background transparent -gravity center -extent 1000x1000 $@
	rm -f temp.png
