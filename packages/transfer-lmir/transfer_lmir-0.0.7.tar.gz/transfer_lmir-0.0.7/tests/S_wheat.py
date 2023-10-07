# Calibration transfer by likelihood maximization
# Wheat dataset


import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import transfer_lmir as tl


plt.close('all')

np.random.seed(7)

#%% LOAD DATA

dataset = np.load('IDRC2016_wheat.npy', allow_pickle=True)
    
X_A1 = dataset.item().get('A1')

X_A5 = dataset.item().get('A5')

X_B5 = dataset.item().get('B5')

X_C2 = dataset.item().get('C2')

Y = dataset.item().get('Y1')
Yvalid = dataset.item().get('Y2')

# Wavelength probe 2
wavelength2 = np.arange(850,1050,2)


#------List of samples selected for data separation-------
# Primary instrument (validation samples-58)
# Samples randomly selected for different y-values to get evenly distributed samples 
sel = np.array([164,176,150,16,70,156,149,170,167,122,2,197,39,11,189,162,194,140\
,38,179,68,123,27,173,229,28,67,215,207,240,221,76,180,102,188,193,135,92\
,48,17,136,235,103,94,208,243,41,79,40,101,226,205,127,33,201,18,143,202], dtype='int')

# Secondary instruments (calibration transfer samples-10)
# A sample randomly selected per protein content

# A5
randA = np.array([134,0,94,86,87,88,110,72,51,45], dtype='int')
# B5
randB = np.array([120,35,32,125,47,114,89,39,98,24], dtype='int')
# C2
randC = np.array([38,44,91,43,71,22,89,108,25,17], dtype='int')


rand1 = [randA, randB, randC]
rand1 = {'A5':randA, 'B5':randB, 'C2':randC}


#%% CHOOSE IF MODELING IN LMIR WITH LINEAR OR NON-LINEAR RELATION

linear = input('Would you like to perform a linear modeling with LMIR ? (0 (linear)/ 1 (non-linear) ')
linear = int(linear)

if linear==0:
    linear = True
    print('\n')
    print('Choice 0: Linear realtionship between y and each variable of X in LMIR.')
else:
    linear = False
    print('\n')
    print('Choice 1: Non-linear realtionship between y and each variable of X in LMIR.')

#%% PRE-TREATMENT

# =============================================================================
# # Declare instruments
# =============================================================================

instruments = {'A1':X_A1, 'A5':X_A5, \
                'B5':X_B5,\
                'C2':X_C2}

primary_key = 'A1'    

# =============================================================================
# # Modify spectra  - truncate & interpolate 
# =============================================================================
# Common wavelength range for instruments
wavelength_mod = np.arange(850,1048.5,0.5)

# Create dictionnary to save modified spectra: truncated and interpolated
instruments_mod = instruments.copy()

# Interpolate spectra for manufacturer C
Xi = instruments_mod['C2']  
X2_interpolated = np.zeros((len(Xi),len(wavelength_mod)))
for i in range(len(Xi)):
    interp_func = interp1d(wavelength2, Xi[i,:])
    X2_interpolated[i,:] = interp_func(wavelength_mod)
instruments_mod['C2'] = X2_interpolated

# Define primary instrument
X1 = instruments_mod[primary_key]    

# Define list of secondary isntruments
secondary = instruments_mod.copy()
del secondary[primary_key]

# =============================================================================
# # Pre-process
# # Separate calibration & validation
# =============================================================================

# Save pre-processed spectra before auto-scale
secondary_p = secondary.copy()

# Save calibration samples 
secondary_c = secondary.copy()
secondary_v = secondary.copy()

#------- Primary instrument ---------
# Pre-process
X1 = tl.EMSC(X1)
X1 = tl.savitzky_golay(X1,15,2,2)

# Cutting extremities because of SG
X1 = X1[:,7:390]
# Autoscale
X1, xm1, xs1 = tl.autoscale(X1)
# Data separation
X1v = X1[sel,:] # validation
X1c = np.delete(X1, sel, axis=0) # cailbration

#------- Secondary instrument ---------
for key in secondary: 
    # Pre-process
    Xi = secondary[key]
    Xi = tl.EMSC(Xi)    
    Xi = tl.savitzky_golay(Xi,15,2,2)    
    # Cutting extremities because of SG
    Xi = Xi[:,7:390]  
    secondary_p[key] = Xi.copy()
    # Autoscale
    Xi, _, _ = tl.autoscale(Xi)
    # Data separation
    secondary_c[key] = Xi[rand1[key],:] # calibration transfer
    secondary_v[key] = np.delete(Xi, rand1[key], axis=0) # validation

#------- Y values ---------

# Dataset 1
Y_0 = Y.copy()
# Autoscale
Y, ym1, ys1 = tl.autoscale(Y)
# Data speration
Y1v_0 = Y_0[sel,:] # validation without autoscale
Y1v = Y[sel,:] # validation 
Y1c = np.delete(Y, sel, axis=0) # calibration without autoscale
Y1c_0 = np.delete(Y_0, sel, axis=0) # calibration


# Dataset 2
Yvalid0 = Yvalid.copy()
# Autoscale
Yvalid = (Yvalid - ym1)/ys1


Y2c = {'A5':None, 'B5':None, 'C2':None}
Y2v = {'A5':None, 'B5':None, 'C2':None}
Y2c_0 = {'A5':None, 'B5':None, 'C2':None}
Y2v_0 = {'A5':None, 'B5':None, 'C2':None}

