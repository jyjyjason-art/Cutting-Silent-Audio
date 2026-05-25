# 音频静音压缩工具

这是一个 Windows 本地小工具，用来批量处理音频里的长静音。它会扫描 `in/` 目录里的音频文件，把较长的静音段压短，然后把处理后的音频输出到 `out/` 目录。

适合处理：

- 口播音频停顿太长
- 商品配音节奏太慢
- 录音里有很多空白
- 想保留原音频内容，但缩短中间等待时间

## 功能

- 递归处理 `in/` 目录里的音频
- 自动识别较长静音段
- 默认把静音段压缩到原来的约 `1/3`
- 非静音的人声/内容基本保留
- 输出目录保持原来的子文件夹结构
- 输出文件名自动加 `_shrinked`

## 支持格式

- `.wav`
- `.mp3`
- `.m4a`
- `.aac`
- `.flac`
- `.ogg`
- `.wma`

## 目录说明

```text
C:\cutting
├── shrink_silence.py              主程序
├── cuttingrun_shrink_silence.bat  一键运行脚本
├── requirements.txt               Python 依赖
├── in\                            放原始音频
└── out\                           输出处理后的音频
```

把要处理的音频放到：

```text
in\
```

处理完成后，到这里找结果：

```text
out\
```

## 使用方法

### 方法一：双击运行

直接双击：

```text
cuttingrun_shrink_silence.bat
```

这个批处理会自动检查：

- Python 是否存在
- `pydub` 是否安装
- `ffmpeg / ffprobe` 是否能找到
- `in / out` 目录是否存在

处理结束后会自动打开 `out` 文件夹。

### 方法二：命令行运行

```powershell
python shrink_silence.py
```

## 依赖

需要安装：

- Python 3.x
- FFmpeg
- pydub

安装 Python 依赖：

```powershell
pip install -r requirements.txt
```

确认 FFmpeg 可用：

```powershell
ffmpeg -version
ffprobe -version
```

## 参数说明

主要参数在 `shrink_silence.py` 里：

```python
KEEP_RATIO = 1/3
MIN_SILENCE_LEN_MS = 300
SILENCE_THRESH_DBFS = -40
MIN_KEEP_MS = 120
CROSSFADE_MS = 5
```

含义：

- `KEEP_RATIO`：静音保留比例，默认保留三分之一
- `MIN_SILENCE_LEN_MS`：多长以上才算需要压缩的静音，默认 `300ms`
- `SILENCE_THRESH_DBFS`：静音判断阈值，数值越高越敏感
- `MIN_KEEP_MS`：每段静音最少保留多长，避免剪得太硬
- `CROSSFADE_MS`：拼接时的淡入淡出，减少爆音

## 注意

`in/`、`out/`、`input/`、`output/` 目录里的音频不会上传到 GitHub。它们已经被 `.gitignore` 忽略。

这个仓库只保存工具代码和说明文档，不保存本地音频素材。
