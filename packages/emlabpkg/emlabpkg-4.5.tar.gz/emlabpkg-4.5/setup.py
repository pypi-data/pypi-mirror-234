from setuptools import setup, find_packages

setup(
    name="emlabpkg",
    version="4.5",
    summary="Univeristy of Cincinnati, Physics Department, Dr. Mikheev's Lab Package. Contains driver for NF-ZM2376 and edited version of sweep.",
    author="Sushant Padhye",
    author_email="padhyesm@mail.uc.edu",
    packages=find_packages(),
    install_requires=["qcodes", "gdspy"],
    description="Lab package for physics sweeps and LCR meter.",
    long_description="Package for the Superconducting Nanoelectronics Lab in the Physics department at the University of Cincinnati. The PI is Dr. Evgeny Mikheev, Assistant Professor."
)