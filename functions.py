import os
import click

SYMLINK_EXCLUSION = ['readme.md', '.DS_Store', 'brew.sh', 'postinstall.sh', '.gitignore']
SYMLINK_DIR = os.path.expanduser('~')

@click.command()
@click.option('--origindir', default=".dotfiles")
def symlink( origindir):
    zsh(origindir)
    neovim(origindir)
    run_scripts(origindir)
    run_homebrew(origindir)

def neovim(dotfilesDir):
    click.echo(click.style("Starting Neovim symlink!", fg="green"))
    neovim_config_dir = f"{SYMLINK_DIR}/.config/nvim"
    neovim_origin_dir = f"{SYMLINK_DIR}/{dotfilesDir}/.config/nvim"
    try:
        os.mkdir(f"{SYMLINK_DIR}/.config")
        os.mkdir(neovim_config_dir)
    except FileExistsError:
        click.echo(click.style(".config/nvim already exists in the root directory, continuing", fg="yellow"))

    dirFiles = os.scandir(neovim_origin_dir)

    for config_file in dirFiles: 
        try:
            os.symlink(config_file.path, f"{neovim_config_dir}/{config_file.name}")
            click.echo(click.style(f"{config_file.name} symlinking success!" , fg="white"))
        except FileExistsError: 
            click.echo(click.style(f"{config_file.name} symlink exists at {neovim_config_dir} ",  fg="yellow"))

    click.echo(click.style(f"neovim symlinking success!",  fg="green"))
    click.echo("")

def zsh( dotfilesDir):
    click.echo(click.style("Starting terminal config symlink!...", fg="green"))
    dirFiles = os.scandir(f"{SYMLINK_DIR}/{dotfilesDir}/zsh")
    for entry in dirFiles:
        if not entry.is_dir() and entry.name not in SYMLINK_EXCLUSION:
            try:
                os.symlink(entry.path, f"{SYMLINK_DIR}/{entry.name}")
                click.echo(click.style(f"{entry.name} symlinking success!",  fg="white"))
            except FileExistsError:
                click.echo(click.style(f"{entry.name} symlink exists at {SYMLINK_DIR}",  fg="yellow"))

    click.echo(click.style("Terminal config symlinked!",  fg="green"))
    click.echo("")

def run_scripts(dotfilesDir):
    scripts_dir = f"{SYMLINK_DIR}/{dotfilesDir}/scripts"

    click.echo(click.style("Starting scripts...", fg="green"))
    scripts = os.scandir(scripts_dir)

    for script in scripts:
        print(f"running script: {script.name}")
        os.system(f"sh {script.path}")

    click.echo(click.style("Finished execting scripts",  fg="green"))

def run_homebrew(dotfilesDir):
    brew_script_dir = f"{SYMLINK_DIR}/{dotfilesDir}/brew/brew.sh"
    click.echo(click.style("Starting brew installs...", fg="green"))
    os.system(f"sh {brew_script_dir}")
    click.echo(click.style("done", fg="green"))

if __name__=="__main__":
    symlink()
