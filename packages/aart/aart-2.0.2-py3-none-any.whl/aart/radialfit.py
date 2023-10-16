import numpy as np
import h5py
from scipy.signal import find_peaks
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from aart import *
import linecache
import sys

## defining constants for unit conversions (makes sin functinon dimensionless when fitting to V_fit)

dM=5.214795112e23  # Distance to M87 in meters
psi=1.07473555940836 # Mass of M87 1 /psi= 6.2e9 Kg
Gc=6.67e-11 # G constant [m^3 kg^-1 s^-2]
cc= 2.99792458e8 # c constant [m/s]
Msc=1.988435e30 # Solar Mass [Kg]
MMkg= 6.2e9*psi*Msc # [Kg]
MM87=MMkg *Gc/cc**2 # Mass of M87 in meters, i.e., (psi*6.2*10^9) psi ("Best fit") Solar Masses 
sizeim=MM87 # Size of M in meters
muas_to_rad = np.pi/648000 *1e-6 #1 microarcsec in radians
unitfact=1/(muas_to_rad*1e9)
M_to_muas=np.arctan(sizeim/(dM))/muas_to_rad

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    

## gets calculated visibility amplitudes stored in directory 'path'
def get_visamps(mask1, mask2, **params):
    spin_case=params.get('spins')[mask1]
    i_case=params.get('i_angles')[mask2]
    
    radonangles=params.get('radonangles')
    path=params.get('path')
    radonfile=params.get('radonfile')
    dx0=params.get('dx0')
    dx1=params.get('dx1')
    dx2=params.get('dx2')
    Ncut=params.get('Ncut')    
    gfactor=params.get('gfactor')
    fudge=params.get('fudge')[mask1]
    fudge=params.get('fudge')[mask1]
    bvapp=params.get('bvapp')
    betaphi=params.get('betaphi')[mask1]
    betar=params.get('betar')[mask1]
    gfactor=params.get('gfactor')
    gammap=params.get('gammap')[mask1]
    sigmap=params.get('sigmap')[mask1]
    path=params.get('path')
    mup=params.get('mup')[mask1]
    sub_kep=params.get('sub_kep')[mask1]
    fudge=params.get('fudge')[mask1]
    
    visamps = []

    for i in range(len(radonangles)):
        radonangle=radonangles[i]
        fnvisamps=path+"Visamp_%s_a_%s_i_%s_dx0_%s_dx1_%s_dx2_%s_sk_%s_bphi_%s_br_%s_bvapp_%s_gfact_%s_gp_%s_sp_%s_fudge_%s_Ncut_%s.h5"%(radonangle,spin_case,i_case, dx0, dx1, dx2, sub_kep, betaphi, betar,  bvapp, gfactor, gammap, sigmap, fudge, int(Ncut))

        h5f = h5py.File(fnvisamps,'r')
        
        '''
        if Ncut==0:
            freqs=h5f['freqs'][:]
        '''    
        visamps.append(h5f['visamp'][:])
        
        h5f.close()
        
#     return np.array(visamps), np.array(norms)  
    return np.array(visamps)

## gets frequencies used in visbility amplitude file stored in directory 'path'
def get_freqs(mask1, mask2, **params):
    
    spin_case=params.get('spins')[mask1]
    i_case=params.get('i_angles')[mask2]
    radonangles=params.get('radonangles')
    path=params.get('path')
    radonfile=params.get('radonfile')
    dx0=params.get('dx0')
    dx1=params.get('dx1')
    dx2=params.get('dx2')
    Ncut=params.get('Ncut')    
    gfactor=params.get('gfactor')
    fudge=params.get('fudge')[mask1]
    bvapp=params.get('bvapp')
    betaphi=params.get('betaphi')[mask1]
    betar=params.get('betar')[mask1]
    gfactor=params.get('gfactor')
    gammap=params.get('gammap')[mask1]
    sigmap=params.get('sigmap')[mask1]
    path=params.get('path')
    mup=params.get('mup')[mask1]
    sub_kep=params.get('sub_kep')[mask1]
    fudge=params.get('fudge')[mask1]
    fnvisamps=path+"Visamp_%s_a_%s_i_%s_dx0_%s_dx1_%s_dx2_%s_sk_%s_bphi_%s_br_%s_bvapp_%s_gfact_%s_gp_%s_sp_%s_fudge_%s_Ncut_%s.h5"%(radonangles[0],spin_case,i_case, dx0, dx1, dx2, sub_kep, betaphi, betar,  bvapp, gfactor, gammap, sigmap, fudge, int(Ncut))

    h5f = h5py.File(fnvisamps,'r')
    
    freqs=h5f['freqs'][:]

    h5f.close()
        
    return freqs

