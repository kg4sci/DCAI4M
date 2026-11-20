# 时间线总览图 · 画图 Prompt

配套文档：`summary/timeline_survey.tex`（AI赋能材料领域数据集建设时间线综述）
数据依据：`summary/timeline_digest.md`（104 条数据集条目，1965–2026，5 类任务）

---

## v1 主 Prompt（单面板，英文，已被 v2 取代）

```text
Create a publication-quality scientific timeline infographic titled "Dataset Construction for AI-Enabled Materials Science, 1965–2026". Wide 16:9 layout, flat vector style, clean white background, thin light-grey gridlines, muted academic color palette, sans-serif English labels, Nature-journal figure aesthetics, no photorealism, no 3D effects, high legibility.

Horizontal time axis from 1965 to 2026 with decade ticks. Five horizontal swimlanes, top to bottom, each with a colored left label: (1) Prediction & Identification (blue), (2) Generation & Inverse Design (teal), (3) Synthesis Route & Step Planning (purple), (4) Optimization & Experiment Recommendation (orange), (5) AI Model Evaluation (red).

Six softly shaded era bands across the top: "Experimental Crystallography 1965–2010", "High-Throughput DFT 2011–2016", "Domain Expansion 2017–2019", "Scale-up & Closed-Loop Labs 2020–2022", "Foundation-Model Data 2023–2024", "Agents & Deep Evaluation 2025–2026".

Place small labeled milestone nodes at their years in the matching lanes: CSD 1965, ICSD 1978, PolyInfo 2000, Materials Project 2011, AFLOW / COD / hMOF 2012, OQMD 2013, QM9 2014, C2DB 2018, GuacaMol 2019, OC20 / Matbench / ZINC20 / MOSES 2020, Olympus 2021, Alexandria 2022, GNoME 2023 (2.2M structures), MPtrj 2023, OMat24 2024 (118M configurations), PolyTAO 2024, Alex-MP-20 / MatterGen 2025, OMol25 2025 (100M DFT), PhononBench 2026, RECOB 2026, MADE 2026, MOCLIP 2026. The planning lane stays sparse (only Materials Project 2013, ChemGymRL 2023, CICERO 2026, Material Discovery Bench 2026) to show the data gap.

Node shape encodes data origin: circle = experimental data, square = simulation data, diamond = hybrid data; include a small legend. Draw thin dotted grey connector lines showing cross-task reuse of Materials Project, QM9, OC20 and GNoME across multiple lanes.

Bottom ribbon: a logarithmic data-scale growth curve rising from 10^3 (early experiments) to 10^8 (OMat24 / OMol25), annotated "3 → 8 orders of magnitude". Right-side callout box: "2025–2026: from static datasets to interactive environments and closed-loop agent benchmarks".
```

## 负面提示（Negative prompt）

```text
photorealistic, 3D render, gradients, cluttered layout, illegible or garbled text, watermark, logo, decorative flourishes, dark background
```

## 建议参数

- 画幅：16:9（如 1792×1024）；若节点文字偏多可改 21:9（2560×1080）。
- 风格关键词已内置：flat vector / Nature figure aesthetics。
- 生图模型对长文本渲染不稳定：若节点名出现乱码，可要求"labels as short abbreviations only"，或改用代码绘图（见下）。

## 中文设计说明（prompt 与综述的对应关系）

