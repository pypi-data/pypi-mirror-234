from typing import Union, Optional, List, Dict, Tuple, Sequence

import math
import numpy as np

from .numerics import array_issubset, safe_div
from quickstats import DescriptiveEnum

class BinErrorOption(DescriptiveEnum):
    AUTO    = (0, "Determine bin error method from data weights")
    SUMW2   = (1, "Errors with Wald approximation: sqrt(sum of weight^2)")
    POISSON = (2, "Errors from Poisson interval at 68.3% (1 sigma)")
    
class HistComparisonMode(DescriptiveEnum):
    RATIO      = (0, "Ratio of data (target / reference)")
    DIFFERENCE = (1, "Difference of data (target - reference)")

def calculate_nll(obs:float, exp:float):
    import ROOT
    return np.log(ROOT.TMath.Poisson(obs, exp))

def calculate_chi2(data_obs, data_exp, error_obs=None, threshold:float=3, epsilon:float=1e-6):
    if np.any(data_obs < 0):
        raise RuntimeError("data observed has negative-value element(s)")
    if np.any(data_exp < 0):
        raise RuntimeError("data expected has negative-value element(s)")        
    if error_obs is None:
        error_obs = np.sqrt(data_obs)
    data_obs = np.array(data_obs, dtype=np.float64)
    data_exp = np.array(data_exp, dtype=np.float64)
    error_obs = np.array(error_obs, dtype=np.float64)
    if data_obs.shape != data_exp.shape:
        raise RuntimeError("data observed and data expected have different shapes")
    if data_obs.shape != error_obs.shape:
        raise RuntimeError("data observed and error observed have different shapes")
    if data_obs.ndim != 1:
        raise RuntimeError("only one dimensional data is supported")
    chi2, chi2_last, obs_aggregate, exp_aggregate, error2_aggregate = 0., 0., 0., 0., 0.
    nbin_chi2 = 0
    bin_last = 1
    n_bins = len(data_obs)
    for i in range(n_bins):
        obs_aggregate += data_obs[i]
        exp_aggregate += data_exp[i]
        error2_aggregate += error_obs[i] ** 2
        if (obs_aggregate / np.sqrt(error2_aggregate) < threshold) or \
           (abs(obs_aggregate) < epsilon):
            if i != (n_bins - 1):
                continue
            else:
                chi2 -= chi2_last
                obs_aggregate = np.sum(data_obs[bin_last:])
                exp_aggregate = np.sum(data_exp[bin_last:])
                error2_aggregate = np.sum(error_obs[bin_last:] ** 2)
                chi2 += ((obs_aggregate - exp_aggregate) / np.sqrt(error2_aggregate)) ** 2
                if nbin_chi2 == 0:
                    nbin_chi2 += 1
        else:
            chi2_last = ((obs_aggregate - exp_aggregate) / np.sqrt(error2_aggregate)) ** 2
            bin_last = i
            chi2 += chi2_last
            nbin_chi2 += 1
            obs_aggregate, exp_aggregate, error2_aggregate = 0., 0., 0.
    # calculate likelihood
    nll, nll_last, nll_sat, nll_sat_last = 0., 0., 0., 0.
    obs_aggregate, exp_aggregate = 0., 0.
    nbin_nll = 0
    bin_last = 0
    for i in range(n_bins):
        obs_aggregate += data_obs[i]
        exp_aggregate += data_exp[i]
        error2_aggregate += error_obs[i] ** 2
        if (obs_aggregate < 2):
            if i != (n_bins - 1):
                continue
            else:
                nll -= nll_last
                nll_sat -= nll_sat_last
                obs_aggregate = np.sum(data_obs[bin_last:])
                exp_aggregate = np.sum(data_exp[bin_last:])
                nll += -1 * self.calculate_nll(obs_aggregate, exp_aggregate)
                # saturated
                nll_sat += -1 * self.calculate_nll(obs_aggregate, obs_aggregate)
                if nbin_nll == 0:
                    nbin_nll += 1
        else:
            nll_last = -1 * self.calculate_nll(obs_aggregate, exp_aggregate)
            nll_sat_last = -1 * self.calculate_nll(obs_aggregate, obs_aggregate)
            nll += nll_last
            nll_sat += nll_sat_last
            bin_last = i
            nbin_nll += 1
            obs_aggregate, exp_aggregate = 0., 0.
    result = {
        'chi2': chi2,
        'nbin_chi2': nbin_chi2,
        'nll': nll,
        'nll_sat': nll_sat,
        'nbin_nll': nbin_nll
    }
    return result

