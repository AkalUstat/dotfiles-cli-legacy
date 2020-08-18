import os
import click
import getpass

SYMLINK_EXCLUSION = ['readme.md', '.DS_Store', 'brew.sh', 'postinstall.sh', '.gitignore']
SYMLINK_DIR = os.path.expanduser('~')
@click.command()
@click.option('--username', default=getpass.getuser())
@click.option('--originDir', default="dotfiles")
def symlink(username):
    click.echo("testing")


def scanDotfiles(username, dotfilesDir="dotfiles"):
    dirFiles = os.scandir(str.format("/Users/{}/{}", username, dotfilesDir))
    for entry in dirFiles:
        if not entry.is_dir() and entry.name not in SYMLINK_EXCLUSION:
            try:
                os.symlink(entry.path, SYMLINK_DIR)
            except FileExistsError:
                click.echo(click.style(f"{entry.name} symlink exists at root",  blink=True, fg="green"))

if __name__=="__main__":
    scanDotfiles("akal-ustatsingh", ".dotfiles")
