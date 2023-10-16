XCF := $(wildcard *.xcf)
PNG32 := $(XCF:%.xcf=32x32/%.png)
PNG256 := $(XCF:%.xcf=256x256/%.png)
SVG := $(XCF:.xcf=.svg)
ICO := toto2titi.ico

all: $(PNG32) $(PNG256) $(SVG) $(ICO)

%.ico: 32x32/%.png
	convert $< $@

.ONESHELL:
32x32/%.png: %.xcf
	cat <<EOF | gimp -i -b -
		(
			let* (
				(image (car (gimp-file-load RUN-NONINTERACTIVE "$<" "$<")))
				(drawable (car (gimp-image-merge-visible-layers image CLIP-TO-IMAGE)))
			)
			(file-png-save RUN-NONINTERACTIVE image drawable "$@" "$@" 0 9 0 0 0 0 0)
			(gimp-image-delete image)
		)
		(gimp-quit 0)
	EOF

256x256/%.png: 32x32/%.png
	convert $< -filter point -resize 256x256 $@

%.svg: 32x32/%.png
	python3 png2svg.py $< $@


