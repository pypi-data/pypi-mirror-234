import os
import json
import click

from .core import cli

__all__ = ['generate_standard_asimov', 'toy_significance', 'toy_limit']

@cli.command(name='generate_standard_asimov')
@click.option('-i', '--input_file', 'filename', required=True, 
              help='Path to the input workspace file.')
@click.option('-o', '--output_file', 'outname', required=True, 
              help='Name of the output workspace containing the '
                   'generated asimov dataset.')
@click.option('-d', '--data', 'data_name', default='combData', show_default=True,
              help='Name of the dataset used in NP profiling.')
@click.option('-p', '--poi', 'poi_name', required=True, 
              help='Name of the parameter of interest (POI). Multiple POIs are separated by commas.')
@click.option('-s', '--poi_scale', type=float, default=1.0, show_default=True,
              help='Scale factor applied to the poi value.')
@click.option('-e', '--eps', type=float, default=1.0, show_default=True,
              help='Minimization convergence criterium.')
@click.option('--strategy', type=int, default=1, show_default=True,
              help='Default minimization strategy.')
@click.option('-f', '--fix', 'fix_param', default="", show_default=True,
              help='Parameters to fix.')
@click.option('-r', '--profile', 'profile_param', default="", show_default=True,
              help='Parameters to profile.')
@click.option('-s', '--snapshot', 'snapshot_name', default=None, show_default=True,
              help='Name of initial snapshot.')
@click.option('--rebuild/--do-not-rebuild', default=False, show_default=True,
              help='Rebuild the workspace.')
@click.option('--asimov_names', default=None, show_default=True,
              help='Names of the output asimov datasets (separated by commas). If not specified, '
                   'a default name for the corresponding asimov type will be given.')
@click.option('--asimov_snapshots', default=None, show_default=True,
              help='Names of the output asimov snapshots (separated by commas). If not specified, '
                   'a default name for the corresponding asimov type will be given.')
@click.option('-t', '--asimov_types', default="0,1,2", show_default=True,
              help='\b\n Types of asimov dataset to generate separated by commas.'
                   '\b\n 0: fit with POI fixed to 0'
                   '\b\n 1: fit with POI fixed to 1'
                   '\b\n 2: fit with POI free and set POI to 1 after fit'
                   '\b\n 3: fit with POI and constrained NP fixed to 0'
                   '\b\n 4: fit with POI fixed to 1 and constrained NP fixed to 0'
                   '\b\n 5: fit with POI free and constrained NP fixed to 0 and set POI to 1 after fit'
                   '\b\n -1: nominal NP with POI set to 0'
                   '\b\n -2: nominal NP with POI set to 1')
@click.option('--extra_minimizer_options', default=None, show_default=True,
              help='Additional minimizer options to include. Format should be <config>=<value> '
                   'separated by commas. Example: "discrete_min_tol=0.001,do_discrete_iteration=1"')
@click.option('--cms_runtimedef', 'runtimedef_expr', default=None, show_default=True,
              help='CMS specific runtime definitions. Format should be <config>=<value> '
                   'separated by commas. Example: "REMOVE_CONSTANT_ZERO_POINT=1,ADDNLL_GAUSSNLL=0"')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level.')
def generate_standard_asimov(**kwargs):
    """
    Generate standard Asimov dataset
    """
    from quickstats.components import AsimovGenerator
    from quickstats.utils.string_utils import split_str
    outname = kwargs.pop('outname')
    asimov_types = kwargs.pop('asimov_types')
    try:
        asimov_types = split_str(asimov_types, sep=",", cast=int)
    except:
        asimov_types = split_str(asimov_types, sep=",")
    fix_param = kwargs.pop('fix_param')
    profile_param = kwargs.pop('profile_param')
    snapshot_name = kwargs.pop('snapshot_name')
    poi_scale = kwargs.pop("poi_scale")
    asimov_names = kwargs.pop("asimov_names")
    asimov_snapshots = kwargs.pop("asimov_snapshots")
    verbosity = kwargs.pop("verbosity")
    rebuild = kwargs.pop("rebuild")
    kwargs['poi_name'] = split_str(kwargs.pop('poi_name'), sep=",")
    config = {
        'fix_param': fix_param,
        'profile_param': profile_param,
        'snapshot_name': snapshot_name
    }
    from quickstats.utils.string_utils import split_str
    if asimov_names is not None:
        asimov_names = split_str(asimov_names, sep=",")
    if asimov_snapshots is not None:
        asimov_snapshots = split_str(asimov_snapshots, sep=",")
    generator = AsimovGenerator(**kwargs, config=config, verbosity=verbosity)
    generator.generate_standard_asimov(asimov_types, poi_scale=poi_scale,
                                       asimov_names=asimov_names,
                                       asimov_snapshots=asimov_snapshots)
    generator.save(outname, rebuild=rebuild)

@cli.command(name='toy_significance')
@click.option('-i', '--input_file', 'filename', required=True, 
              help='Path to the input workspace file.')
@click.option('-o', '--output_file', 'outname', default="toy_study/results.json", 
              help='Name of the output file containing toy results.')
@click.option('-n', '--n_toys', type=int,
              help='Number of the toys to use.')
