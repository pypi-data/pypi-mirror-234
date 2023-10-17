# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panama', 'panama.cli', 'panama.fluxes']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'corsikaio>=0.3,<0.4',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=2.0.0,<3.0.0',
 'particle>=0.21.0,<0.22.0',
 'scipy>=1.10.1,<2.0.0',
 'tables>=3.8.0,<4.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['panama = panama.cli:cli']}

setup_kwargs = {
    'name': 'corsika-panama',
    'version': '0.6.0',
    'description': 'PANdas And Multicore utils for corsikA7',
    'long_description': '# PAN*das* A*nd* M*ulticore utils for corsik*A*7*\n\n[Documentation ![Read the Docs](https://img.shields.io/readthedocs/panama?style=for-the-badge)](https://panama.readthedocs.io/en/latest/)\n\n[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/The-Ludwig/PANAMA/ci.yml?style=for-the-badge)](https://github.com/The-Ludwig/PANAMA/actions/workflows/ci.yml)\n[![Codecov](https://img.shields.io/codecov/c/github/The-Ludwig/PANAMA?label=test%20coverage&style=for-the-badge)](https://app.codecov.io/gh/The-Ludwig/PANAMA)\n[![PyPI](https://img.shields.io/pypi/v/corsika-panama?style=for-the-badge)](https://pypi.org/project/corsika-panama/)\n\n[![GitHub issues](https://img.shields.io/github/issues-raw/The-Ludwig/PANAMA?style=for-the-badge)](https://github.com/The-Ludwig/PANAMA/issues)\n[![GitHub](https://img.shields.io/github/license/The-Ludwig/PANAMA?style=for-the-badge)](https://github.com/The-Ludwig/PANAMA/blob/main/LICENSE)\n[![Codestyle](https://img.shields.io/badge/codesyle-Black-black.svg?style=for-the-badge)](https://github.com/psf/black)\n\nThanks [@Jean1995](https://github.com/Jean1995) for the silly naming idea.\n\n## Installation\n\n```\npip install corsika-panama\n```\n\n## Features\n\n### Run CORSIKA7 on multiple cores\n\nYou need to have [`CORSIKA7`](https://www.iap.kit.edu/corsika/79.php) installed to run this.\n\nRunning 100 showers on 4 cores with primary being proton:\n\n```sh\n$ panama run --corsika path/to/corsika7/executable -j4 ./tests/files/example_corsika.template\n83%|████████████████████████████████████████████████████▋        | 83.0/100 [00:13<00:02, 6.36shower/s]\nJobs should be nearly finished, now we wait for them to exit\nAll jobs terminated, cleanup now\n```\n\nInjecting 5 different primaries (Proton, Helium-4, Carbon-12, Silicon-28, Iron-54 roughly aligning with grouping in H3a) with each primary shower taking 10 jobs:\n\n```sh\n$ panama run --corsika corsika-77420/run/corsika77420Linux_SIBYLL_urqmd --jobs 10 --primary ""{2212: 500, 1000020040: 250, 1000060120: 50, 1000140280: 50, 1000260540: 50}"" ./tests/files/example_corsika.template\n...\n```\n\n### Convert CORSIKA7 DAT files to hdf5 files\n\n```sh\n$ panama hdf5 path/to/corsika/dat/files/DAT* output.hdf5\n```\n\nThe data is available under the `run_header` `event_header` and `particles` key.\n\n### Read CORSIKA7 DAT files to pandas dataframes\n\nExample: Calculate mean energy in the corsika files created in the example above:\n\n```\nIn [1]: import panama as pn\n\nIn [2]: run_header, event_header, particles = pn.read_DAT(glob="corsika_output/DAT*")\n100%|████████████████████████████████████████████████████████████| 2000/2000.0 [00:00<00:00, 10127.45it/s]\nIn [3]: particles["energy"].mean()\nOut[3]: 26525.611020413744\n```\n\n`run_header`, `event_header` and `particles` are all [pandas.DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) and can conveniently be used.\n\nIf `CORSIKA7` is compiled with the `EHIST` option, then the mother particles are automatically deleted, by default (this behaviour can be changed with`drop_mothers=False`).\nIf you want additional columns in the real particles storing the mother information use `mother_columns=True`.\n\n### Weighting to primary spectrum\n\nThis packages also provides facility to add a `weight` column to the dataframe, so you can look at corsika-output\nin physical flux in terms of $(\\mathrm{m^2} \\mathrm{s}\\ \\mathrm{sr}\\ \\mathrm{GeV})^{-1}$.\nUsing the example above, to get the whole physical flux in the complete simulated energy region:\n\n```\nIn [1]: import panama as pn\n\nIn [2]: run_header, event_header, particles = pn.read_DAT(glob="corsika_output/DAT*")\n100%|████████████████████████████████████████████████████████████| 2000/2000.0 [00:00<00:00, 10127.45it/s]\nIn [3]: pn.add_weight(run_header, event_header, particles)\n\nIn [4]: particles["weight"].sum()*(run_header["energy_max"]-run_header["energy_min"])\nOut[4]:\nrun_number\n1.0    1234.693481\n0.0    1234.693481\n3.0    1234.693481\n2.0    1234.693481\ndtype: float32\n\n```\n\nWhich is in units of $(\\mathrm{m^2}\\ \\mathrm{s}\\ \\mathrm{sr})^{-1}$. We get a result for each run, since\nin theory we could have different energy regions. Here, we do not, so the result is always equal.\n\nWeighting can be applied to different primaries, also, if they are known by the flux model.\n\n`add_weight` can also be applied to dataframes loaded in from hdf5 files produced with PANAMA.\n\nTODO: Better documentation of weighting (what is weighted, how, proton/neutrons, area...?)\n\n#### Notes:\n\nThis started a little while ago while I was looking into the `EHIST` option\nof corsika.\nI wanted a way of conveniently running CORSIKA7 on more than 1 core.\nI ended in the same place where most CORSIKA7 users end (see e.g. [fact-project/corsika_wrapper](https://github.com/fact-project/corsika_wrapper))\nand wrote a small wrapper.\n\nread_DAT made possible by [cta-observatory/pycorsikaio](https://github.com/cta-observatory/pycorsikaio).\n\n#### Pitfalls\n\n- The whole `run` folder of CORSIKA7 must be copied for each process, so very high parallel runs have high overhead\n- If you simulate to low energies, python can\'t seem to hold up with the corsika output to `stdin` and essentially slows down corsika this is still a bug in investigation #1\n\n## What this is not\n\nBug-free or stable\n',
    'author': 'Ludwig Neste',
    'author_email': 'ludwig.neste@tu-dortmund.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/The-Ludwig/PANAMA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
