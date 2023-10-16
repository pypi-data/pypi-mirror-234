# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 17:35:02 2023

@author: lenovo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 08:29:59 2023

@author: lenovo
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:33:31 2023

@author: lenovo
"""




def dwarf(u,g,i,z,y,error):
    '''
    This function can be used to estimate the metallicity and effective 
    temperature of the dwarf stars from the CSST broad-band filter systems.

    Args:      
        
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
           color error. An assumption that (u-g) and (g-i) are independent Gaussian variables
           is made.
           
    The output is one file named parameter_dwarf.csv, which stores the photometric metallicity and 
    the effective temperature of the dwarf stars.
    '''

    import numpy as np
    import pandas as pd
    import glob
    import os


    
    xdata=g-i
    ydata=u-g
    xdata1=g-z
    ydata1=g-y    
    #First step: refuse data beyond the applicability range
    m=[]
    n=[]
    m1=[]
    n1=[]
    a,b=0.66,1.24   #a,b denote the lower and upper limit of given (g-i), respectively
    ind=np.where((xdata>a)&(xdata<b))
    xdata=xdata[ind]
    ydata=ydata[ind]  
    xdata1=xdata1[ind]
    ydata1=ydata1[ind]
    for i in np.arange(0,len(xdata)):
        x=xdata[i]
        y=ydata[i]
        x1=xdata1[i]
        y1=ydata1[i]
        m.append(x)   # m is a list to store (g-i) data
        n.append(y)   # n is a list to store (u-g) data
        m1.append(x1) # m1 is a list to store (g-z) data
        n1.append(y1) # n1 is a list to store (g-y) data
    np.savetxt("dwarf_g-i.csv",m)
    np.savetxt("dwarf_u-g.csv",n)  
    np.savetxt("dwarf_g-z.csv",m1)
    np.savetxt("dwarf_g-y.csv",n1)
        
    xdata,ydata=g-i,u-g   
    m=[]
    n=[]    
    m1=[]
    n1=[]
    a,b=0.39,0.66   
    ind=np.where((xdata>a)&(xdata<b))
    xdata=xdata[ind]
    ydata=ydata[ind]
    xdata1=xdata1[ind]
    ydata1=ydata1[ind]
    c=-1.5*np.ones(len(xdata))  # c is [Fe/H]=-1.5 contour
    a00= 1.0333132              # ten polynmial coefficients
    a01= 0.15225969
    a02= 0.04563865
    a03= 0.00146742
    a10=-0.83203227
    a11= 0.24577474
    a12=-0.00143212
    a20= 2.64502924
    a21=-0.07469603
    a30=-0.9814263
    need=a00+a01*c+a02*c**2+a03*c**3+a10*xdata+a11*xdata*c+a12*xdata*c**2\
             +a20*xdata**2+a21*xdata**2*c+a30*xdata**3       # choose data above [Fe/H]= -1.5 contour when 0.39<(g-i)<0.66
    ind=np.where(ydata>=need)  
    xdata1=xdata1[ind]
    ydata1=ydata1[ind]
    xdata=xdata[ind]
    ydata=ydata[ind] 
    for i in np.arange(0,len(xdata)):
        x=xdata[i]
        y=ydata[i]
        x1=xdata1[i]
        y1=ydata1[i]
        m.append(x)   # m is a list to store (g-i) data
        n.append(y)   # n is a list to store (u-g) data
        m1.append(x1) # m1 is a list to store (g-z) data
        n1.append(y1) # n1 is a list to store (g-y) data
    np.savetxt("dwarf1_g-i.csv",m)
    np.savetxt("dwarf1_u-g.csv",n)  
    np.savetxt("dwarf1_g-z.csv",m1)
    np.savetxt("dwarf1_g-y.csv",n1)    
    

    xdata,ydata=g-i,u-g
    m=[]
    n=[]
    m1=[]
    n1=[]
    a,b=0.26,0.39   
    ind=np.where((xdata>a)&(xdata<b))
    xdata=xdata[ind]
    ydata=ydata[ind]
    xdata1=xdata1[ind]
    ydata1=ydata1[ind]
    c=-1*np.ones(len(xdata))  # c is [Fe/H]=-1 contour  
    need=a00+a01*c+a02*c**2+a03*c**3+a10*xdata+a11*xdata*c+a12*xdata*c**2\
             +a20*xdata**2+a21*xdata**2*c+a30*xdata**3 
    ind=np.where(ydata>=need)     # choose data that above [Fe/H]=-1 contour when 0.26<(g-i)<0.39
    xdata=xdata[ind]
    ydata=ydata[ind] 
    xdata1=xdata1[ind]
    ydata1=ydata1[ind]
    for i in np.arange(0,len(xdata)):
        x=xdata[i]
        y=ydata[i]
        x1=xdata1[i]
        y1=ydata1[i]
        m.append(x)   # m is a list to store (g-i) data
        n.append(y)   # n is a list to store (u-g) data
        m1.append(x1) # m1 is a list to store (g-z) data
        n1.append(y1) # n1 is a list to store (g-y) data
    np.savetxt("dwarf2_g-i.csv",m)
    np.savetxt("dwarf2_u-g.csv",n)  
    np.savetxt("dwarf2_g-z.csv",m1)
    np.savetxt("dwarf2_g-y.csv",n1)    

    csv_list=glob.glob('*g-i.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('g-i_use.csv','a',encoding='utf-8') as f:
            f.write(fr)         
    csv_list=glob.glob('*u-g.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('u-g_use.csv','a',encoding='utf-8') as f:
            f.write(fr)
    csv_list=glob.glob('*g-z.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('g-z_use.csv','a',encoding='utf-8') as f:
            f.write(fr)         
    csv_list=glob.glob('*g-y.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('g-y_use.csv','a',encoding='utf-8') as f:
            f.write(fr)
            
    #Second step: predict [Fe/H] with derived polynomial
    m=[]
    n=[]
    m1=[]
    n1=[]
    xdata=np.loadtxt("g-i_use.csv",delimiter=',') 
    ydata=np.loadtxt("u-g_use.csv",delimiter=',')
    xdata1=np.loadtxt("g-z_use.csv",delimiter=',') 
    ydata1=np.loadtxt("g-y_use.csv",delimiter=',')

    for i in np.arange(0,len(xdata)):
        x1=xdata[i]                        # x1 denotes (g-i) 
        y1=ydata[i]                        # y1 denotes (u-g) 
        x2=xdata1[i]                       # x2 denotes (g-z)
        y2=ydata1[i]                       # y2 denotes (g-y)
        if (x1>0.66):
            f1=np.linspace(-4,1,101)                # given [Fe/H]
            x10=x1+error*np.random.randn(101)       #g,i are both Gaussian variables
            y10=y1+error*np.random.randn(101)       #u,g are both Gaussian variables
            x20=x2+error*np.random.randn(101)       #g,z are both Gaussian variables
            y20=y2+error*np.random.randn(101)       #g,y are both Gaussian variables 
            need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
             +a20*x10**2+a21*x10**2*f1+a30*x10**3
            sigma=error/(2**0.5)
            likelihood=((2*np.pi)**0.5*sigma)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma**2))
            f=np.argmax(likelihood)
            m.append(f1[f])                         # m is a list to store [Fe/H]
            n.append(x10[f])                         # n is a list to store (g-i)
            m1.append(x20[f])                         # m1 is a list to store (g-z)
            n1.append(y20[f])                         # n1 is a list to store (g-y)
        elif (0.39<=x1<=0.66):
            f1=np.linspace(-1.5,1,51)                    
            x10=x1+error*np.random.randn(51)       
            y10=y1+error*np.random.randn(51) 
            x20=x2+error*np.random.randn(51)       
            y20=y2+error*np.random.randn(51)
            need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
                +a20*x10**2+a21*x10**2*f1+a30*x10**3 
            sigma=error/(2**0.5) 
            likelihood=((2*np.pi)**0.5*sigma)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma**2))
            f=np.argmax(likelihood)
            m.append(f1[f]) 
            n.append(x10[f])
            m1.append(x20[f])
            n1.append(y20[f])
        else:
            f1=np.linspace(-1,1,41)                    
            x10=x1+error*np.random.randn(41)       
            y10=y1+error*np.random.randn(41)  
            x20=x2+error*np.random.randn(51)       
            y20=y2+error*np.random.randn(51)
            need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
             +a20*x10**2+a21*x10**2*f1+a30*x10**3 
            sigma=error/(2**0.5) 
            likelihood=((2*np.pi)**0.5*sigma)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma**2))
            f=np.argmax(likelihood)
            m.append(f1[f])
            n.append(x10[f])
            m1.append(x20[f])
            n1.append(y20[f])
    np.savetxt("dwarf_feh_estimated.csv",m)
    np.savetxt("dwarf_g-i_final.csv",n)
    np.savetxt("dwarf_g-z_final.csv",m1)
    np.savetxt("dwarf_g-y_final.csv",n1)
    
    #Third step: output files containing [Fe/H] information and delete intermediate files
    e1=pd.read_csv('dwarf_feh_estimated.csv')
    e2=pd.read_csv("dwarf_g-i_final.csv")
    file=[e1,e2]
    data=pd.concat(file,axis=1)
    data.to_csv("dwarf_p.csv",index=0,sep=',')
    e3=pd.read_csv('dwarf_p.csv') 
    e4=pd.read_csv("dwarf_g-z_final.csv")
    file=[e3,e4]    
    data=pd.concat(file,axis=1)
    data.to_csv("dwarf_pa.csv",index=0,sep=',')
    e5=pd.read_csv('dwarf_pa.csv')     
    e6=pd.read_csv("dwarf_g-y_final.csv")    
    file=[e5,e6]    
    data=pd.concat(file,axis=1)
    data.to_csv("dwarf_parameter.csv",index=0,sep=',')

    os.remove("dwarf_u-g.csv")
    os.remove("dwarf_g-i.csv")
    os.remove("dwarf1_u-g.csv")
    os.remove("dwarf1_g-i.csv")
    os.remove("dwarf2_u-g.csv")
    os.remove("dwarf2_g-i.csv")
    os.remove("dwarf_g-z.csv")
    os.remove("dwarf_g-y.csv")
    os.remove("dwarf1_g-z.csv")
    os.remove("dwarf1_g-y.csv")
    os.remove("dwarf2_g-z.csv")
    os.remove("dwarf2_g-y.csv")
    os.remove("u-g_use.csv")
    os.remove("g-i_use.csv")
    os.remove("g-z_use.csv")
    os.remove("g-y_use.csv")
    os.remove("dwarf_feh_estimated.csv")
    os.remove("dwarf_g-i_final.csv")
    os.remove("dwarf_g-z_final.csv")
    os.remove("dwarf_g-y_final.csv")
    os.remove("dwarf_p.csv")
    os.remove("dwarf_pa.csv")


    
# estimate effective temperature    
    data=pd.read_csv('dwarf_parameter.csv')
    headerList = ['feh', 'g-i', 'g-z', 'g-y']
    data.to_csv("dwarf_parameter2.csv", header=headerList, index=False)
#only stars with [Fe/H]>= -1.5, teff can be estimated
    data=pd.read_csv('dwarf_parameter2.csv')    
    feh=data['feh']
    ind0=np.arange(len(feh))
    ind1=np.where((feh>=-1.5)&(feh<=0.5))

    drid=list(set(ind0)-set(ind1[0]))
    df1=data.drop(labels=drid,axis=0)
    df1.to_excel(r'dwarf_CSST_MidRes(4500-6600K)_choose.xlsx')    


    data=pd.read_excel(r"dwarf_CSST_MidRes(4500-6600K)_choose.xlsx")
    xdata2=data.loc[:,['g-i']].values
    ydata2=data.loc[:,['feh']].values
    xdata3=data.loc[:,['g-z']].values
    ydata3=data.loc[:,['g-y']].values
    #Determine teff
    m2,n2,m3,n3=[],[],[],[]
    for i in np.arange(0,len(xdata2)):
        x2=xdata2[i]                             # x2 denotes (g-i)                 
        y2=ydata2[i]                             # y2 denotes [Fe/H]
        x3=xdata3[i]                             # x3 denotes (g-z)
        y3=ydata3[i]                             # y3 denotes (g-y)
        need1= 7466.46019175+83.22449937*y2+79.34173462*y2**2-3558.88890004*x2\
        +136.99301103*x2*y2+974.032979*x2**2        
        m2.append(need1)
        n2.append(y2)
        need2=7155.10097251+27.94692845*y2+59.58256183*y2**2-2762.7842155*x3\
        +119.48064571*x3*y2+642.53483267*x3**2
        m3.append(need2)
        need3=7084.24203992+30.73469921*y2+51.62153297*y2**2-2578.76137869*y3\
        +92.96753749*y3*y2+574.94946637*y3**2 

        if (pd.isnull(y3)):
            if(pd.isnull(x3)):
                n3.append(need1)
            elif(pd.isnull(x2)):
                n3.append(need2)
            elif((x2 is not None)&(x3 is not None)):
                n3.append(need2)
        elif(y3 is not None):
            n3.append(need3)
    
    np.savetxt("teff_g-i.csv",m2)
    np.savetxt("1feh.csv",n2)
    np.savetxt("teff_g-z.csv",m3)
    np.savetxt("teff_g-y.csv",n3)    
    

#For stars with [Fe/H]<-1.5, teff can not be estimated
    data=pd.read_csv('dwarf_parameter2.csv')    
    feh=data['feh']
    ind0=np.arange(len(feh))
    ind1=np.where((feh>=-4)&(feh<-1.5))

    drid=list(set(ind0)-set(ind1[0]))
    df1=data.drop(labels=drid,axis=0)
    df1.to_excel(r'dwarf_CSST_MidRes(4500-6600K)_choose2.xlsx')   
    
    data=pd.read_excel(r"dwarf_CSST_MidRes(4500-6600K)_choose2.xlsx")
    ydata4=data.loc[:,['feh']].values
    m4,n4,m5,n5=[],[],[],[]
    for i in np.arange(0,len(ydata4)):               
        y4=ydata4[i]                             # y4 denotes [Fe/H]   
        m4.append(y4)   
    np.savetxt("2feh.csv",m4)

    
    os.remove("dwarf_CSST_MidRes(4500-6600K)_choose.xlsx")
    os.remove("dwarf_CSST_MidRes(4500-6600K)_choose2.xlsx")  
    os.remove("dwarf_parameter.csv")
    os.remove("dwarf_parameter2.csv")    

    csv_list=glob.glob('*feh.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('metallicity_use.csv','a',encoding='utf-8') as f:
            f.write(fr) 
    e1=pd.read_csv('metallicity_use.csv')
    e2=pd.read_csv("teff_g-y.csv")
    file=[e1,e2]
    data=pd.concat(file,axis=1)
    data.to_csv("parameter2.csv",index=0,sep=',')


    data=pd.read_csv('parameter2.csv')
    headerList = ['feh', 'teff']
    data.to_csv("parameter_dwarf.csv", header=headerList, index=False)   

    
    os.remove("1feh.csv")
    os.remove("2feh.csv") 
    os.remove("metallicity_use.csv")
    os.remove("teff_g-i.csv") 
    os.remove("teff_g-y.csv")             
    os.remove("teff_g-z.csv")     
    os.remove("parameter2.csv")







def giant(u,g,i,z,y,error):
    '''
    This function is used to estimate the metallicity and effective 
    temperature of the giant stars from the CSST broad-band filter systems.

    Args:      
        
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
           color error. An assumption that (u-g) and (g-i) are independent Gaussian variables
           is made.
           
    The output is one file named parameter_giant.csv, which stores the photometric metallicity and 
    the effective temperature of the giant stars.
    '''

    import numpy as np
    import pandas as pd
    import glob
    import os

    xdata=g-i
    ydata=u-g
    xdata1=g-z
    ydata1=g-y
    #First step: refuse data beyond the applicability range
    m=[]
    n=[]
    m1=[]
    n1=[]
    a,b=0.53,1.24   #a,b denote lower and upper limit of given (g-i), respectively
    ind=np.where((xdata>a)&(xdata<b))
    xdata=xdata[ind]
    ydata=ydata[ind]
    xdata1=xdata1[ind]
    ydata1=ydata1[ind]    
    c=-4*np.ones(len(xdata))  # c is [Fe/H]=-4 contour       
    a00= 2.09930709          # ten polynimial coefficients
    a01= 0.17332003 
    a02= 0.03528203
    a03= 0.00134865
    a10=-3.72264553
    a11= 0.21243626
    a12= 0.0267093
    a20= 5.29212155
    a21= 0.0251359
    a30=-1.69978467
    need=a00+a01*c+a02*c**2+a03*c**3+a10*xdata+a11*xdata*c+a12*xdata*c**2\
             +a20*xdata**2+a21*xdata**2*c+a30*xdata**3 
    ind=np.where(ydata>=need)     # choose data that above [Fe/H]=-4 contour
    xdata=xdata[ind]
    ydata=ydata[ind]
    xdata1=xdata1[ind]
    ydata1=ydata1[ind] 
    for i in np.arange(0,len(xdata)):
        x=xdata[i]
        y=ydata[i]
        x1=xdata1[i]
        y1=ydata1[i]
        m.append(x)   # m is a list to store (g-i) data
        n.append(y)   # n is a list to store (u-g) data
        m1.append(x1) # m1 is a list to store (g-z) data
        n1.append(y1) # n1 is a list to store (g-y) data
    np.savetxt("g-i_use.csv",m)
    np.savetxt("u-g_use.csv",n)  
    np.savetxt("g-z_use.csv",m1)
    np.savetxt("g-y_use.csv",n1)   
             
    #Second step: predict [Fe/H] with derived polynomial
    m=[]
    n=[]
    m1=[]
    n1=[]
    xdata=np.loadtxt("g-i_use.csv",delimiter=',') 
    ydata=np.loadtxt("u-g_use.csv",delimiter=',')
    xdata1=np.loadtxt("g-z_use.csv",delimiter=',') 
    ydata1=np.loadtxt("g-y_use.csv",delimiter=',')    
    
    for i in np.arange(0,len(xdata)-1):
        x1=xdata[i]                        # x1 denotes (g-i) 
        y1=ydata[i]                        # y1 denotes (u-g)
        x2=xdata1[i]                       # x2 denotes (g-z)
        y2=ydata1[i]                       # y2 deontes (g-y)        
        f1=np.linspace(-4,0.5,91)           # given [Fe/H]
        x10=x1+error*np.random.randn(91)       #g,i are both Gaussian variables
        y10=y1+error*np.random.randn(91)       #u,g are both Gaussian variables
        x20=x2+error*np.random.randn(91)       #g,z are both Gaussian variables
        y20=y2+error*np.random.randn(91)       #g,y are both Gaussian variables        
        need=a00+a01*f1+a02*f1**2+a03*f1**3+a10*x10+a11*x10*f1+a12*x10*f1**2\
             +a20*x10**2+a21*x10**2*f1+a30*x10**3    
        sigma=error/(2**0.5)             
        likelihood=((2*np.pi)**0.5*sigma)**(-1)*(np.e)**(-((y10-need)**2)/(2*sigma**2))
        f=np.argmax(likelihood)
        m.append(f1[f])                         # m is a list to store [Fe/H]
        n.append(x10[f])                         # n is a list to store (g-i)
        m1.append(x20[f])                         # m1 is a list to store (g-z)
        n1.append(y20[f])                         # n1 is a list to store (g-y)
    np.savetxt("giant_feh_estimated.csv",m)
    np.savetxt("giant_g-i_final.csv",n)
    np.savetxt("giant_g-z_final.csv",m1)
    np.savetxt("giant_g-y_final.csv",n1)
    
    
    #Third step: output files containing [Fe/H] information and delete intermediate files
    e1=pd.read_csv('giant_feh_estimated.csv')
    e2=pd.read_csv("giant_g-i_final.csv")
    file=[e1,e2]
    data=pd.concat(file,axis=1)
    data.to_csv("giant_p.csv",index=0,sep=',')
    e3=pd.read_csv('giant_p.csv') 
    e4=pd.read_csv("giant_g-z_final.csv")
    file=[e3,e4]    
    data=pd.concat(file,axis=1)
    data.to_csv("giant_pa.csv",index=0,sep=',')
    e5=pd.read_csv('giant_pa.csv')     
    e6=pd.read_csv("giant_g-y_final.csv")    
    file=[e5,e6]    
    data=pd.concat(file,axis=1)
    data.to_csv("giant_parameter.csv",index=0,sep=',')
        
    os.remove("u-g_use.csv")
    os.remove("g-i_use.csv")
    os.remove("g-z_use.csv")
    os.remove("g-y_use.csv")    
    os.remove("giant_feh_estimated.csv")
    os.remove("giant_g-i_final.csv")
    os.remove("giant_g-z_final.csv")
    os.remove("giant_g-y_final.csv")
    os.remove("giant_p.csv")
    os.remove("giant_pa.csv")



# estimate effective temperature    
    data=pd.read_csv('giant_parameter.csv')
    headerList = ['feh', 'g-i', 'g-z', 'g-y']
    data.to_csv("giant_parameter2.csv", header=headerList, index=False)
#only stars with [Fe/H]>= -1.5, teff can be estimated
    data=pd.read_csv('giant_parameter2.csv')    
    feh=data['feh']
    ind0=np.arange(len(feh))
    ind1=np.where((feh>=-1.5)&(feh<=0.5))

    drid=list(set(ind0)-set(ind1[0]))
    df1=data.drop(labels=drid,axis=0)
    df1.to_excel(r'giant_CSST_MidRes(4500-5800K)_choose.xlsx')    


    data=pd.read_excel(r"giant_CSST_MidRes(4500-5800K)_choose.xlsx")
    xdata2=data.loc[:,['g-i']].values
    ydata2=data.loc[:,['feh']].values
    xdata3=data.loc[:,['g-z']].values
    ydata3=data.loc[:,['g-y']].values
    #Determine teff
    m2,n2,m3,n3=[],[],[],[]
    for i in np.arange(0,len(xdata2)):
        x2=xdata2[i]                             # x2 denotes (g-i)                 
        y2=ydata2[i]                             # y2 denotes [Fe/H]
        x3=xdata3[i]                             # x3 denotes (g-z)
        y3=ydata3[i]                             # y3 denotes (g-y)
        need1= 7144.05864569+228.36499743*y2+100.95537008*y2**2-2809.36338573*x2\
        +45.97629437*x2*y2+547.81920701*x2**2        
        m2.append(need1)
        n2.append(y2)
        need2=6950.04480788+158.65446197*y2+81.49999583*y2**2-2324.4064961*x3\
        +46.76723044*x3*y2+418.44436227*x3**2
        m3.append(need2)
        need3=6930.97643956+151.15322892*y2+71.3479295*y2**2-2250.37121756*y3\
        +24.64501618*y3*y2+404.62705625*y3**2
  
        if (pd.isnull(y3)):
            if(pd.isnull(x3)):
                n3.append(need1)
            elif(pd.isnull(x2)):
                n3.append(need2)
            elif((x2 is not None)&(x3 is not None)):
                n3.append(need2)
        elif(y3 is not None):
            n3.append(need3)    
            
    np.savetxt("teff_g-i.csv",m2)
    np.savetxt("1feh.csv",n2)
    np.savetxt("teff_g-z.csv",m3)
    np.savetxt("teff_g-y.csv",n3)   
    

#For stars with [Fe/H]<-1.5, teff can not be estimated
    data=pd.read_csv('giant_parameter2.csv')    
    feh=data['feh']
    ind0=np.arange(len(feh))
    ind1=np.where((feh>=-4)&(feh<-1.5))

    drid=list(set(ind0)-set(ind1[0]))
    df1=data.drop(labels=drid,axis=0)
    df1.to_excel(r'giant_CSST_MidRes(4500-5800K)_choose2.xlsx')   
    
    data=pd.read_excel(r"giant_CSST_MidRes(4500-5800K)_choose2.xlsx")
    ydata4=data.loc[:,['feh']].values
    m4,n4,m5,n5=[],[],[],[]
    for i in np.arange(0,len(ydata4)):               
        y4=ydata4[i]                             # y4 denotes [Fe/H]   
        m4.append(y4) 
    np.savetxt("2feh.csv",m4)

    
    os.remove("giant_CSST_MidRes(4500-5800K)_choose.xlsx")
    os.remove("giant_CSST_MidRes(4500-5800K)_choose2.xlsx")  
    os.remove("giant_parameter.csv")
    os.remove("giant_parameter2.csv")    

    csv_list=glob.glob('*feh.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('metallicity_use.csv','a',encoding='utf-8') as f:
            f.write(fr) 
    e1=pd.read_csv('metallicity_use.csv')
    e2=pd.read_csv("teff_g-y.csv")
    file=[e1,e2]
    data=pd.concat(file,axis=1)
    data.to_csv("parameter2.csv",index=0,sep=',')

    data=pd.read_csv('parameter2.csv')
    headerList = ['feh', 'teff']
    data.to_csv("parameter_giant.csv", header=headerList, index=False) 
    
    os.remove("1feh.csv")
    os.remove("2feh.csv") 
    os.remove("metallicity_use.csv")
    os.remove("teff_g-i.csv") 
    os.remove("teff_g-y.csv")             
    os.remove("teff_g-z.csv")   
    os.remove("parameter2.csv")

    
    
    





def CSST_parameter(NUV,u,g,i,z,y,error):
    '''
    This program is designed specially to estimate the metallicity and effective 
    temperature of the stars from the CSST broad-band filter systems.

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
           color error. An assumption that (u-g) and (g-i) are independent Gaussian variables
           is made.
           
    The output is one file named CSST_parameter.csv, which stores the photometric metallicity and 
    the effective temperature of the stars.
    '''
    
    import numpy as np
    import pandas as pd
    import glob
    import os
    NUV,u,g,i,z,y1=NUV,u,g,i,z,y
    error=error
    xdata=g-i
    ydata=NUV-u
    m,n,m1,n1=[],[],[],[]
    m2,n2,m3,n3=[],[],[],[]
    m4,n4,m5,n5=[],[],[],[]
    m6,n6,m7,n7=[],[],[],[]
    m8,n8,m9,n9=[],[],[],[]
#select giant stars 
    for j in np.arange(0,len(xdata)):
        x=xdata[j]            # x denotes (g-i)
        y=ydata[j]            # y denotes (NUV-u)
        u2=u[j]
        g2=g[j]
        i2=i[j]
        z2=z[j]
        y2=y1[j]

        if (0.26<=x<=0.6):
            if (y<0.375*x+0.5212):
                m.append(u2)
                m1.append(g2)
                m2.append(i2)
                m3.append(z2)
                m4.append(y2)
            elif (y>=0.375*x+0.5212):
                n.append(u2)
                n1.append(g2)
                n2.append(i2)
                n3.append(z2)
                n4.append(y2)                
        elif (0.6<x<=1.15):
            if (y<0.462*x+0.469):
                m5.append(u2)
                m6.append(g2)
                m7.append(i2)
                m8.append(z2)
                m9.append(y2)
            elif (y>=0.462*x+0.469):
                n5.append(u2)
                n6.append(g2)
                n7.append(i2)
                n8.append(z2)
                n9.append(y2)

    np.savetxt("1dwarf_u.csv",m)
    np.savetxt("1dwarf_g.csv",m1)
    np.savetxt("1dwarf_i.csv",m2)
    np.savetxt("1dwarf_z.csv",m3)
    np.savetxt("1dwarf_y.csv",m4)    
    np.savetxt("2dwarf_u.csv",m5)
    np.savetxt("2dwarf_g.csv",m6)
    np.savetxt("2dwarf_i.csv",m7)
    np.savetxt("2dwarf_z.csv",m8)
    np.savetxt("2dwarf_y.csv",m9)     
    np.savetxt("1giant_u.csv",n)
    np.savetxt("1giant_g.csv",n1)
    np.savetxt("1giant_i.csv",n2)
    np.savetxt("1giant_z.csv",n3)
    np.savetxt("1giant_y.csv",n4)    
    np.savetxt("2giant_u.csv",n5)
    np.savetxt("2giant_g.csv",n6)
    np.savetxt("2giant_i.csv",n7)
    np.savetxt("2giant_z.csv",n8)
    np.savetxt("2giant_y.csv",n9)  


    csv_list=glob.glob('*dwarf_u.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('dwarf_u.csv','a',encoding='utf-8') as f:
            f.write(fr)   
            
    csv_list=glob.glob('*dwarf_g.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('dwarf_g.csv','a',encoding='utf-8') as f:
            f.write(fr)             
 
    csv_list=glob.glob('*dwarf_i.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('dwarf_i.csv','a',encoding='utf-8') as f:
            f.write(fr) 
            
    csv_list=glob.glob('*dwarf_z.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('dwarf_z.csv','a',encoding='utf-8') as f:
            f.write(fr)             

    csv_list=glob.glob('*dwarf_y.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('dwarf_y.csv','a',encoding='utf-8') as f:
            f.write(fr) 
            
            
            
    csv_list=glob.glob('*giant_u.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('giant_u.csv','a',encoding='utf-8') as f:
            f.write(fr)   
            
    csv_list=glob.glob('*giant_g.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('giant_g.csv','a',encoding='utf-8') as f:
            f.write(fr)             
 
    csv_list=glob.glob('*giant_i.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('giant_i.csv','a',encoding='utf-8') as f:
            f.write(fr) 
            
    csv_list=glob.glob('*giant_z.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('giant_z.csv','a',encoding='utf-8') as f:
            f.write(fr) 

    csv_list=glob.glob('*giant_y.csv')
    for i in csv_list:
        fr=open(i,'r',encoding='utf-8').read()
        with open('giant_y.csv','a',encoding='utf-8') as f:
            f.write(fr) 
            
            

    os.remove("1dwarf_u.csv")
    os.remove("1dwarf_g.csv") 
    os.remove("1dwarf_i.csv") 
    os.remove("1dwarf_z.csv")
    os.remove("1dwarf_y.csv") 
    os.remove("2dwarf_u.csv")
    os.remove("2dwarf_g.csv") 
    os.remove("2dwarf_i.csv")
    os.remove("2dwarf_z.csv")
    os.remove("2dwarf_y.csv") 
    os.remove("1giant_u.csv")
    os.remove("1giant_g.csv") 
    os.remove("1giant_i.csv") 
    os.remove("1giant_z.csv")
    os.remove("1giant_y.csv") 
    os.remove("2giant_u.csv")
    os.remove("2giant_g.csv") 
    os.remove("2giant_i.csv") 
    os.remove("2giant_z.csv")
    os.remove("2giant_y.csv") 
    
    u=np.loadtxt("dwarf_u.csv",delimiter=',') 
    g=np.loadtxt("dwarf_g.csv",delimiter=',')
    i=np.loadtxt("dwarf_i.csv",delimiter=',')
    z=np.loadtxt("dwarf_z.csv",delimiter=',') 
    y=np.loadtxt("dwarf_y.csv",delimiter=',') 
    dwarf(u,g,i,z,y,error)            
    u=np.loadtxt("giant_u.csv",delimiter=',') 
    g=np.loadtxt("giant_g.csv",delimiter=',')
    i=np.loadtxt("giant_i.csv",delimiter=',')
    z=np.loadtxt("giant_z.csv",delimiter=',') 
    y=np.loadtxt("giant_y.csv",delimiter=',') 
    giant(u,g,i,z,y,error)                

    os.remove("dwarf_u.csv")
    os.remove("dwarf_g.csv")
    os.remove("dwarf_i.csv")
    os.remove("dwarf_z.csv")
    os.remove("dwarf_y.csv") 
    os.remove("giant_u.csv")
    os.remove("giant_g.csv")
    os.remove("giant_i.csv")
    os.remove("giant_z.csv")
    os.remove("giant_y.csv")     
    
    e1=pd.read_csv('parameter_dwarf.csv')
    e2=pd.read_csv("parameter_giant.csv")
    file=[e1,e2]
    data=pd.concat(file,axis=0)
    data.to_csv("CSST_parameter.csv",index=0,sep=',')   
    
    os.remove("parameter_dwarf.csv")
    os.remove("parameter_giant.csv")