def get_poisson_interval(data:np.ndarray, n_sigma:float=1):
    """
        Calculate the Poisson error interval for binned data.
        
        Arguments:
            data: np.ndarray
                Array containing the event number in each bin.
            n_simg: float
                Number of sigma to use for the Poisson interval.
    """
    from quickstats.interface.root import TH1
    result = TH1.GetPoissonError(data, n_sigma)
    return result

def get_counting_significance(s:float, b:float, sigma_b:float=0, leading_order:bool=False):
    """
        Asimov approximation for the median significance in a counting experiment.
        
        Arguments:
        -------------------------------------------------------------------------------
            s: float
                Expected number of signal events.
            b: float
                Expected number of background events.
            sigma_b: float, default = 0
                Background uncertainty. A zero value means the number of
                background events is exactly known.
            leading_order: bool, default=False
                Whether to use leading order approximation.
    """
    if sigma_b == 0:
        if leading_order:
            return s / np.sqrt(b)
        n = s + b
        return np.sqrt(2 * ((n * np.log(n / b)) - s))
    else:
        sigma_b2 = sigma_b * sigma_b
        if leading_order:
            return s / np.sqrt(b + sigma_b2)
        n = s + b
        b_plus_sigma2 = b + sigma_b2
        first_term = n * np.log((n * b_plus_sigma2)/(b * b + n * sigma_b2))
        second_term = b * b / sigma_b2 * np.log(1 + (sigma_b2 * s) / (b * b_plus_sigma2))
        return np.sqrt(2 * (first_term - second_term))
    
def get_combined_counting_significance(s:np.ndarray, b:np.ndarray,
                                       sigma_b:Union[np.ndarray, float]=0,
                                       leading_order:bool=False):
    """
        Combined significance in multiple independent counting experiments.
        
        Arguments:
        ----------------------------------------------------------------------------
            s: np.ndarray of float
                Array of expected number of signal events in each experiment.
            b: np.ndarray of float
                Array of expected number of background events in each experiment.
            sigma_b: float / np.ndarray of float, default = 0
                Array of background uncertainties in each experiment. A zero value
                means the number of background events is exactly known.
            leading_order: bool, default=False
                Whether to use leading order approximation.
    """
    if sigma_b == 0:
        if leading_order:
            Z2 = s * s / b
        else:
            n = s + b
            Z2 = 2 * ((n * np.log(n / b)) - s)
    else:
        sigma_b2 = sigma_b * sigma_b
        if leading_order:
            Z2 = s * s / (b + sigma_b2)
        else:
            n = s + b
            b_plus_sigma2 = b + sigma_b2
            first_term = n * np.log((n * b_plus_sigma2)/(b * b + n * sigma_b2))
            second_term = b * b / sigma_b2 * np.log(1 + (sigma_b2 * s) / (b * b_plus_sigma2))
            Z2 = 2 * (first_term - second_term)
    if Z2.ndim > 1:
        Z_combined = np.sqrt(np.sum(Z2, axis=Z2.ndim - 1))
    else:
        Z_combined = np.sqrt(np.sum(Z2))
    return Z_combined

def bin_edge_to_bin_center(bin_edge:np.ndarray):
    return 0.5 * (bin_edge[1:] + bin_edge[:-1])

def bin_center_to_bin_edge(bin_center:np.ndarray):
    bin_widths = np.round(np.diff(bin_center), 8)
    if len(np.unique(bin_widths)) != 1:
        raise ValueError("can not deduce bin edges from bin centers of irregular bin widths")
    bin_width = bin_widths[0]
    bin_edges = np.concatenate([bin_center - bin_width / 2, [bin_center[-1] + bin_width/2]])
    return bin_edges

def bin_edge_to_bin_width(bin_edge:np.ndarray):
    return np.diff(bin_edge)

