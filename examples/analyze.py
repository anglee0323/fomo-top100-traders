# /// script
# requires-python = ">=3.11"
# dependencies = ["duckdb>=1.4,<2", "pandas>=2.2", "pyarrow>=18", "matplotlib>=3.9", "scikit-learn>=1.5"]
# ///
"""Create descriptive tables, an activity chart and a numeric ML matrix."""
import argparse
import json
from pathlib import Path

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def literal(path):
    return "'" + str(path).replace("'", "''") + "'"


def build(root):
    metadata = json.loads((root / "metadata.json").read_text())
    accounts = json.loads((root / "accounts.json").read_text())
    db = duckdb.connect()
    db.execute("SET memory_limit='1GB'")
    if metadata["dataset"] == "gmgn":
        db.execute(f"CREATE VIEW activity AS SELECT account_id, rank, handle, wallet, chain, tx_hash, TRY_CAST(timestamp_utc AS TIMESTAMPTZ) AS ts, event_type FROM read_parquet({literal(root / 'events.parquet')})")
        members = pd.DataFrame(accounts["accounts"])[["account_id", "rank", "wallet", "chain"]]
        observed = db.execute("""SELECT account_id, rank, wallet, chain, COUNT(*)::BIGINT AS event_count,
            COUNT(DISTINCT tx_hash)::BIGINT AS transaction_count,
            COUNT(*) FILTER (WHERE event_type='buy')::BIGINT AS buy_observation_count,
            COUNT(*) FILTER (WHERE event_type='sell')::BIGINT AS sell_observation_count,
            COUNT(DISTINCT CAST(ts AS DATE))::BIGINT AS active_days,
            MIN(ts) AS first_seen_utc, MAX(ts) AS last_seen_utc FROM activity GROUP BY ALL""").df()
        features = members.merge(observed, on=["account_id", "rank", "wallet", "chain"], how="left", validate="one_to_one")
    else:
        db.execute(f"""CREATE VIEW activity AS
            SELECT account_id, rank, handle, wallet, 'sol' AS chain, tx_hash,
                TRY_CAST(timestamp_utc AS TIMESTAMPTZ) AS ts FROM read_parquet({literal(root / 'solana/transactions.parquet')})
            UNION ALL SELECT 'original_fomo:' || rank::VARCHAR || ':' || handle AS account_id,
                rank, handle, wallet, CASE chain_id WHEN 1 THEN 'eth' WHEN 56 THEN 'bsc'
                WHEN 8453 THEN 'base' WHEN 4663 THEN 'robinhood' ELSE chain_id::VARCHAR END,
                tx_hash, TRY_CAST(timestamp_utc AS TIMESTAMPTZ) FROM read_parquet({literal(root / 'evm_transactions.parquet')})""")
        rows = []
        for a in accounts:
            account_id = f"original_fomo:{a['rank']}:{a['handle']}"
            if a.get("sol_address"):
                rows.append(dict(account_id=account_id, rank=a["rank"], wallet=a["sol_address"], chain="sol"))
            for chain in ("eth", "bsc", "base", "robinhood"):
                rows.append(dict(account_id=account_id, rank=a["rank"], wallet=a["evm_address"], chain=chain))
        observed = db.execute("""SELECT account_id, rank, wallet, chain, COUNT(*)::BIGINT AS event_count,
            COUNT(DISTINCT tx_hash)::BIGINT AS transaction_count,
            COUNT(DISTINCT CAST(ts AS DATE))::BIGINT AS active_days,
            MIN(ts) AS first_seen_utc, MAX(ts) AS last_seen_utc FROM activity GROUP BY ALL""").df()
        members = pd.concat([pd.DataFrame(rows), observed[["account_id", "rank", "wallet", "chain"]]], ignore_index=True).drop_duplicates()
        features = members.merge(observed, on=["account_id", "rank", "wallet", "chain"], how="left", validate="one_to_one")
    counts = [c for c in features if c.endswith("_count") or c == "active_days"]
    features[counts] = features[counts].fillna(0).astype("int64")
    features["has_observed_activity"] = features["event_count"] > 0
    features = features.sort_values(["chain", "rank"]).reset_index(drop=True)
    daily = db.execute("""SELECT CAST(ts AS DATE) AS date_utc, chain, COUNT(*)::BIGINT AS observation_count,
        COUNT(DISTINCT tx_hash)::BIGINT AS distinct_transaction_hashes FROM activity
        WHERE ts IS NOT NULL GROUP BY ALL ORDER BY 1, 2""").df()
    db.close()
    return features, daily


def main(root, output):
    if output.exists():
        raise ValueError("Choose a new output directory")
    features, daily = build(root)
    output.mkdir(parents=True)
    features.to_parquet(output / "account_features.parquet", index=False)
    features.to_csv(output / "account_features.csv", index=False)
    daily.to_csv(output / "daily_activity.csv", index=False)
    columns = ["event_count", "transaction_count", "active_days"]
    matrix = StandardScaler().fit_transform(np.log1p(features[columns].to_numpy(dtype=float)))
    if not np.isfinite(matrix).all():
        raise ValueError("ML feature matrix contains nonfinite values")
    np.save(output / "features.npy", matrix, allow_pickle=False)
    (output / "feature_columns.json").write_text(json.dumps(dict(columns=columns,
        transformation="log1p then StandardScaler; rows follow account_features.parquet",
        purpose="descriptive snapshot features; no prediction target supplied"), indent=2) + "\n")
    chart = daily.pivot(index="date_utc", columns="chain", values="observation_count").fillna(0)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    chart.plot(ax=ax, linewidth=1)
    ax.set(xlabel="Date (UTC)", ylabel="Source observations", title="Observed activity by chain")
    ax.set_yscale("symlog", linthresh=1)
    ax.set_ylim(bottom=0)
    ax.legend(title="Chain", loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    fig.tight_layout(); fig.savefig(output / "activity_by_chain.png", dpi=160); plt.close(fig)
    print(json.dumps(dict(feature_rows=len(features), daily_rows=len(daily), ml_shape=list(matrix.shape), output=str(output))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parents[1] / "dataset")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); main(args.dataset, args.output)