## returns points (x, y) corresponding to maxima in y, with a y value greater than minval
def filter_maxima(x, y, minval):
    x_new = []
    y_new = []
    for k in range(1, len(x)-1):
            if (y[k+1]-y[k]<0) and (y[k]-y[k-1]>0):
                if y[k]>minval:
                    x_new.append(x[k])
                    y_new.append(y[k])
    return x_new, y_new

## finds argument of element in 'array' with value closest to 'value'
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

## given arrays of arrays x and y, returns a set of curves beginning at each element in x[0], where the next point in the ith curve is that in x[1] closest to x[0][i], and so on
def generate_curves(x, y):
    x_curves = []   ## x-values for the curves
    y_curves = []   ## y-values for the curves
        
    Lx = len(x)
    
    for j in range(0,len(x[0])):
        x_curve=[x[0][j]]
        y_curve=[y[0][j]]
        
        x_new=x_curve
        for i in range(1,Lx):
            closest=find_nearest(x[i], x_new)
            x_curve.append(x[i][closest])
            y_curve.append(y[i][closest])
            x_new=x[i][closest]
            
        x_curves.append(x_curve)
        y_curves.append(y_curve)
    return x_curves, y_curves

def circlipse(x, r0, r1, r2, phi0):
        return 2*r0 + 2*np.sqrt((r1**2)*(np.sin(x-phi0)**2)+(r2**2)*(np.cos(x-phi0)**2))
    
## takes in a clean 1d signal x, and outputs a corresponding signal with gaussian noise profile (mean=mu, std=s)
def gaussian_noise(x, mu, s):
    noise = np.random.normal(mu,s,len(x))
    #return x + noise
    return np.abs(x + noise)

## define a function to add noise to each snapshot of the visibility spectrum and average into one profile
def average_snapshots(visamps, mu_n, s_n, norms):
    """
    :param norms: nested array containing 36 norms for each snapshot in the ns=0.0 visamp file corresponding to "visamps"
    """
    noisy_visamps=[]
    normmax=np.max([np.max(norms[i]) for i in range(len(norms))])
    for i in range(len(visamps)):
        ## normalize so that the zero astro noise profile at snaphshot i starts at 1 for all baseline angles
        visampss=visamps[i]/normmax

        ## add noise to each visibility profile across the 36 baseline angles
        visampss=np.array([rf.gaussian_noise(vis, mu_n, s_n) for vis in visampss])
        noisy_visamps.append(visampss)

    ## now average the snapshots that now have both instrumental and astrophysical noise
    visamps_n=np.zeros(noisy_visamps[0].shape) 
    for i in range(len(noisy_visamps)):
        visamps_n+=noisy_visamps[i]/len(noisy_visamps)
    return visamps_n, normmax

