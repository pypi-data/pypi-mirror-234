
import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="certora-cli-alpha-shelly-cert3672astariabuild",
        version="20231007.21.31.820875",
        author="Certora",
        author_email="support@certora.com",
        description="Runner for the Certora Prover",
        long_description="Commit d80a18c. Build and Run scripts for executing the Certora Prover on Solidity smart contracts.",
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/certora-cli-alpha-shelly-cert3672astariabuild",
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=['click', 'json5', 'pycryptodome', 'requests', 'sly', 'tabulate', 'tqdm', 'StrEnum'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        entry_points={
            "console_scripts": [
                "certoraRun = certora_cli.certoraRun:entry_point",
                "certoraMutate = certora_cli.certoraMutate:gambit_entry_point",
                "certoraEqCheck = certora_cli.certoraEqCheck:equiv_check_entry_point"
            ]
        },
        python_requires='>=3.8',
    )
        