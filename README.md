# ssh-config

解析 SSH 客户端配置：Host 通配与否定、关键字大小写归一、首值优先、Include 展开，以及按主机与关键字查找。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m sshconf --sample=first
python3 -m sshconf --sample=negate
python3 -m sshconf --sample=case
python3 -m sshconf --sample=include
python3 -m sshconf --sample=work
```

## 口径

- **块**：`Host 模式...` 开一个块；关键字与值按空白切分，关键字大小写不敏感。
- **模式**：`*` 与 `?` 通配；`!模式` 表示否定，命中的块里只要有一个否定模式匹配就不算命中。
- **首值优先**：同一个关键字在多个命中的块里出现时，取最靠前那个值；同一块内重复出现也取第一个。
- **Include**：`Include 路径` 把另一份配置插到当前位置展开。
- **查找**：按主机与关键字查找走索引，不逐块比较。

## 不变量

- 取到的值来自第一个命中且设置了该关键字的块。
- 被否定模式排除的块不参与取值。
- `scanned` 不随块数乘查询次数放大：八百个块查八百次的 `scanned` 不超过 6000。

## 输出契约

`get(host, key)` 返回取值或空串。场景打印一行 JSON。
`--sample=work` 打印 `{"blocks": N, "scanned": N}`。