def min_max_to_range(min_val:Optional[float]=None, max_val:Optional[float]=None):
    if (min_val is None) and (max_val is None):
        return None
    if (min_val is not None) and (max_val is not None):
        return (min_val, max_val)
    raise ValueError("min and max values must be all None or all float")
    
def get_clipped_data(x:np.ndarray,
                     bin_range:Optional[Sequence]=None,
                     clip_lower:bool=True,
                     clip_upper:bool=True):
    if (bin_range is None) or ((clip_lower == False) and (clip_upper == False)):
        return np.array(x)
    xmin = bin_range[0] if clip_lower else None
    xmax = bin_range[1] if clip_upper else None
    return np.clip(x, xmin, xmax)

def histogram(x:np.ndarray, weights:Optional[np.ndarray]=None,
              bins:Union[int, Sequence]=10,
              bin_range:Optional[Sequence]=None,
              underflow:bool=False,
              overflow:bool=False,
              divide_bin_width:bool=False,
              normalize:bool=True,
              clip_weight:bool=False,
              evaluate_error:bool=False,
              error_option:Union[BinErrorOption, str]="auto"):
    """
        Compute the histogram of a data array.
        
        Arguments:
        -------------------------------------------------------------------------------
        x: ndarray
            Input data array from which the histogram is computed.
        weights: (optional) ndarray
            Array of weights with same shape as input data. If not given, the
            input data is assumed to have unit weights.
        bins: (optional) int or sequence of scalars, default = 10
            If integer, it defines the number of equal-width bins in the
            given range.
            If sequence, it defines a monotonically increasing array of bin edges,
            including the rightmost edge.
       bin_range: (optional) sequence of the form (float, float)
           The lower and upper range of the bins.  If not provided, range is simply 
           ``(x.min(), x.max())``.  Values outside the range are ignored.
       underflow: bool, default = False
           Include undeflow data in the first bin.
       overflow: bool, default = False
           Include overflow data in the last bin.
       divide_bin_width: bool, default = False
           Divide each bin by the bin width.           
       normalize: bool, default = True
           Normalize the sum of weights to one. Weights outside the bin range will
           not be counted if ``clip_weight`` is set to false, so the sum of bin
           content could be less than one.
       clip_weight: bool, default = False
           Ignore data outside given range when evaluating total weight
           used in normalization.
       evaluate_error: bool, default = True
           Evaluate the error of the bin contents using the given error option.
       error_option: BinErrorOption or str, default = "auto"
           How to evaluate bin errors. If "sumw2", symmetric errors from the Wald
           approximation is used (square root of sum of squares of weights). If
           "poisson", asymmetric errors from Poisson interval at one sigma is
           used. If "auto", it will use sumw2 error if data has unit weights,
           else Poisson error will be used.
           
       Returns
       -------------------------------------------------------------------------------
       bin_content: np.ndarray
           The bin content of the histogram.
       bin_edges: np.ndarray
           The bin edges of the histogram.
       bin_errors: np.ndarray
           The bin errors of the histogram.
    """
    x = get_clipped_data(x, bin_range=bin_range, clip_lower=underflow,
                         clip_upper=overflow)
    
    if weights is None:
        weights = np.ones(x.shape)
    else:
        # fix overflow bugs
        weights = np.array(weights, dtype=float)
        
    if normalize:
        if clip_weight and (bin_range is not None):
            first_edge, last_edge = bin_range
            norm_factor = weights[(x >= first_edge) & (x <= last_edge)].sum()
        else:
            norm_factor = weights.sum()
    else:
        norm_factor = 1
        
    bin_content, bin_edges = np.histogram(x, bins=bins, range=bin_range, weights=weights)
    
    if divide_bin_width:
        bin_width = bin_edge_to_bin_width(bin_edges)
        bin_content /= bin_width
    
    if evaluate_error:
        error_option = BinErrorOption.parse(error_option)
        if error_option == BinErrorOption.AUTO:
            unit_weight = np.allclose(weights, np.ones(weights.shape))
            error_option = BinErrorOption.POISSON if unit_weight else BinErrorOption.SUMW2
        if error_option == BinErrorOption.POISSON:
            pois_interval = get_poisson_interval(bin_content)
            bin_errors =  (pois_interval["lo"], pois_interval["hi"])
        elif error_option == BinErrorOption.SUMW2:
            bin_content_weight2, _ = np.histogram(x, bins=bins, range=bin_range, weights=weights**2)
            bin_errors = np.sqrt(bin_content_weight2)
        if norm_factor != 1:
            if isinstance(bin_errors, tuple):
                bin_errors = (bin_errors[0] / norm_factor, bin_errors[1] / norm_factor)
            else:
                bin_errors /= norm_factor
    else:
        bin_errors = None
        
    if norm_factor != 1:
        bin_content /= norm_factor
    
    return bin_content, bin_edges, bin_errors
        
