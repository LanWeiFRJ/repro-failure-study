# 缺陷复现智能体失效行为研究

《大语言模型缺陷复现智能体失效行为的实证研究》的实验实例列表与统计分析脚本。

## 实例列表

`data/instances.csv`与`data/instances.json`包含最终100个实验实例。字段为原实验顺序`index`（从0开始）、`instance_id`、所属仓库`repo`、语言`repo_language`和缺陷版本提交`base_commit`。

实例来自SWE-Bench Pro，覆盖9个仓库：Python 45例、Go 32例、JavaScript/TypeScript 23例。`js`沿用源清单的语言代码。清单采用完成9例替换后的最终版本，不是替换前清单。

## 分析脚本与论文对应关系

| 脚本 | 论文对应内容 |
| --- | --- |
| `scripts/analyze_outcomes.py` | 第4.4节式(2)、式(3)，第5.3.1节复现率及差值，第5.3.2节表8与基线跨轮次更替率 |
| `scripts/bootstrap_table7.py` | 第5.3.1节以实例为聚类单位的配对Bootstrap与表7置信区间 |
| `scripts/summarize_failure_labels.py` | 第4.4节式(5)，第5.1—5.2节基线失效阶段、主模式及子模式分布 |
| `scripts/taxonomy.py` | 15种子模式、六种主模式及派生阶段之间的映射 |

脚本按论文使用的统计口径整理为可移植入口，并已用本地留存数据核验。它们从逐次结果和既有标签进行统计，不重新调用模型、运行实验或产生失效标签；原始轨迹解析和开放编码不在这些脚本的功能范围内。

## 使用方法

需要Python 3.10及以上和NumPy。实例列表及脚本公开；运行结果表和标签表不随仓库提供。统计脚本的输入字段如下，输入目录由`--data-dir`指定。

`run_outcomes.csv`：

```text
model,framework,round,profile,instance_id,resolved
```

模型为`DeepSeek-V4-Flash`、`DeepSeek-V4-Pro`和`GPT-5`；前两者分别与`OpenHands`、`PatchTwin`、`ReProAgent`组合，GPT-5仅与OpenHands组合。`profile`为`baseline`、`weak_understanding`、`weak_localization`、`weak_construction`或`weak_verification`。`resolved`只允许0或1。每个组合、实例、轮次和配置只能有一条记录，缺失项会报错，不按失败填补。

`round`按时间先后统一为1、2、3。OpenHands—Pro的历史r0、r1、r2对应1、2、3，其余组合沿用原1、2、3轮次。完整设计为100例×7组合×3轮×5配置，共10,500条结果。

`baseline_failure_labels.csv`（仅失效汇总脚本需要）：

```text
model,framework,round,profile,instance_id,fine_mode_code,parent_mode,primary_stage
```

该表每条基线失败运行恰有一个标签；`profile`应为`baseline`，子模式代码和主模式名称见`taxonomy.py`。阶段按主模式映射，不替代为独立阶段编码。脚本检查标签键与结果表中的全部基线失败一一对应，比例以相应组的失败数为分母。

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/analyze_outcomes.py --data-dir /path/to/inputs
python scripts/bootstrap_table7.py --data-dir /path/to/inputs
python scripts/summarize_failure_labels.py --data-dir /path/to/inputs
```

默认输出至`results/`，可用`--output-dir`另行指定。输入文件不会被修改。

Bootstrap以100个实例为聚类单位，有放回抽取100例，每例保留全部三轮和配置；合并分析还同步保留七个固定组合。重采样50,000次，随机种子20261003，取2.5%和97.5%分位数。基线跨轮次匹配使用(1,2)、(1,3)、(2,3)，方向以较早轮次为参照。统计结果均是描述性比较，不估计阶段能力的因果效应。

## 验证

```sh
python -m unittest discover -s tests -v
```

公开测试仅使用实例列表和程序生成的合成结果，不包含真实逐次运行结果。发布前另用本地留存数据验证了全部10,500条结果与1,525条基线标签的对应关系、论文计数，以及表7保存的28项置信区间。流程对应关系及验证结果见`VALIDATION.md`。

## 许可

`scripts/`与`tests/`代码采用MIT许可证。上游基准、仓库代码、任务正文和参考补丁不在本仓库重新分发；其使用仍遵循各自许可。
