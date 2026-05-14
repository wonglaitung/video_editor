#!/usr/bin/env python3
"""
视频压缩工具 - 压缩视频文件大小

支持两种模式:
1. 指定目标大小: 自动计算最佳码率
2. 指定码率: 直接使用指定码率压缩

使用示例:
    python video_compressor.py input.mp4 -s 50m       # 压缩到50MB
    python video_compressor.py input.mp4 -s 100       # 压缩到100MB
    python video_compressor.py input.mp4 -b 500k      # 使用500k码率
"""

import argparse
import os
import re
import sys
from pathlib import Path

from moviepy import VideoFileClip


def parse_size(size_str: str) -> float:
    """
    解析大小字符串为 MB

    支持格式:
    - 纯数字: "50", "100" (默认 MB)
    - MB: "50m", "50M", "50MB"
    - GB: "1g", "1G", "1GB"
    - KB: "500k", "500K", "500KB"

    Args:
        size_str: 大小字符串

    Returns:
        MB 数值
    """
    size_str = size_str.strip().upper()

    # 纯数字，默认 MB
    if re.match(r'^\d+(\.\d+)?$', size_str):
        return float(size_str)

    # 带单位
    match = re.match(r'^(\d+(?:\.\d+)?)(KB|MB|GB|K|M|G)$', size_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2)

        if unit in ('KB', 'K'):
            return value / 1024
        elif unit in ('MB', 'M'):
            return value
        elif unit in ('GB', 'G'):
            return value * 1024

    raise ValueError(f"无效的大小格式: {size_str}")


def calculate_bitrate(
    target_size_mb: float,
    duration_seconds: float,
    audio_bitrate_kbps: int = 64
) -> str:
    """
    根据目标大小计算视频码率

    Args:
        target_size_mb: 目标大小 (MB)
        duration_seconds: 视频时长 (秒)
        audio_bitrate_kbps: 音频码率 (kbps)

    Returns:
        视频码率字符串 (如 "500k")
    """
    # 目标大小转换为 bits
    # 1 MB = 8 * 1024 * 1024 bits
    target_bits = target_size_mb * 8 * 1024 * 1024

    # 音频占用 bits
    audio_bits = audio_bitrate_kbps * 1000 * duration_seconds

    # 视频可用 bits
    video_bits = target_bits - audio_bits

    # 计算视频码率 (bps)
    video_bitrate_bps = video_bits / duration_seconds

    # 转换为 kbps
    video_bitrate_kbps = video_bitrate_bps / 1000

    # 确保最小码率 (至少 100k)
    video_bitrate_kbps = max(video_bitrate_kbps, 100)

    return f"{int(video_bitrate_kbps)}k"


def compress_video(
    input_path: str,
    output_path: str,
    bitrate: str = None,
    audio_bitrate: str = "64k",
    target_size: float = None
) -> None:
    """
    压缩视频文件

    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        bitrate: 视频码率 (如 "500k")
        audio_bitrate: 音频码率 (默认 64k)
        target_size: 目标大小 (MB)，如果指定则自动计算码率
    """
    print(f"加载视频: {input_path}")

    # 获取原始文件大小
    original_size = os.path.getsize(input_path) / (1024 * 1024)
    print(f"原始大小: {original_size:.1f} MB")

    # 加载视频
    video = VideoFileClip(input_path)
    duration = video.duration

    print(f"视频时长: {duration:.2f} 秒 ({duration/60:.1f} 分钟)")

    # 解析音频码率
    audio_bitrate_kbps = int(audio_bitrate.replace('k', '').replace('K', ''))

    # 计算或使用指定码率
    if target_size is not None:
        # 检查目标大小是否合理
        if target_size >= original_size:
            print(f"警告: 目标大小 ({target_size:.1f} MB) 大于原始大小，无需压缩")
            video.close()
            return

        bitrate = calculate_bitrate(target_size, duration, audio_bitrate_kbps)
        print(f"目标大小: {target_size:.1f} MB")
        print(f"计算码率: {bitrate}")
    else:
        print(f"指定码率: {bitrate}")

    print(f"音频码率: {audio_bitrate}")

    # 输出目录
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 压缩输出
    print(f"正在压缩: {output_path}")
    video.write_videofile(
        output_path,
        codec="libx264",
        bitrate=bitrate,
        audio_codec="aac",
        audio_bitrate=audio_bitrate
    )

    video.close()

    # 获取压缩后大小
    compressed_size = os.path.getsize(output_path) / (1024 * 1024)
    ratio = (1 - compressed_size / original_size) * 100

    print(f"\n压缩完成!")
    print(f"原始大小: {original_size:.1f} MB")
    print(f"压缩后: {compressed_size:.1f} MB")
    print(f"压缩率: {ratio:.1f}%")

    if target_size is not None:
        diff = compressed_size - target_size
        print(f"目标偏差: {diff:.1f} MB ({diff/target_size*100:.1f}%)")

    print(f"输出文件: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="视频压缩工具 - 压缩视频文件大小",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 指定目标大小 (自动计算码率)
  %(prog)s input.mp4 -s 50m        # 压缩到 50MB
  %(prog)s input.mp4 -s 100        # 压缩到 100MB
  %(prog)s input.mp4 -s 1g         # 压缩到 1GB

  # 指定码率
  %(prog)s input.mp4 -b 500k       # 使用 500k 码率
  %(prog)s input.mp4 -b 800k -a 64k

大小格式支持:
  纯数字: 50, 100 (默认 MB)
  MB: 50m, 50M, 50MB
  GB: 1g, 1G, 1GB
  KB: 500k (注意: 用 -b 指定码率时 k 表示 kbps)

码率参考:
  高质量: 2000k-5000k
  中等质量: 800k-1500k
  低质量: 300k-800k
        """
    )

    parser.add_argument(
        "input",
        help="输入视频文件路径"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出视频文件路径 (默认: compressed_<input>)"
    )

    parser.add_argument(
        "-s", "--size",
        help="目标文件大小 (如 50m, 100MB, 1g)，自动计算最佳码率"
    )

    parser.add_argument(
        "-b", "--bitrate",
        default="800k",
        help="视频码率 (默认: 800k)，指定 -s 时忽略此参数"
    )

    parser.add_argument(
        "-a", "--audio-bitrate",
        default="64k",
        help="音频码率 (默认: 64k)"
    )

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 设置默认输出路径
    if args.output is None:
        input_path = Path(args.input)
        args.output = str(input_path.parent / f"compressed_{input_path.name}")

    # 解析目标大小
    target_size = None
    if args.size:
        try:
            target_size = parse_size(args.size)
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    # 执行压缩
    try:
        compress_video(
            args.input,
            args.output,
            bitrate=args.bitrate,
            audio_bitrate=args.audio_bitrate,
            target_size=target_size
        )
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()