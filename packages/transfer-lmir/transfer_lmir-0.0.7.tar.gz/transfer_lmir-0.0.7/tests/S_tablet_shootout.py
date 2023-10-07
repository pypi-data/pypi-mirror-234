# NIR shootout
# NIR spectra for 2 probes

import numpy as np
import matplotlib.pyplot as plt
import transfer_lmir as tl


plt.close('all')
print(100*('\n'))

np.random.seed(27)

#%% Load data

wavelength = np.arange(600,1900,2)

# Load data
data = tl.loadmat('nir_tabletshootout_2002.mat')

# # Assay of API
Y = data['calibrate_Y']['data']
Y = Y[:,2][np.newaxis].T # to check

# Delete outliers (based on previous papers)
Y = np.delete(Y, [18,121,125,126], axis=0)

# probe 1
X1 = data['calibrate_1']['data'] 
X1 = np.delete(X1, [18,121,125,126], axis=0)
# Reduce wavelength range (based on previous papers)
X1 = X1[:,:520]


# Probe 2
X2 = data['calibrate_2']['data'] # probe 
X2 = np.delete(X2, [18,121,125,126], axis=0)


#%% Data separation

# Separate Y to have not same y values for each calibration set
# Based on a random sampling but saved here 
randi = [150,86,40,66,118,41,52,98,11,51,121,116,32,113,28,70,85,24,46,37,84,124,63,138,130\
,139,101,82,105,141,134,80,22,140,74,45,36,5,17,97,143,77,133,120,115,49,65,62,148,29,3,39\
,79,13,96,128,60,54,26,8,43,88,111,106,59,15,53,20,14,76,117,12,108,47,58,137,95,94,18,50\
,2,107,81,122,57,30,33,90,119,27,132,91,114,100,21,104,102,7,126,109]
    
Y1 = Y[randi,:]
Y2 = np.delete(Y, [randi], axis=0)

X1 = X1[randi,:]
X2 = np.delete(X2, [randi], axis=0)

#%% Pre-process application 

X1, _ = tl.MSC(X1)
X1 = tl.detrend(X1)

X2 = tl.EMSC(X2)
X2 = tl.SNV(X2)

X1_0 = X1.copy()
X2_0 = X2.copy()

# Autoscale
X1, _, _ = tl.autoscale(X1)
X2, _, _ = tl.autoscale(X2)

#%% Data separation

rand = [14,20,47,44,6,9,27,23,28,39]

X2c = X2[rand, :]
Y2c = Y2[rand,:]

X2v = np.delete(X2, rand, axis=0)
Y2v = np.delete(Y2, rand, axis=0)

X2c_0 = X2_0[rand, :]
X2v_0 = np.delete(X2_0, rand, axis=0)

#%% Y scaling

Y1_0 = Y1.copy()
Y1, ym1, ys1 = tl.autoscale(Y1)

Y2c_0 = Y2c.copy()
Y2v_0 = Y2v.copy()
Y2c = (Y2c - ym1)/ys1
Y2v = (Y2v - ym1)/ys1

#%% PLS


# =============================================================================
#   Random subset Cross validation
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

# =============================================================================
#  Modeling
# =============================================================================


nbPC = 3
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
plt.plot(Y2v_0, Yhat_v,'o',c='r', label='validation')
plt.text(210,170,'RMSEcal = '+str(np.round(RMSEC,1)), c='b')
plt.text(210,160,'RMSEval = '+str(np.round(RMSEV,1)), c='r')
plt.xlabel("y expected (mg)", fontsize=12)
plt.ylabel("y predicted (mg)", fontsize=12)
plt.title('(A) PLS, 3 EF', fontsize=14, fontweight='bold')
plt.legend()
plt.grid()


# %% P-PLS

# =============================================================================
#   Random subset Cross validation
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
plt.plot(Y2v_0, Yhat_v,'o',c='r', label='validation')
plt.text(210,170,'RMSEcal = '+str(np.round(RMSEC,1)), c='b')
plt.text(210,160,'RMSEval = '+str(np.round(RMSEV,1)), c='r')
plt.xlabel("y expected (mg)", fontsize=12,)
plt.ylabel("y predicted (mg)", fontsize=12,)
plt.title('(B) P-PLS, 1 EF', fontsize=14, fontweight='bold')
plt.legend()
plt.grid()


# %% LMIR for probe 2

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
plt.plot(Y2c_0, ypred_cal2, 'ob')
plt.plot(Y2v_0, ypred_all2, 'or')
plt.plot(np.unique(Y1_0), np.unique(Y1_0),'-k')
plt.text(210,170,'RMSEcal = '+str(np.round(RMSEC,1)), c='b')
plt.text(210,160,'RMSEval = '+str(np.round(RMSEV,1)), c='r')
plt.xlabel("y expected (mg)", fontsize=12,)
plt.ylabel("y predicted (mg)", fontsize=12,)
plt.title('(C) LMIR', fontsize=14, fontweight='bold')
plt.grid()


# %% LMIR


model, ypred1 = tl.LMIR_create(X1, Y1)

f = np.diag(model["covE"])<0.3
f1 = np.diag(model["covE"])
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

factor_k =0.02
R1_all, g1_all, R2_all, g2_all = tl.estimation_model(X1, Y1, X2c, Y2c,factor_k,nb_pairs=30)

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
plt.plot(Y2v_0,ypred_all,'o',c='r', label='validation')
plt.text(210,170,'RMSEcal = '+str(np.round(RMSECt,1)), c='b')
plt.text(210,160,'RMSEval = '+str(np.round(RMSEV,1)), c='r')
plt.xlabel("y expected (mg)", fontsize=12,)
plt.ylabel("y predicted (mg)", fontsize=12,)
plt.title('(D) CT', fontsize=14, fontweight='bold')
plt.legend()
plt.grid()