for key in secondary: 
    # Data separation
    Y2c[key] = Yvalid[rand1[key]] # calibration transfer
    Y2v[key] = np.delete(Yvalid, rand1[key], axis=0) # validation
    Y2c_0[key] = Yvalid0[rand1[key]] # calibration transfer without autoscale
    Y2v_0[key] = np.delete(Yvalid0, rand1[key], axis=0) # validation without autoscale



#%% LMIR

model, ypred1 = tl.LMIR_create(X1c, Y1c,linear)

f = np.diag(model["covE"])<0.3
f1 = np.diag(model["covE"])
X1c = X1c[:,f]

n1, k1  = X1c.shape
model, ypred1 = tl.LMIR_create(X1c, Y1c,linear)

ypred1 = ypred1*ys1 + ym1
E = ypred1 - Y1c_0
MSE = np.mean(E**2)
RMSEC1 = np.sqrt(np.mean(E**2))  
R2_c1 = tl.fct_R2(Y1c_0, ypred1)

print('\nCalibration LMIR on probe 1')
print('RMSE: ', np.round(RMSEC1, 1))
print('R2: ', np.round(R2_c1[0], 2))

X1v = X1v[:,f]
ypred_v1 = tl.LMIR_exploit(X1v, model)
ypred_v1 = ypred_v1*ys1 + ym1
E = ypred_v1 - Y1v_0
MSE = np.mean(E**2)
RMSEV1 = np.sqrt(np.mean(E**2))  
R2_v1 = tl.fct_R2(Y1v_0, ypred_v1)

print('\nValidation LMIR on probe 1')
print('RMSE: ', np.round(RMSEV1, 1))
print('R2: ', np.round(R2_v1[0], 2))

plt.figure()
plt.plot(np.arange(8,20), np.arange(8,20),'-k')
plt.plot(Y1c_0,ypred1,'ob',label='calibration')
plt.plot(Y1v_0,ypred_v1,'o',c='orange', label='validation')
plt.text(16,9,'RMSEC = '+str(np.round(RMSEC1,1)), c='b')
plt.text(16,8,'RMSEV = '+str(np.round(RMSEV1,1)), c='orange')
plt.xlabel("y expected (%)", fontsize=12,)
plt.ylabel("y predicted (%)", fontsize=12,)
plt.title(str(primary_key), fontsize=16, fontweight='bold')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('Primary',dpi=300)

#%% Cal transfer with LMIR

for key in secondary:
    X2c = secondary_c[key]
    X2v = secondary_v[key]
    
    factor_k = 0.01
    R1_all, g1_all, R2_all, g2_all = tl.estimation_model(X1c, Y1c, X2c, Y2c[key],factor_k,nb_pairs=30)
    ypred_ct, x1hat_ct, covx1_ct = tl.estimation_exploit(R1_all,g1_all,R2_all,g2_all,X2c,X1c,model)
    
    ypred_ct = ypred_ct*ys1 + ym1
    E = ypred_ct - Y2c_0[key]
    RMSECt = np.sqrt(np.mean(E**2))
    R2_ct = tl.fct_R2(Y2c_0[key], ypred_ct)
    
    
    ypred_all, x1hat_all, covx1_all = tl.estimation_exploit(R1_all,g1_all,R2_all,g2_all,X2v,X1c,model)
    
    ypred_all = ypred_all*ys1 + ym1
    E = ypred_all - Y2v_0[key]
    MSEv = np.mean(E**2)
    RMSEV = np.sqrt(np.mean(E**2))  
    R2_v = tl.fct_R2(Y2v_0[key], ypred_all)
    
    # =============================================================================
    # Results
    # =============================================================================
    
    print('\nResults for calibration transfer for probe : ',key)
    print('R2 calibration: ', np.round(R2_ct[0],2))
    print('RMSE calibration: ', np.round(RMSECt,1))
    print('R2 validation: ', np.round(R2_v[0],2))
    print('RMSE validation: ', np.round(RMSEV,1))
    

    if 'A' in key:    
        list_outlier = [58,59,52,54]
        list_r = [1,2,3,4]   
    elif 'B' in key:
        list_outlier = [56,57,50,52,124]
        list_r = [1,2,3,4,5]
    else:
        list_outlier = [55,56,49,51]
        list_r = [1,2,3,4]          
    
    plt.figure()
    plt.plot(np.unique(Y1c_0), np.unique(Y1c_0),'-k')
    plt.plot(Y2c_0[key],ypred_ct,'ob',label='calibration')
    plt.plot(Y2v_0[key],ypred_all,'o',c='orange', label='validation')
    plt.plot(Y2c_0[key],ypred_ct,'ob')
    for i in range(len(list_outlier)):
        plt.text(Y2v_0[key][list_outlier[i]], ypred_all[list_outlier[i]], list_r[i])
    plt.text(16,9,'RMSEC = '+str(np.round(RMSECt,1)), c='b')
    plt.text(16,8,'RMSEV = '+str(np.round(RMSEV,1)), c='orange')
    plt.xlabel("y expected (%)", fontsize=14)
    plt.ylabel("y predicted (%)", fontsize=14)
    plt.title(str(key), fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('CT_'+str(key),dpi=300)
    
    # Model without outlier samples
    Y2vr_0 = np.delete(Y2v_0[key], list_outlier, axis=0)
    ypred_allr = np.delete(ypred_all, list_outlier, axis=0)
    
    E = ypred_allr - Y2vr_0
    RMSEV2 = np.sqrt(np.mean(E**2))
    print('RMSEV excluding outliers', np.round(RMSEV2,2))
