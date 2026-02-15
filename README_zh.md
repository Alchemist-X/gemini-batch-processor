# Gemini 批量处理器

一个强大的 Google Gemini API 批量处理系统，支持并发请求、自动重试、提示优化和结构化输出归档。

## 功能特性

- 🚀 **并发处理**: 同时处理多张图片
- 🔁 **自动重试**: 智能错误处理与指数退避
- 🧠 **提示优化**: 基于失败分析自动优化提示词
- 📁 **结构化归档**: 带元数据的有序输出目录
- 📊 **进度追踪**: 实时进度监控与统计
- ⚡ **速率限制处理**: 自动节流以遵守 API 限制

## 安装

```bash
git clone https://github.com/your-username/gemini-batch-processor.git
cd gemini-batch-processor
pip install -r requirements.txt
```

## 配置

创建 `.env` 文件：

```env
GEMINI_API_KEY=your_gemini_api_key_here
MAX_CONCURRENT_REQUESTS=5
MAX_RETRIES=5
OUTPUT_DIR=./output
```

## 使用方法

### 基础用法

```bash
python main.py --input-dir /path/to/images --prompt "将此转换为动漫风格"
```

### 高级选项

```bash
python main.py \
  --input-dir /path/to/images \
  --prompt "动漫风格插画" \
  --output-dir ./results \
  --max-concurrent 10 \
  --max-retries 8 \
  --enable-prompt-optimization \
  --archive-format zip
```

## 命令行参数

| 参数 | 描述 | 默认值 |
|----------|-------------|---------|
| `--input-dir` | 包含图片的输入目录 | 必需 |
| `--prompt` | 所有图片的基础提示词 | 必需 |
| `--output-dir` | 结果输出目录 | `./output` |
| `--max-concurrent` | 最大并发请求数 | `5` |
| `--max-retries` | 每张图片的最大重试次数 | `5` |
| `--enable-prompt-optimization` | 启用自动提示词优化 | `False` |
| `--archive-format` | 归档格式 (`zip`, `tar`, `none`) | `none` |
| `--dry-run` | 测试模式（不实际调用 API） | `False` |

## 架构

```
gemini-batch-processor/
├── main.py                 # 入口文件
├── config.py              # 配置管理
├── processor.py           # 核心处理逻辑
├── retry_handler.py       # 重试与错误处理
├── prompt_optimizer.py    # 提示词优化引擎
├── archiver.py            # 输出归档系统
├── utils/
│   ├── image_validator.py # 图片验证工具
│   └── logger.py         # 日志工具
├── requirements.txt
└── README.md
```

## 示例工作流

1. **输入**: 包含 100 张图片的目录
2. **处理**: 
   - 并发处理图片（遵守速率限制）
   - 自动重试失败请求（指数退避）
   - 为持续失败的图片优化提示词
3. **输出**: 
   - 结构化目录
   - 元数据 JSON 文件
   - 可选压缩归档

## 错误处理

系统智能处理不同类型的错误：

- **429 速率限制**: 更长的指数退避
- **400 无效请求**: 跳过并记录，不重试
- **网络错误**: 标准指数退避
- **超时错误**: 重试并增加超时时间

## 提示词优化

当图片持续失败时，系统会自动：
1. 分析失败模式
2. 修改提示词使其更具体或更简单
3. 使用优化后的提示词重试

提示词演进示例：
- 原始: `"动漫风格"`
- 优化后: `"简约动漫插画，清晰线条，极简背景"`

## 输出结构

```
output/
├── successful/
│   ├── image1.jpg_result.txt
│   ├── image2.png_result.txt
│   └── ...
├── failed/
│   ├── image3.jpg_error.log
│   └── ...
├── metadata/
│   ├── processing_stats.json
│   ├── prompt_evolution.json
│   └── error_analysis.json
└── archive.zip (如果启用)
```

## 依赖要求

- Python 3.8+
- Google Generative AI SDK
- Pillow (用于图片验证)
- python-dotenv (用于配置)

## 许可证

MIT 许可证