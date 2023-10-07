
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import gaussian_filter1d
from sklearn.linear_model import Lasso

#%%

def rate_histogram(spike_ts, bin_width, bins=None):
    r"""
    Function to calculate firing rates from spike times.
    
    Parameters
    ----------
    spike_ts : array-like
        Spike timestamps
    bin_width : float
        Width of bins in seconds
    bins : array-like 
        If None, bins rate histograms will go from t=0 to t=time last spike

    

    Returns
    ---------
    rate_hist : 1d-array
        Firing rate historrgam of neuron
    """

    if bins == None:
        last_spike = spike_ts[-1]
        bins = np.arange(0, last_spike, bin_width)
        

    elif np.ndim(bins) != 0:
        bins = bins

    else: 
        raise TypeError(f"Expected bins to be array-like type but got {type(bins)} instead")
    
    rate_hist = np.histogram(spike_ts, bins)

    return rate_hist


#Peri-event histogram analysis for neurons
def spiking_peh(spike_ts, ref_ts, min_max, bin_width):
    r"""
    Function to perform a peri-event histogram of spiking activity.
    
    Parameters
    ----------
    spike_ts : array-like
        Spike timestamps
    ref_ts : array-like
        Reference events that spiking will be aligned to
    min_max : tuple
        Time window in seconds around ref_ts to be analyzed in seconds. E.g. (-4,8)
    bin_width : float
        Bin width in seconds

    Returns
    ---------
    trials_hists : 2d-array
        Spiking activity around each timestamp in ref_ts
    """
    if not isinstance(spike_ts,np.ndarray):
        try:
            spike_ts = np.array(spike_ts)          
        except:
            raise TypeError(f"Expected spike_ts to be of type: array-like but got {type(spike_ts)} instead")
    
    if not isinstance(ref_ts,np.ndarray):
        try:
            ref_ts = np.array(ref_ts)     
        except:
            raise TypeError(f"Expected spike_ts to be of type: array-like but got {type(spike_ts)} instead")
    
    bins = np.linspace(min_max[0], min_max[1], int((min_max[1]-min_max[0])/bin_width))
    
    left_idx = np.searchsorted(spike_ts, ref_ts+min_max[0])
    right_idx = np.searchsorted(spike_ts, ref_ts+min_max[1])
    
    raw_trial_spikes = np.array([spike_ts[left_idx[i]:right_idx[i]] for i in range(left_idx.shape[0])], dtype=object)
    trial_spikes = np.subtract(raw_trial_spikes, ref_ts)
    trial_hists = np.vstack([np.histogram(trial,bins)[0] for trial in trial_spikes])
    
    return trial_hists

    
#%%

#Downsample function for photometry (or any other continuous variable) data
def downsample_1d(var_ts, var_vals,bin_width):
    r"""
    Downsamples 1d time series
    
    Parameters
    ----------
    var_ts : array-like
        Continuous variable timestamps
    var_vals : array-like
        Continuous variable values
    bin_width : float
        Bin width of new sampling rate (i.e. 1/new_sampling_rate)
    
    Returns
    ---------
    ds_ts : 1d np.array
        downsampled timestamps
    ds_vale : 1d np.array
        downsampled values
    """
    ds_ts = np.linspace(var_ts.min(), var_ts.max(), int((var_ts.max()-var_ts.min())/bin_width))
    ds_vals = np.interp(ds_ts, var_ts, var_vals)
    
    return ds_ts, ds_vals

#%%

#Peri-event histogram for continuous values.
def contvar_peh(var_ts, var_vals, ref_ts, min_max, bin_width = False):
    r"""
    Function to perform a peri-event histogram of spiking activity.
    
    Parameters
    ----------
    var_ts : array-like
        Continuous variable timestamps
    var_vals : array-like
        Continuous variable values
    ref_ts : array-like
        Reference events that spiking will be aligned to
    min_max : tuple
        Time window in seconds around ref_ts to be analyzed in seconds. E.g. (-4,8)
    bin_width : float
        Bin width of hsitogram in seconds

    Returns
    ---------
    all_trials : 2d-array
        Continuous variable values around each timestamp in ref_ts in bin_width wide bins
    """
    if bin_width:
        ds_ts = np.linspace(var_ts.min(), var_ts.max(), int((var_ts.max()-var_ts.min())/bin_width))
        ds_vals = np.interp(ds_ts, var_ts, var_vals)
        rate = bin_width
    
    else:
        rate = np.diff(var_ts).mean()
        ds_ts, ds_vals = (np.array(var_ts), np.array(var_vals))       
        
    left_idx = int(min_max[0]/rate)
    right_idx = int(min_max[1]/rate)
    
    all_idx = np.searchsorted(ds_ts,ref_ts, "right")   
    all_trials = np.vstack([ds_vals[idx+left_idx:idx+right_idx] for idx in all_idx])
    
    return all_trials

#%%