## given a visibility profile across specified baseline angles (=radonangles), stores its radial profile in directory 'path'
def radialfit(visamps, freq, radonangles, mu_n, s_n, ulim1_fit, ulim2_fit, gfit_min, path, p0_ratio, norms=[]):
    """
    :param visamps: 2d array of visibility amplitdues values for different radonangles
    :param freq: array of baseline frequencies over which each visibility amplitude is recorded. 
    :param radonangles: iterable object containing the projection angles for the radon transformation
    :param mu_n: mean of the gaussian noise added to visamps
    :param s_n: standard deviation of the gaussian noise added to visamps
    :param ulim1_fit: beginning of the baseline window for fits
    :param ulim2_fit: end of the baseline window for fits
    :param gfit_min: minimum goodness of fit for projected diameter in fits
    :param path: path for saving the output
    :param p0_ratio: parameter in (0,1) used in intial guess p0=[aL_max*p0_ratio, aR_max*p0_ratio, 40] for curve_fit 
    """
    
    if len(norms)!=0:
        normax=np.max(norms)
        visamps=visamps/normax

    mask=np.where((freq>=ulim1_fit) & (freq<=ulim2_fit))[0]
    freqfit=freq[mask]
    datas=[]
    power=np.array([])
    upower=(ulim2_fit+ulim1_fit)/2
    datas=np.array([gaussian_noise(visamps[i], mu_n, s_n) for i in range (len(radonangles))])
    d_vals=[]
    g_vals=[]
    
    try:
        for i in range(len(radonangles)):
            data=datas[i][mask]

            ## in presence of noise, aL and aR are fixed parameters
            def visamp_func(u, aL, aR, dphi):
                return np.sqrt(aL**2+aR**2+2*aL*aR*np.sin(2*np.pi*dphi*u/unitfact))/np.sqrt(u*1e9)

            ## goodness of fit
            def g_fit(aL, aR, d, x, y):
                deviation= np.sum((visamp_func(x, aL, aR, d)-np.abs(y))**2)
                avg_v_fit = np.sum(visamp_func(x, aL, aR, d))
                return np.exp(-np.sqrt(deviation/len(x))/(avg_v_fit/len(x)))

            ## approximate bounds for aL and aR
            visamp=data
            vmax=np.max(visamp)
            umax=freqfit[np.argmax(visamp)]
            vmin=np.min(visamp)
            umin=freqfit[np.argmin(visamp)]

            aL_max=(1/2)*(vmax*np.sqrt(1e9*umax)+vmin*np.sqrt(1e9*umin))
            aR_max=(1/2)*(vmax*np.sqrt(1e9*umax)-vmin*np.sqrt(1e9*umin))


            ## find best fit params
            bounds = ([0,0,35], [aL_max, aL_max, 45]) 
            p0 = [aL_max*p0_ratio, aR_max*p0_ratio, 40]
            params, pcov_v = curve_fit(visamp_func, freqfit, data,p0=p0, bounds=bounds, maxfev=2000)  

            aL0 = params[0]
            aR0 = params[1]
            dphi0 = params[2]

            drange = np.arange(8*M_to_muas, 12*M_to_muas, 1/100)

            ## corresponding goodness of fit for each d \in drange
            gvals = [g_fit(aL0, aR0, d, freqfit, data) for d in drange]

            ## keep values of d with g(d) above gfit_min
            d_maxima, g_maxima = filter_maxima(drange, gvals, gfit_min)
            
            d_vals.append(np.array(d_maxima))
            g_vals.append(np.array(g_maxima))

        d_vals=np.array(d_vals)
        g_vals=np.array(g_vals)
        
        # construct circlipses  
        circlipses, g_circlipses = generate_curves(d_vals, g_vals) ## generate various circlipses
        g_circlipses = [np.prod(g) for g in g_circlipses]  ## joint goodness of fit for each circlipse

        best_circlipse = circlipses[np.array(g_circlipses).argmax()]


        params, pcov_v = curve_fit(circlipse, np.array(radonangles)*np.pi/180, best_circlipse,bounds=([0,0,0,-np.pi/2],[50,50,50,np.pi/2]),maxfev=2000)
        

        RMSD_a=np.sqrt(np.average((best_circlipse-circlipse(np.array(radonangles)*np.pi/180,*params))**2))/np.average(circlipse(np.array(radonangles)*np.pi/180,*params))

        RMSD_b=np.sqrt(np.average((best_circlipse-circlipse(np.array(radonangles)*np.pi/180,*params))**2))/np.ptp(circlipse(np.array(radonangles)*np.pi/180,*params))

        
        R_0 = params[0]
        R_1 = params[1]
        R_2 = params[2]
        phi0 = params[3]
        
        # see if fit is good
        ## check 1: enforce d_para > d_perp
        if np.abs(phi0)<70*np.pi/180:
            if best_circlipse[0]>best_circlipse[18]:
                print("failed requirement d_para > d_perp")
                raise ValueError('Fit not possible')
        else:
            if best_circlipse[0]<best_circlipse[18]: 
                print("failed requirement d_para > d_perp")
                raise ValueError('Fit not possible')
                
        ## check 2: preclude jumping between circlipses- max gap between consecutive points is 0.02M
        if np.max(np.abs(np.diff(best_circlipse)))>0.1*M_to_muas: 
            print("failed due to jumping between circlipses")
            raise ValueError('Fit not possible')
        

        d_1=2*(R_0+R_2)/M_to_muas
        d_2=2*(R_0+R_1)/M_to_muas
        d_perp=min(d_1, d_2)  ## d_perp <= d_para
        d_para=max(d_1, d_2)
        # fractional asymmetry
        f_a = 1-d_perp/d_para

        observables=[d_perp, d_para, f_a]


    except Exception as error:
        print("Fit not possible. The following exception occurred:")
        PrintException()
        best_circlipse=[np.nan]
        circlipses=[np.nan]
        g_circlipses=[np.nan]
        d_vals=[np.nan]
        g_vals=[np.nan]
        RMSD_a=np.nan
        RMSD_b=np.nan
        params=[np.nan, np.nan, np.nan, np.nan]
        observables=[np.nan, np.nan, np.nan]
        

    param_dict={
        "mu":best_circlipse,
        "circlipses":circlipses,
        "g_circlipses":g_circlipses,
        "d_vals":d_vals,
        "g_vals":g_vals,
        "rmsda":RMSD_a,
        "rmsdb":RMSD_b,
        "fit":params,
        "observables":observables,
        "power":power
    }
    
        # Create a directory for the results
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    np.savez(path+"Fit_%s_%s_gfit_%s_mun_%s_sn_%s.npz"%(ulim1_fit,ulim2_fit, gfit_min, mu_n, s_n),**param_dict)