def get_hist_data(x:np.ndarray, weights:Optional[np.ndarray]=None,
                  bins:Union[int, Sequence]=10,
                  bin_range:Optional[Sequence]=None,
                  underflow:bool=False,
                  overflow:bool=False,
                  divide_bin_width:bool=False,
                  normalize:bool=True,
                  clip_weight:bool=False,
                  xerr:bool=True,
                  yerr:bool=True,
                  error_option:Union[BinErrorOption, str]="auto"):
    """
        Extract histogram data from a data array.
        
        Arguments:
        -------------------------------------------------------------------------------
        x: ndarray
            Input data array from which the histogram is computed.
        weights: (optional) ndarray
            Array of weights with same shape as input data. If not given, the
            input data is assumed to have unit weights.
        bins: (optional) int or sequence of scalars, default = 10
            If integer, it defines the number of equal-width bins in the
            given range.
            If sequence, it defines a monotonically increasing array of bin edges,
            including the rightmost edge.
        bin_range: (optional) sequence of the form (float, float)
            The lower and upper range of the bins.  If not provided, range is simply 
            ``(x.min(), x.max())``.  Values outside the range are ignored.
        underflow: bool, default = False
            Include undeflow data in the first bin.
        overflow: bool, default = False
            Include overflow data in the last bin.
        divide_bin_width: bool, default = False
            Divide each bin by the bin width.
        normalize: bool, default = True
            Normalize the sum of weights to one. Weights outside the bin range will
            not be counted if ``clip_weight`` is set to false, so the sum of bin
            content could be less than one.
        clip_weight: bool, default = False
            If True, ignore data outside given range when evaluating total weight
            used in normalization.
        xerr: bool, default = True
            If True, evaluate the error of the bin centers (= bin widths / 2).
        yerr: bool, default = True
            If True, evaluate the error of the bin contents using the given error
            option.
        error_option: BinErrorOption or str, default = "auto"
            How to evaluate bin errors. If "sumw2", symmetric errors from the Wald
            approximation is used (square root of sum of squares of weights). If
            "poisson", asymmetric errors from Poisson interval at one sigma is
            used. If "auto", it will use sumw2 error if data has unit weights,
            else Poisson error will be used.
            
        Returns
        -------------------------------------------------------------------------------
        hist_data: dict
            A dictionary with the keys "x", "y", "xerr", "yerr" with the bin centers,
            bin content, half bin widths and bin errors as values.
    """
    y, bin_edges, yerr = histogram(x, weights=weights,
                                   bins=bins, bin_range=bin_range,
                                   underflow=underflow,
                                   overflow=overflow,
                                   normalize=normalize,
                                   divide_bin_width=divide_bin_width,
                                   clip_weight=clip_weight,
                                   evaluate_error=yerr,
                                   error_option=error_option)
    x = bin_edge_to_bin_center(bin_edges)
    if xerr:
        # todo do not hard-code number of digits to keep
        xerr = np.round(np.diff(bin_edges) / 2, 5)
    else:
        xerr = None
    hist_data = {
        "x": x,
        "y": y,
        "xerr": xerr,
        "yerr": yerr
    }
    return hist_data

