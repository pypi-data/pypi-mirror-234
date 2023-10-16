from .main import run
import click

@click.command()
@click.argument('seismic_dir', required=True, nargs=-1, type=click.Path(exists=True))
@click.option('--output', '-o', help='Output directory for the DREEM-formatted files', default='.', type=click.Path(exists=True))
@click.option('--ow', help='Overwrite existing output files')
@click.option('--mask/--no-mask', help='Use the mask-per-pos.csv file instead of the relate-per-read.csv.gz file')
@click.option('--beautify/--no-beautify', help='Beautify JSON output')
@click.option('--verbose/--no-verbose', help='Print warnings')
def cli(seismic_dir, **kwargs):
    """seismic2dreem converts SEISMIC data to DREEM format.

    SEISMIC_DIR is the name of the SEISMIC input directory.
    
    """
    
    run(seismic_dir, **kwargs)
    