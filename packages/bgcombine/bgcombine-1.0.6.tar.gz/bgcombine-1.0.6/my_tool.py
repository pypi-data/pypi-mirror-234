import click
import app.attendance as attendance
import app.personal_info_all_data as info

@click.command()
@click.argument('mode')
@click.argument('pth_out')
@click.option('--c')
@click.option('--filtered')
@click.version_option('1.0.6')
def main(mode, pth_out, c, filtered):
    if mode == 'info':
        pth_in = click.prompt("\n--------------------------------------------------\nenter path to child and family data input folder")
        info.main(pth_in, pth_out)
    elif mode == 'attendance':
        pth_in = click.prompt("\n--------------------------------------------------\nenter path to attendance data input folder")
        attendance.main(pth_in, pth_out, filtered, c)
    else:
        click.echo(f'{mode} is not a supported mode. Type --help for accepted commands.')