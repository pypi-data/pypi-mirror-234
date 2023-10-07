from typing import Dict, Union, List, Optional, Tuple
import itertools
import uuid

import numpy as np

from quickstats import semistaticmethod, AbstractObject
from quickstats.interface.cppyy.vectorize import as_np_array, as_vector, np_type_str_maps
from .TH1 import TH1
from .TH2 import TH2
from .TH3 import TH3
from .TArrayData import TArrayData

class RooAbsPdf(AbstractObject):
    
    @staticmethod
    def extract_sum_pdfs_by_category(pdf:"ROOT.RooAbsPdf", poi:Optional["ROOT.RooRealVar"]=None):
        pdf_class = pdf.ClassName()
        if pdf_class != "RooSimultaneous":
            raise RuntimeError(f"input pdf must be a RooSimultaneous instance (`{pdf_class}` received)")
        cat = pdf.indexCat()
        n_cat = cat.size()
        result = {}
        for i in range(n_cat):
            cat.setBin(i)
            cat_name = cat.getLabel()
            cat_pdf = pdf.getPdf(cat_name)
            cat_pdf_class = cat_pdf.ClassName()
            if cat_pdf_class != "RooProdPdf":
                raise RuntimeError(f"category pdf must be a RooProdPdf instance (`{cat_pdf_class}` received)")
            target_pdf = [i for i in cat_pdf.pdfList() if i.ClassName() == "RooRealSumPdf" and i != cat_pdf]
            if not target_pdf:
                raise RuntimeError(f"category pdf does not contain a RooRealSumPdf component")
            if len(target_pdf) > 1:
                raise RuntimeError(f"expect only one RooRealSumPdf component from category pdf but {len(target_pdf)} found")
            target_pdf = target_pdf[0]
            if poi is None:
                result[cat_name] = [i for i in pdf.getComponents()]
            else:
                result[cat_name] = [i for i in pdf.getComponents() if i.dependsOn(poi)]
        return result
    
    @semistaticmethod
    def get_values(self, pdf:"RooAbsPdf",
                   observables:"ROOT.RooArgSet",
                   bin_centers:np.ndarray):
        import ROOT
        vec_bin_centers = as_vector(bin_centers)
        type_str = np_type_str_maps.get(bin_centers.dtype, None)
        if type_str is None:
            bin_centers = bin_centers.astype(float)
            type_str = 'double'
        vec_values = ROOT.RFUtils.GetPdfValues[type_str](pdf, observables, vec_bin_centers)
        values = TArrayData.vec_to_array(vec_values)
        return values
    
    @semistaticmethod
    def get_histogram(self, pdf:"RooAbsPdf",
                      observables:"ROOT.RooArgSet",
                      histname:str='hist',
                      histtitle:Optional[str]=None,
                      nbins:Optional[int]=None,
                      bin_range:Optional[Tuple[float]]=None,
                      weight_scale:Optional[float]=None):
        distribution = self.get_distribution(pdf, observables,
                                             nbins=nbins,
                                             bin_range=bin_range,
                                             weight_scale=weight_scale)
        from quickstats.interface.root import TH1
        from quickstats.maths.statistics import bin_center_to_bin_edge
        bin_edges = bin_center_to_bin_edge(distribution['x'])
        hist = TH1.from_numpy_histogram(distribution['y'],
                                        bin_edges=bin_edges)
        roohist = hist.to_ROOT(histname, histtitle)
        return roohist
    
    @semistaticmethod
    def get_distribution(self, pdf:"RooAbsPdf",
                         observables:"ROOT.RooArgSet", 
                         nbins:Optional[int]=None,
                         bin_range:Optional[Tuple[float]]=None,
                         weight_scale:Optional[float]=None):
        # the observables are needed for normalization
        pdf_obs = pdf.getObservables(observables)
        target_obs = pdf_obs.first()
        if nbins is None:
            nbins = target_obs.numBins()
        if bin_range is None:
            obs_name = target_obs.GetName()
            histogram = pdf.createHistogram(obs_name, nbins)
            py_histogram = TH1(histogram)
            binning_class = target_obs.getBinning().ClassName()
            if binning_class == "RooUniformBinning":
                bin_widths = py_histogram.bin_width
            else:
                bin_widths = RooRealVar.get_bin_widths(target_obs)
            x = py_histogram.bin_center
            y = py_histogram.bin_content * bin_widths
            # free memory to avoid memory leak
            histogram.Delete()
        else:
            assert len(bin_range) == 2
            from quickstats.maths.statistics import get_bin_centers_from_range
            x = get_bin_centers_from_range(bin_range[0], bin_range[1], nbins)
            y = self.get_values(pdf, observables, x)
            normalization = pdf.expectedEvents(pdf_obs)
            bin_width = round((bin_range[1] -  bin_range[0]) / nbins, 8)
            y = y * normalization * bin_width
        if weight_scale is not None:
            y *= weight_scale
        result = {
            'x': x,
            'y': y
        }
        return result
    
    @semistaticmethod
    def get_expected_events_over_range(self, pdf:"RooAbsPdf",
                                       observables:"ROOT.RooArgSet",
                                       range_lo:float,
                                       range_li:float,
                                       normalize:bool=False):
        import ROOT
        expected_events = ROOT.RFUtils.GetPdfExpectedEventsOverRange(pdf, observables,
                                                                     range_lo, range_li,
                                                                     normalize)
        return expected_events
    
    @semistaticmethod
    def get_expected_events_and_error_band_over_range(self, pdf:"RooAbsPdf",
                                                      observables:"ROOT.RooArgSet",
                                                      range_lo:float,
                                                      range_hi:float,
                                                      parameters:"ROOT.RooArgSet",
                                                      fit_result,
                                                      dataset:Optional[Dict]=None,
                                                      Z:int=1,
                                                      n_samples:Optional[int]=None,
                                                      seed:int=0):
        import ROOT
        central_curve = ROOT.RooCurve()
        nominal_yield = self.get_expected_events_over_range(pdf, observables, range_lo, range_hi)
        central_curve.addPoint(0, nominal_yield)
        clone_func = pdf.cloneTree()
        clone_params = clone_func.getObservables(fit_result.floatParsFinal())
        error_params = clone_params.selectCommon(parameters)
        param_pdf = fit_result.createHessePdf(error_params)
        if dataset is None:
            ROOT.gRandom.SetSeed(seed)
            if n_samples is None:
                n_samples = int(100 / ROOT.TMath.Erfc(Z / ROOT.TMath.Sqrt2())) * 100
            if (n_samples < 100):
                n_samples = 100
            dataset = param_pdf.generate(error_params, n_samples)
        else:
            from quickstats.interface.root import RooDataSet
            dataset = RooDataSet.from_numpy(dataset, error_params)
        toy_values = ROOT.RFUtils.GetPdfExpectedEventsOverRangeAcrossDataset(clone_func, dataset,
                                                                             observables,
                                                                             range_lo, range_hi)
        from quickstats.interface.cppyy.vectorize import as_np_array
        values = as_np_array(toy_values)
        median_yield = np.median(values)
        median_curve = ROOT.RooCurve()
        median_curve.addPoint(0, median_yield)
        errorband_curve = ROOT.RFUtils.createErrorBandFromArrayData(central_curve, toy_values, Z)
        median_errorband_curve = ROOT.RFUtils.createErrorBandFromArrayData(median_curve, toy_values, Z)
        # only one point, no need to loop over points
        result = {
            'central': central_curve.GetPointY(0),
            'median' : median_curve.GetPointY(0),
            'errorlo': central_curve.GetPointY(0) - errorband_curve.GetPointY(0),
            'errorhi': errorband_curve.GetPointY(1) - central_curve.GetPointY(0),
            'median_errorlo': median_curve.GetPointY(0) - median_errorband_curve.GetPointY(0),
            'median_errorhi': median_errorband_curve.GetPointY(1) - median_curve.GetPointY(0),
            'values': values
        }
        return result
    
    @semistaticmethod
    def get_asimov_dataset_sim_pdf(self, pdf:"RooSimultaneous",
                                   observables:"ROOT.RooArgSet",
                                   weight_name:Optional[str]="weight",
                                   dataset_name:Optional[str]="asimovData",
                                   remove_non_positive_bins=True):
        import ROOT
        assert pdf.InheritsFrom("RooSimultaneous")
        pdf_observables = pdf.getObservables(observables)
        dataset_map = {}
        channel_cat = pdf.indexCat()
        for cat_data in channel_cat:
            label = cat_data.first
            cat_pdf = pdf.getPdf(label)
            # name does not really matter here
            cat_dataset_name = f"{dataset_name}_{label}"
            cat_dataset = self.get_asimov_dataset(cat_pdf, pdf_observables,
                                                  weight_name=weight_name,
                                                  dataset_name=cat_dataset_name,
                                                  remove_non_positive_bins=remove_non_positive_bins)
            dataset_map[label] = cat_dataset
        if weight_name not in pdf_observables:
            weight_var = ROOT.RooRealVar(weight_name, weight_name, 1)
            pdf_observables.add(weight_var)
        else:
            weight_var = pdf_observables[weight_name]
        if channel_cat not in pdf_observables:
            pdf_observables.add(channel_cat)
        from quickstats.interface.root import RooDataSet
        # reset initial values of observables 
        for obs in pdf_observables:
            obs.setBin(0)
        c_dataset_map = RooDataSet.get_dataset_map(dataset_map)
        asimov_data = ROOT.RooDataSet(dataset_name, dataset_name, 
                                      pdf_observables,
                                      ROOT.RooFit.Index(channel_cat),
                                      ROOT.RooFit.Import(c_dataset_map),
                                      ROOT.RooFit.WeightVar(weight_var))
        return asimov_data
    
    # has precision issue since the histograms are always of type "float"
    @semistaticmethod
    def _get_histo_values_old(self, pdf:"ROOT.RooAbsPdf",
                              obs_x:"ROOT.RooRealVar",
                              obs_y:Optional["ROOT.RooRealVar"]=None,
                              obs_z:Optional["ROOT.RooRealVar"]=None):
        import ROOT
        var_y = ROOT.RooFit.YVar(obs_y) if obs_y is not None else ROOT.RooCmdArg.none()
        var_z = ROOT.RooFit.ZVar(obs_z) if obs_z is not None else ROOT.RooCmdArg.none()
        rhist = pdf.createHistogram(f'{uuid.uuid4().hex}', obs_x, var_y, var_z)
        ndim = rhist.GetDimension()
        if ndim == 1:
            result = TH1.GetBinContentArray(rhist).flatten()
        elif ndim == 2:
            result = TH2.GetBinContentArray(rhist).flatten()          
        elif ndim == 3:
            result = TH3.GetBinContentArray(rhist).flatten()         
        else:
            raise RuntimeError('histogram dimension must be 1, 2 or 3')
        rhist.Delete()
        return result
                                    
    @semistaticmethod
    def _get_histo_values(self, pdf:"ROOT.RooAbsPdf", observables:"ROOT.RooRealVar"):
        rhist = self.create_histogram(f'{uuid.uuid4().hex}', observables, 'double')
        if pdf.canBeExtended():
            scale_factor = pdf.expectedEvents(observables)
        else:
            scale_factor = 1.0
        pdf.fillHistogram(rhist, observables, scale_factor, 0, False)
        ndim = rhist.GetDimension()
        if ndim == 1:
            result = TH1.GetBinContentArray(rhist).flatten()
        elif ndim == 2:
            result = TH2.GetBinContentArray(rhist).flatten()          
        elif ndim == 3:
            result = TH3.GetBinContentArray(rhist).flatten()         
        else:
            raise RuntimeError('histogram dimension must be 1, 2 or 3')
        rhist.Delete()
        return result
    
    @semistaticmethod
    def get_asimov_dataset(self, pdf:"ROOT.RooAbsPdf",
                           observables:"ROOT.RooArgSet",
                           weight_name:Optional[str]="weight",
                           dataset_name:Optional[str]="asimovData",
                           remove_non_positive_bins:bool=True):
        if pdf.InheritsFrom("RooSimultaneous"):
            return self.get_asimov_dataset_sim_pdf(pdf, observables,
                                                   weight_name=weight_name,
                                                   dataset_name=dataset_name)
        import ROOT
        from quickstats.interface.root import RooRealVar
        from quickstats.interface.root import RooDataSet
        from quickstats.interface.cppyy.vectorize import as_np_array
        bin_centers = {}
        bin_indices = {}
        bin_widths  = {}
        pdf_observables = pdf.getObservables(observables)
        for obs in pdf_observables:
            obs_name = obs.GetName()
            obs_binning = RooRealVar.get_binning(obs)
            bin_centers[obs_name] = obs_binning['bin_center']
            bin_widths[obs_name] = obs_binning['bin_width']
            bin_indices[obs_name] = list(range(obs.numBins()))
        self.stdout.debug(f'Generating asimov dataset for the pdf {pdf.GetName()} (observables = {list(bin_centers)}) ')
        bin_center_combination = np.array(list(itertools.product(*bin_centers.values())), dtype=float)
        bin_width_combination = np.array(list(itertools.product(*bin_widths.values())))
        bin_index_combination = np.array(list(itertools.product(*bin_indices.values())))
        np_ds = {}
        for i, obs_name in enumerate(bin_centers):
            np_ds[obs_name] = bin_center_combination[:, i]
        nobs = len(bin_centers)
        # use histogram method for low dimensions
        if nobs in [1, 2, 3]:
            pdf_values = self._get_histo_values(pdf, pdf_observables)
        else:
            ds = RooDataSet.from_numpy(np_ds, pdf_observables)
            pdf_values = ROOT.RFUtils.GetPdfValuesAcrossObsDataset(pdf, ds, True)
            pdf_values = as_np_array(pdf_values)
        # multiply by bin width(s)
        num_events = pdf_values * np.prod(bin_width_combination, axis=1)
        np_ds[weight_name] = num_events
        if self.stdout.verbosity == "DEBUG":
            for bin_index, bin_center, exp_event in zip(bin_index_combination, bin_center_combination, np_ds[weight_name]):
                self.stdout.debug(f'Expected events = {exp_event}, Bin index = {bin_index}, '
                                  f' Bin value = {bin_center}')
        if remove_non_positive_bins:
            mask = np_ds[weight_name] <= 0
            if mask.sum() > 0:
                obs_names = list(bin_centers)
                np_bin_index = bin_index_combination[mask]
                np_bin_center = bin_center_combination[mask]
                np_exp_event = np_ds[weight_name][mask]
                self.stdout.warning(f'Detected bin(s) in pdf {pdf.GetName()} (observables = {list(bin_centers)}) '
                                    f'with zero or negative expected events! Please check your input.')
                for bin_index, bin_center, exp_event in zip(np_bin_index, np_bin_center, np_exp_event):
                    self.stdout.warning(f'Expected events = {exp_event}, Bin index = {bin_index}, '
                                        f' Bin value = {bin_center}')
                for key in np_ds:
                    np_ds[key] = np_ds[key][~mask]
        if weight_name not in pdf_observables:
            weight_var = ROOT.RooRealVar(weight_name, weight_name, 1)
            pdf_observables.add(weight_var)
        asimov_data = RooDataSet.from_numpy(np_ds, pdf_observables, weight_name=weight_name)
        if (asimov_data.sumEntries() != asimov_data.sumEntries()):
            raise RuntimeError("asimov data sum entries is nan")        
        return asimov_data
    
    @staticmethod
    def get_pdf_map(pdf_dict:Dict):
        import ROOT
        from quickstats.interface.cppyy.basic_methods import get_std_object_map
        pdf_map = get_std_object_map(pdf_dict, 'RooAbsPdf')
        return pdf_map
    
    @semistaticmethod
    def build_simultaneous_pdf(self, pdfs:Union["RooAbsPdf", List["RooAbsPdf"]],
                               pdf_name:str="simPdf",
                               cat_name:str="indexCat"):
        import ROOT
        category = ROOT.RooCategory(cat_name, cat_name)
        sim_pdf = ROOT.RooSimultaneous(pdf_name, pdf_name, category)
        if not isinstance(pdfs, list):
            pdfs = [pdfs]
        for pdf in pdfs:
            category_name = pdf.GetName()
            category.defineType(category_name)
            sim_pdf.addPdf(pdf, category_name)
        ROOT.SetOwnership(category, False)
        return sim_pdf

    @semistaticmethod
    def remove_disconnected_components(self, pdf:"ROOT.RooProdPdf",
                                       data:"ROOT.RooDataSet",
                                       pdf_name:Optional[str]=None,
                                       pdf_title:Optional[str]=None):
        assert pdf.ClassName() == "RooProdPdf"
        pdf_parameters = pdf.getParameters(data)
        data_parameters = data.get()
        constraints = pdf.getAllConstraints(data_parameters, pdf_parameters, True)
        disconnected_constraints = pdf.getAllConstraints(data_parameters, pdf_parameters, False)
        disconnected_constraints.remove(constraints)
        import ROOT
        base_components = ROOT.RooArgSet()
        ROOT.RFUtils.GetProdPdfBaseComponents(pdf, base_components)
        # remove disconnected pdfs
        base_components.remove(disconnected_constraints)
        if pdf_name is None:
            pdf_name = pdf.GetName()
        if pdf_title is None:
            pdf_title = pdf.GetTitle()
        new_pdf = ROOT.RooProdPdf(pdf_name, pdf_title, base_components)
        return new_pdf
    
    @semistaticmethod
    def create_histogram(self, name:str, observables:"ROOT.RooArgSet", dtype:str="double"):
        ndim = len(observables)
        if (ndim < 1) or (ndim > 3):
            raise ValueError('dimension not supported')
        binnings = [observable.getBinning() for observable in observables]
        if dtype not in ["float", "double"]:
            raise RuntimeError('dtype must be "float" or "double"')
        import ROOT
        if ndim == 1:
            cls = ROOT.TH1D if dtype == "double" else ROOT.TH1F
            if binnings[0].isUniform():
                histogram = cls(name, name,
                                binnings[0].numBins(),
                                binnings[0].lowBound(),
                                binnings[0].highBound())
            else:
                histogram = cls(name, name,
                                binnings[0].numBins(),
                                binnings[0].array())
        elif ndim == 2:
            cls = ROOT.TH2D if dtype == "double" else ROOT.TH2F
            if (binnings[0].isUniform() and binnings[1].isUniform()):
                histogram = cls(name, name,
                                binnings[0].numBins(),
                                binnings[0].lowBound(),
                                binnings[0].highBound(),
                                binnings[1].numBins(),
                                binnings[1].lowBound(),
                                binnings[1].highBound())
            else:
                histogram = cls(name, name,
                                binnings[0].numBins(),
                                binnings[0].array(),
                                binnings[1].numBins(),
                                binnings[1].array())
        else:
            cls = ROOT.TH3D if dtype == "double" else ROOT.TH3F
            if (binnings[0].isUniform() and binnings[1].isUniform() and binnings[2].isUniform()):
                histogram = cls(name, name,
                                binnings[0].numBins(),
                                binnings[0].lowBound(),
                                binnings[0].highBound(),
                                binnings[1].numBins(),
                                binnings[1].lowBound(),
                                binnings[1].highBound(),
                                binnings[2].numBins(),
                                binnings[2].lowBound(),
                                binnings[2].highBound())
            else:
                histogram = cls(name, name,
                                binnings[0].numBins(),
                                binnings[0].array(),
                                binnings[1].numBins(),
                                binnings[1].array(),
                                binnings[2].numBins(),
                                binnings[2].array())
        return histogram        