def get_stacked_hist_data(x:List[np.ndarray],
                          weights:List[Optional[np.ndarray]]=None,
                          bins:Union[int, Sequence]=10,
                          bin_range:Optional[Sequence]=None,
                          underflow:bool=False,
                          overflow:bool=False,
                          divide_bin_width:bool=False,
                          normalize:bool=True,
                          clip_weight:bool=False,
                          xerr:bool=True,
                          yerr:bool=True,
                          merge:bool=True,
                          error_option:Union[BinErrorOption, str]="auto"):
    merged_x = np.concatenate(x)
    if bin_range is None:
        bin_range = (np.min(merged_x), np.max(merged_x))
    if merge:
        if weights is not None:
            merged_weights = np.concatenate(weights)
            assert merged_x.shape == merged_weights.shape
        else:
            merged_weights = None
        hist_data = get_hist_data(x=merged_x, weights=merged_weights,
                                  bins=bins, bin_range=bin_range,
                                  underflow=underflow,
                                  overflow=overflow,
                                  divide_bin_width=divide_bin_width,
                                  normalize=normalize,
                                  clip_weight=clip_weight,
                                  xerr=xerr, yerr=yerr,
                                  error_option=error_option)
        return hist_data
    else:
        stacked_hist_data = {
            "x": [],
            "y": [],
            "xerr": [],
            "yerr": []
        }
        if weights is None:
            weights = len(x) * None
        for x_i, weights_i in zip(x, weights):
            hist_data = get_hist_data(x=x_i, weights=weights_i,
                                      bins=bins, bin_range=bin_range,
                                      underflow=underflow,
                                      overflow=overflow,
                                      divide_bin_width=False,
                                      normalize=False,
                                      clip_weight=clip_weight,
                                      xerr=xerr, yerr=yerr,
                                      error_option=error_option)
            stacked_hist_data['x'].append(hist_data['x'])
            stacked_hist_data['y'].append(hist_data['y'])
            stacked_hist_data['xerr'].append(hist_data['xerr'])
            stacked_hist_data['yerr'].append(hist_data['yerr'])
        if normalize:
            norm_factor = np.sum(stacked_hist_data['y'])
            stacked_hist_data['y'] = [y / norm_factor for y in stacked_hist_data['y']]
        if divide_bin_width:
            bin_edges = np.histogram_bin_edges([bin_range[0], bin_range[1]],
                                               bins=bins, range=bin_range)
            bin_widths = bin_edge_to_bin_width(bin_edges)
            stacked_hist_data['y'] = [y / bin_widths for y in stacked_hist_data['y']]
        return stacked_hist_data

def get_sumw2(weights:np.ndarray):
    return np.sqrt(np.sum(weights ** 2))

def get_hist_mean(x:np.ndarray, y:np.ndarray):
    return np.sum(x * y) / np.sum(y)

def get_hist_std(x:np.ndarray, y:np.ndarray):
    mean = get_hist_mean(x, y)
    count = np.sum(y)
    if count == 0.:
        return 0.
    # for negative stddev (e.g. when having negative weights) - return std=0
    std2 = np.max([np.sum(y * (x - mean)**2) / count, 0.])
    return np.sqrt(std2)


def get_hist_effective_entries(y:np.ndarray, yerr:np.ndarray):
    # neff = \frac{(\sum Weights )^2}{(\sum Weight^2 )}
    sumw2 = np.sum(yerr ** 2)
    if sumw2 != 0.:
        return (np.sum(y) ** 2) / sumw2
    else:
        return 0
    
def get_hist_mean_error(x:np.ndarray, y:np.ndarray, yerr:np.ndarray):
    # mean error = StdDev / sqrt( Neff )
    neff = get_hist_effective_entries(y, yerr)
    if neff > 0.:
        std = get_hist_std(x, y)
        return std / np.sqrt(neff)
    else:
        return 0.
    
def get_cumul_hist(y:np.ndarray, yerr:np.ndarray):
    y_cum = np.cumsum(y)
    yerr_cum = np.sqrt(np.cumsum(yerr ** 2))
    return y_cum, yerr_cum

def get_bin_centers_from_range(xlow:float, xhigh:float, nbins:int, bin_precision:int=8):
    bin_width = (xhigh - xlow) / nbins
    low_bin_center  = xlow + bin_width / 2
    high_bin_center = xhigh - bin_width /2
    bins = np.around(np.linspace(low_bin_center, high_bin_center, nbins), bin_precision)
    return bins

