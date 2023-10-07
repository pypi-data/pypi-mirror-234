import os
import json
import click

from .core import cli

__all__ = ['likelihood_fit', 'likelihood_scan']

@cli.command(name='likelihood_fit')
@click.option('-i', '--input_file', "filename", required=True, 
              help='Path to the input workspace file.')
@click.option('-o', '--outname', default='fit_result.json', show_default=True,
              help='Name of output file.')
@click.option('--display/--no-display', default=True, show_default=True,
              help='Display fit result.')
@click.option('--save/--no-save', "save_result", default=False, show_default=True,
              help='Save fit result.')
@click.option('--save_log/--skip_log', default=False, show_default=True,
              help='Save log file.')
@click.option('--save_ws', default=None, show_default=True,
              help='Save fitted workspace to a given path.')
@click.option('--save_snapshot', default=None, show_default=True,
              help='Save fitted values of all variables as a snapshot and restore all variables to '
              'their initial values. Should be used together with --save_ws.')
@click.option('--rebuild/--no-rebuild', default=True, show_default=True,
              help='Save fitted workspace by rebuilding it. Should be used together with --save_ws.')
@click.option('--export_as_np_pulls/--skip_export_as_np_pulls', default=False, show_default=True,
              help='Export (constrained) NP results for pulls plot.')
@click.option('--outdir', default="pulls", show_default=True,
              help='Output directory for pulls output.')
@click.option('-w', '--workspace', 'ws_name', default=None, show_default=True,
              help='Name of workspace. Auto-detect by default.')
@click.option('-m', '--model_config', 'mc_name', default=None, show_default=True,
              help='Name of model config. Auto-detect by default.')
@click.option('-d', '--data', 'data_name', default='combData', show_default=True,
              help='Name of dataset.')
@click.option('-s', '--snapshot', 'snapshot_name', default=None, show_default=True,
              help='Name of initial snapshot.')
@click.option('-r', '--profile', 'profile_param', default="", show_default=True,
              help='Parameters to profile.')
@click.option('-f', '--fix', 'fix_param', default="", show_default=True,
              help='Parameters to fix.')
@click.option('--pois', default="", show_default=True,
              help='Define the set of POIs (separated by commas) set for calculating Minos errors.')
@click.option('--constrain/--no-constrain', 'constrain_nuis', default=True, show_default=True,
              help='Use constrained NLL (i.e. include systematics).')
@click.option('--minos/--no-minos', default=False, show_default=True,
              help='Evaluate errors using Minos.')
@click.option('-t', '--minimizer_type', default="Minuit2", show_default=True,
              help='Minimizer type.')
@click.option('-a', '--minimizer_algo', default="Migrad", show_default=True,
              help='Minimizer algorithm.')
@click.option('--strategy', type=int, default=1, show_default=True,
              help='Default minimization strategy.')
@click.option('-e', '--eps', type=float, default=1.0, show_default=True,
              help='Minimization convergence criterium.')
@click.option('--retry', type=int, default=1, show_default=True,
              help='Maximum number of retries upon a failed fit.')
@click.option('--optimize', type=int, default=2, show_default=True,
              help='Optimize constant terms.')
@click.option('--minimizer_offset', type=int, default=1, show_default=True,
              help='Enable minimizer offsetting.')
@click.option('--offset/--no-offset', default=True, show_default=True,
              help='Offset likelihood.')
@click.option('--binned/--unbinned', 'binned_likelihood', default=True, show_default=True,
              help='Activate binned likelihood for RooRealSumPdf.')
@click.option('--print_level', type=int, default=-1, show_default=True,
              help='Minimizer print level.')
@click.option('-c', '--num_cpu', type=int, default=1, show_default=True,
              help='Number of CPUs to use during minimization.')
@click.option('--batch_mode/--no-batch', default=False, show_default=True,
              help='Batch mode when evaluating likelihood.')
@click.option('--int_bin_precision', type=float, default=-1., show_default=True,
              help='Integrate the PDF over the bins instead of using the probability '
                   'density at the bin center.')
@click.option('--extra_minimizer_options', default=None, show_default=True,
              help='Additional minimizer options to include. Format should be <config>=<value> '
                   'separated by commas. Example: "discrete_min_tol=0.001,do_discrete_iteration=1"')
@click.option('--cms_runtimedef', 'runtimedef_expr', default=None, show_default=True,
              help='CMS specific runtime definitions. Format should be <config>=<value> '
                   'separated by commas. Example: "REMOVE_CONSTANT_ZERO_POINT=1,ADDNLL_GAUSSNLL=0"')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level.')
