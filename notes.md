## 1. data exploration
- csv存在重复列名，需检查原因（确实重复，还是错误使用一样的名字）
- 使用pd.Series(df.columns).value_counts()找出哪些列名重复

- 验证 PropertyType 与 PropertyType.1 内容完全一致,判定为数据源重复导出
- 假设所有月份文件都有同样问题(暂不逐月验证,后续合并时留意)


## 2. data cleaning
- 清理完后剩下27个数据集
- 当选择Residential住宅时，出现了ResidentialIncome和ResidentialLease两个额外选项。由于这个任务专注【买卖】房子率，租赁不考虑在内，所以忽略这两行

## 3. 缺失值处理
- 删除缺失率 >90% 的列(listed 13 列,sold 17 列)
- 两份数据都 100% 全空的 8 列:TaxYear, TaxAnnualAmount, ElementarySchoolDistrict, MiddleOrJuniorSchoolDistrict, BusinessType, CoveredSpaces, AboveGradeFinishedArea, FireplacesTotal。
- 原因(假设,待对照 Trestle Metadata 核实):字段在 API 里存在但数据源没填,两份同时全空说明不是代码问题。
- 其中 BusinessType 只适用于商业房产,已筛选 Residential 故无值;税务、学区多不在公开数据流里;车位/面积/壁炉可能被 GarageSpaces、LivingArea、FireplaceYN 替代。
- 其余高缺失列(BelowGradeFinishedArea, CoBuyerAgentFirstName 等)只适用于少数房源,属正常。

## 4. 日期输入错误
- 日期先后检查:listed 违规 72/265/271 条,sold 58/240/261 条(均 <0.1%),属零星录入问题,仅标记不删除,特征工程时排除相关记录。
- 无效值标记:listed 面积≤0: 59 条、daysonmarket<0: 29 条;sold 面积≤0: 144 条、DOM<0:46 条、成交价≤0: 1 条;卧室/卫生间无负数。
- 坐标检查:listed 缺失 80,145(14.8%),sold 15,822(4.0%);经纬度为 0 分别 60/25;真正越界(排除缺失)约 287/84。缺坐标记录保留,仅不能用于点位地图,邮编热力图用 PostalCode。