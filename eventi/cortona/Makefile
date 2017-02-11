first: locandina.pdf

cv.tex: cv.gnuplot
	gnuplot < $<

pde.tex: pde.gnuplot
	gnuplot < $<

locandina.pdf: locandina.tex cv.tex pde.tex sfondo.jpg
	pdflatex $<