#Zscore every column of a dataframe
def zscore_peh(peh, trials="rows"):
    r"""
    Z-score peri-event histrogram by trial. 
    Specially written for output of invian.contvar_peh or invian.spiking_peh.
    
    Parameters
    ----------
    peh : 2d-array or pd.DataFrame
        Peri-event histogram data. 
    trials : str
        If "rows", each row is assumed to be a trial and each columns a time bin.
        If "columns", each column is assumed to be a trial an each row a time bin

    Returns
    ---------
    z_peh : 2d-array or pd.DataFrane
        Z-scored 
    """
    if isinstance(peh, np.ndarray):
        if trials == "rows":
            z_peh = (peh - peh.mean(axis=1)[:,np.newaxis]) / peh.std(axis=1)[:,np.newaxis]
        elif trials == "columns":
            z_peh = (peh - peh.mean(axis=0)) / peh.std(axis=0)
    
    elif isinstance(peh, pd.core.frame.DataFrame):
        if trials == "rows":
            z_peh = peh.subtract(peh.mean(axis=1),axis=0).divide(peh.mean(axis=1),axis=0)
        if trials == "columns":
            z_peh = peh.subtract(peh.mean(axis=0),axis=1).divide(peh.mean(axis=0),axis=1)
    else:
        raise TypeError(f"Expected np.ndarray or pd.core.frame.DataFrame but got {type(peh)} instead")
    
    return z_peh

#%%

#Z-scoring every column of a dataframe to a specific baseline
def zscore_peh_tobaseline(peh, min_max, baseline, trials="rows"):
    r"""
    Z-score peri-event histrogram by trial to a specific baseline window. 
    Specially written for output of invian.contvar_peh or invian.spiking_peh.
    
    Parameters
    ----------
    peh : 2d-array or pd.DataFrame
        Peri-event histogram data
    min_max : tuple
        Minimum and maximum time, in seconds, around reference events (should be the same as input of
        invian.contvar_peh or invian.spiking_peh).
    baseline: tuple
        Minimum and maximum baseline interval, in seconds. E.g. (-4,-2).
    trials : str
        If "rows", each row is assumed to be a trial and each columns a time bin.
        If "columns", each column is assumed to be a trial an each row a time bin

    Returns
    ---------
    z_peh : 2d-array or pd.DataFrane
        Z-scored 
    """
    xaxis = np.linspace(min_max[0], min_max[1], peh.shape[1])
    intervs = np.searchsorted(xaxis, list(baseline))
    start = intervs[0]
    end = intervs[1]
    
    if isinstance(peh, np.ndarray):
        if trials == "rows":
            baseline = peh[:,start:end]
            baseline_avg = baseline.mean(axis=1)
            baseline_avg = baseline_avg[:,np.newaxis]
            baseline_std = baseline.std(axis=1)
            baseline_std = baseline_std[:,np.newaxis]
            z_peh = np.divide(np.subtract(peh,baseline_avg), baseline_std)
        elif trials == "columns":
            print("not yet implemented")
            z_peh = np.nan

    elif isinstance(peh, pd.core.Frame.DataFrame):
        if trials == "rows":
            baseline = peh.iloc[:,start:end]
            baseline_avg = baseline.mean(axis=1)
            baseline_std = baseline.std(axis=1)
            z_peh = peh.subtract(baseline_avg,axis=0).divide(baseline_std,axis=0)

        elif trials == "columns":
            print('not yet implemented')
            z_peh = np.nan
    
    else:
        raise TypeError(f"Expected np.ndarray but got {type(peh)} instead")
    
    return z_peh

#%%

#Smooth every column of a dataframe using a gaussian filter
def smooth_units(data, sigma):
    for unit in data:
        data[unit] = gaussian_filter1d(data[unit],sigma)
        
    return data

#%%

#Subtracting a baseline from every column of a dataframe
def subtract_baseline(df, baseline = (0,40)):
    start = baseline[0]
    end = baseline[1]
    for column in df:
        baseline = df[column].iloc[start:end]
        baseline_avg = np.mean(baseline)
        df[column] = df[column] - baseline_avg
        
    return df

#%%

def remove_isosbestic(gcamp_signal, isosbestic_signal):
    regr = Lasso()
    regr.fit(isosbestic_signal.reshape(-1,1), gcamp_signal.reshape(-1,1))
    isos_pred = regr.predict(isosbestic_signal.reshape(-1,1))
    
    norm_gcamp_signal = gcamp_signal - isos_pred
    
    return norm_gcamp_signal



#%%

def plot_peh(all_trials, xrange, title = None):
    fig, ax = plt.subplots(2,1)
    sns.heatmap(all_trials, cbar = False, xticklabels = False, yticklabels = False, ax = ax[0])
    ax[1].plot(np.linspace(xrange[0], xrange[1], all_trials.shape[1]), all_trials.mean(axis = 0))
    ax[1].set_xlim(xrange[0], xrange[1])
    
    if title != None:
        ax[0].set_title(title)
    
    return fig, ax
    