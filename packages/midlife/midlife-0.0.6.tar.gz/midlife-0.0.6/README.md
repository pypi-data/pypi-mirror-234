# midlife
[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/2444117/tree)

This is under review.

midlife is a PyPI application for evaluating and visualzing the impact of COVID-19 on mortality of midlife in five age groups from 40 to 64 years old.

CDC dataset is used for this study:
https://data.cdc.gov/api/views/chcz-j2du/rows.csv


# How to install midlife
$ pip install midlife

# How to run midlife

midlife needs the degree of polynomial regression and sex: F or M. 
The following example can show the 3rd degree of polynomial and Female.

$ midlife 3 F

<img src='https://github.com/ytakefuji/midlife/raw/main/Fmidlife.png' width=640 height=480>
