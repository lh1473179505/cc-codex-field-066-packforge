# 适配包与夹具

`fixtures/packs/catalog-v1.yaml` 是旧格式（字段直接写选择器字符串）。`catalog-v2.yaml` 是新格式（字段为 primary/fallback，并带 circuit_breaker）。两份包都要能跑；v1 没有 fallback 字段时，按只有 primary 处理。

列表阶段的选择器相对于当前 item 节点（不要用整页第一个匹配去填所有卡片）。详情阶段相对于整页。

选择器语法：

- `css:<selector>` 取文本；`css:<selector> @attr` 取属性
- `xpath:<expr>` 取文本或节点值
- `regex:<pattern>` 在当前页面 HTML 上搜索，取第一个捕获组，匹配不到视为该字段缺失

## 降级与熔断

某个字段的 primary 取不到时，改用 fallback。若 fallback 也没有，该字段记为缺失。v2 包里 `circuit_breaker.max_consecutive_field_misses` 表示：连续这么多个 **item**（列表卡片或详情页）出现至少一个必填字段缺失后，停止继续翻页，并在 report 里写 `template_broken=true` 和 `stopped_at`。必填字段是 title、href（列表）以及 sku、price（详情）。熔断前已经抽到的行要保留。

夹具 `--skin v2` 的列表用 `div.product-row`，标题有时在 `span.nm`，有时只在 `b` 里；下一页链接在 `a[rel=next]` 而不是 `a.page-next`。详情 sku 有时只出现在正文 “SKU-XXXX” 文本里，没有 `span.code`。所以只走 primary 会很快熔断，必须用 fallback 才能收全。`--skin v1` 仍与 catalog-v1 的选择器完全吻合，用来确认旧包没有被改坏。

## 运行

先编译包再抓取。`--out/items.jsonl` 每件商品一行：`sku,title,price,detail_url`。`--out/report.json` 含 `pages_fetched`、`items`、`template_broken`、`stopped_at`（未熔断则为 null）。价格写成整数分：`$12.30` 或 `1230` 或 `data-price="1230"` 都要变成 1230。

`verify` 默认对照 v2 皮肤 + catalog-v2 包的收全结果。
