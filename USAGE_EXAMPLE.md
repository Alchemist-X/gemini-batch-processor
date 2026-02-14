# Usage Examples

## Basic Setup

1. **Set up your API key**:
```bash
export GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Example 1: Basic Batch Processing

Process all images in a directory with a simple prompt:

```bash
python main.py \
  --input-dir /path/to/your/manga/images \
  --prompt "convert this to anime style illustration" \
  --output-dir ./anime_results
```

## Example 2: Advanced Processing with Optimization

Enable prompt optimization and concurrent processing:

```bash
python main.py \
  --input-dir /path/to/your/images \
  --prompt "anime style, detailed illustration" \
  --output-dir ./results \
  --max-concurrent 8 \
  --max-retries 10 \
  --enable-prompt-optimization \
  --archive-format zip
```

## Example 3: Dry Run Testing

Test your setup without making actual API calls:

```bash
python main.py \
  --input-dir /path/to/test/images \
  --prompt "test prompt" \
  --dry-run
```

## Expected Output Structure

After processing, you'll get:

```
./results/
├── successful/
│   ├── image1_result.txt
│   ├── image2_result.txt
│   └── ...
├── failed/
│   ├── problematic_image_error.log
│   └── ...
├── metadata/
│   ├── processing_stats.json
│   ├── prompt_evolution.json
│   └── ...
└── results.zip (if archive enabled)
```

## Environment Variables

You can also configure via environment variables:

```env
GEMINI_API_KEY=your_key_here
MAX_CONCURRENT_REQUESTS=10
MAX_RETRIES=8
OUTPUT_DIR=./my_results
ENABLE_PROMPT_OPTIMIZATION=true
ARCHIVE_FORMAT=zip
DRY_RUN=false
```

## Error Handling Examples

The system automatically handles:

- **Rate limiting**: Slows down requests when hitting limits
- **Invalid images**: Skips corrupted or unsupported files
- **Content safety blocks**: Optimizes prompts to be more appropriate
- **Network timeouts**: Retries with exponential backoff

## Performance Tips

- Start with `--max-concurrent 3-5` to avoid rate limits
- Use `--enable-prompt-optimization` for consistent failures
- Monitor the `metadata/processing_stats.json` for optimization insights