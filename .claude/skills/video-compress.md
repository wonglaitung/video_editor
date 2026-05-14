---
name: video-compress
description: 压缩视频文件大小，支持指定目标大小自动计算码率
userInvocable: true
---

# 视频压缩

压缩视频文件大小。支持两种模式：
1. **指定目标大小**：自动计算最佳码率
2. **指定码率**：直接使用指定码率压缩

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
   - 原始文件大小
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

## 功能特性

- **智能计算**：指定目标大小后自动计算最佳码率
- **多种格式**：支持 MB、GB、KB 等大小单位
- **偏差显示**：显示实际大小与目标的偏差
- **码率控制**：可手动指定视频和音频码率
