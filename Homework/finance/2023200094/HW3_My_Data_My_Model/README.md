## 1. 文件结构

```
.
├── Data/
│   ├── Tianjin_Quanyechang_esf_data.xlsx  (及其他原始数据)
│   ├── Tianjin_Quanyechang_zu_data.xlsx  (及其他原始数据)
│   ├── cleaned_full_data.parquet   (清洗合并后的主数据)
│   └── OLS_predicted_data.parquet  (含模型预测值的数据)
│
├── Model/
│   ├── data_preprocessing.ipynb
│   ├── descriptive_and_economic_analysis.ipynb
│   ├── simple_regression_model.ipynb
│   └── advanced_model.ipynb
│
├── figure/
│   ├── FigureA.png
│   ├── FigureB.png
│   ├── FigureC.png
│
└── README.md
```

### **各模块主要内容:**

* **`Data/`**: 存放所有数据文件。包括从“房天下”网站爬取的原始 `.xlsx` 文件，以及经过处理、合并后的 `.parquet` 中间文件和结果文件。
* **`Model/`**: 存放所有的 Jupyter Notebook 分析代码，按数字顺序执行即可复现整个分析流程。
    * `01_...`: **数据整合与清洗**。将所有分散的Excel文件合并，添加地区和类型标签，并计算租金单价。
    * `02_...`: **描述性分析**。对各地区单价进行统计描述，通过箱线图识别离群值，并基于原始数据计算租售比。
    * `03_...`: **回归建模**。构建了多个OLS回归模型，包括简单线性模型、含地区虚拟变量的模型，并对整个数据集进行交叉预测。
    * `04_...`: **特征工程与模型改进**。通过可视化发现非线性关系，引入面积的二次项及地区交互项来优化模型，并使用`Stargazer`对比展示了模型改进的效果。
* **`figure/`**: 存放所有由代码生成的可视化图表，如箱线图、回归图、核密度图等。

---

## 3. 使用的技术与工具

* **数据采集**: `Selenium`
* **数据处理与分析**: `Pandas`, `NumPy`
* **统计建模**: `statsmodels`
* **数据可视化**: `Matplotlib`, `Seaborn`
* **报告生成**: `Stargazer` for Python

    每个文件都会生成相应的中间数据或图表，并被后续文件所调用。
