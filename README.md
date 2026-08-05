# DataStory 日常工具集

用于 DataStory 日常数据查询、接口调用、数据校验和批处理的 Python 脚本仓库。

当前仓库仍保留原有目录，避免一次性移动脚本导致相对路径、配置文件和本地使用习惯失效。后续新增代码应按 [目录整理方案](docs/目录整理方案.md) 放置，旧代码再按业务逐步迁移。

## 快速开始

项目当前使用 Python 3.9。

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

多数脚本是独立入口。支持文件参数的脚本可以从仓库根目录执行，并显式传入输入文件：

```bash
python3 Elasticsearch查询/parse_output.py
python3 测试中功能/es查询转csv/es_query_to_csv.py \
  测试中功能/es查询转csv/query_config_sample.json
```

部分历史脚本仍直接读取当前目录下的 `accounts.json` 或输入文件，运行前需要先进入脚本目录：

```bash
cd ds_koy_tools/batch_reload_tasks
python3 batch_reload_task.py
```

迁移后的脚本应改为基于脚本文件定位资源，或通过命令行参数接收路径，不再依赖执行命令时所在的目录。

## 当前目录职责

| 目录 | 内容 | 后续归属 |
| --- | --- | --- |
| `Elasticsearch查询/` | ES 查询生成、解析和数据问题排查 | `scripts/elasticsearch/` |
| `PF_工具箱/` | 全量库、转链、重载、额度等稳定工具 | `scripts/pf/` |
| `api中心/` | 社媒 API 的独立调用脚本 | `scripts/social_api/` |
| `测试中功能/` | 尚在验证中的功能 | `scripts/experimental/` |
| `Temp/` | 一次性脚本和临时材料 | `scratch/` 或删除 |

完整的目标结构、迁移顺序和文件映射见 [docs/目录整理方案.md](docs/目录整理方案.md)。

## 维护约定

- 可复用的认证、HTTP 请求和文件处理逻辑放入 `src/datastory_tools/`，业务脚本只保留参数和流程编排。
- 账号、密码、Token 和服务地址使用环境变量或本地配置，仓库只提交 `.example` 模板。
- 输入样例放在 `data/samples/`；运行输入放在 `data/input/`；所有生成文件放在 `data/output/`。
- 新脚本使用英文 `snake_case` 文件名；面向使用者的文档和输出内容可以使用中文。
- 临时验证代码放入 `scratch/`，确认可复用后再迁入 `scripts/`，不再长期堆积在 `Temp/`。

## 安全提示

仓库历史中已有 `accounts.json`、`token_cache.json` 以及脚本内鉴权信息。新增忽略规则只能防止未跟踪文件被提交，不能保护已经进入 Git 历史的密钥。应尽快轮换仍然有效的凭据，并在迁移脚本时改为从环境变量或本地配置读取。