def likelihood_fit(**kwargs):
    """
    Perform likelihood fit on a workspace
    """
    do_minos = kwargs.pop("minos")
    rebuild = kwargs.pop("rebuild")
    from quickstats.utils.string_utils import split_str
    pois = split_str(kwargs.pop("pois"), sep=',', remove_empty=True)
    _kwargs = {}
    for arg_name in ["outname", "save_log", "display", "save_result",
                     "export_as_np_pulls", "outdir", "save_ws", "save_snapshot"]:
        _kwargs[arg_name] = kwargs.pop(arg_name)
    _init_kwargs = {}
    for arg_name in ["filename", "data_name", "verbosity"]:
        _init_kwargs[arg_name] = kwargs.pop(arg_name)
    _init_kwargs['config'] = kwargs
    _init_kwargs['poi_name'] = pois
    from quickstats.components import AnalysisBase
    if _kwargs['save_log']:
        from quickstats.concurrent.logging import standard_log
        log_path = os.path.splitext(_kwargs["outname"])[0] + ".log"
        with standard_log(log_path) as logger:
            analysis = AnalysisBase(**_init_kwargs)
            if _kwargs['export_as_np_pulls']:
                analysis.minimizer.configure(hesse=True)
            fit_result = analysis.nll_fit(mode=3, do_minos=do_minos)
        print(f"INFO: Saved fit log to `{log_path}`")
    else:
        analysis = AnalysisBase(**_init_kwargs)
        fit_result = analysis.nll_fit(mode=3, do_minos=do_minos)
    output = {}
    output['fit_result'] = fit_result
    df = {'pois':{}, 'nuisance_parameters':{}}
    analysis.load_snapshot("currentSnapshot")
    df['pois']['prefit'] = analysis.model.as_dataframe('poi')
    df['nuisance_parameters']['prefit'] = analysis.model.as_dataframe('nuisance_parameter')
    analysis.load_snapshot("nllFit")
    if do_minos:
        df['pois']['postfit'] = analysis.model.as_dataframe('poi', asym_error=True)
    else:
        df['pois']['postfit'] = analysis.model.as_dataframe('poi')
    df['nuisance_parameters']['postfit'] = analysis.model.as_dataframe('nuisance_parameter')
    if _kwargs['display']:
        import pandas as pd
        pd.set_option('display.max_rows', None)
    for key in ['pois', 'nuisance_parameters']:
        df[key]['combined'] = df[key]['prefit'].drop(["value", "error"], axis=1)
        df[key]['combined']['value_prefit'] = df[key]['prefit']['value']
        df[key]['combined']['value_postfit'] = df[key]['postfit']['value']
        df[key]['combined']['error_prefit'] = df[key]['prefit']['error']
        if (key == "pois") and do_minos:
            df[key]['combined']['errorlo_postfit'] = df[key]['postfit']['errorlo']
            df[key]['combined']['errorhi_postfit'] = df[key]['postfit']['errorhi']
        else:
            df[key]['combined']['error_postfit'] = df[key]['postfit']['error']
        output[key] = df[key]['combined'].to_dict("list")
        if _kwargs['display']:
            print("{}:".format(key.title()))
            print(df[key]['combined'])
            print()
    if _kwargs['save_result']:
        import json
        with open(_kwargs["outname"], "w") as f:
            json.dump(output, f, indent=2)
        print(f"INFO: Saved fit result to `{_kwargs['outname']}`")
    if _kwargs['export_as_np_pulls']:
        outdir = _kwargs['outdir']
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        nuis_df = df[key]['combined'].drop(['min', 'max', 'is_constant', 'error_prefit'], axis=1)
        nuis_df = nuis_df.rename(columns={"value_prefit":"nuis_nom", "name":"nuisance", 
                                          "value_postfit":"nuis_hat", "error_postfit":"nuis_hi"})
        nuis_df["nuis_lo"] = nuis_df["nuis_hi"]
        nuis_df["nuis_prefit"] = 1.0
        nuis_df = nuis_df.set_index(['nuisance'])
        constrained_np = [i.GetName() for i in analysis.model.get_constrained_nuisance_parameters()]
        nuis_df = nuis_df.loc[constrained_np].reset_index()
        nuis_data = nuis_df.to_dict('index')
        import json
        for i in nuis_data:
            data = nuis_data[i]
            np_name = data['nuisance']
            outpath = os.path.join(outdir, f"{np_name}.json")
            with open(outpath, "w") as outfile:
                json.dump({"nuis": data}, outfile, indent=2)
    if _kwargs["save_ws"] is not None:
        filename = _kwargs["save_ws"]
        if _kwargs["save_snapshot"] is not None:
            snapshot_name = _kwargs["save_snapshot"]
            from quickstats.components.basics import WSArgument
            analysis.save_snapshot(snapshot_name, WSArgument.MUTABLE)
            analysis.load_snapshot(analysis.kInitialSnapshotName)
        analysis.save(filename, rebuild=rebuild)

