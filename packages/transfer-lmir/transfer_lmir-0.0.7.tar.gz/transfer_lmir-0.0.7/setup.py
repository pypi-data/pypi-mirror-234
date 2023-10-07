import setuptools


setuptools.setup(
    name="transfer_lmir",
    version="0.0.7",
    author="Giverny Robert, Francis B. Lavoie, Ryan Gosselin",
    author_email="giverny.robert@usherbrooke.ca, francis.b.lavoie@usherbrooke.ca, ryan.gosselin@usherbrooke.ca",
    
    packages=["transfer_lmir"],
    description="Functions to perform calibration transfer with LMIR",
    long_description="\nFunctions to perform calibration transfer by likelihood maximization: a standard-free approach capable of handling non-overlapping wavelength ranges.\
        \n\
        \nIn this approach, calibration for spectral data on primary instrument is performed by likelihood maximization inverse regression (LMIR).\
        \nBased on a limited number of spectra from a secondary instrument and the corresponding reference values, an estimation model is created based on block pairs.\
        \nThe latter can then be used to estimate spectra from secondary instrument in the domain of primary instrument to be able to use to primary calibration.\
        \n\
        \nCf: F.B. Lavoie, A. Langlet, K. Muteki, R. Gosselin, Likelihood Maximization Inverse Regression: A novel non-linear multivariate model, Chemom. Intell. Lab. Syst. 194 (2019) 103844. https://doi.org/10.1016/j.chemolab.2019.103844.\
        \n\
        \nF.B. Lavoie, G. Robert, A. Langlet, R. Gosselin, Calibration transfer by likelihood maximization : A standard-free approach capable of handling non-overlapping wavelength ranges, Chemom. Intell. Lab. Syst. 234 (2023) 104766. https://doi.org/10.1016/j.chemolab.2023.104766.\
        \n\
        \n# Call function\
        \nmodel, ypred = LMIR_create(X1,Y1,linear=True)\
        \n\
        \nR1_all, g1_all, R2_all, g2_all = estimation_model(X1, Y1, X2c, Y2c,factor_k,nb_pairs=30,B)\
        \n\
        \nypred_ct, x1hat_ct, covx1_ct = estimation_exploit(R1_all,g1_all,R2_all,g2_all,X2v,X1,model)\
        \n\
        \n# Input arguments\
        \n1. X1 (n1,k1): spectral data from primary instrument\
        \n2. Y1 (n1,1): reference values for spectra from primary instrument\
        \n3. X2c (n2,k2): spectral data from secondary instrument\
        \n4. Y2c (n2,1): reference values for spectra from secondary instrument\
        \n5. factor_k: parameter for supervised selection of observations for estimation model\
        \n6. X2v: spectral data from secondary instrument for validation\
        \n\
        \n# Optional input arguments\
        \n7. linear: option to create linear or non-linear models linking y to each varibale in X for LMIR modeling (default_value=True for linear modeling)\
        \n8. nb_pairs: number of block pairs in estimation model (default_value=30)\
        \n9. B: number of variable bootstrapping trials (default_value=3*max(k1,k2))\
        \n\
        \n# Outputs\
        \n1. model: model created by LMIR\
        \n2. ypred: predicted values by LMIR\
        \n3. R1_all, g1_all, R2_all, g2_all: blocks pairs in estimation model\
        \n4. ypred_ct: predicted values using estimation model and LMIR model from spectra from secondary instrument\
        \n5. x1hat_ct: estimated spectra in domain of primary instrument\
        \n6. covx1_ct: uncertainty associated to estimation of spectra in domain of primary instrument\
        \n\
        \n# Examples\
        \nTwo full examples, along with datasets are provided in folder 'tests' of 'Download Files'.\
        \n- Example 1: Tablet shootout dataset\
        \n- Example 2: Coating times dataset\
        \n- Example 3: Wheat shootout dataset\
        \n\
        \n# Compatibility\
        \ntransfer_lmir tested on Python 3.8 using the following modules:\
        \n- numpy 1.20.1\
        \n- matplotlib 3.3.4\
        \n- SciPy 1.6.2",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)