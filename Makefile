# remeber: compile bfm library with -g and -fPIC
# @author : epascolo, plazzari

FC=ifort
CC=icc
F2PY= f2py3

NETCDF_LIBRARY= -L$(NETCDF_LIB) -L$(NETCDFF_LIB) -lnetcdff -lnetcdf
NETCDF_INCLUDE = -I$(NETCDFF_INC)
BFM_LIB = -L../bfm/lib -lbfm
BFM_INCLUDE = -I../bfm/include


bfm_derivative_interface: bfm_derivative_ppc.f90 
	$(F2PY) -c $^ --f90flags=-g --fcompiler=intelem $(NETCDF_INCLUDE) $(BFM_INCLUDE) $(NETCDF_LIBRARY) $(BFM_LIB) -m $@

bfm_derivative_ppc.f90: bfm_derivative.F90
	$(FC)  -P  -D PYTHON_WRAPPER $(BFM_INCLUDE) -o $@  $<

clean:
		rm *.so bfm_derivative_ppc.f90

.PHONY: clean
