# Gemini Batch Processor

A robust batch processing system for Google Gemini API that handles multiple images with concurrent requests, automatic retry, prompt optimization, and organized output archiving.

## Features

- 🚀 **Concurrent Processing**: Process multiple images simultaneously
- 🔁 **Automatic Retry**: Exponential backoff with intelligent error handling
- 🧠 **Prompt Optimization**: Automatically refine prompts based on failure analysis
- 📁 **Organized Archiving**: Structured output directory with metadata
- 📊 **Progress Tracking**: Real-time progress monitoring and statistics
- ⚡ **Rate Limit Handling**: Automatic throttling to respect API limits

## Installation

```bash
git clone https://github.com/your-username/gemini-batch-processor.git
cd gemini-batch-processor
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MAX_CONCURRENT_REQUESTS=5
MAX_RETRIES=5
OUTPUT_DIR=./output
```

## Usage

### Basic Usage

```bash
python main.py --input-dir /path/to/images --prompt "Convert this to anime style"
```

### Advanced Options

```bash
python main.py \
  --input-dir /path/to/images \
  --prompt "anime style illustration" \
  --output-dir ./results \
  --max-concurrent 10 \
  --max-retries 8 \
  --enable-prompt-optimization \
  --archive-format zip
```

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input-dir` | Input directory containing images | Required |
| `--prompt` | Base prompt for all images | Required |
| `--output-dir` | Output directory for results | `./output` |
| `--max-concurrent` | Maximum concurrent requests | `5` |
| `--max-retries` | Maximum retry attempts per image | `5` |
| `--enable-prompt-optimization` | Enable automatic prompt refinement | `False` |
| `--archive-format` | Archive format (`zip`, `tar`, `none`) | `none` |
| `--dry-run` | Test without making actual API calls | `False` |

## Architecture

```
gemini-batch-processor/
├── main.py                 # Entry point
├── config.py              # Configuration management
├── processor.py           # Core processing logic
├── retry_handler.py       # Retry and error handling
├── prompt_optimizer.py    # Prompt optimization engine
├── archiver.py            # Output archiving system
├── utils/
│   ├── image_validator.py # Image validation utilities
│   └── logger.py         # Logging utilities
├── requirements.txt
└── README.md
```

## Example Workflow

1. **Input**: Directory with 100 images
2. **Processing**: 
   - Concurrently process images (respecting rate limits)
   - Automatically retry failed requests with exponential backoff
   - Optimize prompts for consistently failing images
3. **Output**: 
   - Organized directory structure
   - Metadata JSON files
   - Optional compressed archive

## Error Handling

The system intelligently handles different types of errors:

- **429 Rate Limit**: Longer exponential backoff
- **400 Invalid Request**: Skip and log, don't retry
- **Network Errors**: Standard exponential backoff
- **Timeout Errors**: Retry with increased timeout

## Prompt Optimization

When images consistently fail, the system automatically:
1. Analyzes the failure pattern
2. Modifies the prompt to be more specific or less complex
3. Retries with the optimized prompt

Example prompt evolution:
- Original: `"anime style"`
- Optimized: `"simple anime illustration, clean lines, minimal background"`

## Output Structure

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
└── archive.zip (if enabled)
```

## Requirements

- Python 3.8+
- Google Generative AI SDK
- Pillow (for image validation)
- python-dotenv (for configuration)

## License

MIT License