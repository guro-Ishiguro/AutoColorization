import os
import sys
import argparse
import pandas as pd


def parse_args():
    p = argparse.ArgumentParser(
        description="Update leaderboard from submission summary"
    )
    p.add_argument(
        "-s",
        "--sub-file",
        required=True,
        help="Path to submission.csv (must contain date and score)",
    )
    p.add_argument(
        "-o",
        "--out-file",
        default="leaderboard.csv",
        help="Path to leaderboard.csv to update",
    )
    return p.parse_args()


def main():
    args = parse_args()

    df_sub = pd.read_csv(args.sub_file)
    if "score" not in df_sub.columns or "date" not in df_sub.columns:
        print(
            "Error: submission.csv must contain 'date' and 'score' columns",
            file=sys.stderr,
        )
        sys.exit(1)
    row = df_sub.iloc[0].to_dict()
    date = row["date"]
    score = row["score"]

    ref = os.environ.get("GITHUB_REF", "")
    branch = ref.split("/")[-1] if ref.startswith("refs/heads/") else "unknown"

    rec = {"name": branch, "date": date, "score": score}

    lb_path = args.out_file
    if os.path.exists(lb_path):
        lb = pd.read_csv(lb_path)
    else:
        lb = pd.DataFrame(columns=["name", "date", "score"])

    lb = lb[lb["name"] != branch]

    lb = pd.concat([lb, pd.DataFrame([rec])], ignore_index=True)

    lb.sort_values("score", ascending=False, inplace=True)

    if "rank" in lb.columns:
        lb = lb.drop(columns=["rank"])

    lb = lb.reset_index(drop=True)
    lb.insert(0, "rank", lb.index + 1)

    lb.to_csv(lb_path, index=False)

    print("=== Updated leaderboard entry ===")
    for k, v in rec.items():
        print(f"{k:8s}: {v}")
    print(f"\nLeaderboard written to: {lb_path}")


if __name__ == "__main__":
    main()
