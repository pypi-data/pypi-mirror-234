import click
import app.attendance as attendance
import app.personal_info_all_data as info

@click.command()
@click.argument('mode')
@click.argument('pth_out')
@click.option('--c')
def main(mode, pth_out, c):
    if mode == 'info':
        pth_in = click.prompt("\n--------------------------------------------------\nenter path to child and family data input folder")
        info.main(pth_in, pth_out)
    elif mode == 'attendance':
        pth_in = click.prompt("\n--------------------------------------------------\nenter path to attendance data input folder")
        pth_filter = click.prompt("\n--------------------------------------------------\nenter path to child and family data file")
        attendance.main(pth_in, pth_out, pth_filter, c)
    else:
        click.echo(f'{mode} is not a supported mode. Type --help for accepted commands.')