def pvalue_to_significance(pvalue:float):
    import ROOT
    significance = ROOT.RooStats.PValueToSignificance(pvalue)
    return significance

def dataset_is_binned(x:np.ndarray, y:np.ndarray, xlow:float, xhigh:float, nbins:int,
                      ghost_threshold:float=1e-8, bin_precision:int=8):
    bin_centers = get_bin_centers_from_range(xlow, xhigh, nbins, bin_precision=bin_precision)
    x = np.around(x, bin_precision)
    same_nbins = len(x) == len(bin_centers)
    if same_nbins and np.allclose(bin_centers, x):
        return True
    elif np.all(y == 1.):
        return False
    else:
        y_no_ghost = y[y > ghost_threshold]
        unit_weight_no_ghost = np.all(y_no_ghost) == 1.
        scaled_weight_no_ghost = len(np.unique(y_no_ghost)) == 1
        if unit_weight_no_ghost or scaled_weight_no_ghost:
            return False
        elif same_nbins:
            return True
        elif array_issubset(bin_centers, x):
            return True
    raise RuntimeError('found dataset with invalid binning')
    
def fill_missing_bins(x:np.ndarray, y:np.ndarray, xlow:float, xhigh:float, nbins:int,
                      value:float=0, bin_precision:int=8):
    bin_centers = get_bin_centers_from_range(xlow, xhigh, nbins, bin_precision=bin_precision)
    x_rounded = np.around(x, bin_precision)
    missing_bins = np.setdiff1d(bin_centers, x_rounded)
    if value == 0:
        missing_values = np.zeros(missing_bins.shape)
    else:
        missing_values = np.full(missing_bins.shape, value)
    x = np.concatenate([x, missing_bins])
    y = np.concatenate([y, missing_values])
    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]
    return x, y

def rebin_dataset(x:np.ndarray, y:np.ndarray, nbins:int):
    bin_edges = bin_center_to_bin_edge(x)
    from quickstats.interface.root import TH1
    pyh = TH1.from_numpy_histogram(y, bin_edges=bin_edges)
    pyh.rebin(nbins)
    x = pyh.bin_center
    y = pyh.bin_content
    return x, y

