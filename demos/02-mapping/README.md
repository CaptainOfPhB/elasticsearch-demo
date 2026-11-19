# 02-mapping

弄清 `text` 和 `keyword` 的分工即可。

## 目标

- `text`：分词后做全文检索（`match`）
- `keyword`：不分词，做精确过滤 / 聚合（`term`、`terms` agg）
- multi-field：`title` + `title.keyword`

## 运行

```bash
# Dev Tools：粘贴 console.http
python demos/02-mapping/main.py
```

## 预期

- `match title=键盘` 能命中
- `term brand=KeyChron` 能命中
- 对 `title` 直接 `term` 全文通常为 0；对 `title.keyword` 则为 1
