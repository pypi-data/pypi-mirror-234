#! /usr/bin/env python

"""
Module for simplex or grid search of best fit spectrum in a template library.
"""

__author__ = 'V. Christiaens'
__all__ = ['best_fit_tmp',
           'get_chi']

from datetime import datetime
from multiprocessing import cpu_count
import numpy as np
import os
from scipy.optimize import minimize
from .config import time_ini, timing, time_fin, pool_map, iterable
from .chi import gof_scal
from .model_resampling import resample_model
from .utils_spec import extinction, find_nearest
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_chi(lbda_obs, spec_obs, err_obs, tmp_name, tmp_reader, 
            search_mode='simplex', lambda_scal=None, scale_range=(0.1,10,0.01), 
            ext_range=None, dlbda_obs=None, instru_corr=None, instru_res=None, 
            instru_idx=None, use_weights=True, filter_reader=None, 
            simplex_options=None, red_chi2=True, remove_nan=False, 
            force_continue=False, min_npts=1, verbose=False, **kwargs):
    """ Routine calculating chi^2, optimal scaling factor and optimal 
    extinction for a given template spectrum to match an observed spectrum.
    
    Parameters
    ----------
    lbda_obs : numpy 1d ndarray or list
        Wavelengths of observed spectrum. If several instruments were used, the 
        wavelengths should be ordered per instrument, not necessarily as 
        monotonically increasing wavelength. Hereafter, :math:`n_{ch}` is the 
        length of ``lbda_obs``.
    spec_obs : numpy 1d ndarray or list
        Observed spectrum for each value of ``lbda_obs``. Should have a length
        of :math:`n_{ch}`.
    err_obs : numpy 1d/2d ndarray or list
        Uncertainties on the observed spectrum. The array (list) can have either
        a length of :math:`n_{ch}`, or a shape of :math:`(2,n_{ch})` for lower 
        (first column) and upper (second column) uncertainties provided.
    tmp_name :  str
        Template spectrum filename.
    tmp_reader : python routine
        External routine that reads a model file and returns a 3D numpy array, 
        where the first column corresponds to wavelengths, the second 
        contains flux values, and the third the uncertainties on the flux.
    search_mode: str, opt {'simplex', 'grid'}
        How is the best fit template found? Simplex or grid search.
    lambda_scal: float, optional
        Wavelength where a first scaling will be performed between template
        and observed spectra. If not provided, the middle wavelength of the 
        osberved spectra will be considered.
    scale_range: tuple, opt
        If grid search, this parameter should be provided as a tuple of 3 
        floats: lower limit, upper limit and step of the grid search for the 
        scaling factor to be applied AFTER the first rough scaling (i.e.
        scale_range should always encompass 1).
    ext_range : tuple or None, opt
        - If None: differential extinction is not considered as a free parameter. 
        - If a tuple: it should contain 2 floats (for simplex \
        ``search_mode``) or 3 floats (for grid search ``search_mode``) \
        corresponding to the lower limit, upper limit (and step for the grid \
        search). For the simplex search, the lower and upper limits are used \
        to set a chi square of infinity outside of the range.
    dlbda_obs : numpy 1d ndarray or list, optional
        Respective spectral channel width or FWHM of the photometric filters 
        used for each point of the observed spectrum. This vector is used to 
        infer which part(s) of a combined spectro+photometric spectrum should 
        involve convolution+subsampling (model resolution higher than 
        measurements), interpolation (the opposite), or convolution by the 
        transmission curve of a photometric filter. If not provided, it will be 
        inferred from the difference between consecutive lbda_obs points (i.e. 
        inaccurate for a combined spectrum). It must be provided IF one wants to 
        weigh each measurement based on the spectral resolution of each 
        instrument (as in [OLO16]_), through the ``use_weights`` argument.
    instru_corr : numpy 2d ndarray, optional
        Spectral correlation between post-processed images in which the 
        spectrum is measured. It is specific to the instrument, PSF subtraction 
        algorithm and radial separation of the companion from the central star.
        Can be computed using ``special.spec_corr.spectral_correlation``. In 
        case of a spectrum obtained with different instruments, it is 
        recommended to construct the final spectral_correlation matrix with
        ``special.spec_corr.combine_corrs``. If ``instru_corr`` is not provided, 
        the uncertainties in each spectral channel will be considered 
        independent. See [GRE16]_ for more details.
    instru_res : float or list of floats/strings, optional
        The mean instrumental resolving power(s) OR filter names. This is 
        used to convolve the model spectrum. If several instruments are used, 
        provide a list of resolving power values / filter names, one for 
        each instrument used.
    instru_idx: numpy 1d array, optional
        1d array containing an index representing each instrument used 
        to obtain the spectrum, label them from 0 to the number of instruments 
        (:math:`n_{ins}`). Zero for points that don't correspond to any of the 
        ``instru_res`` values provided, and i in :math:`[1,n_{ins}]` for points
        associated to instru_res[i-1]. This parameter must be provided if the 
        spectrum consists of points obtained with different instruments.
    use_weights: bool, optional
        For the likelihood calculation, whether to weigh each point of the 
        spectrum based on the spectral resolution or bandwidth of photometric
        filters used. Weights will be proportional to ``dlbda_obs/lbda_obs`` if 
        ``dlbda_obs`` is provided, or set to 1 for all points otherwise.
    filter_reader: python routine, optional
        External routine that reads a filter file and returns a 2D numpy array, 
        where the first column corresponds to wavelengths, and the second 
        contains transmission values. Important: if not provided, but strings 
        are detected in instru_res, the default file reader will be used. 
        It assumes the following format for the files:
            
        - first row contains headers (titles of each column)
        - starting from 2nd row: 1st column: wavelength, 2nd col.: transmission
        - Unit of wavelength can be provided in parentheses of first header \
        key name: e.g. "WL(AA)" for angstrom, "wavelength(mu)" for micrometer \
        or "lambda(nm)" for nanometer. Note: only what is in parentheses \
        matters for the units.
     
    red_chi2: bool, optional
        Whether to compute the reduced chi square. If False, considers chi^2.
    remove_nan: bool, optional
        Whether to remove NaN values from template spectrum BEFORE resampling
        to the wavelength sampling of the observed spectrum. Whether it is set
        to True or False, a check is made just before chi^2 is calculated 
        (after resampling), and only non-NaN values will be considered.
    simplex_options: dict, optional
        The ``scipy.optimize.minimize`` simplex (Nelder-Mead) options.
    force_continue: bool, optional
        In case of issue with the fit, whether to continue regardless (this may
        be useful in an uneven spectral library, where some templates have too
        few points for the fit to be performed).
    verbose: str, optional
        Whether to print more information when fit fails. 
    min_npts: int or None, optional
        Iinimum number of (resampled) points to consider a template spectrum 
        valid in the minimization search. A Nan value will be returned for chi 
        if the condition is not met.
    **kwargs: optional
        Other optional arguments to the ``scipy.optimize.minimize`` function.
        
    Returns
    -------
    best_chi: float
        goodness of fit scored by the template
    best_scal:
        best-fit scaling factor for the considered template
    best_ext:
        best-fit optical extinction for the considered template

    Note
    ----
    If several filter filenames are provided in ``instru_res``, the filter files
    must all have the same format and wavelength units (for reading by the same
    ``filter_reader`` snippet or default function). 
        
    """
    # read template spectrum
    try:
        lbda_tmp, spec_tmp, spec_tmp_err = tmp_reader(tmp_name, 
                                                      verbose=verbose>1)
    except:
        msg = "{} could not be opened. Corrupt file?".format(tmp_name)
        if force_continue:
            if verbose:
                print(msg)
            return np.inf, 1, 0, 1
        else:
            raise ValueError(msg)
            
    # look for any nan and replace
    if remove_nan:
        if np.isnan(spec_tmp).any() or np.isnan(spec_tmp_err).any():
            bad_idx = np.where(np.isnan(spec_tmp))[0]
            #bad_idx2 = np.where(np.isnan(spec_tmp_err))[0]
            #all_bad = np.concatenate((bad_idx1,bad_idx2))
            nch = len(lbda_tmp)
            new_lbda = [lbda_tmp[i] for i in range(nch) if i not in bad_idx]
            new_spec = [spec_tmp[i] for i in range(nch) if i not in bad_idx]
            new_err = [spec_tmp_err[i] for i in range(nch) if i not in bad_idx]
            lbda_tmp = np.array(new_lbda)
            spec_tmp = np.array(new_spec)
            spec_tmp_err = np.array(new_err)
        
    # don't consider template spectra whose range is smaller than observed one
    if lbda_obs[0] < lbda_tmp[0] or lbda_obs[-1] > lbda_tmp[-1]:
        msg = "Wavelength range of template {} ({:.2f}, {:.2f})mu too short"
        msg+= " compared to that of observed spectrum ({:.2f}, {:.2f})mu"
        if force_continue:
            if verbose:
                print(msg.format(tmp_name, lbda_tmp[0],lbda_tmp[-1],
                                        lbda_obs[0],lbda_obs[-1]))
            return np.inf, 1, 0, len(lbda_tmp)-2
        else:
            raise ValueError(msg.format(tmp_name, lbda_tmp[0],lbda_tmp[-1],
                                        lbda_obs[0],lbda_obs[-1]))
    
    # try to resample tmp as observed spectrum - just used to raise error early
    try:
        _, spec_res = resample_model(lbda_obs, lbda_tmp, spec_tmp, 
                                     dlbda_obs=dlbda_obs, 
                                     instru_res=instru_res, 
                                     instru_idx=instru_idx,
                                     filter_reader=filter_reader)
    except:
        msg = "Issue with resampling of template {}. Does the wavelength "
        msg+= "range extend far enough ({:.2f}, {:.2f})mu?"
        if force_continue:
            if verbose:
                print(msg.format(tmp_name, lbda_tmp[0],lbda_tmp[-1]))
            return np.inf, 1, 0, len(lbda_tmp)-2
        else:
            raise ValueError(msg.format(tmp_name, lbda_tmp[0],lbda_tmp[-1]))
    
    # first rescaling fac
    if not lambda_scal:
        lambda_scal = (lbda_obs[0]+lbda_obs[-1])/2
    idx_cen = find_nearest(lbda_obs, lambda_scal)
    idx_tmp = find_nearest(lbda_tmp, lambda_scal)
    scal_fac = spec_obs[idx_cen]/spec_tmp[idx_tmp]
    spec_tmp*=scal_fac
    #spec_tmp_err*=scal_fac
    
    # EDIT: Don't combine observed and template uncertainties;
    # the best fit would be the most noisy tmp of the library!)
    #err_obs = np.sqrt(np.power(spec_tmp_err,2)+np.power(err_obs,2))
    
    
    # only consider non-zero and non-nan values for chi^2 calculation
    all_conds = np.where(np.isfinite(spec_res))[0]
    # cond2 = np.where(np.isfinite(err_obs))[0] 
    # cond3 = np.where(spec_tmp>0)[0]
    # all_conds = np.sort(np.unique(np.concatenate((cond1,cond2,cond3))))
    ngood_ch = len(all_conds)
    #good_ch = (all_conds,)
    # lbda_obs = lbda_obs[good_ch]
    # spec_obs = spec_obs[good_ch]
    # err_obs = err_obs[good_ch]
    #lbda_tmp = lbda_tmp[good_ch]
    #spec_tmp = spec_tmp[good_ch]
    
    n_dof = ngood_ch-1-(ext_range is not None)
    if n_dof <= 0:
        msg = "Not enough dof with remaining points of template spectrum {}"
        if force_continue:
            if verbose:
                print(msg.format(tmp_name))
            return np.inf, 1, 0, n_dof
        else:
            raise ValueError(msg.format(tmp_name))
    
    best_chi = np.inf
    best_scal = np.nan
    best_ext = np.nan
    if ngood_ch < min_npts:
        msg = "Unsufficient number of good points ({} < {}). Tmp discarded."
        if verbose:
            print(msg.format(ngood_ch,min_npts))
        return best_chi, best_scal, best_ext, n_dof
    
    # simplex search
    if search_mode == 'simplex':
        if simplex_options is None:
            simplex_options = {'xatol': 1e-6, 'fatol': 1e-6, 'maxiter': 1000,
                               'maxfev': 5000}
        if not ext_range:
            p = (1,)
        else:
            AV_ini = (ext_range[0]+ext_range[1])/2
            p = (1,AV_ini)
        
        try:
            res = minimize(gof_scal, p, args=(lbda_obs, spec_obs, err_obs, 
                                              lbda_tmp, spec_tmp, dlbda_obs, 
                                              instru_corr, instru_res, 
                                              instru_idx, use_weights, 
                                              filter_reader, ext_range),
                           method='Nelder-Mead', options=simplex_options, 
                           **kwargs)
        except:
            msg = "Issue with simplex minimization for template {}. "
            msg+= "Try grid search?"
            if force_continue:
                if verbose:
                    print(msg.format(tmp_name))
                return np.inf, 1, 0, n_dof
            else:
                raise ValueError(msg.format(tmp_name))
        best_chi = res.fun
        if not ext_range:
            best_scal = res.x
            best_ext = 0
        else:
            best_scal, best_ext = res.x
        if np.isfinite(best_scal):
            best_scal*=scal_fac
        
    # or grid search        
    elif search_mode == 'grid':
        test_scale = np.arange(scale_range[0], scale_range[1], scale_range[2])
        n_test = len(test_scale)
        if ext_range is None:
            test_ext = np.array([0])
            n_ext = 1
        elif isinstance(ext_range, tuple) and len(ext_range)==3:
            test_ext = np.arange(ext_range[0], ext_range[1], ext_range[2])
            n_ext = len(test_ext)
        else:
            raise TypeError("ext_range can only be None or tuple of length 3")

        chi = np.zeros([n_test,n_ext])
        
        for cc, scal in enumerate(test_scale):
            for ee, AV in enumerate(test_ext):
                p = (scal,AV)
                chi[cc,ee] = gof_scal(p, lbda_obs, spec_obs, err_obs, lbda_tmp, 
                                      spec_tmp, dlbda_obs=dlbda_obs, 
                                      instru_corr=instru_corr, 
                                      instru_res=instru_res, 
                                      instru_idx=instru_idx, 
                                      use_weights=use_weights,
                                      filter_reader=filter_reader,
                                      ext_range=ext_range)
        try:
            best_chi = np.nanmin(chi)
            best_idx = np.nanargmin(chi)
            best_idx = np.unravel_index(best_idx,chi.shape)
            best_scal = test_scale[best_idx[0]]*scal_fac
            best_ext = test_ext[best_idx[1]]
        except:
            if force_continue:
                return best_chi, best_scal, best_ext, n_dof
            else:
                msg = "Issue with grid search minimization for template {}. "
                print(msg.format(tmp_name))
                import pdb
                pdb.set_trace()
    
    else:
        msg = "Search mode not recognised. Should be 'simplex' or 'grid'."
        raise TypeError(msg)
    
    if red_chi2:
        best_chi /= n_dof
        
    
    return best_chi, best_scal, best_ext, n_dof



