
# BFM module caller
# before lunch compile the f90 code through makefile
# @author : epascolo,plazzari

import bfm_derivative_interface as bfm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm
def fmt_1(x, pos):
    a, b = '{:.1e}'.format(x).split('e')
    return r'${}$ '.format(a)
def fmt_2(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'$ \times 10^{{{}}}$'.format(b)

bfm.init_bfm_derivative()

iidx=np.zeros(6,dtype=np.int32)
bfm.dim_bfm_derivative(iidx)
jptra=iidx[0]; jp_er=iidx[1]; jp_sv=iidx[3]; jptra_dia=iidx[4]; jptra_dia_2d=iidx[5]
#Init state

st_in=np.zeros(jptra,dtype=float)

st_in[0]=240 # Oxygen
st_in[1]=0.25 # Phosphate
st_in[2]=2.0 # Nitrate
st_in[3]=0.5 # Ammonia
st_in[4]=1.
st_in[5]=2.5 # Silicates
st_in[6]=0.1
st_in[7]=8.0
st_in[8]=0.00001
st_in[9]=0.00001
st_in[10]=8.0      #P1c
st_in[11]=0.01     #P1n
st_in[12]=0.001    #P1p
st_in[13]=0.1      #P1s
st_in[14]=0.01     #P1l
st_in[15]=8.0
st_in[16]=0.01
st_in[17]=0.001
st_in[18]=0.1
st_in[19]=8.0
st_in[20]=0.01
st_in[21]=0.001
st_in[22]=0.1
st_in[23]=8.0
st_in[24]=0.01
st_in[25]=0.001
st_in[26]=0.1
st_in[27]=1.2
st_in[28]=0.015
st_in[29]=0.001
st_in[30]=1.2
st_in[31]=0.015
st_in[32]=0.001
st_in[33]=1.2
st_in[34]=0.015
st_in[35]=0.001
st_in[36]=1.2
st_in[37]=0.015
st_in[38]=0.001
st_in[39]=0.01
st_in[40]=0.0004
st_in[41]=0.00004
st_in[42]=0.01
st_in[43]=0.001
st_in[44]=0.01
st_in[45]=0.0004
st_in[46]=0.00004
st_in[47]=0.0004
st_in[48]=2.66E+04
st_in[49]=2.55E+03

st_orig=st_in.copy()

#init environmental state
er_in=np.zeros(jp_er,dtype=float)
er_in[0]=20.
er_in[1]=35.
er_in[2]=1024.
er_in[3]=0.
er_in[4]=390.
er_in[5]=1000000.
er_in[6]=24.
er_in[7]=5.
er_in[8]=1.
er_in[9]=8.
er_orig=er_in.copy()
#Output
so_out=np.zeros(jptra,dtype=float)
sv_out=np.zeros(jp_sv,dtype=float)
di_out=np.zeros(jptra_dia,dtype=float)
di2_out=np.zeros(jptra_dia_2d,dtype=float)
#compute derivative
bfm.calc_bfm_derivative(0, 0, st_in, er_in, so_out, sv_out, di_out, di2_out)

#print(so_out)
#print(sv_out)
#print(di_out)

L=500
dP1c_dt=np.zeros((L,L), dtype=float)
dP2c_dt=np.zeros((L,L), dtype=float)
dP3c_dt=np.zeros((L,L), dtype=float)
dP4c_dt=np.zeros((L,L), dtype=float)
fig = plt.figure()
# P-N PLOT
ax = fig.add_subplot(2,2,1)
PO4_max = 0.00125
NO3_max = 0.025 
NH4_max = 0.0125

PO4_array = np.arange(0.,PO4_max,PO4_max/L)
NO3_array = np.arange(0.,NO3_max,NO3_max/L)
NH4_array = np.arange(0.,NH4_max,NH4_max/L)

for i,pp in enumerate(PO4_array):
    for j,nn in enumerate(NO3_array):
        so_out=np.zeros(jptra,dtype=float)
        st_in[1] = pp;
        st_in[2] = NO3_array[j];
        st_in[3] = NH4_array[j];
        bfm.calc_bfm_derivative(0, 0, st_in, er_in, so_out, sv_out, di_out, di2_out)
        dP1c_dt[i,j]=so_out[10]
        dP2c_dt[i,j]=so_out[15]
        dP3c_dt[i,j]=so_out[19]
        dP4c_dt[i,j]=so_out[23]
    
N_array=NO3_array+NH4_array

#print(data2plot)

#plot 1
plt.contour(N_array,PO4_array,dP1c_dt,levels=[0.,],colors='k',linestyles='dashed',linewidths=(2,))
plt.contour(N_array,PO4_array,dP2c_dt,levels=[0.,],colors='w',linestyles='dashed',linewidths=(2,))
plt.contour(N_array,PO4_array,dP3c_dt,levels=[0.,],colors='g',linestyles='dashed',linewidths=(2,))
plt.contour(N_array,PO4_array,dP4c_dt,levels=[0.,],colors='b',linestyles='dashed',linewidths=(2,))
plt.pcolor(N_array,PO4_array,dP3c_dt, cmap='RdBu')

ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(fmt_1))
ax.set_xlabel('$N$ ' + '$[mmolN.m^{-3}$' + fmt_2(N_array.mean(),0) + '$]$')

ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(fmt_1))
ax.set_ylabel('$PO_4$ ' + '$[mmolP.m^{-3}$ ' + fmt_2(PO4_array.mean(),0) + '$]$')