@cli.command(name='likelihood_scan')
@click.option('-i', '--input_path', required=True, 
              help='Input directory/path containing the workspace file(s) to process.')
@click.option('--file_expr', default=None, show_default=True,
              help='\b\n File name expression describing the external parameterisation.'
                   '\b\n Example: "<mass[F]>_kl_<klambda[P]>"'
                   '\b\n Regular expression is supported'
                   '\b\n Refer to documentation for more information')
@click.option('-p', '--param_expr', default=None,
              help='\b\n Parameter expression, e.g.'
                   '\b\n 1D scan: "poi_name=<poi_min>_<poi_max>_<step>"'
                   '\b\n 2D scan: "poi_1_name=<poi_1_min>_<poi_1_max>_<step_1>,'
                   '\b\n           poi_2_name=<poi_2_min>_<poi_2_max>_<step_2>"')
@click.option('--filter', 'filter_expr', default=None, show_default=True,
              help='\b\n Filter parameter points by expression.'
                   '\b\n Example: "mass=2*,350,400,450;klambda=1.*,2.*,-1.*,-2.*"'
                   '\b\n Refer to documentation for more information')
@click.option('--exclude', 'exclude_expr', default=None, show_default=True,
              help='\b\n Exclude parameter points by expression.'
                   '\b\n Example: "mass=2*,350,400,450;klambda=1.*,2.*,-1.*,-2.*"'
                   '\b\n Refer to documentation for more information')
@click.option('--cache/--no-cache', default=True, show_default=True,
              help='Cache existing result.')
@click.option('-o', '--outname', default='{poi_names}.json', show_default=True,
              help='Name of output file.')
@click.option('--outdir', default='likelihood_scan', show_default=True,
              help='Output directory.')
@click.option('--cachedir', default='cache', show_default=True,
              help='Cache directory relative to the output directory.')
@click.option('--save_log/--skip_log', default=True, show_default=True,
              help='Save log file.')
@click.option('-w', '--workspace', 'ws_name', default=None, show_default=True,
              help='Name of workspace. Auto-detect by default.')
@click.option('-m', '--model_config', 'mc_name', default=None, show_default=True,
              help='Name of model config. Auto-detect by default.')
@click.option('-d', '--data', 'data_name', default='combData', show_default=True,
              help='Name of dataset.')
@click.option('-s', '--snapshot', 'snapshot_name', default=None, show_default=True,
              help='Name of initial snapshot.')
@click.option('--uncond_snapshot', default=None, show_default=True,
              help='Name of snapshot with unconditional fit result.')
@click.option('-r', '--profile', 'profile_param', default="", show_default=True,
              help='Parameters to profile.')
@click.option('-f', '--fix', 'fix_param', default="", show_default=True,
              help='Parameters to fix.')
@click.option('--constrain/--no-constrain', 'constrain_nuis', default=True, show_default=True,
              help='Use constrained NLL (i.e. include systematics).')
@click.option('--allow-nan/--not-allow-nan', default=True, show_default=True,
              help='Allow cached nll to be nan.')
@click.option('-t', '--minimizer_type', default="Minuit2", show_default=True,
              help='Minimizer type.')
@click.option('-a', '--minimizer_algo', default="Migrad", show_default=True,
              help='Minimizer algorithm.')
@click.option('--strategy', type=int, default=1, show_default=True,
              help='Default minimization strategy.')
@click.option('-e', '--eps', type=float, default=1.0, show_default=True,
              help='Minimization convergence criterium.')
@click.option('--retry', type=int, default=1, show_default=True,
              help='Maximum number of retries upon a failed fit.')
@click.option('--optimize', type=int, default=2, show_default=True,
              help='Optimize constant terms.')
@click.option('--minimizer_offset', type=int, default=1, show_default=True,
              help='Enable minimizer offsetting.')
