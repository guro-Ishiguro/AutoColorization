import pandas as pd
import os

df = pd.read_csv("leaderboard.csv")

df = df.sort_values("score", ascending=False).reset_index(drop=True)

if "rank" in df.columns:
    df = df.drop(columns=["rank"])

df = df.head(5)

df.insert(
    0,
    "rank",
    df["score"]
      .rank(method="min", ascending=False)  
      .astype(int)                          
      .values
)

table_html = df.to_html(
    index=False,
    classes="table table-striped",
    float_format="{:0.4f}".format,
    justify="left",
)

os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>コンペティション リーダーボード</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-4">
  <h1 class="mb-4">コンペティション リーダーボード</h1>
  {table_html}
</div>
</body>
</html>
""")

print("Generated docs/index.html")
