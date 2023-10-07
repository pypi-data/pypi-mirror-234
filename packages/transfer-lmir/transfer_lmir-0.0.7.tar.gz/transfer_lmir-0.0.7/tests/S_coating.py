# Coating times
# NIR spectra for 2 probes

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import transfer_lmir as tl

plt.close('all')
print(100*('\n'))

np.random.seed(18)

#%% Load data

wavelength1 = np.linspace(600,1898,256)
wavelength2 = np.linspace(800,2779,4615)

# Load data
data = tl.loadmat('coating.mat')

X1 = data['X1']
Y1 = data['Y1']
Y1 = Y1[np.newaxis].T
Y1 = np.array(Y1, dtype=float)

X2 = data['X2']
Y2 = data['Y2']
Y2 = Y2[np.newaxis].T
Y2 = np.array(Y2, dtype=float)

# Delete outlier
X1 = np.delete(X1, [1037],axis=0)
Y1 = np.delete(Y1, [1037],axis=0)


#%%  Reduction of X2

# =============================================================================
# Option 1: bin directly all spectra from X2 to 576 variables
# =============================================================================

# Bin directly X2
X2b = st.binned_statistic(np.round(wavelength2), X2, 'mean', \
                              576).statistic
    
wavelength2b = st.binned_statistic(np.round(wavelength2), wavelength2, 'mean', \
                              576).statistic


X2 = X2b

#%%

X1 = tl.SNV(X1)
for i in range(len(X1)):
    X1[i,:] = np.gradient(X1[i,:])

X2 = tl.SNV(X2)
for i in range(len(X2)):
    X2[i,:] = np.gradient(X2[i,:])


# Autoscale
X1, xm1, _ = tl.autoscale(X1)
X2, xm2, _ = tl.autoscale(X2)

plt.figure()
plt.plot(wavelength1, xm1.T,'-',c='deepskyblue', label='probe 1')
plt.plot(wavelength2b, xm2.T,'-b', label='probe 2')
plt.legend()
plt.xlabel('Wavelength (nm)', fontsize=12)
plt.ylabel('Absorbance', fontsize=12)
plt.title('(B)', fontsize=14, fontweight='bold')




#%% Data separation

# Select calibration samples - from random sampling
rand = [13,38,18,20,30,44,22,45,33,34,3,43,40,36,35]

X2c = X2[rand, :]
Y2c = Y2[rand,:]

X2v = np.delete(X2, rand, axis=0)
Y2v = np.delete(Y2, rand, axis=0)

#%% Y scaling

Y1_0 = Y1.copy()
Y1, ym1, ys1 = tl.autoscale(Y1)

Y2c_0 = Y2c.copy()
Y2v_0 = Y2v.copy()
Y2c = (Y2c - ym1)/ys1
Y2v = (Y2v - ym1)/ys1

#%% PLS


# =============================================================================
#  Random subset Cross validation
# =============================================================================

# RMSECV_all = []

# for nbPC in range(1,10):    
#     E = []  
    
#     nb = 100 # Number of random picks
#     CVnb = 5 # Number of lines predicted in each CV
#     for i in range(nb):
#         r = np.random.choice(X2c.shape[0], CVnb, replace=False)
#         Xcv = np.delete(X2c, r, 0)
#         Ycv = np.delete(Y2c, r, 0)
    
#         T, U, P, W, Q, B, Yhat, SSX, SSY = tl.PLS(Xcv,Ycv, nbPC)  
#         Wstar = W@np.linalg.inv(P.T@W)
#         beta = Wstar@B@Q.T
        
#         Xpred = X2c[r,:]
#         Ypred = Y2c[r,:]
        
#         Yhat = Xpred@beta
#         e = Ypred - Yhat
#         E.append(e)
      
#     E = np.array(E)    
    
#     RMSECV = np.sqrt(np.mean(E**2))
#     RMSECV_all.append(RMSECV)

# RMSECV_all = np.array(RMSECV_all)

# plt.figure()
# plt.plot(np.arange(1,len(RMSECV_all)+1), RMSECV_all,'-b')
# plt.xlabel('Number of principal components')

# print('nbPC: 1')

# =============================================================================
#  Modeling
# =============================================================================


nbPC = 1
T, U, P, W, Q, B, Yhat, SSX, SSY = tl.PLS(X2c,Y2c,nbPC)
Wstar = W@np.linalg.inv(P.T@W)
beta = Wstar@B@Q.T