cint=np.maximum( abs(dP3c_dt.min()), dP3c_dt.max())
plt.clim(-cint,cint)
cb = plt.colorbar(format=ticker.FuncFormatter(fmt_1))
cb.set_label('$NPP_{pico}$ ' + '$[mgC.m^{-3}.s^{-1}$ ' + fmt_2(cint,0) + '$]$')
####################################
# P-I PLOT
st_in=st_orig.copy()

ax = fig.add_subplot(2,2,2)
PO4_max = 0.00125
IRR_max = 100

PO4_array = np.arange(0.,PO4_max,PO4_max/L)
IRR_array = np.arange(0.,IRR_max,IRR_max/L)

for i,pp in enumerate(PO4_array):
    for j,nn in enumerate(IRR_array):
        so_out=np.zeros(jptra,dtype=float)
        st_in[1] = pp;
        er_in[5] = nn;
        bfm.calc_bfm_derivative(0, 0, st_in, er_in, so_out, sv_out, di_out, di2_out)
        dP1c_dt[i,j]=so_out[10]
        dP2c_dt[i,j]=so_out[15]
        dP3c_dt[i,j]=so_out[19]
        dP4c_dt[i,j]=so_out[23]

#print(data2plot)

#plot 1
plt.contour(IRR_array,PO4_array,dP1c_dt,levels=[0.,],colors='k',linestyles='dashed',linewidths=(2,))
plt.contour(IRR_array,PO4_array,dP2c_dt,levels=[0.,],colors='w',linestyles='dashed',linewidths=(2,))
plt.contour(IRR_array,PO4_array,dP3c_dt,levels=[0.,],colors='g',linestyles='dashed',linewidths=(2,))
plt.contour(IRR_array,PO4_array,dP4c_dt,levels=[0.,],colors='b',linestyles='dashed',linewidths=(2,))
plt.pcolor (IRR_array,PO4_array,dP3c_dt, cmap='RdBu')
cint=np.maximum( abs(dP3c_dt.min()), dP3c_dt.max())
plt.clim(-cint,cint)

ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(fmt_1))
ax.set_xlabel('$PAR$ ' + '$[\mu moles.m^{-2}.s^{-1}$' + fmt_2(IRR_array.mean(),0) + '$]$')

ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(fmt_1))
ax.set_ylabel('$PO_4$ ' + '$[mmolP.m^{-3}$ ' + fmt_2(PO4_array.mean(),0) + '$]$')

cb = plt.colorbar(format=ticker.FuncFormatter(fmt_1))
cb.set_label('$NPP_{pico}$ ' + '$[mgC.m^{-3}.s^{-1}$ ' + fmt_2(cint,0) + '$]$')
####################################


# N-I PLOT
st_in=st_orig.copy()
er_in=er_orig.copy()

ax = fig.add_subplot(2,2,3)
NO3_max = 0.025 
NH4_max = 0.0125
IRR_max = 100

NO3_array = np.arange(0.,NO3_max,NO3_max/L)
NH4_array = np.arange(0.,NH4_max,NH4_max/L)
IRR_array = np.arange(0.,IRR_max,IRR_max/L)

for i,nn in enumerate(NO3_array):
    for j,pp in enumerate(IRR_array):
        so_out=np.zeros(jptra,dtype=float)
        st_in[2] = NO3_array[i];
        st_in[3] = NH4_array[i];
        er_in[5] = pp;
        bfm.calc_bfm_derivative(0, 0, st_in, er_in, so_out, sv_out, di_out, di2_out)
        dP1c_dt[i,j]=so_out[10]
        dP2c_dt[i,j]=so_out[15]
        dP3c_dt[i,j]=so_out[19]
        dP4c_dt[i,j]=so_out[23]

#print(data2plot)
N_array=NO3_array+NH4_array

#plot 1
plt.contour(IRR_array,N_array,dP1c_dt,levels=[0.,],colors='k',linestyles='dashed',linewidths=(2,))
plt.contour(IRR_array,N_array,dP2c_dt,levels=[0.,],colors='w',linestyles='dashed',linewidths=(2,))
plt.contour(IRR_array,N_array,dP3c_dt,levels=[0.,],colors='g',linestyles='dashed',linewidths=(2,))
plt.contour(IRR_array,N_array,dP4c_dt,levels=[0.,],colors='b',linestyles='dashed',linewidths=(2,))
plt.pcolor (IRR_array,N_array,dP3c_dt, cmap='RdBu')
cint=np.maximum( abs(dP3c_dt.min()), dP3c_dt.max())
plt.clim(-cint,cint)

ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(fmt_1))
ax.set_xlabel('$PAR$ ' + '$[\mu moles.m^{-2}.s^{-1}$' + fmt_2(IRR_array.mean(),0) + '$]$')

ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(fmt_1))
ax.set_ylabel('$N$ ' + '$[mmolN.m^{-3}$ ' + fmt_2(N_array.mean(),0) + '$]$')

cb = plt.colorbar(format=ticker.FuncFormatter(fmt_1))
cb.set_label('$NPP_{pico}$ ' + '$[mgC.m^{-3}.s^{-1}$ ' + fmt_2(cint,0) + '$]$')
####################################

plt.annotate('Diatom',(50,0.03),color='k',fontsize='8')
plt.annotate('Flagellate',(50,0.027),color='w',fontsize='8')
plt.annotate('Picophytoplankton',(50,0.024),color='g',fontsize='8')
plt.annotate('Dinoflagellate',(50,0.021),color='b',fontsize='8')

plt.tight_layout()
#plt.show()

#bfm.finalize_bfm_derivative()
fileout="prova.png"
plt.savefig(fileout, format='png',dpi=900)
