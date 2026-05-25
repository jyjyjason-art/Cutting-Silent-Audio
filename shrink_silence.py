# -*- coding: utf-8 -*-
# 将 C:\cutting\in（含子文件夹）里的音频批量处理：
#   把 ≥ MIN_SILENCE_LEN_MS 的静音段按 KEEP_RATIO 压缩（默认 1/3）
#   输出到 C:\cutting\out，并保留原有子目录结构，文件名加 _shrinked
# 依赖：pydub（pip install pydub）+ 本机可用的 ffmpeg/ffprobe

import os, sys
from pydub import AudioSegment
from pydub.silence import detect_silence
from pydub.utils import which

# -------- 基础路径（自动以脚本所在目录为 BASE）--------
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
IN_DIR    = os.path.join(BASE_DIR, "in")
OUT_DIR   = os.path.join(BASE_DIR, "out")

# 兼容老目录名（存在则优先使用）
if not os.path.exists(IN_DIR) and os.path.exists(os.path.join(BASE_DIR, "input")):
    IN_DIR = os.path.join(BASE_DIR, "input")
if not os.path.exists(OUT_DIR) and os.path.exists(os.path.join(BASE_DIR, "output")):
    OUT_DIR = os.path.join(BASE_DIR, "output")

# -------- 处理参数（按需调整）--------
KEEP_RATIO = 1/3          # 静音保留比例（900ms->300ms）
MIN_SILENCE_LEN_MS = 300  # 仅处理 ≥300ms 的静音（建议 300~600）
SILENCE_THRESH_DBFS = -40 # 静音阈值（-35 更敏感，-45 更保守）
MIN_KEEP_MS = 120         # 每段静音压缩后至少保留
CROSSFADE_MS = 5          # 拼接交叉淡入/淡出，防点击声
ADD_SUFFIX = True         # 输出文件名是否加 _shrinked

SUPPORT_EXT = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".wma"}

def is_audio_file(path: str) -> bool:
    return os.path.splitext(path)[1].lower() in SUPPORT_EXT

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def merge_intervals(intervals):
    if not intervals: return []
    intervals = sorted(intervals)
    merged = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged

def map_out_path(in_abs: str) -> str:
    rel = os.path.relpath(in_abs, start=IN_DIR)  # 例如 子A\1.wav
    base, ext = os.path.splitext(rel)
    if ADD_SUFFIX:
        rel = f"{base}_shrinked{ext or '.wav'}"
    return os.path.join(OUT_DIR, rel)

def process_one(infile: str, outfile: str):
    try:
        audio = AudioSegment.from_file(infile)
    except Exception as e:
        print(f"[失败: 读入] {infile} -> {e}")
        return

    silences = detect_silence(audio,
                              min_silence_len=MIN_SILENCE_LEN_MS,
                              silence_thresh=SILENCE_THRESH_DBFS)
    silences = merge_intervals(silences)

    if not silences:
        # 没有长静音也复制一份，方便统一替换
        ensure_dir(os.path.dirname(outfile))
        try:
            ext = os.path.splitext(outfile)[1][1:] or "wav"
            audio.export(outfile, format=ext)
            print(f"[复制] 无≥{MIN_SILENCE_LEN_MS}ms静音：{infile}")
        except Exception as e:
            print(f"[失败: 导出] {outfile} -> {e}")
        return

    out = AudioSegment.silent(duration=0, frame_rate=audio.frame_rate)
    cursor = 0
    for s, e in silences:
        if s > cursor:  # 非静音段
            seg = audio[cursor:s]
            out = out.append(seg, crossfade=CROSSFADE_MS if len(out) and len(seg) else 0)
        dur = e - s     # 静音段
        keep = int(max(MIN_KEEP_MS, dur * KEEP_RATIO))
        keep_seg = audio[s:s+keep]
        out = out.append(keep_seg, crossfade=CROSSFADE_MS if len(out) and len(keep_seg) else 0)
        cursor = e

    if cursor < len(audio):  # 尾段
        tail = audio[cursor:]
        out = out.append(tail, crossfade=CROSSFADE_MS if len(out) and len(tail) else 0)

    ensure_dir(os.path.dirname(outfile))
    try:
        ext = os.path.splitext(outfile)[1][1:] or "wav"
        out.export(outfile, format=ext)
        print(f"[完成] {infile}")
    except Exception as e:
        print(f"[失败: 导出] {outfile} -> {e}")

def main():
    if which("ffmpeg") is None or which("ffprobe") is None:
        print("[警告] 未检测到 ffmpeg/ffprobe；若报错请将其加入 PATH 或与脚本同目录。")
    if not os.path.exists(IN_DIR):
        print(f"[错误] 输入目录不存在：{IN_DIR}")
        sys.exit(1)
    ensure_dir(OUT_DIR)

    # 统计数量
    total = 0
    for root, _, files in os.walk(IN_DIR):
        for n in files:
            if is_audio_file(n):
                total += 1
    print(f"[开始] 将处理 {total} 个音频文件（递归子文件夹）。")
    if total == 0:
        print(f"[提示] 未发现音频。支持：{', '.join(sorted(SUPPORT_EXT))}")
        return

    done = 0
    for root, _, files in os.walk(IN_DIR):
        for n in files:
            if not is_audio_file(n): continue
            in_abs  = os.path.join(root, n)
            out_abs = map_out_path(in_abs)
            process_one(in_abs, out_abs)
            done += 1

    print(f"[全部完成] {done}/{total} 个已输出到：{OUT_DIR}")

if __name__ == "__main__":
    main()
