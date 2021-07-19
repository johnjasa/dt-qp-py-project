# dt-qp-py-project
## Python version and IDE
- I am currently using python 3.9, and spyder as the IDE [https://www.spyder-ide.org/](https://www.spyder-ide.org/).

## Python Dependencies
- Numpy, Scipy, Matplotlib, and OSQP are the current packages that are being used

## To install OSQP, follow the instructions on the following link
- [https://osqp.org/docs/get_started/python.html](https://osqp.org/docs/get_started/python.html)
- You will need to install GCC [https://gcc.gnu.org/](https://jmeubank.github.io/tdm-gcc/articles/2021-05/10.3.0-release), Cmake [https://cmake.org/](https://cmake.org/), and if you are using windows vsiual studio [https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017)
- After these programs are available, build osqp using the instructions given at the end of the page [https://osqp.org/docs/get_started/python.html](https://osqp.org/docs/get_started/python.html)
 
 ## To Do (in no particular order)
- opts.timer field
- Better documentation throughout the project
- Highlight differences between the python and matlab implementations.
- Wind turbine and additional examples
- DTQPy_plotcommon, plotting is manually done
- DTQPy_commonwindowtask, and other visual imporovements
- Handle Nan cases from the optimizer (currently there in no check)
- Organize the code into the respective folders
- Install and setup file as needed
- Class field names, some are inconsistent and will be changed.
- CQHS, HS methods for thr objective and defects
- DTQPy_mesh_pts currently only ED (equidistant mesh) is possible
