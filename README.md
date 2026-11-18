# 校园供餐分量调整与采购核算

共用厨房的领餐、配方、抽称和采购承诺。示例为称重记账单位，不含个人资料。
这里的记录全部为合成资料。日期按当地日历解释，未附时区的时间使用东八区。

## 交接资料

CSV 使用 UTF-8 和逗号分隔。值留空表示这条资料未给出该字段，不等于零。
`data/schema.json` 登记表头与跨表编号关系；`data/policy.json` 保存本期业务配置。

- `data/menu_runs.csv`：每次出餐按配方可食部称重，prepared 为加工后可食公斤，served 为实际领出份数。 字段：`batch`, `school`, `date`, `menu`, `grams`, `prepared`, `served`, `day_kind`。
- `data/serving_split.csv`：班级与学段的实际领餐，空的公斤字段表示只确认了份数。更精细分配由后续签认单提供。 字段：`claim`, `batch`, `stage`, `class`, `served`, `kg_min`, `kg_max`, `received`。
- `data/waste_weighs.csv`：source 为 kitchen、plate 或 mixed。classes 为空表示不能定位到班；空重量表示未完成计划，不能按零。 字段：`weigh`, `batch`, `source`, `classes`, `kg`, `portions`, `invitation`, `state`。
- `data/nutrition.csv`：学段约定的可食供给下界；允许替代的菜单分号分隔。 字段：`stage`, `minimum_grams`, `menus`。
- `data/recipes.csv`：同种原料可服务多个菜单，grams_raw_per_serving 为名义原料用量。 字段：`menu`, `ingredient`, `grams_raw_per_serving`, `usable_fraction`。
- `data/purchases.csv`：stock 为可用库存，arrival_short 为较计划短交的可证数量，locked 为不可改订货。 字段：`record`, `site`, `ingredient`, `kind`, `kg`, `unit_price`, `min_increment`, `date`。
- `data/next_service.csv`：同一 site 对应共用采购；同站同一期预算值相同并且只计一次。 字段：`plan`, `site`, `stage`, `portions`, `menus`, `budget_yuan`。

## 资料校验

使用 Python 3.11.2 标准库，不需要安装扩展包。资料入口只核查交接格式，不计算业务结果。

```sh
python3 inspect_inputs.py
python3 -m unittest discover -s tests -v
```
