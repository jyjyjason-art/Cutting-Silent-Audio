# Cutting Silent Audio

Batch audio silence shrinker for Windows. It scans audio files under `in/`,
shortens long silent parts, and writes processed files to `out/` while keeping
the original folder structure.

## What It Does

- Recursively processes audio files in `in/`
- Detects silent sections longer than 300 ms
- Keeps about one third of each detected silent section
- Preserves non-silent speech/audio content
- Writes output files to `out/`
- Adds `_shrinked` to output filenames

This is useful for tightening voice recordings, product narration, and short
audio clips that contain long pauses.

## Supported Formats

- `.wav`
- `.mp3`
- `.m4a`
- `.aac`
- `.flac`
- `.ogg`
- `.wma`

## Requirements

- Windows
- Python 3.x
- FFmpeg and FFprobe available in `PATH`
- Python package: `pydub`

Install Python dependency:

```powershell
pip install -r requirements.txt
```

FFmpeg can be installed separately. After installation, make sure both commands
work:

```powershell
ffmpeg -version
ffprobe -version
```

## Folder Layout

```text
C:\cutting
├── shrink_silence.py
├── cuttingrun_shrink_silence.bat
├── in\
└── out\
```

Put source audio files into `in/`. Processed files will be written to `out/`.

## Usage

### Option 1: Run the Batch File

Double-click:

```text
cuttingrun_shrink_silence.bat
```

The batch file checks Python, installs `pydub` if needed, checks FFmpeg, runs the
processor, and opens the output folder.

### Option 2: Run Python Directly

```powershell
python shrink_silence.py
```

## Processing Settings

The main settings are inside `shrink_silence.py`:

```python
KEEP_RATIO = 1/3
MIN_SILENCE_LEN_MS = 300
SILENCE_THRESH_DBFS = -40
MIN_KEEP_MS = 120
CROSSFADE_MS = 5
```

Adjust these values if the silence detection is too aggressive or too mild.

## Notes

The `in/`, `out/`, `input/`, and `output/` folders are ignored by git because
they may contain local audio material. Only the tool code and documentation are
intended to be committed.
