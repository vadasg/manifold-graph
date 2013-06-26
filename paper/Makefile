TEX_NAME = paper
SI_NAME = supplemental

all:
	make clean
	pdflatex ${TEX_NAME}
	pdflatex ${TEX_NAME}
	bibtex ${TEX_NAME}
	pdflatex ${TEX_NAME}
	pdflatex ${TEX_NAME}
	open ${TEX_NAME}.pdf &
	make clean
	pdflatex ${SI_NAME}
	pdflatex ${SI_NAME}
	#bibtex ${SI_NAME}
	open ${SI_NAME}.pdf &
	make clean

clean:
	#rm -f ${TEX_NAME}.pdf
	rm -f *.log
	rm -f *.aux
	rm -f *.bbl
	rm -f *.blg
	rm -f *.out
	rm -f *.tcp
	rm -f *.tps
