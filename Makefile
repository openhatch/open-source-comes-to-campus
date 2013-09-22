all:	printme.pdf

printme.pdf: document.tex
# In two steps, for atomicity of printme.pdf.
	pdflatex document.tex
	mv document.pdf printme.pdf
