"""
utility for latex.
"""
from distutils.spawn import find_executable
import os
import subprocess
import matplotlib.pyplot as plt

latex_cmd = "pdftex"


# ==================================================
def check_latex_installed():
    """
    check if LaTeX is installed.

    Returns:
        bool: True if installed.
    """
    return find_executable(latex_cmd)


# ==================================================
def latex_version():
    """
    LaTeX version.

    Returns:
        str: LaTeX version.
    """
    completedProcess = subprocess.run([latex_cmd, "--version"], stdout=subprocess.PIPE)
    ver = completedProcess.stdout.decode()
    ver = ver[: ver.find("\n")]
    return ver


# ==================================================
def latex_setting(mode):
    """
    set LaTeX mode.

    Args:
        mode (str): setting mode, "standard/times/pgf".
    """
    # see, matplotlib: High Quality Vector Graphics for LaTeX Paper
    # https://www.alanshawn.com/tech/2021/03/27/matplotlib-latex-style.html
    if mode == "standard":

        plt.rcParams.update(
            {
                "text.usetex": True,
                "mathtext.fontset": "stix",
                "text.latex.preamble": r"\usepackage{physics}\usepackage[varg]{txfonts}",
                "svg.fonttype": "none",
            }
        )
    elif mode == "times":
        import subprocess
        import matplotlib.font_manager as font_manager

        kpse_cp = subprocess.run(["kpsewhich", "-var-value", "TEXMFDIST"], capture_output=True, check=True)
        font_loc1 = os.path.join(kpse_cp.stdout.decode("utf8").strip(), "fonts", "opentype", "public", "tex-gyre")
        font_dirs = [font_loc1]
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)
        plt.rcParams.update(
            {
                "font.family": "TeX Gyre Termes",
                "mathtext.fontset": "stix",
                "text.usetex": True,
                "text.latex.preamble": r"\usepackage{physics}",
                "svg.fonttype": "none",
            }
        )
    elif mode == "pgf":  # some problem is reported.
        import matplotlib

        # switch to pgf backend
        matplotlib.use("pgf")
        plt.rcParams.update(
            {
                "font.family": "serif",
                "text.usetex": True,
                "pgf.rcfonts": False,
                "pgf.texsystem": "pdflatex",  # default is xetex
                "pgf.preamble": [r"\usepackage[T1]{fontenc}", r"\usepackage{mathpazo}"],
                "svg.fonttype": "none",
            }
        )
