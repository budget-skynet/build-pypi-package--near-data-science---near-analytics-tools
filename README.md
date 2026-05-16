# near-data-science

A Python data analysis package for NEAR Protocol blockchain analytics and insights.

## Installation

```bash
pip install near-data-science
```

## Overview

`near-data-science` provides tools to analyze NEAR Protocol data including account information, block data, and network metrics. Extract, transform, and visualize blockchain data with ease.

## Quick Start

```python
from near_data_science import DataAnalyzer

# Initialize analyzer
analyzer = DataAnalyzer()

# Fetch account information
account_data = analyzer.fetch_account_info("example.near")

# Get latest block info
block_data = analyzer.fetch_block_info()

# Create DataFrame from multiple accounts
accounts = ["alice.near", "bob.near", "charlie.near"]
df = analyzer.create_account_dataframe(accounts)

# Aggregate data by metric
stats = analyzer.aggregate_by_metric("balance")

# Visualize account balances
analyzer.plot_account_balances(output_file="balances.png")
```

## Features

- **Account Analysis**: Retrieve and analyze individual account data
- **Block Information**: Query block details and metrics
- **Data Aggregation**: Aggregate metrics across multiple accounts
- **Visualization**: Generate charts for account balances and trends
- **DataFrame Export**: Convert blockchain data to pandas DataFrames

## Requirements

- Python 3.7+
- pandas
- requests

## License

MIT