| 图中元素 | 综述依据 |
|---|---|
| 五条泳道 | 5 个任务 sheet：预测与识别 / 生成与逆向设计 / 路线与步骤规划 / 优化与实验推荐 / AI模型评测 |
| 六个时代色带 | §2 六阶段：实验晶体学积累 → 高通量 DFT → 领域扩展 → 规模化与闭环 → 基础模型数据 → 智能体与深度评测 |
| 节点形状（圆/方/菱） | 表内 E/S/H 三分法：E 实验 20 条、S 模拟 66 条、H 混合 17 条 |
| 跨泳道虚线 | §7 趋势 3：MP 本体跨 3 个任务（衍生基准覆盖 4 类），QM9/OC20/GNoME 等跨 2+ 任务复用 |
| 底部对数规模曲线 | §7 趋势 1：10³（早期实验）→ 10⁸（OMat24 1.18 亿、OMol25 1 亿+ DFT） |
| 规划泳道刻意稀疏 | §5/§8：仅 4 条，真实合成路线数据空白 |
| 右侧 2025–2026 标注 | §7 趋势 7：该时段 32 条中 66% 集中在优化/评测/规划，重心从"喂模型"转向"考模型+闭环" |

## v1 MCP 精简版（单面板，≤800 字符，已被 v2 取代）

`bailian_image_gen` 的 prompt 超过 800 字符会自动截断，故将主 prompt 压缩如下（保留五泳道、六时代、关键节点、E/S/H 形状、复用虚线与对数规模曲线）。
调用参数：`size=1664*928`（16:9），`prompt_extend=false`，`n=1`。

```text
Flat-vector timeline infographic, white background, Nature-journal style, English labels, 16:9. Title: 'Materials AI Datasets 1965–2026'. Axis 1965–2026. Five swimlanes: Prediction & Identification (blue), Generation & Inverse Design (teal), Route Planning (purple), Optimization & Experiments (orange), AI Evaluation (red). Era bands: Crystallography –2010, DFT 2011–16, Expansion 2017–19, Scale-up 2020–22, Foundation Data 2023–24, Agents 2025–26. Nodes: CSD 1965, ICSD 1978, Materials Project 2011, QM9 2014, GuacaMol 2019, OC20 2020, GNoME 2023, OMat24 2024, OMol25 2025, PhononBench 2026, MADE 2026; planning lane sparse. Circle=experimental, square=simulation, diamond=hybrid; legend. Dotted lines: Materials Project, QM9, OC20, GNoME reused across lanes. Bottom: log-scale curve 10^3→10^8.
```

## v2 双面板（当前使用）：趋势与限制概览在上 + 时间线在下

布局：上面板（约 40% 高）为左右两框 **TRENDS / LIMITATIONS**，各 6 条短标签；下面板（约 60% 高）沿用 v1 时间线（五泳道 + 六时代色带 + 节点 + 复用虚线 + 对数规模曲线）。画幅 4:3 横版（1472*1140）。

### v2 完整 Prompt（英文，供代码绘图 / 长上下文生图）

```text
Create a publication-quality two-panel scientific infographic, flat vector style, clean white background, muted academic palette, sans-serif English labels, Nature-journal aesthetics, landscape 4:3.

TOP PANEL (about 40% height), titled 'System Trends & Limitations': two side-by-side rounded boxes. Left box 'TRENDS' (green accent) with six icon bullets: (1) Data scale leap 10^3 to 10^8; (2) Source loop: experiment to simulation to closed-loop experiment reflux; (3) Cross-task reuse of foundation databases (Materials Project, QM9, OC20, GNoME); (4) Modality expansion: structures to spectra/images to synthesis text to interactive environments; (5) Evaluation upgrade: validity/novelty to stability and leakage control to out-of-distribution and closed-loop efficiency; (6) Focus shift: 66% of 2025-26 entries in optimization, evaluation, planning. Right box 'LIMITATIONS' (amber accent) with six warning bullets: (1) Route-planning data scarce (4 entries, no real synthesis records); (2) Decision-level experiment records scarce (10^2-10^4 per campaign); curated E libraries are large but state-only; (3) All 18 evaluation benchmarks simulation-only, no real-experiment ground truth; (4) Inconsistent version/snapshot reporting; (5) License barriers (commercial and paid bulk databases); (6) Negative/failed results largely missing.

BOTTOM PANEL (about 60% height): timeline 'Materials AI Datasets 1965-2026': horizontal axis 1965-2026; five swimlanes Prediction & Identification (blue), Generation & Inverse Design (teal), Route & Step Planning (purple), Optimization & Experiment Recommendation (orange), AI Model Evaluation (red); six era bands Crystallography -2010, DFT 2011-16, Expansion 2017-19, Scale-up 2020-22, Foundation Data 2023-24, Agents 2025-26; milestone nodes CSD 1965, ICSD 1978, Materials Project 2011, QM9 2014, GuacaMol 2019, OC20 2020, GNoME 2023, OMat24 2024, OMol25 2025, PhononBench 2026, MADE 2026 with sparse planning lane; node shapes circle=experimental, square=simulation, diamond=hybrid with legend; dotted grey reuse connectors; bottom log-scale ribbon 10^3 to 10^8.
```

