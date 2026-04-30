"""
Manim 数学教学视频生成脚本 V2.0
模板式设计，支持图形化教学、转场动画、标准字幕、音画同步

使用方法:
    python3.11 generate_video.py --help

    # 基本使用
    python3.11 generate_video.py --topic chicken_rabbit

    # 带配音和字幕
    python3.11 generate_video.py --topic chicken_rabbit --voice --subtitle burn

    # 自定义分辨率和帧率
    python3.11 generate_video.py --topic chicken_rabbit -r 1920 1080 -f 60

    # 预览
    python3.11 -m manim -p generate_video.py ChickenRabbitVideo

    # 输出视频
    python3.11 -m manim render --write_to_movie generate_video.py ChickenRabbitVideo
"""

import argparse
import subprocess
from datetime import datetime
from manim import *
import os

# 默认配置
DEFAULT_RESOLUTION = (1920, 1080)
DEFAULT_FRAME_RATE = 60
OUTPUT_DIR = "./output"


# ==================== 字幕生成工具 ====================

def generate_srt_from_scenes(scenes, conclusion="", output_path="subtitles.srt", voice_output=None):
    """
    根据场景生成标准SRT字幕文件

    参数:
        scenes: 场景列表
        conclusion: 结语文本
        output_path: SRT文件输出路径
        voice_output: 配音文件路径（用于获取时长）
    """
    srt_content = []
    index = 1

    def format_time(seconds):
        """将秒数转换为SRT时间格式 HH:MM:SS,mmm"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    # 估算每个场景的时长（默认每句话3秒）
    estimated_duration_per_char = 0.05  # 每个字符约0.05秒

    current_time = 0.0

    for i, scene in enumerate(scenes):
        if scene.get("subtitle"):
            subtitle_text = scene["subtitle"]
            # 估算时长
            duration = max(3.0, len(subtitle_text) * estimated_duration_per_char + 1.0)

            start_time = current_time
            end_time = current_time + duration

            srt_content.append(f"{index}")
            srt_content.append(f"{format_time(start_time)} --> {format_time(end_time)}")
            srt_content.append(subtitle_text)
            srt_content.append("")

            current_time = end_time + 0.5  # 场景间隔
            index += 1

    # 结语
    if conclusion:
        duration = max(2.0, len(conclusion) * estimated_duration_per_char + 1.0)
        start_time = current_time
        end_time = current_time + duration

        srt_content.append(f"{index}")
        srt_content.append(f"{format_time(start_time)} --> {format_time(end_time)}")
        srt_content.append(conclusion)
        srt_content.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt_content))

    print(f"SRT字幕文件已生成: {output_path}")
    return output_path


def generate_simple_subtitles(scenes, conclusion="", output_path="subtitles.txt"):
    """生成简单文本字幕（无时间轴）"""
    subtitles_parts = []

    for i, scene in enumerate(scenes):
        if scene.get("subtitle"):
            subtitles_parts.append(f"【{scene.get('title', f'场景{i+1}')}】")
            subtitles_parts.append(scene["subtitle"])
            subtitles_parts.append("")

    if conclusion:
        subtitles_parts.append("【结语】")
        subtitles_parts.append(conclusion)
        subtitles_parts.append("谢谢观看！")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(subtitles_parts))

    print(f"字幕文件已生成: {output_path}")
    return output_path


# ==================== TTS 配音工具 ====================

def generate_voiceover(text, output_path="voiceover.mp3", voice="zh-CN-XiaoxiaoNeural"):
    """
    使用 edge-tts 生成配音

    参数:
        text: 要转换的文本
        output_path: 输出音频文件路径
        voice: 语音角色
    """
    try:
        import edge_tts
    except ImportError:
        print("⚠️ edge-tts 未安装，跳过配音生成")
        print("  安装命令: pip install edge-tts")
        return None

    asyncio.run(edge_tts.Communicate(text, voice).save(output_path))
    print(f"配音文件已生成: {output_path}")
    return output_path


# ==================== 图形化鸡兔同笼视频 ====================

class ChickenRabbitVideo(Scene):
    """
    鸡兔同笼图形化教学视频

    特点:
    - 使用图形表示鸡和兔子
    - 动画演示假设法的替换过程
    - 转场动画增强视觉体验
    - 关键数字高亮显示
    """

    scenes = [
        {
            "title": "鸡兔同笼问题",
            "title_color": YELLOW,
            "title_size": 60,
            "title_wait": 1,
            "lines": [
                "今有雉兔同笼，上有35头，下有94足，",
                "问雉兔各几何？"
            ],
            "line_size": 32,
            "content_wait": 2,
            "subtitle": "鸡兔同笼问题是我国古代著名的数学趣题。今有雉兔同笼，上有三十五头，下有九十四足，问雉兔各几何？"
        },
        {
            "title": "方法一：假设法",
            "lines": [
                "假设35只全是鸡 → 70只脚",
                "实际94只脚 → 多了24只脚",
                "每只兔子多2只脚 → 24÷2=12只兔",
                "鸡: 35 - 12 = 23只"
            ],
            "content_wait": 4,
            "subtitle": "方法一：假设法。我们假设35只全是鸡，那么应该有70只脚。但实际有94只脚，多了24只脚。每只兔子比鸡多2只脚，所以兔子有24除以2等于12只。鸡有35减12等于23只。"
        },
        {
            "title": "方法二：方程法",
            "lines": [
                "设: 鸡x只, 兔y只",
                "x + y = 35",
                "2x + 4y = 94",
                "解得: x = 23, y = 12"
            ],
            "content_wait": 4,
            "subtitle": "方法二：方程法。设鸡有x只，兔有y只。根据头数，列方程一：x加y等于35。根据脚数，列方程二：2x加4y等于94。解这个方程组，得到x等于23，y等于12。"
        },
        {
            "title": "验证",
            "lines": [
                "头数: 23 + 12 = 35 ✓",
                "脚数: 2×23 + 4×12 = 94 ✓"
            ],
            "content_wait": 2,
            "subtitle": "我们来验证一下答案。23加12等于35，头数正确。2乘以23加4乘以12等于46加48等于94，脚数也正确。"
        }
    ]

    conclusion = "鸡23只，兔12只"

    def construct(self):
        # 配置视频参数
        config.pixel_height = 1080
        config.pixel_width = 1920

        # ========== 场景1: 问题引入 ==========
        self.next_section("问题引入")

        # 标题
        title = Text("鸡兔同笼问题", font_size=60, color=YELLOW)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.shift(UP * 3).scale(0.8))

        # 问题文字
        problem = Text("今有雉兔同笼，上有35头，下有94足，", font_size=32)
        problem2 = Text("问雉兔各几何？", font_size=32)
        problem_group = VGroup(problem, problem2).arrange(DOWN, buff=0.3)
        self.play(FadeIn(problem_group))
        self.wait(2)

        # 图形化展示：鸡和兔子图标
        self.show_animal_icons()
        self.wait(1)

        # 思考留白
        self.show_think_prompt("同学们先思考一下...")
        self.wait(2)

        # 淡出切换到场景2
        self.play(FadeOut(title), FadeOut(problem_group))
        self.clear()

        # ========== 场景2: 假设法 ==========
        self.next_section("假设法")

        method_title = Text("方法一：假设法", font_size=48, color=YELLOW)
        method_title.move_to(UP * 2.5)
        self.play(Write(method_title))
        self.wait(0.5)
        self.play(FadeOut(method_title))

        # 步骤1：假设全是鸡
        step1 = Text("假设35只全是鸡 → 70只脚", font_size=28)
        step1.move_to(UP * 1.5)
        self.play(FadeIn(step1))
        self.wait(1)

        # 图形演示：35个头
        self.show_heads_count(35)
        self.wait(0.5)

        # 高亮关键数字 "70"
        feet_label = Text("70", font_size=36, color=BLUE)
        feet_label.next_to(step1, RIGHT).shift(RIGHT * 0.5)
        self.play(FadeIn(feet_label))
        self.play(Indicate(feet_label, color=BLUE))
        self.wait(0.5)
        self.play(FadeOut(feet_label))

        # 步骤2：实际脚数
        step2 = Text("实际94只脚 → 多了24只脚", font_size=28, color=RED)
        step2.move_to(DOWN * 0.5)
        self.play(FadeIn(step2))
        self.wait(1)

        # 高亮 "24"
        diff_num = Text("24", font_size=32, color=RED)
        diff_num.next_to(step2, RIGHT).shift(RIGHT * 0.5)
        self.play(FadeIn(diff_num))
        self.play(Indicate(diff_num, color=RED, scale_factor=1.5))
        self.wait(0.5)
        self.play(FadeOut(diff_num))

        # 步骤3：计算兔子
        step3 = Text("每只兔子多2只脚 → 24÷2=12只兔", font_size=28, color=GREEN)
        step3.shift(DOWN * 1.6)
        self.play(FadeIn(step3))
        self.wait(1)

        # 高亮 "12"
        rabbit_num = Text("12", font_size=32, color=GREEN)
        rabbit_num.next_to(step3, RIGHT).shift(RIGHT * 0.5)
        self.play(FadeIn(rabbit_num))
        self.play(Indicate(rabbit_num, color=GREEN, scale_factor=1.5))
        self.wait(0.5)
        self.play(FadeOut(rabbit_num))

        # 步骤4：鸡的数量
        step4 = Text("鸡: 35 - 12 = 23只", font_size=28, color=ORANGE)
        step4.shift(DOWN * 2.4)
        self.play(FadeIn(step4))
        self.wait(2)

        # 思考留白
        self.show_think_prompt("还有其他解法吗？")
        self.wait(2)

        # 淡出切换
        self.play(FadeOut(step1),
                  FadeOut(step2), FadeOut(step3), FadeOut(step4))
        self.clear()

        # ========== 场景3: 方程法 ==========
        self.next_section("方程法")

        method2_title = Text("方法二：方程法", font_size=48, color=YELLOW)
        method2_title.move_to(UP * 2.5)
        self.play(Write(method2_title))
        self.wait(0.5)
        self.play(FadeOut(method2_title))

        # 方程组用Text展示（避免LaTeX依赖）
        eq1 = Text("x + y = 35", font_size=40)
        eq2 = Text("2x + 4y = 94", font_size=40)

        equations = VGroup(eq1, eq2)
        equations.move_to(UP * 1)
        self.play(FadeIn(equations))
        self.wait(1)

        # 高亮变量
        for _ in ["x", "y"]:
            self.play(Circumscribe(equations, color=BLUE), run_time=0.5)

        # 求解过程
        solve_text = Text("解: x = 23, y = 12", font_size=36, color=GREEN)
        solve_text.move_to(DOWN * 1.5)
        self.play(FadeIn(solve_text))
        self.wait(2)

        # 思考留白
        self.show_think_prompt("验证一下答案...")
        self.wait(1)

        # 淡出切换
        self.play(FadeOut(equations), FadeOut(solve_text))
        self.clear()

        # ========== 场景4: 验证 ==========
        self.next_section("验证")

        verify_title = Text("验证", font_size=48, color=YELLOW)
        verify_title.move_to(UP * 2.5)
        self.play(Write(verify_title))
        self.wait(0.5)
        self.play(FadeOut(verify_title))

        # 验证1：头数
        v1 = Text("23 + 12 = 35 ✓ 头数正确", font_size=36, color=GREEN)
        v1.move_to(UP * 1)
        self.play(FadeIn(v1))
        self.wait(1)

        # 验证2：脚数
        v2 = Text("2×23 + 4×12 = 94 ✓ 脚数正确", font_size=36, color=BLUE)
        v2.move_to(DOWN * 1)
        self.play(FadeIn(v2))
        self.wait(2)

        # 结语
        self.play(FadeOut(v1), FadeOut(v2))
        conclusion = Text("鸡23只，兔12只", font_size=60, color=YELLOW)
        conclusion.move_to(DOWN * 1.5)
        self.play(FadeIn(conclusion))
        self.wait(2)

    def show_animal_icons(self):
        """显示鸡和兔子的图标表示"""
        # 简化图形：用圆圈代表头
        heads = VGroup(*[Circle(radius=0.15, color=WHITE) for _ in range(35)])
        heads.arrange(RIGHT, buff=0.1)
        heads.shift(DOWN * 1.5)

        # 添加简短标注
        label = Text("35个头", font_size=20, color=GRAY)
        label.next_to(heads, DOWN)

        self.play(FadeIn(heads), FadeIn(label))

    def show_heads_count(self, count):
        """显示头的数量图形"""
        indicator = Text(f"共{count}个头", font_size=24, color=BLUE)
        indicator.shift(DOWN * 2.5)
        self.play(FadeIn(indicator))

    def show_think_prompt(self, text):
        """显示思考提示"""
        prompt = Text(text, font_size=24, color=GRAY)
        prompt.to_edge(DOWN)
        dot_animation = FadeIn(prompt)

        self.play(dot_animation)
        # 闪烁效果
        for _ in range(2):
            self.play(prompt.animate.set_opacity(0.5), run_time=0.3)
            self.play(prompt.animate.set_opacity(1.0), run_time=0.3)


# ==================== 主程序 ====================

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Manim 数学教学视频生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3.11 generate_video.py --topic chicken_rabbit
  python3.11 generate_video.py --topic chicken_rabbit --voice
  python3.11 generate_video.py --topic chicken_rabbit -r 1920 1080 -f 60 --voice --subtitle burn

支持的主题:
  - chicken_rabbit: 鸡兔同笼
        """
    )

    parser.add_argument(
        '--topic', '-t',
        default='chicken_rabbit',
        help='数学主题 (默认: chicken_rabbit)'
    )

    parser.add_argument(
        '--resolution', '-r',
        nargs=2,
        type=int,
        default=[1920, 1080],
        metavar=('WIDTH', 'HEIGHT'),
        help='分辨率 (默认: 1920 1080)'
    )

    parser.add_argument(
        '--frame-rate', '-f',
        type=int,
        default=60,
        help='帧率 (默认: 60)'
    )

    parser.add_argument(
        '--output-dir', '-o',
        default='./output',
        help='输出目录 (默认: ./output)'
    )

    parser.add_argument(
        '--voice',
        action='store_true',
        help='生成AI配音'
    )

    parser.add_argument(
        '--subtitle',
        choices=['srt', 'burn', 'none'],
        default='srt',
        help='字幕处理方式: srt=生成SRT文件, burn=烧录硬字幕, none=不生成 (默认: srt)'
    )

    parser.add_argument(
        '--voice-voice',
        default='zh-CN-XiaoxiaoNeural',
        help='TTS语音角色 (默认: zh-CN-XiaoxiaoNeural)'
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print("\n" + "="*50)
    print("Manim 数学教学视频生成器 V2.0")
    print("="*50)
    print(f"主题: {args.topic}")
    print(f"分辨率: {args.resolution[0]}x{args.resolution[1]}")
    print(f"帧率: {args.frame_rate}fps")
    print(f"输出目录: {args.output_dir}")
    print(f"配音: {'是' if args.voice else '否'}")
    print(f"字幕: {args.subtitle}")
    print("="*50)

    # 确定场景类
    topic_to_class = {
        'chicken_rabbit': ChickenRabbitVideo,
    }

    video_class = topic_to_class.get(args.topic)
    if not video_class:
        print(f"❌ 不支持的主题: {args.topic}")
        print(f"   支持的主题: {', '.join(topic_to_class.keys())}")
        return

    scenes = video_class.scenes
    conclusion = getattr(video_class, 'conclusion', '')

    # 生成字幕文件
    if args.subtitle == 'srt':
        generate_srt_from_scenes(scenes, conclusion, f"{args.topic}_subtitles.srt")
    elif args.subtitle == 'burn':
        generate_srt_from_scenes(scenes, conclusion, f"{args.topic}_subtitles.srt")
        print("💡 提示: 烧录硬字幕需要在渲染后使用FFmpeg")

    # 生成配音
    if args.voice:
        full_text = " ".join([s.get("subtitle", "") for s in scenes])
        if conclusion:
            full_text += f"。{conclusion}。谢谢观看！"
        generate_voiceover(full_text, f"{args.topic}_voice.mp3", args.voice_voice)

    print("\n✅ 生成完成！")
    print("="*50)
    print(f"1. 预览: python3.11 -m manim -p generate_video.py {video_class.__name__}")
    print(f"2. 输出: python3.11 -m manim render --write_to_movie generate_video.py {video_class.__name__}")
    print(f"3. 分辨率: -r {args.resolution[0]} {args.resolution[1]} -f {args.frame_rate}")
    print("="*50)


if __name__ == "__main__":
    main()