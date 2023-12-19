# North Dakota Secretary of State Crawler

This project explores the busines relationships in the North Dakota Secretary of State search engine.

It can be found here https://firststop.sos.nd.gov/search/business

There are 3 components
  - A crawler
  - A plotter
  - An problem exploration guide

# Running

First create a conda enviornment and install the required packages.
```
conda create --name ndcrawlenv
conda activate ndcrawlenv
conda install --file package-list.txt --channel conda-forge
```

Within the root folder the crawler can be run with the following starting char paramter of X.

```
scrapy crawl names -O names.jsonl -a starting_char=X
```

The crawler outputs jsonlines each containing entities and the name of the parent company for debugging purposes.

The plotter can be run using the followng command.

```
python plot_connected_components.py
```

The problem_exploration.ipynb is a walkthrough of the thought process used to solve the problem.
A few interesting topics came up.

The data requested in located in names.jsonl and the plot is located in names.png.