### v2 MCP 精简版（≤800 字符，供 TextGenerateImage）

```text
Two-panel flat-vector infographic, white background, Nature style, English text. TOP: two boxes. TRENDS: Scale 10^3→10^8; E→S→closed-loop; cross-task reuse; multimodal expansion; deeper evaluation; shift to optimization. LIMITATIONS: sparse planning data; E/S imbalance; no real-experiment eval; version drift; license barriers; missing negatives. BOTTOM: timeline 1965–2026, five swimlanes (Prediction blue, Generation teal, Planning purple, Optimization orange, Evaluation red), era bands Crystallography/DFT/Expansion/Scale-up/Foundation/Agents, nodes CSD 1965, ICSD 1978, MP 2011, QM9 2014, GuacaMol 2019, OC20 2020, GNoME 2023, OMat24 2024, OMol25 2025, PhononBench 2026; circle=experimental, square=simulation, diamond=hybrid; dotted reuse lines; log ribbon 10^3→10^8.
```

调用参数：`size=1472*1140`（4:3），`prompt_extend=false`，`n=1`；负面提示同 v1。

### v2 概览内容依据（综述 §7 趋势 / §8 缺口）

| 面板 | 条目 | 综述依据 |
|---|---|---|
| TRENDS 1 | 规模跃迁 10³→10⁸ | §7-1：QM9 1.3×10⁵ → OMat24 1.18×10⁸ |
| TRENDS 2 | 来源闭环 E→S→E+S 回流 | §7-2：SDL/纳米压痕/MOCLIP/RECOB |
| TRENDS 3 | 基础库跨任务复用 | §7-3：MP 本体跨 3 个 sheet，衍生基准覆盖 4 类任务 |
| TRENDS 4 | 模态扩展 | §7-4：结构→光谱/图像→配方文本→交互环境 |
| TRENDS 5 | 评测升级 | §7-5：有效性→稳定性/泄漏→OOD/闭环效率 |
| TRENDS 6 | 重心后移 | §7-7：2025–26 条目 66% 在优化/评测/规划 |
| LIMITATIONS 1 | 规划数据稀缺 | §8：仅 4 条，无真实合成步骤记录 |
| LIMITATIONS 2 | 实验/模拟失衡 | §8：决策级实验记录 10²–10⁴；文献型 E 大库仅状态标签 |
| LIMITATIONS 3 | 评测无真实终判 | §8：18/18 基准全为模拟 |
| LIMITATIONS 4 | 版本口径不一 | §8：多条自注规模随版本变化 |
| LIMITATIONS 5 | 许可壁垒 | §8：商业库与付费批量限制复用 |
| LIMITATIONS 6 | 负结果缺位 | §8：失败实验记录极少 |

## 备选：代码绘图（发表级推荐）

生图模型难以保证 104 个节点与文字精确无误。若用于论文正式插图，建议用 matplotlib/TikZ 直接从
`summary/raw/*.json` 渲染同一设计（泳道 + 时代色带 + E/S/H 形状 + 复用虚线 + 对数规模曲线），
可完全复现且文字可控。需要时可直接生成脚本。
