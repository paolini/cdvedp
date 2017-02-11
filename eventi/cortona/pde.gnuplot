unset xtics
unset ytics
unset ztics
unset key
set border 0
set isosamples 30
set samples 100
set hidden offset 0
set term latex
set output "pde.tex"
set xrange [-2:2]
set yrange [-2:2]
#set zrange [0:8]
set size ratio 1
splot (x**2 + y**2)*sin(7*atan2(x,y))