def best_fit_tmp(lbda_obs, spec_obs, err_obs, tmp_reader, search_mode='simplex',
                 n_best=1, lambda_scal=None, scale_range=(0.1,10,0.01), 
                 ext_range=None, simplex_options=None, dlbda_obs=None, 
                 instru_corr=None, instru_res=None, instru_idx=None, 
                 filter_reader=None, lib_dir='tmp_lib/', tmp_endswith='.fits', 
                 red_chi2=True, remove_nan=False, nproc=1, verbosity=0, 
                 force_continue=False, min_npts=1, **kwargs):
    """ Finds the best fit template spectrum to a given observed spectrum, 
    within a spectral library.  By default, a single free parameter is 
    considered: the scaling factor of the spectrum. A first automatic scaling 
    is performed by comparing the flux of the observed and template spectra at 
    lambda_scal. Then a more refined scaling is performed, either through 
    simplex or grid search (within scale_range).
    If fit_extinction is set to True, the exctinction is also considered as a 
    free parameter.
    
    Parameters
    ----------
    lbda_obs : numpy 1d ndarray or list
        Wavelengths of observed spectrum. If several instruments were used, the 
        wavelengths should be ordered per instrument, not necessarily as 
        monotonically increasing wavelength. Hereafter, :math:`n_{ch}` is the 
        length of ``lbda_obs``.
    spec_obs : numpy 1d ndarray or list
        Observed spectrum for each value of ``lbda_obs``. Should have a length
        of :math:`n_{ch}`.
    err_obs : numpy 1d/2d ndarray or list
        Uncertainties on the observed spectrum. The array (list) can have either
        a length of :math:`n_{ch}`, or a shape of :math:`(2,n_{ch})` for lower 
        (first column) and upper (second column) uncertainties provided.
    tmp_reader : python routine
        External routine that reads a model file and returns a 3D numpy array, 
        where the first column corresponds to wavelengths, the second 
        contains flux values, and the third the uncertainties on the flux.
    search_mode: str, optional, {'simplex','grid'}
        How is the best fit template found? Simplex or grid search.
    n_best: int, optional
        Number of best templates to be returned (default: 1)
    lambda_scal: float, optional
        Wavelength where a first scaling will be performed between template
        and observed spectra. If not provided, the middle wavelength of the 
        osberved spectra will be considered.
    scale_range: tuple, opt
        If grid search, this parameter should be provided as a tuple of 3 
        floats: lower limit, upper limit and step of the grid search for the 
        scaling factor to be applied AFTER the first rough scaling (i.e.
        scale_range should always encompass 1).
    ext_range : tuple or None, opt
        - If None: differential extinction is not considered as a free parameter. 
        - If a tuple: it should contain 2 floats (for simplex \
        ``search_mode``) or 3 floats (for grid search ``search_mode``) \
        corresponding to the lower limit, upper limit (and step for the grid \
        search). For the simplex search, the lower and upper limits are used \
        to set a chi square of infinity outside of the range.
    dlbda_obs : numpy 1d ndarray or list, optional
        Respective spectral channel width or FWHM of the photometric filters 
        used for each point of the observed spectrum. This vector is used to 
        infer which part(s) of a combined spectro+photometric spectrum should 
        involve convolution+subsampling (model resolution higher than 
        measurements), interpolation (the opposite), or convolution by the 
        transmission curve of a photometric filter. If not provided, it will be 
        inferred from the difference between consecutive lbda_obs points (i.e. 
        inaccurate for a combined spectrum). It must be provided IF one wants to 
        weigh each measurement based on the spectral resolution of each 
        instrument (as in [OLO16]_), through the ``use_weights`` argument.
    instru_corr : numpy 2d ndarray, optional
        Spectral correlation between post-processed images in which the 
        spectrum is measured. It is specific to the instrument, PSF subtraction 
        algorithm and radial separation of the companion from the central star.
        Can be computed using ``special.spec_corr.spectral_correlation``. In 
        case of a spectrum obtained with different instruments, it is 
        recommended to construct the final spectral_correlation matrix with
        ``special.spec_corr.combine_corrs``. If ``instru_corr`` is not provided, 
        the uncertainties in each spectral channel will be considered 
        independent. See [GRE16]_ for more details.
    instru_res : float or list of floats/strings, optional
        The mean instrumental resolving power(s) OR filter names. This is 
        used to convolve the model spectrum. If several instruments are used, 
        provide a list of resolving power values / filter names, one for 
        each instrument used.
    instru_idx: numpy 1d array, optional
        1d array containing an index representing each instrument used 
        to obtain the spectrum, label them from 0 to the number of instruments 
        (:math:`n_{ins}`). Zero for points that don't correspond to any of the 
        ``instru_res`` values provided, and i in :math:`[1,n_{ins}]` for points
        associated to instru_res[i-1]. This parameter must be provided if the 
        spectrum consists of points obtained with different instruments.
    filter_reader: python routine, optional
        External routine that reads a filter file and returns a 2D numpy array, 
        where the first column corresponds to wavelengths, and the second 
        contains transmission values. Important: if not provided, but strings 
        are detected in instru_res, the default file reader will be used. 
        It assumes the following format for the files:
            
        - first row contains headers (titles of each column)
        - starting from 2nd row: 1st column: wavelength, 2nd col.: transmission
        - Unit of wavelength can be provided in parentheses of first header \
        key name: e.g. "WL(AA)" for angstrom, "wavelength(mu)" for micrometer \
        or "lambda(nm)" for nanometer. Note: only what is in parentheses \
        matters for the units.
     
    simplex_options: dict, optional
        The scipy.optimize.minimize simplex (Nelder-Mead) options.
    red_chi2: bool, optional
        Whether to compute the reduced chi square. If False, considers chi^2.
    remove_nan: bool, optional
        Whether to remove NaN values from template spectrum BEFORE resampling
        to the wavelength sampling of the observed spectrum. Whether it is set
        to True or False, a check is made just before chi^2 is calculated 
        (after resampling), and only non-NaN values will be considered.
    nproc: None or int, optional
        The number of processes to use for parallelization. If set to None, 
        will automatically use half of the available CPUs on the machine.
    verbosity: 0, 1 or 2, optional
        Verbosity level. 0 for no output and 2 for full information.
    force_continue: bool, optional
        In case of issue with the fit, whether to continue regardless (this may
        be useful in an uneven spectral library, where some templates have too
        few points for the fit to be performed).
    min_npts: int or None, optional
        Minimum number of (resampled) points to consider a 
        template spectrum valid in the minimization search.
    **kwargs: optional
        Optional arguments to the scipy.optimize.minimize function
         
    Returns
    -------
    final_tmpname: tuple of n_best str
        Best-fit template filenames
    final_tmp: tuple of n_best 3D numpy array
        Best-fit template spectra (3D: lbda+spec+spec_err)
    final_chi: 1D numpy array of length n_best
        Best-fit template chi^2
    final_params: 2D numpy array (2xn_best)
        Best-fit parameters (optimal scaling and optical extinction). Note if 
        extinction is not fitted, optimal AV will be set to 0.
        
    """
    # create list of template filenames
    tmp_filelist = [x for x in os.listdir(lib_dir) if x.endswith(tmp_endswith)]
    n_tmp = len(tmp_filelist)
    
    if verbosity > 0:
        start_time = time_ini()
        int_time = start_time
        print("{:.0f} template spectra will be tested.".format(n_tmp))
    
    chi = np.ones(n_tmp)
    scal = np.ones_like(chi)
    ext = np.zeros_like(chi)
    n_dof =  np.ones_like(chi)
    
    if nproc is None:
        nproc = cpu_count()//2
        if verbosity:
            print("{:.0f} CPUs will be used".format(nproc))

    if verbosity:
        print("****************************************\n")
    
    if nproc == 1:
        for tt in range(n_tmp):
            if verbosity>1 and search_mode=='simplex':
                print('Nelder-Mead minimization is running...')
            res = get_chi(lbda_obs, spec_obs, err_obs, tmp_filelist[tt], 
                          tmp_reader, search_mode=search_mode, 
                          scale_range=scale_range, ext_range=ext_range,
                          lambda_scal=lambda_scal, dlbda_obs=dlbda_obs, 
                          instru_corr=instru_corr, instru_res=instru_res, 
                          instru_idx=instru_idx, filter_reader=filter_reader,
                          simplex_options=simplex_options, red_chi2=red_chi2,
                          remove_nan=remove_nan, force_continue=force_continue,
                          verbose=verbosity, min_npts=min_npts, **kwargs)
            chi[tt], scal[tt], ext[tt], n_dof[tt] = res
            
            shortname = tmp_filelist[tt][:-len(tmp_endswith)]
            if not np.isfinite(chi[tt]):
                if verbosity>0:
                    msg_err = "{:.0f}/{:.0f} ({}) FAILED"
                    if np.isnan(chi[tt]):
                        msg_err += " (simplex did not converge)"
                    print(msg_err.format(tt+1, n_tmp, tmp_filelist[tt]))
            else:
                if verbosity > 0 and tt==0:
                    msg = "{:.0f}/{:.0f}: {}, chi_r^2 = {:.1f}, ndof={:.0f}"
                    if verbosity>1:
                        msg+=", done in {}s."
                        indiv_time = time_fin(start_time)
                        print(msg.format(tt+1, n_tmp, shortname, chi[tt], 
                                         n_dof[tt], indiv_time))
                    else:
                        print(msg.format(tt+1, n_tmp, shortname, chi[tt], n_dof[tt]))
                    now = datetime.now()
                    delta_t = now.timestamp()-start_time.timestamp()
                    tot_time = np.ceil(n_tmp*delta_t/60)
                    msg = "Based on the first fit, it may take ~{:.0f}min to"
                    msg += " test the whole library \n"
                    print(msg.format(tot_time))
                    int_time = time_ini(verbose=False)
                elif verbosity > 0:
                    msg = "{:.0f}/{:.0f}: {}, chi_r^2 = {:.1f}, ndof={:.0f}"
                    if verbosity>1:
                        msg+=" done in {}s."                    
                        indiv_time = time_fin(int_time)
                        int_time = time_ini(verbose=False)
                        print(msg.format(tt+1, n_tmp, shortname, chi[tt], 
                                         n_dof[tt], indiv_time))
                    else:
                        print(msg.format(tt+1, n_tmp, shortname, chi[tt],
                                         n_dof[tt]))
                        

    else:
        res = pool_map(nproc, get_chi, lbda_obs, spec_obs, err_obs, 
                       iterable(tmp_filelist), tmp_reader, search_mode, 
                       lambda_scal, scale_range, ext_range, dlbda_obs, 
                       instru_corr, instru_res, instru_idx, filter_reader,
                       simplex_options, red_chi2, remove_nan, force_continue,
                       verbosity, min_npts)

        res = np.array(res, dtype=object)
        chi = res[:,0]
        scal = res[:,1]
        ext = res[:,2]
        n_dof = res[:,3]
        
    n_success = np.sum(np.isfinite(chi))
        
    if verbosity > 0:
        print("****************************************\n")
        msg = "{:.0f}/{:.0f} template spectra were fitted. \n"
        print(msg.format(n_success, n_tmp))
        timing(start_time)
        
    return best_n_tmp(chi, scal, ext, n_dof, tmp_filelist, tmp_reader, 
                      n_best=n_best, verbose=verbosity)
    
    
