---
name: manim
description: 使用Manim制作数学教学视频。生成动画视频（无声音），配合剪映AI配音和字幕。解决文字重叠问题。
origin: ECC
---

# Manim 数学教学视频制作

使用 Manim 生成数学讲解动画视频，配合剪映完成配音和字幕。

## When to Activate

- 用户说"制作数学教学视频"
- 用户说"用manim生成视频"
- 用户说"制作数学动画"
- 用户需要演示数学问题的解题过程

## 视频内容结构

**原则：灵活结构，按数学主题定制**

根据数学主题设计合适的场景数量：
- 鸡兔同笼 → 4个场景（问题引入→假设法→方程法→验证）
- 勾股定理 → 3个场景（问题→证明→应用）
- 一元二次方程 → 4个场景（问题→公式→求解→验证）

场景设计指南：
1. **问题引入** - 展示数学题目/背景
2. **方法讲解** - 展示解题方法或公式
3. **步骤演示** - 详细展示计算过程
4. **结论验证** - 总结答案并验证

## 防重叠技术

**核心原则：每个场景前清场，避免文字叠加覆盖**

### 关键实现

```python
class MyScene(Scene):
    def construct(self):
        # 场景1
        self.next_section("场景名")
        # ... 显示内容 ...

        # 清场准备下一个场景
        self.clear()

        # 场景2
        self.next_section("场景名2")
        # ... 显示内容 ...
```

### 布局方式

```python
# 使用VGroup统一布局，避免逐行叠加
step_texts = [Text(step, font_size=28) for step in steps]
steps_group = VGroup(*step_texts).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
steps_group.to_edge(LEFT).shift(DOWN * 0.5)
self.play(FadeIn(steps_group))
```

### 禁止的做法

```python
# ❌ 错误：逐行显示导致叠加
for i, step in enumerate(steps):
    s = Text(step, font_size=28)
    s.to_edge(LEFT).shift(DOWN * (2 - i * 0.7))  # 位置重叠
    self.play(Write(s))  # 新内容覆盖旧内容

# ✅ 正确：VGroup + clear
step_texts = [Text(step, font_size=28) for step in steps]
steps_group = VGroup(*step_texts).arrange(DOWN, buff=0.5)
self.play(FadeIn(steps_group))
```

## 输出文件

1. **视频文件**: `media/videos/.../xxx.mp4` - 动画视频（无声音）
2. **字幕文件**: `subtitles.txt` - 解说词（用于剪映配音）

## 使用流程

1. 与用户确认数学主题和内容结构
2. 根据主题设计场景和脚本
3. 运行 `python3.11 -m manim render --write_to_movie generate_video.py SceneName` 生成视频
4. 用剪映打开视频，导入字幕文件
5. 使用剪映AI配音功能生成配音
6. 导出最终视频

## 依赖安装

```bash
# 需要 Python 3.11+
brew install python@3.11
python3.11 -m pip install manim
```

## 运行命令

```bash
cd skills/manim

# 预览
python3.11 -m manim -p generate_video.py SceneName

# 输出视频
python3.11 -m manim render --write_to_movie generate_video.py SceneName
```

## 实现文件

- `generate_video.py` - Manim场景代码
- `subtitles.txt` - 字幕解说词
- `media/videos/` - 生成的视频目录