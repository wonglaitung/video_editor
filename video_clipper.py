#!/usr/bin/env python3
"""
视频剪辑工具 - 从视频中剪辑多个片段并合并成一个完整视频

使用示例:
    python video_clipper.py input.mp4 -o output.mp4 -c 0:10-0:30 -c 1:00-1:30
    python video_clipper.py input.mp4 -c 10-30 -c 60-90
"""

import argparse
import os
import sys
from pathlib import Path

from moviepy import VideoFileClip, concatenate_videoclips


def parse_time(time_str: str) -> float:
    """
    解析时间字符串为秒数

    支持格式:
    - 秒数: "30", "120"
    - 分:秒: "1:30", "2:45"
    - 时:分:秒: "0:01:30", "1:02:30"

    Args:
        time_str: 时间字符串

    Returns:
        秒数
    """
    parts = time_str.split(":")

    if len(parts) == 1:
        # 纯秒数
        return float(parts[0])
    elif len(parts) == 2:
        # 分:秒
        return float(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:
        # 时:分:秒
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    else:
        raise ValueError(f"无效的时间格式: {time_str}")


def parse_clip(clip_str: str) -> tuple[float, float]:
    """
    解析剪辑时间段字符串

    格式: "开始-结束"，例如 "0:10-0:30" 或 "10-30"

    Args:
        clip_str: 时间段字符串

    Returns:
        (开始秒数, 结束秒数) 元组
    """
    if "-" not in clip_str:
        raise ValueError(f"时间段格式错误，应为 '开始-结束': {clip_str}")

    start_str, end_str = clip_str.split("-", 1)
    start = parse_time(start_str)
    end = parse_time(end_str)

    if start >= end:
        raise ValueError(f"开始时间必须小于结束时间: {clip_str}")

    return start, end


def clip_video(
    input_path: str,
    output_path: str,
    clips: list[tuple[float, float]]
) -> None:
    """
    从视频中剪辑多个片段并合并

    Args:
        input_path: 输入视频路径
        output_path: 输出视频路径
        clips: 时间段列表，每个元素为 (开始秒数, 结束秒数)
    """
    print(f"加载视频: {input_path}")

    # 加载源视频
    video = VideoFileClip(input_path)
    duration = video.duration

    print(f"视频时长: {duration:.2f} 秒")

    # 验证时间段
    for i, (start, end) in enumerate(clips):
        if end > duration:
            raise ValueError(
                f"片段 {i+1} 结束时间 ({end:.2f}s) 超出视频时长 ({duration:.2f}s)"
            )
        print(f"片段 {i+1}: {start:.2f}s - {end:.2f}s ({end-start:.2f}s)")

    # 提取子片段
    subclips = []
    for start, end in clips:
        subclip = video.subclipped(start, end)
        subclips.append(subclip)

    # 拼接片段
    print("正在合并片段...")
    final_clip = concatenate_videoclips(subclips)

    # 输出视频
    print(f"正在输出视频: {output_path}")

    # 获取输出目录
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    # 清理资源
    final_clip.close()
    video.close()

    print(f"完成! 输出文件: {output_path}")
    print(f"输出时长: {final_clip.duration:.2f} 秒")


def main():
    parser = argparse.ArgumentParser(
        description="视频剪辑工具 - 从视频中剪辑多个片段并合并",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s input.mp4 -o output.mp4 -c 0:10-0:30 -c 1:00-1:30
  %(prog)s input.mp4 -c 10-30 -c 60-90
  %(prog)s video.mp4 -c 0:01:00-0:02:30

时间格式支持:
  秒数:     30, 120
  分:秒:    1:30, 2:45
  时:分:秒: 0:01:30, 1:02:30
        """
    )

    parser.add_argument(
        "input",
        help="输入视频文件路径"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出视频文件路径 (默认: clipped_<input>)"
    )

    parser.add_argument(
        "-c", "--clip",
        action="append",
        required=True,
        metavar="TIME",
        help="剪辑时间段，格式: '开始-结束' (可多次指定)"
    )

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 设置默认输出路径
    if args.output is None:
        input_path = Path(args.input)
        args.output = str(input_path.parent / f"clipped_{input_path.name}")

    # 解析时间段
    try:
        clips = [parse_clip(clip_str) for clip_str in args.clip]
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    # 执行剪辑
    try:
        clip_video(args.input, args.output, clips)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