def best_n_tmp(chi, scal, ext, n_dof, tmp_filelist, tmp_reader, n_best=1, 
               verbose=False):
    """
    Routine returning the n best template spectra.

    Returns
    -------
    final_tmpname: tuple of n_best str
        Best-fit template filenames
    final_tmp: tuple of n_best 3D numpy array
        Best-fit template spectra (3D: lbda+spec+spec_err)
    final_chi: 1D numpy array of length n_best
        Best-fit template chi^2
    final_params: 2D numpy array (2xn_best)
        Best-fit parameters (optimal scaling and optical extinction). Note if 
        extinction is not fitted, optimal AV will be set to 0.
        
    """
    # sort from best to worst match
    order = np.argsort(chi)
    sort_chi = chi[order]
    sort_scal = scal[order]
    sort_ext = ext[order]
    sort_ndof = n_dof[order]
    sort_filelist = [tmp_filelist[i] for i in order]
    
    if verbose:
        print("best chi: ", sort_chi[:n_best])
        print("best scale fac: ", sort_scal[:n_best])
        print("n_dof: ", sort_ndof[:n_best])
    # take the n_best first ones
    best_tmp = []
    for n in range(n_best):
        lbda_tmp, spec_tmp, spec_tmp_err = tmp_reader(sort_filelist[n])
        Albdas = extinction(lbda_tmp,abs(sort_ext[n]))
        extinc_fac = np.power(10.,-Albdas/2.5)
        if sort_ext[n]>0:
            final_scal = sort_scal[n]*extinc_fac
        elif sort_ext[n]<0:
            final_scal = sort_scal[n]/extinc_fac
        else:
            final_scal = sort_scal[n]
        best_tmp.append(np.array([lbda_tmp, spec_tmp*final_scal, 
                                  spec_tmp_err*final_scal]))
        if verbose:
            msg = "The best template #{:.0f} is: {} "
            msg+="(Delta A_V={:.1f}mag)\n"
            print(msg.format(n+1, sort_filelist[n], sort_ext[n]))
            
    best_tmpname = tuple(sort_filelist[:n_best])
    best_tmp = tuple(best_tmp)
    best_params = np.array([sort_scal[:n_best],sort_ext[:n_best]])
    
    return (best_tmpname, best_tmp, sort_chi[:n_best], best_params, 
            sort_ndof[:n_best])