Yhat_c = (X2c@beta)*ys1+ym1
R2_c = tl.fct_R2(Y2c_0,Yhat_c)
E = Yhat_c - Y2c_0
RMSEC = np.sqrt(np.mean(E**2))

Yhat_v = (X2v@beta)*ys1+ym1
R2_v = tl.fct_R2(Y2v_0,Yhat_v)
E = Yhat_v - Y2v_0
RMSEV = np.sqrt(np.mean(E**2))

print('\nResults for PLS : ')
print('R2 calibration: ', np.round(R2_c[0],2))
print('RMSE calibration: ', np.round(RMSEC,1))

print('R2 validation: ', np.round(R2_v[0],2))
print('RMSE validation: ', np.round(RMSEV,1))

plt.figure(figsize=(5, 4))
plt.plot(np.unique(Y1_0), np.unique(Y1_0),'-k')
plt.plot(Y2c_0, Yhat_c,'ob',label='calibration')
plt.plot(Y2v_0, Yhat_v,'o',c='g', label='validation')
plt.text(10,2,'RMSEcal = '+str(np.round(RMSEC,1)), c='b')
plt.text(10,0,'RMSEval = '+str(np.round(RMSEV,1)), c='g')
plt.xlabel("y expected (min)", fontsize=12,)
plt.ylabel("y predicted (min)", fontsize=12,)
plt.title('(A) PLS, 1 EF', fontsize=14, fontweight='bold')
plt.legend()
plt.grid()
plt.tight_layout()

#%% P-PLS

# =============================================================================
#  Random subset Cross validation
# =============================================================================

# RMSECV_all = []

# for nbPC in range(1,10):    
#     E = []  
    
#     nb = 100 # Number of random picks
#     CVnb = 5 # Number of lines predicted in each CV
#     for i in range(nb):
#         r = np.random.choice(X2c.shape[0], CVnb, replace=False)
#         Xcv = np.delete(X2c, r, 0)
#         Ycv = np.delete(Y2c, r, 0)
    
#         beta, all_scores, y_pred_final = tl.PPLS(Xcv,Ycv,nbPC) 

#         Xpred = X2c[r,:]
#         Ypred = Y2c[r,:]
#         Yhat = (np.sum(Xpred@beta.T,axis=1)).T

#         e = Ypred - Yhat
#         E.append(e)
      
#     E = np.array(E)    
    
#     RMSECV = np.sqrt(np.mean(E**2))
#     RMSECV_all.append(RMSECV)

# RMSECV_all = np.array(RMSECV_all)

# plt.figure()
# plt.plot(np.arange(1,len(RMSECV_all)+1), RMSECV_all,'-b')
# plt.xlabel('Number of principal components')

# print('nbPC: 1 option 1')


# =============================================================================
#  Modeling
# =============================================================================


nbPC = 1
beta, all_scores, y_pred_final = tl.PPLS(X2c,Y2c,nbPC) 

Yhat_c = (np.sum(X2c@beta.T,axis=1)*ys1+ym1).T
R2_c = tl.fct_R2(Y2c_0,Yhat_c)
E = Yhat_c - Y2c_0
RMSEC = np.sqrt(np.mean(E**2))

Yhat_v = (np.sum(X2v@beta.T,axis=1)*ys1+ym1).T
R2_v = tl.fct_R2(Y2v_0,Yhat_v)
E = Yhat_v - Y2v_0
RMSEV = np.sqrt(np.mean(E**2))

print('\nResults for P-PLS : ')
print('R2 calibration: ', np.round(R2_c[0],2))
print('RMSE calibration: ', np.round(RMSEC,1))

print('R2 validation: ', np.round(R2_v[0],2))
print('RMSE validation: ', np.round(RMSEV,1))


plt.figure(figsize=(5, 4))
plt.plot(np.unique(Y1_0), np.unique(Y1_0),'-k')
plt.plot(Y2c_0, Yhat_c,'ob',label='calibration')
plt.plot(Y2v_0, Yhat_v,'o',c='g', label='validation')
plt.text(10,2,'RMSEcal = '+str(np.round(RMSEC,1)), c='b')
plt.text(10,0,'RMSEval = '+str(np.round(RMSEV,1)), c='g')
plt.xlabel("y expected (min)", fontsize=12,)
plt.ylabel("y predicted (min)", fontsize=12,)
plt.title('(B) P-PLS, 1 EF', fontsize=14, fontweight='bold')
plt.legend()
plt.grid()
plt.tight_layout()

