"""
Manim 数学教学视频生成脚本
模板式设计，根据不同数学主题生成对应视频

使用方法:
    python3.11 generate_video.py          # 生成字幕
    python3.11 -m manim -p generate_video.py SceneName  # 预览
    python3.11 -m manim render --write_to_movie generate_video.py SceneName  # 输出视频
"""

from manim import *
import os

OUTPUT_DIR = "./output"
SUBTITLE_FILE = "subtitles.txt"


class MathVideoTemplate(Scene):
    """
    数学视频模板 - 可根据不同主题自定义内容

    使用方式:
    1. 定义 self.scenes 列表，包含多个场景
    2. 每个场景包含: title, lines, subtitle_text
    3. 系统自动处理场景切换和防重叠
    """

    # 子类需要定义 scenes 属性
    # scenes = [
    #     {
    #         "title": "场景标题",
    #         "title_color": YELLOW,
    #         "title_size": 36,
    #         "lines": ["第1行内容", "第2行内容", ...],
    #         "line_size": 28,
    #         "subtitle": "场景的解说词，用于AI配音"
    #     },
    #     ...
    # ]

    def construct(self):
        if not hasattr(self, 'scenes'):
            raise NotImplementedError("子类必须定义 self.scenes")

        for i, scene in enumerate(self.scenes):
            # 场景标题
            if scene.get("title"):
                title = Text(
                    scene["title"],
                    font_size=scene.get("title_size", 36),
                    color=scene.get("title_color", YELLOW)
                )
                self.play(Write(title))
                self.wait(scene.get("title_wait", 0.5))

            # 内容区域
            if scene.get("lines"):
                line_size = scene.get("line_size", 28)
                texts = [Text(line, font_size=line_size) for line in scene["lines"]]
                content_group = VGroup(*texts)

                # 根据行数自动布局
                if len(texts) == 1:
                    content_group.move_to(ORIGIN)
                else:
                    content_group.arrange(
                        DOWN,
                        aligned_edge=LEFT,
                        buff=scene.get("line_buff", 0.5)
                    )

                content_group.to_edge(LEFT).shift(DOWN * 0.5)
                self.play(FadeIn(content_group))

                wait_time = scene.get("content_wait", 3)
                self.wait(wait_time)

            # 清场准备下一个场景（最后一个场景不清场）
            if i < len(self.scenes) - 1:
                self.clear()

        # 最终结论/结束语
        if hasattr(self, 'conclusion'):
            conclusion = Text(
                self.conclusion,
                font_size=48,
                color=YELLOW
            )
            self.play(FadeIn(conclusion))
            self.wait(2)


class ChickenRabbitVideo(MathVideoTemplate):
    """鸡兔同笼视频 - 演示如何自定义场景"""

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
            "content_wait": 3,
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
            "content_wait": 3,
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


def generate_subtitles(scenes=None):
    """根据场景生成字幕文件"""
    if scenes is None:
        # 默认使用鸡兔同笼场景
        from generate_video import ChickenRabbitVideo
        scenes = ChickenRabbitVideo.scenes

    subtitles_parts = []

    for i, scene in enumerate(scenes):
        if scene.get("subtitle"):
            subtitles_parts.append(f"Scene {i+1} - {scene.get('title', '场景' + str(i+1))}")
            subtitles_parts.append(scene["subtitle"])
            subtitles_parts.append("")  # 空行分隔

    # 添加结语
    if hasattr(ChickenRabbitVideo, 'conclusion'):
        subtitles_parts.append(f"结语\nChickenRabbitVideo.conclusion")
        subtitles_parts.append("所以答案是鸡23只，兔12只。谢谢观看！")

    subtitles = "\n".join(subtitles_parts)

    with open(SUBTITLE_FILE, 'w', encoding='utf-8') as f:
        f.write(subtitles)

    print(f"字幕文件已生成: {SUBTITLE_FILE}")
    return subtitles


if __name__ == "__main__":
    print("\n" + "="*50)
    print("Manim 数学教学视频生成器")
    print("="*50)

    # 生成字幕
    generate_subtitles()

    print("\n生成完成！")
    print("="*50)
    print("1. 运行 python3.11 -m manim -p generate_video.py ChickenRabbitVideo 预览")
    print("2. 运行 python3.11 -m manim render --write_to_movie generate_video.py ChickenRabbitVideo 输出视频")
    print(f"3. 字幕文件: {SUBTITLE_FILE}")
    print("4. 用剪映导入视频和字幕，完成配音")
    print("="*50)

    print("\n如需创建新主题视频，请继承 MathVideoTemplate 类并定义 scenes 属性")