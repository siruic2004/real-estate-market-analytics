## 1. data exploration
- csv存在重复列名，需检查原因（确实重复，还是错误使用一样的名字）
- 使用pd.Series(df.columns).value_counts()找出哪些列名重复

- 验证 PropertyType 与 PropertyType.1 内容完全一致,判定为数据源重复导出
- 假设所有月份文件都有同样问题(暂不逐月验证,后续合并时留意)