#%% LMIR for probe 2

model, ypred_cal2 = tl.LMIR_create(X2c, Y2c)

ypred_cal2 = ypred_cal2*ys1 + ym1
E = ypred_cal2 - Y2c_0
MSEc = np.mean(E**2)
RMSEC = np.sqrt(np.mean(E**2))  
R2 = tl.fct_R2(Y2c_0, ypred_cal2)

print('\nResults for LMIR')
print('R2 calibration: ', np.round(R2[0], 1))
print('RMSE calibration: ', np.round(RMSEC, 1))

# Validation directly
ypred_all2 = tl.LMIR_exploit(X2v, model)

ypred_all2 = ypred_all2*ys1 + ym1
E = ypred_all2 - Y2v_0
MSEv = np.mean(E**2)
RMSEV = np.sqrt(np.mean(E**2))  
R2v = tl.fct_R2(Y2v_0, ypred_all2)

print('R2 validation: ', np.round(R2v[0], 2))
print('RMSE validation: ', np.round(RMSEV, 1))


plt.figure(figsize=(5, 4))
plt.plot(Y2c_0, ypred_cal2, 'ob',label='calibration')
plt.plot(Y2v_0, ypred_all2, 'og',label='validation')
plt.plot(np.unique(Y1_0), np.unique(Y1_0),'-k')
plt.text(10,2,'RMSEcal = '+str(np.round(RMSEC,1)), c='b')
plt.text(10,0,'RMSEval = '+str(np.round(RMSEV,1)), c='g')
plt.legend()
plt.xlabel("y expected (min)", fontsize=12,)
plt.ylabel("y predicted (min)", fontsize=12,)
plt.title('(C) LMIR', fontsize=14, fontweight='bold')
plt.grid()
plt.tight_layout()

#%% LMIR


model, ypred1 = tl.LMIR_create(X1, Y1)
f = np.diag(model["covE"])<0.3
X1 = X1[:,f]

n1, k1  = X1.shape
model, ypred1 = tl.LMIR_create(X1, Y1)

ypred1 = ypred1*ys1 + ym1
E = ypred1 - Y1_0
MSE = np.mean(E**2)
RMSEC1 = np.sqrt(np.mean(E**2))  
R2_1 = tl.fct_R2(Y1_0, ypred1)

print('\nCalibration LMIR on probe 1')
print('RMSE: ', np.round(RMSEC1, 1))
print('R2: ', np.round(R2_1[0], 2))


# %% Cal transfer   

factor_k =0.001
R1_all, g1_all, R2_all, g2_all = tl.estimation_model(X1, Y1, X2c, Y2c,factor_k, nb_pairs=20)

ypred_ct, x1hat_ct, covx1_ct = tl.estimation_exploit(R1_all,g1_all,R2_all,g2_all,X2c,X1,model)

ypred_ct = ypred_ct*ys1 + ym1
E = ypred_ct - Y2c_0
RMSECt = np.sqrt(np.mean(E**2))
R2_ct = tl.fct_R2(Y2c_0, ypred_ct)


ypred_all, x1hat_all, covx1_all = tl.estimation_exploit(R1_all,g1_all,R2_all,g2_all,X2v,X1,model)
ypred_all = ypred_all*ys1 + ym1
E = ypred_all - Y2v_0
MSEv = np.mean(E**2)
RMSEV = np.sqrt(np.mean(E**2))  
R2_v = tl.fct_R2(Y2v_0, ypred_all)


#%% Results

print('\nResults for calibration transfer: ')
print('R2 calibration: ', np.round(R2_ct[0],2))
print('RMSE calibration: ', np.round(RMSECt,1))
print('R2 validation: ', np.round(R2_v[0],2))
print('RMSE validation: ', np.round(RMSEV,1))


plt.figure(figsize=(5, 4))
plt.plot(np.unique(Y1_0), np.unique(Y1_0),'-k')
plt.plot(Y2c_0,ypred_ct,'ob',label='calibration')
plt.plot(Y2v_0,ypred_all,'o',c='g', label='validation')
plt.text(10,2,'RMSEcal = '+str(np.round(RMSECt,1)), c='b')
plt.text(10,0,'RMSEval = '+str(np.round(RMSEV,1)), c='g')
plt.xlabel("y expected (min)", fontsize=12,)
plt.ylabel("y predicted (min)", fontsize=12,)
plt.title('(D) CT', fontsize=14, fontweight='bold')
plt.legend()
plt.grid()
plt.tight_layout()
