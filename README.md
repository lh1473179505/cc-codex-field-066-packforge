# packforge

把 YAML 站点适配包编译成抽取器，并在选择器失效时按包里的降级和熔断规则跑完本地夹具站。

```
python -m packforge site --port 8766 --skin v2
python -m packforge harvest --base http://127.0.0.1:8766 --pack fixtures/packs/catalog-v2.yaml --out <out> --checkpoint <ckpt>
python -m packforge verify --out <out> --expect fixtures/expected/items.json
```
