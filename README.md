# FOMO Top 100 Traders: Multichain Intelligence Dataset

[English](README.md) | [简体中文](README_CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Snapshot: 2026--10--09](https://img.shields.io/badge/snapshot-2026--10--09_15%3A45_UTC-blue.svg)](data/)

Open-source historical dataset covering the **Top 100+ traders** on the FOMO platform (`fomo.family`).

This repository is a **static historical snapshot captured on 2026-10-09 15:45:23 UTC**. It provides raw data files for quantitative research, backtesting, and machine learning without subjective conclusions or external runtime dependencies.

Includes **unmasked EVM & Solana wallet addresses**, multi-chain asset balances across **6 chains ($90M+ total capital)**, token-level holdings, 7d/30d performance metrics, granular DEX swap logs, and a **pre-normalized feature matrix**.

---

## Dataset Scope & Snapshot Info

* **Snapshot Timestamp**: `2026-10-09 15:45:23 UTC`
* **Data State**: Immutable offline archive
* **Tracked Entities**: 134 Trader Profiles (Top 97 net-worth whales + 37 momentum leaders)
* **Total Tracked Assets**: $90,042,918 USD across 6 chains (Robinhood, Solana, BSC, Base, Ethereum, Arc)
* **Address Mapping**: Dual-chain mapping (EVM hex `0x...` and Solana base58)

---

## Repository Structure

```
fomo-top100-traders/
├── README.md                      # English documentation (this file)
├── README_CN.md                   # Chinese documentation (中文说明)
├── pyproject.toml                 # Project metadata
├── LICENSE                        # MIT License
└── data/
    ├── traders_profiles.csv       # Tabular profiles (rank, handles, unmasked wallets, balances, PnL)
    ├── traders_profiles.json      # Structured nested JSON of all trader profiles
    ├── tokens_holdings.csv        # Token holdings (trader, symbol, chain, USD value, co-holders)
    ├── tokens_holdings.json       # Structured token holdings list
    ├── ml_features.csv            # Pre-normalized feature matrix ready for modeling
    ├── shared_tokens_graph.json   # Inter-trader co-holding network
    └── sample_dex_swaps/          # Sample on-chain DEX Buy/Sell executions
        ├── dumbcrayoneater_swaps.json  # 500 historical DEX swaps on Base & Solana
        └── unipcs_swaps.json           # DEX swap execution history
```

---

## Data Schema & Field Dictionary

### 1. `data/traders_profiles.csv`

| Column | Type | Description |
| :--- | :--- | :--- |
| `rank` | Integer | Overall wealth rank (1 to 134) |
| `handle` | String | Primary trader identifier |
| `name` | String | Display name |
| `x_username` | String | Associated X (Twitter) handle |
| `address_status` | String | `unmasked` or `masked` |
| `evm_address` | String | Unmasked EVM wallet (Robinhood, Base, BSC, Ethereum) |
| `sol_address` | String | Unmasked Solana native wallet (base58) |
| `total_usd` | Float | Verified multichain portfolio value in USD |
| `primary_chain` | String | Dominant chain by asset allocation (`hood`, `solana`, `bsc`, etc.) |
| `evm_usd` | Float | Aggregate asset value on EVM chains |
| `sol_usd` | Float | Asset value on Solana |
| `hood_usd` | Float | Asset value on Robinhood chain |
| `solana_usd` | Float | Asset value on Solana |
| `bsc_usd` | Float | Asset value on Binance Smart Chain |
| `base_usd` | Float | Asset value on Base |
| `ethereum_usd` | Float | Asset value on Ethereum |
| `arc_usd` | Float | Asset value on Arc |
| `active_chains_count` | Integer | Number of chains with balance > $10 |
| `tokens_count` | Integer | Number of major token positions |
| `top_token_symbol` | String | Symbol of largest token holding |
| `top_token_usd` | Float | USD value of largest token holding |
| `top_token_concentration_pct` | Float | Largest position as percentage of portfolio |
| `pnl_24h_usd` | Float | 24-hour PnL |
| `pnl_7d_usd` | Float | 7-day PnL |
| `pnl_30d_usd` | Float | 30-day PnL |
| `volume_usd` | Float | Trading volume |
| `trades_count` | Integer | Trade count |
| `avg_swap_usd` | Float | Average swap size in USD |
| `followers_x` | Integer | Follower count on X |
| `archetype` | String | Rule-based profile tag |
| `hhi_concentration` | Float | Herfindahl-Hirschman concentration index |
| `chain_entropy` | Float | Shannon entropy across chains |
| `network_co_holding_score` | Float | Mean co-holding degree with other top traders |

### 2. `data/tokens_holdings.csv`

| Column | Type | Description |
| :--- | :--- | :--- |
| `trader_handle` | String | Trader handle reference |
| `symbol` | String | Token symbol |
| `chain` | String | Deployment chain (`hood`, `solana`, `bsc`, `base`, `ethereum`, `arc`) |
| `usd_value` | Float | USD valuation at snapshot time |
| `portfolio_share_pct` | Float | Percentage of trader's portfolio |
| `co_holders_count` | Integer | Number of top traders simultaneously holding this token |

### 3. `data/ml_features.csv`

Normalized feature table ($N=134$, 17 columns) including log portfolio scale (`log_total_usd`), allocation ratios (`pct_hood`, `pct_sol`, `pct_bsc`, `pct_base`, `pct_eth`, `pct_arc`, `pct_evm_total`), concentration metrics (`hhi_concentration`), and cross-chain entropy (`chain_entropy`).

---

## Loading Data in Python

```python
import pandas as pd

# Load trader profiles
traders = pd.read_csv("data/traders_profiles.csv")
print(f"Loaded {len(traders)} traders. Total tracked capital: ${traders['total_usd'].sum():,.2f}")

# Load token holdings
holdings = pd.read_csv("data/tokens_holdings.csv")
print(f"Loaded {len(holdings)} token positions.")

# Load machine learning features
features = pd.read_csv("data/ml_features.csv")
print(f"Feature matrix shape: {features.shape}")
```

---

## License & Disclaimer

This dataset is released under the [MIT License](LICENSE). 

This repository is strictly intended for academic, data science, and quantitative research purposes. It does not constitute financial, investment, or trading advice.
