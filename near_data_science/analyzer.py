#!/usr/bin/env python3
"""
near-data-science: NEAR Blockchain Analytics Tools
Package for fetching, analyzing, and visualizing NEAR blockchain data.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


class DataAnalyzer:
    """Main analyzer class for NEAR blockchain data"""
    
    def __init__(self, rpc_url: str = "https://rpc.mainnet.near.org"):
        self.rpc_url = rpc_url
        self.data = pd.DataFrame()
        
    def fetch_account_info(self, account_id: str) -> Dict:
        """Fetch account information from NEAR RPC"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": "dontcare",
                "method": "query",
                "params": {
                    "request_type": "view_account",
                    "finality": "final",
                    "account_id": account_id
                }
            }
            response = requests.post(self.rpc_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("result", {})
        except Exception as e:
            print(f"Error fetching account {account_id}: {e}")
            return {}
    
    def fetch_block_info(self, block_id: str = "final") -> Dict:
        """Fetch block information"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": "dontcare",
                "method": "block",
                "params": {"finality": block_id}
            }
            response = requests.post(self.rpc_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("result", {})
        except Exception as e:
            print(f"Error fetching block {block_id}: {e}")
            return {}
    
    def create_account_dataframe(self, accounts: List[str]) -> pd.DataFrame:
        """Create DataFrame from multiple accounts"""
        data = []
        for account in accounts:
            info = self.fetch_account_info(account)
            if info:
                data.append({
                    "account_id": account,
                    "amount": float(info.get("amount", 0)) / 1e24,
                    "locked": float(info.get("locked", 0)) / 1e24,
                    "code_hash": info.get("code_hash", "N/A"),
                    "storage_usage": info.get("storage_usage", 0),
                    "timestamp": datetime.now()
                })
        self.data = pd.DataFrame(data)
        return self.data
    
    def aggregate_by_metric(self, metric: str) -> pd.Series:
        """Aggregate data by metric"""
        if self.data.empty:
            return pd.Series(dtype=float)
        return self.data[metric].describe()
    
    def plot_account_balances(self, output_file: str = "account_balances.png"):
        """Create bar chart of account balances"""
        if self.data.empty:
            print("No data to plot")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(self.data["account_id"], self.data["amount"], color="steelblue")
        ax.set_xlabel("Account ID")
        ax.set_ylabel("Balance (NEAR)")
        ax.set_title("NEAR Account Balances")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_file, dpi=100)
        print(f"Chart saved to {output_file}")
        plt.close()
    
    def plot_storage_usage(self, output_file: str = "storage_usage.png"):
        """Create visualization of storage usage"""
        if self.data.empty:
            print("No data to plot")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(self.data["amount"], self.data["storage_usage"], 
                   color="coral", s=100, alpha=0.7)
        ax.set_xlabel("Balance (NEAR)")
        ax.set_ylabel("Storage Usage (bytes)")
        ax.set_title("NEAR Account: Balance vs Storage Usage")
        plt.tight_layout()
        plt.savefig(output_file, dpi=100)
        print(f"Chart saved to {output_file}")
        plt.close()
    
    def to_csv(self, filename: str = "near_accounts.csv"):
        """Export data to CSV"""
        if self.data.empty:
            print("No data to export")
            return
        self.data.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
    
    def get_statistics(self) -> Dict:
        """Get statistical summary"""
        if self.data.empty:
            return {}
        return {
            "total_accounts": len(self.data),
            "total_balance": float(self.data["amount"].sum()),
            "avg_balance": float(self.data["amount"].mean()),
            "max_balance": float(self.data["amount"].max()),
            "min_balance": float(self.data["amount"].min()),
            "total_storage": int(self.data["storage_usage"].sum()),
            "avg_storage": float(self.data["storage_usage"].mean())
        }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="NEAR Blockchain Data Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  near-data-science analyze alice.near bob.near --plot
  near-data-science stats alice.near --export data.csv
  near-data-science block
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    analyze_parser = subparsers.add_parser("analyze", help="Analyze accounts")
    analyze_parser.add_argument("accounts", nargs="+", help="Account IDs")
    analyze_parser.add_argument("--plot", action="store_true", help="Create visualizations")
    analyze_parser.add_argument("--export", type=str, help="Export to CSV file")
    
    stats_parser = subparsers.add_parser("stats", help="Get statistics")
    stats_parser.add_argument("accounts", nargs="+", help="Account IDs")
    stats_parser.add_argument("--export", type=str, help="Export to CSV file")
    
    block_parser = subparsers.add_parser("block", help="Get latest block info")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        analyzer = DataAnalyzer()
        analyzer.create_account_dataframe(args.accounts)
        print(analyzer.data.to_string())
        if args.plot:
            analyzer.plot_account_balances()
            analyzer.plot_storage_usage()
        if args.export:
            analyzer.to_csv(args.export)
    
    elif args.command == "stats":
        analyzer = DataAnalyzer()
        analyzer.create_account_dataframe(args.accounts)
        stats = analyzer.get_statistics()
        print(json.dumps(stats, indent=2))
        if args.export:
            analyzer.to_csv(args.export)
    
    elif args.command == "block":
        analyzer = DataAnalyzer()
        block = analyzer.fetch_block_info()
        if block:
            print(f"Block Height: {block.get('header', {}).get('height')}")
            print(f"Block Hash: {block.get('header', {}).get('hash')}")
            print(f"Timestamp: {block.get('header', {}).get('timestamp')}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()