@click.option('--offset/--no-offset', default=True, show_default=True,
              help='Offset likelihood.')
@click.option('--binned/--unbinned', 'binned_likelihood', default=True, show_default=True,
              help='Activate binned likelihood for RooRealSumPdf.')
@click.option('--print_level', type=int, default=-1, show_default=True,
              help='Minimizer print level.')
@click.option('-c', '--num_cpu', type=int, default=1, show_default=True,
              help='Number of CPUs to use during minimization.')
@click.option('--batch_mode/--no-batch', default=False, show_default=True,
              help='Batch mode when evaluating likelihood.')
@click.option('--int_bin_precision', type=float, default=-1., show_default=True,
              help='Integrate the PDF over the bins instead of using the probability '
                   'density at the bin center.')
@click.option('--extra_minimizer_options', default=None, show_default=True,
              help='Additional minimizer options to include. Format should be <config>=<value> '
                   'separated by commas. Example: "discrete_min_tol=0.001,do_discrete_iteration=1"')
@click.option('--cms_runtimedef', 'runtimedef_expr', default=None, show_default=True,
              help='CMS specific runtime definitions. Format should be <config>=<value> '
                   'separated by commas. Example: "REMOVE_CONSTANT_ZERO_POINT=1,ADDNLL_GAUSSNLL=0"')
@click.option('--parallel', type=int, default=-1, show_default=True,
              help='\b\n Parallelize job across the N workers.'
                   '\b\n Case  0: Jobs are run sequentially (for debugging).'
                   '\b\n Case -1: Jobs are run across N_CPU workers.')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level.')
def likelihood_scan(**kwargs):
    """
    Evaluate a set of parmeterised likelihood values
    """
    _kwargs = {}
    for arg_name in ["input_path", "file_expr", "param_expr", "data_name", "outdir", "filter_expr",
                     "uncond_snapshot", "exclude_expr", "outname", "cache", "cachedir", "save_log",
                     "parallel", "verbosity", "allow_nan"]:
        _kwargs[arg_name] = kwargs.pop(arg_name)
    _kwargs['config'] = kwargs
    from quickstats.concurrent import ParameterisedLikelihood
    runner = ParameterisedLikelihood(**_kwargs)
    runner.run()

@cli.command(name='significance_scan')
@click.option('-i', '--input_path', required=True, 
              help='Path to the input workspace file or directory containing the parameterised '
                   'input workspace files.')
@click.option('-p', '--poi', 'poi_name', default=None,
              help='Name of the parameter of interest (POI). If None, the first POI is used.')
@click.option('--mu_exp', type=float, default=0., show_default=True,
              help='Expected value of the POI under the null hypothesis.')
@click.option('--asimov_type', type=int, default=None,
              help='\b\n Evaluate significance on an Asimov dataset of this type. '
                   'If not specified, the observed data is used. '
                   '\b\n Choices of asimov types are'
                   '\b\n 0: fit with POI fixed to 0'
                   '\b\n 1: fit with POI fixed to 1'
                   '\b\n 2: fit with POI free and set POI to 1 after fit'
                   '\b\n 3: fit with POI and constrained NP fixed to 0'
                   '\b\n 4: fit with POI fixed to 1 and constrained NP fixed to 0'
                   '\b\n 5: fit with POI free and constrained NP fixed to 0 and set POI to 1 after fit'
                   '\b\n -1: nominal NP with POI set to 0'
                   '\b\n -2: nominal NP with POI set to 1')
@click.option('--file_expr', default=r"[\w-]+", show_default=True,
              help='\b\n File name expression describing the external parameterisation.'
                   '\b\n Example: "<mass[F]>_kl_<klambda[P]>"'
                   '\b\n Regular expression is supported'
                   '\b\n Refer to documentation for more information')
@click.option('--param_expr', default=None, show_default=True,
              help='\b\n Parameter name expression describing the internal parameterisation.'
                   '\b\n Example: "klambda=-10_10_0.2,k2v=(1,2,3)"'
                   '\b\n Refer to documentation for more information')
@click.option('--filter', 'filter_expr', default=None, show_default=True,
              help='\b\n Filter parameter points by expression.'
                   '\b\n Example: "mass=(2*,350,400,450);klambda=(1.*,2.*,-1.*,-2.*)"'
                   '\b\n Refer to documentation for more information')