@click.option('-b', '--batchsize', type=int, default=100, show_default=True,
              help='Divide the task into batches each containing this number of toys. '
                   'Result from each batch is saved for caching and different batches '
                   'are run in parallel if needed.')
@click.option('-s', '--seed', type=int, default=0,  show_default=True,
              help='Random seed used for generating toy datasets.')
@click.option('-p', '--poi', 'poi_name', default=None,
              help='Name of the parameter of interest (POI). If None, the first POI is used.')
@click.option('-v', '--poi_val', type=float, default=0,  show_default=True,
              help='POI value when generating the toy dataset.')
@click.option('--binned/--unbinned', default=True, show_default=True,
              help='Generate binned toy dataset.')
@click.option('--cache/--no-cache', default=True,  show_default=True,
              help='Cache existing batch results.')
@click.option('--fit_options', default=None, help='A json file specifying the fit options.')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level.')
@click.option('--parallel', type=int, default=-1, show_default=True,
              help='\b\n Parallelize job across the N workers.'
                   '\b\n Case  0: Jobs are run sequentially (for debugging).'
                   '\b\n Case -1: Jobs are run across N_CPU workers.')
def toy_significance(**kwargs):
    """
    Generate toys and evaluate significance
    """
    from quickstats.components import PValueToys
    n_toys = kwargs.pop("n_toys")
    batchsize = kwargs.pop("batchsize")
    seed = kwargs.pop("seed")
    cache = kwargs.pop("cache")
    outname = kwargs.pop("outname")
    parallel = kwargs.pop("parallel")
    pvalue_toys = PValueToys(**kwargs)
    pvalue_toys.get_toy_results(n_toys=n_toys, batchsize=batchsize, seed=seed,
                                cache=cache, save_as=outname, parallel=parallel)
    
@cli.command(name='toy_limit')
@click.option('-i', '--input_file', 'filename', required=True, 
              help='Path to the input workspace file.')
@click.option('-d', '--data', 'data_name', default='combData', show_default=True,
              help='Name of the dataset used for computing observed limit.')
@click.option('-o', '--output_file', 'outname', 
              default="toy_study/toy_result_seed_{seed}_batch_{batch}.root",
              show_default=True,
              help='Name of the output file containing toy results.')
@click.option('--poi_max', type=float, default=None,
              help='Maximum range of POI.')
@click.option('--poi_min', type=float, default=None,
              help='Minimum range of POI.')
@click.option('--scan_max', type=float, default=None,
              help='Maximum scan value of POI.')
@click.option('--scan_min', type=float, default=None,
              help='Minimum scan value of POI.')
@click.option('--steps', type=int, default=10, show_default=True,
              help='Number of scan steps.')
@click.option('--mu_val', type=float, default=None,
              help='Value of POI for running a single point.')
@click.option('-n', '--n_toys', type=int,
              help='Number of the toys to use.')
@click.option('-b', '--batchsize', type=int, default=50, show_default=True,
              help='Divide the task into batches each containing this number of toys. '
                   'Result from each batch is saved for caching and different batches '
                   'are run in parallel if needed.')
@click.option('-s', '--seed', type=int, default=2021,  show_default=True,
              help='Random seed used for generating toy datasets.')
@click.option('-t', '--tolerance', type=float, default=1.,  show_default=True,
              help='Tolerance for minimization.')
@click.option('-p', '--poi', 'poi_name', default=None,
              help='Name of the parameter of interest (POI). If None, the first POI is used.')
@click.option('--minimizer_type', default="Minuit2", show_default=True,
              help='Minimizer type.')
@click.option('--strategy', type=int, default=1, show_default=True,
              help='Default minimization strategy.')
@click.option('--offset/--no-offset', default=True, show_default=True,
              help='Use NLL offset.')
@click.option('--print_level', type=int, default=-1, show_default=True,
              help='Minimizer print level.')
@click.option('-v', '--verbosity', default='INFO', show_default=True,
              type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
              help='Verbosity level.')
@click.option('-f', '--fix', 'fix_param', default="", show_default=True,
              help='Parameters to fix.')
@click.option('-r', '--profile', 'profile_param', default="", show_default=True,
              help='Parameters to profile.')
@click.option('--snapshot', 'snapshot_name', default=None, help='Name of initial snapshot')
@click.option('--parallel', type=int, default=-1, show_default=True,
              help='\b\n Parallelize job across the N workers.'
                   '\b\n Case  0: Jobs are run sequentially (for debugging).'
                   '\b\n Case -1: Jobs are run across N_CPU workers.')
def toy_limit(**kwargs):
    """
    Generate toys and evaluate limits
    """
    from quickstats.components.toy_limit_calculator import evaluate_batched_toy_limits
    if not (((kwargs['scan_min'] is None) and (kwargs['scan_max'] is None) and (kwargs['mu_val'] is not None)) or \
           ((kwargs['scan_min'] is not None) and (kwargs['scan_max'] is not None) and (kwargs['mu_val'] is None))):
        raise ValueError("please provide either (scan_min, scan_max, steps) for running a scan or (mu_val)"
                         " for running a single point")        
    evaluate_batched_toy_limits(**kwargs)