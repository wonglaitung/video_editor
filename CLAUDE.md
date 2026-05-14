# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

视频编辑工具集，基于 MoviePy 库，提供视频剪辑和压缩功能。

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 视频剪辑
python video_clipper.py input.mp4 -c 0:10-0:30 -c 1:00-1:30 -o output.mp4

# 视频压缩 (指定目标大小)
python video_compressor.py input.mp4 -s 50m

# 视频压缩 (指定码率)
python video_compressor.py input.mp4 -b 500k
```

## 架构

```
video_editor/
├── video_clipper.py      # 视频剪辑：提取多个片段并合并
├── video_compressor.py   # 视频压缩：支持目标大小或码率
├── requirements.txt      # 依赖：moviepy>=1.0.3
└── .claude/skills/       # Claude Code 技能定义
    ├── video-clip.md     # /video-clip 技能
    └── video-compress.md # /video-compress 技能
```

## 核心功能

### video_clipper.py
- `parse_time()`: 解析时间字符串（支持秒、分:秒、时:分:秒）
- `parse_clip()`: 解析时间段字符串（格式：开始-结束）
- `clip_video()`: 剪辑并合并多个片段

### video_compressor.py
- `parse_size()`: 解析大小字符串（支持 KB、MB、GB）
- `calculate_bitrate()`: 根据目标大小计算视频码率
- `calculate_optimal_resolution()`: 根据码率计算最佳分辨率
- `compress_video()`: 压缩视频，支持画质优化

## 技能调用

用户可通过 `/video-clip` 和 `/video-compress` 技能直接调用功能，详见 `.claude/skills/` 目录。