@click.option('--exclude', 'exclude_expr', default=None, show_default=True,
              help='\b\n Exclude parameter points by expression.'
                   '\b\n Example: "mass=(2*,350,400,450);klambda=(1.*,2.*,-1.*,-2.*)"'
                   '\b\n Refer to documentation for more information')
@click.option('--outdir', default='significance', show_default=True,
              help='Output directory where cached limit files and the merged limit file are saved.')
@click.option('--cachedir', default='cache', show_default=True,
              help='Cache directory relative to the output directory.')
@click.option('--cache/--no-cache', default=True, show_default=True,
              help='Cache existing result.')
@click.option('-o', '--outname', default='{param_names}.json', show_default=True,
              help='Name of the output significance file (all parameter points merged).')
@click.option('--save_log/--skip_log', default=True, show_default=True,
              help='Save log file.')
@click.option('-w', '--workspace', 'ws_name', default=None, show_default=True,
              help='Name of workspace. Auto-detect by default.')
@click.option('-m', '--model_config', 'mc_name', default=None, show_default=True,
              help='Name of model config. Auto-detect by default.')
@click.option('-d', '--data', 'data_name', default='combData', show_default=True,
              help='Name of dataset.')
@click.option('-s', '--snapshot', 'snapshot_name', default=None, show_default=True,
              help='Name of initial snapshot.')
@click.option('-r', '--profile', 'profile_param', default="", show_default=True,
              help='Parameters to profile.')
@click.option('-f', '--fix', 'fix_param', default="", show_default=True,
              help='Parameters to fix.')
@click.option('-t', '--minimizer_type', default="Minuit2", show_default=True,
              help='Minimizer type.')
@click.option('-a', '--minimizer_algo', default="Migrad", show_default=True,
              help='Minimizer algorithm.')
@click.option('--strategy', type=int, default=1, show_default=True,
              help='Default minimization strategy.')
@click.option('-e', '--eps', type=float, default=1.0, show_default=True,
              help='Minimization convergence criterium.')
@click.option('--retry', type=int, default=1, show_default=True,
              help='Maximum number of retries upon a failed fit.')
@click.option('--optimize', type=int, default=2, show_default=True,
              help='Optimize constant terms.')
@click.option('--minimizer_offset', type=int, default=1, show_default=True,
              help='Enable minimizer offsetting.')
@click.option('--offset/--no-offset', default=True, show_default=True,
              help='Offset likelihood.')
@click.option('--binned/--unbinned', 'binned_likelihood', default=True, show_default=True,
              help='Activate binned likelihood for RooRealSumPdf.')
@click.option('--print_level', type=int, default=-1, show_default=True,
              help='Minimizer print level.')
@click.option('-c', '--num_cpu', type=int, default=1, show_default=True,
              help='Number of CPUs to use during minimization.')
@click.option('--batch_mode/--no-batch', default=False, show_default=True,
              help='Batch mode when evaluating likelihood.')
@click.option('--int_bin_precision', type=float, default=-1., show_default=True,
              help='Integrate the PDF over the bins instead of using the probability '
                   'density at the bin center.')
@click.option('--extra_minimizer_options', default=None, show_default=True,
              help='Additional minimizer options to include. Format should be <config>=<value> '
                   'separated by commas. Example: "discrete_min_tol=0.001,do_discrete_iteration=1"')
@click.option('--cms_runtimedef', 'runtimedef_expr', default=None, show_default=True,
              help='CMS specific runtime definitions. Format should be <config>=<value> '
                   'separated by commas. Example: "REMOVE_CONSTANT_ZERO_POINT=1,ADDNLL_GAUSSNLL=0"')
@click.option('--parallel', type=int, default=-1, show_default=True,
              help='\b\n Parallelize job across the N workers.'
                   '\b\n Case  0: Jobs are run sequentially (for debugging).'
                   '\b\n Case -1: Jobs are run across N_CPU workers.')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level.')
def significance_scan(**kwargs):
    """
    Evaluate a set of parmeterised significance values
    """
    _kwargs = {}
    for arg_name in ["input_path", "poi_name", "data_name", "file_expr", "param_expr",
                     "filter_expr", "exclude_expr", "mu_exp", "asimov_type",
                     "snapshot_name", "outdir", "cachedir", "outname", "cache",
                     "save_log", "parallel", "verbosity"]:
        _kwargs[arg_name] = kwargs.pop(arg_name)
    _kwargs['config'] = kwargs
    from quickstats.concurrent import ParameterisedSignificance
    runner = ParameterisedSignificance(**_kwargs)
    runner.run()