# CSST_parameter
The code is used to estimate the metallicity and effective temperature of the stars from the CSST broad-band filter systems. It is worth noting that only FGK-type stars are valid.
# How to install

    #from PyPI
    pip install CSST
# Quick start 
The input are NUV, u, g, i, z, y magnitudes and color error. An assumption that magnitudes are independent Gaussian variables is made. You can precess the data through the command line like this. 

    from CSST import CSST
    CSST.CSST_parameter(NUV,u,g,i,z,y,error) 
The output is one file named CSST_parameter.csv, which stores the photometric metallicity and the effective temperature of the stars.
# An example
If a file (a.csv) is given, NUV, u, g, i, z, y magnitudes are contained in this file. Once the color error is given, you can precess the data through the command line like this.

    py
    import pandas as pd
    data=pd.read_csv('a.csv')
    NUV0=data.loc[:,['NUV']].values
    u0=data.loc[:,['u']].values
    g0=data.loc[:,['g']].values
    i0=data.loc[:,['i']].values
    z0=data.loc[:,['z']].values
    y0=data.loc[:,['y']].values
    NUV,u,g,i,z,y=NUV0.flatten(),u0.flatten(),g0.flatten(),i0.flatten(),z0.flatten(),y0.flatten()
    # give the color error
    error=(0.01**2+0.01**2)**0.5
    # estimate the parameter of the stars 
    from CSST import CSST
    CSST.CSST_parameter(NUV,u,g,i,z,y,error)           
The output is one file named CSST_parameter.csv, which stores the photometric metallicity and the effective temperature of the stars.
# API

    CSST_parameter(NUV,u,g,i,z,y,error)
           
    Args:      
        
        NUV: array-like, shape (n, )
           CSST NUV band
        
        u: array-like, shape (n, )
           CSST u band
        
        g: array-like, shape (n, )
           CSST g band
           
        i: array-like, shape (n, )
           CSST i band

        z: array-like, shape (n, )
           CSST z band
           
        y: array-like, shape (n, )
           CSST y band           
           
        error: float
           color error.     
