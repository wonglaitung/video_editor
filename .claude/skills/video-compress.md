---
name: video-compress
description: 压缩视频文件大小，支持指定目标大小自动计算码率，优先保持画质
userInvocable: true
---

# 视频压缩

压缩视频文件大小。支持两种模式：
1. **指定目标大小**：自动计算最佳码率，优先保持画质
2. **指定码率**：直接使用指定码率压缩

## 画质优化

默认开启画质优化，根据码率自动调整分辨率：
| 码率 | 分辨率 |
|------|--------|
| 5000k+ | 1080p |
| 3000k+ | 720p |
| 1500k+ | 480p |
| 800k+ | 360p |
| 400k+ | 240p |
| 更低 | 180p |

## 用法

```
/video-compress <输入视频> -s <目标大小>
/video-compress <输入视频> -b <视频码率>
```

## 参数说明

- `<输入视频>`: 源视频文件路径（必需）
- `-s <目标大小>`: 目标文件大小，自动计算最佳码率
- `-b <视频码率>`: 指定视频码率（默认 800k）
- `-o <输出路径>`: 输出文件路径（可选）
- `-a <音频码率>`: 音频码率（可选，默认 64k）
- `--no-keep-quality`: 保持原始分辨率，不自动调整

## 大小格式

| 格式 | 示例 |
|------|------|
| 纯数字 (MB) | `50`, `100` |
| MB | `50m`, `50MB` |
| GB | `1g`, `1GB` |
| KB | `500k` |

## 执行步骤

当用户调用此技能时，执行以下操作：

1. 解析用户提供的参数

2. 运行压缩脚本：
   ```bash
   python3 video_compressor.py "<输入视频>" -s <目标大小>
   # 或
   python3 video_compressor.py "<输入视频>" -b <视频码率>
   ```

3. 报告压缩结果，包括：
   - 原始文件大小和分辨率
   - 调整后的分辨率（如果启用画质优化）
   - 压缩后文件大小
   - 压缩率
   - 目标偏差（如果指定了目标大小）

## 示例调用

用户输入：
```
/video-compress video.mp4 -s 50m
```

执行：
```bash
python3 video_compressor.py "video.mp4" -s 50m
```

用户输入：
```
/video-compress large.mp4 -s 100
```

执行：
```bash
python3 video_compressor.py "large.mp4" -s 100
```

用户输入：
```
/video-compress input.mp4 -b 500k -o small.mp4
```

执行：
```bash
python3 video_compressor.py "input.mp4" -b 500k -o "small.mp4"
```

用户输入：
```
/video-compress video.mp4 -s 50m --no-keep-quality
```

执行：
```bash
python3 video_compressor.py "video.mp4" -s 50m --no-keep-quality
```

## 功能特性

- **智能计算**：指定目标大小后自动计算最佳码率
- **画质优化**：根据码率自动调整分辨率，避免画质模糊
- **高质量编码**：使用 H.264 高质量编码参数
- **多种格式**：支持 MB、GB、KB 等大小单位