def get_hist_comparison_data(reference_data, target_data,
                             mode:Union[HistComparisonMode, str]="ratio"):
    mode = HistComparisonMode.parse(mode)
    if not np.allclose(target_data['x'], reference_data['x']):
        raise RuntimeError("cannot compare two distributions with different binnings")
    comparison_data = {}
    comparison_data['x'] = reference_data['x']
    source_data = {}
    all_zero = {}
    # fill zero error if not given
    for key, data in [('reference', reference_data), 
                 ('target', target_data)]:
        source_data[key] = {}
        all_zero[key] = {}
        for errtype in ['xerr', 'yerr']:
            if (errtype not in data) or (data[errtype] is None):
                source_data[key][errtype] = np.zeros(comparison_data['x'].shape)
                all_zero[key][errtype] = True
            else:
                source_data[key][errtype] = data[errtype]
                all_zero[key][errtype] = not np.any(data[errtype])
    # fix the case where symmetric and asymmetric errors are mixed
    for errtype in ['xerr', 'yerr']:
        has_tuple_err = any(isinstance(source_data[key][errtype], tuple) for key in source_data)
        if not has_tuple_err:
            continue
        for key in source_data:
            err_data = source_data[key][errtype]
            if not isinstance(err_data, tuple):
                source_data[key][errtype] = (err_data, err_data)
    if isinstance(source_data['reference']['xerr'], tuple):
        allclose = all(np.allclose(source_data['reference']['xerr'][i],
                                   source_data['target']['xerr'][i]) \
                       for i in [0, 1])
    else:
        allclose = np.allclose(source_data['reference']['xerr'],
                               source_data['target']['xerr'])
    if not allclose:
        if (all_zero['reference']['xerr'] or all_zero['target']['xerr']):
            if not all_zero['reference']['xerr']:
                comparison_xerr = source_data['reference']['xerr']
            else:
                comparison_xerr = source_data['target']['xerr']
        else:
            raise RuntimeError('xerr of the reference and target distributions must match')
    else:
        comparison_xerr = source_data['reference']['xerr']
    
    if not (all_zero['reference']['xerr'] and all_zero['target']['xerr']):
        comparison_data['xerr'] = comparison_xerr
    else:
        comparison_data['xerr'] = np.zeros(comparison_data['x'].shape)
        
    if mode == HistComparisonMode.RATIO:
        comparison_data['y'] = safe_div(target_data['y'], reference_data['y'], True)
    elif mode == HistComparisonMode.DIFFERENCE:
        comparison_data['y'] = target_data['y'] - reference_data['y']
    
    if not (all_zero['reference']['yerr'] and all_zero['target']['yerr']):
        yerr_ref, yerr_tgt = source_data['reference']['yerr'], source_data['target']['yerr']
        if mode == HistComparisonMode.RATIO:
            if isinstance(yerr_ref, tuple):
                errlo = np.sqrt(safe_div(yerr_ref[0], reference_data['y'], True)**2 + 
                                safe_div(yerr_tgt[0], target_data['y'], True)**2)
                errhi = np.sqrt(safe_div(yerr_ref[1], reference_data['y'], True)**2 + 
                                safe_div(yerr_tgt[1], target_data['y'], True)**2)
                comparison_data['yerr'] = (errlo, errhi)
            else:
                comparison_data['yerr'] = np.sqrt(safe_div(yerr_ref, reference_data['y'], True)**2 + 
                                                  safe_div(yerr_tgt, target_data['y'], True)**2)
        elif mode == HistComparisonMode.DIFFERENCE:
            if isinstance(yerr_ref, tuple):
                errlo = np.sqrt(yerr_ref[0]**2 + yerr_tgt[0]**2)
                errhi = np.sqrt(yerr_ref[1]**2 + yerr_tgt[1]**2)
                comparison_data['yerr'] = (errlo, errhi)
            else:
                comparison_data['yerr'] = np.sqrt(yerr_ref**2 + yerr_tgt**2)
    else:
        comparison_data['yerr'] = np.zeros(comparison_data['x'].shape)
    return comparison_data

def get_global_pvalue_significance(x:np.ndarray, pvalue_local:Optional[np.ndarray]=None,
                                   Z_local:Optional[np.ndarray]=None, Z_ref:float=0):
    import ROOT
    def pval_to_Z(pvals):
        return np.array([ROOT.RooStats.PValueToSignificance(pval) for pval in pvals])
    if (pvalue_local is None) and (Z_local is None):
        raise ValueError('either pvalue_local or Z_local must be provided')
    elif (pvalue_local is not None) and (Z_local is not None):
        raise ValueError('can not specify both pvalue_local and Z_local')        
    elif (pvalue_local is not None) and (Z_local is None):
        Z_local = pval_to_Z(pvalue_local)
        pvalue_local = np.array(pvalue_local)
    elif (pvalue_local is None) and (Z_local is not None):
        Z_local = np.array(Z_local)
        pvalue_local = np.array([1 - ROOT.Math.normal_cdf(s, 1, 0) for s in Z_local])
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    Z_local = Z_local[sort_idx]
    pvalue_local = pvalue_local[sort_idx]
    asign = np.sign(Z_local - Z_ref)
    sign_change = (np.roll(asign, 1) - asign)
    sign_change[0] = 0
    # number of downcrossings
    N_up = np.sum(sign_change < 0)
    exp_term = np.exp(-0.5*(Z_local**2 - Z_ref**2))
    p_global = N_up * exp_term + pvalue_local
    delta_p_global = np.sqrt(N_up) * exp_term
    Z_global = pval_to_Z(p_global)
    Z_global_errhi = Z_global - pval_to_Z(p_global + delta_p_global)
    Z_global_errlo = pval_to_Z(p_global - delta_p_global) - Z_global
    result = {
        'N_up'           : np.full(p_global.shape, N_up),
        'p_global'       : p_global,
        'p_global_err'   : delta_p_global,
        'Z_global'       : Z_global,
        'Z_global_errhi' : Z_global_errhi,
        'Z_global_errlo' : Z_global_errlo
    }
    return result