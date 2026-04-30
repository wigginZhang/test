---
name: manim
description: 使用Manim制作数学教学视频。支持图形化演示、转场动画、标准字幕(SRT)、AI配音(TTS)、音画同步。
origin: ECC
---

# Manim 数学教学视频制作 V2.0

使用 Manim 生成数学讲解动画视频，支持图形化教学、AI配音、标准字幕。

## When to Activate

- 用户说"制作数学教学视频"
- 用户说"用manim生成视频"
- 用户说"制作数学动画"
- 用户需要演示数学问题的解题过程

## 核心特性

| 特性 | 说明 |
|------|------|
| **图形化教学** | 使用图形、动画演示数学概念 |
| **转场动画** | FadeOut/FadeIn 平滑切换 |
| **关键高亮** | Indicate、Circumscribe 高亮重点 |
| **互动留白** | 思考提示，增强教学效果 |
| **标准字幕** | SRT时间轴文件，可导入剪映 |
| **AI配音** | edge-tts 生成配音（可选） |
| **灵活配置** | 命令行参数支持自定义 |

## 视频内容结构

**原则：灵活结构，按数学主题定制**

根据数学主题设计合适的场景数量：
- 鸡兔同笼 → 4个场景（问题引入→假设法→方程法→验证）
- 其他主题可自定义场景

场景设计指南：
1. **问题引入** - 展示数学题目/背景
2. **方法讲解** - 展示解题方法或公式
3. **步骤演示** - 详细展示计算过程
4. **结论验证** - 总结答案并验证

## 命令行参数

```bash
python3.11 generate_video.py [OPTIONS]

选项:
  -t, --topic TOPIC          数学主题 (默认: chicken_rabbit)
  -r WIDTH HEIGHT           分辨率 (默认: 1920 1080)
  -f, --frame-rate FPS      帧率 (默认: 60)
  -o, --output-dir DIR      输出目录 (默认: ./output)
  --voice                   生成AI配音
  --subtitle {srt,burn,none} 字幕处理: srt=生成文件, burn=烧录硬字幕, none=不生成
  --voice-voice VOICE       TTS语音角色 (默认: zh-CN-XiaoxiaoNeural)
```

### 示例

```bash
# 基本使用
python3.11 generate_video.py --topic chicken_rabbit

# 带配音和字幕
python3.11 generate_video.py --topic chicken_rabbit --voice --subtitle burn

# 自定义分辨率和帧率
python3.11 generate_video.py -r 1920 1080 -f 60
```

## 生成视频

```bash
# 预览
python3.11 -m manim -p generate_video.py ChickenRabbitVideo

# 输出视频
python3.11 -m manim render --write_to_movie generate_video.py ChickenRabbitVideo
```

## 图形化教学实现

### 核心原则：避免文字叠加

```python
# ✅ 正确：场景切换时清场
if i < len(self.scenes) - 1:
    self.clear()

# ✅ 正确：使用VGroup统一布局
texts = [Text(line, font_size=28) for line in scene["lines"]]
content_group = VGroup(*texts).arrange(DOWN, buff=0.5)
self.play(FadeIn(content_group))

# ❌ 错误：逐行显示导致叠加
for i, step in enumerate(steps):
    s = Text(step)
    self.play(Write(s))  # 新内容覆盖旧内容
```

### 转场与高亮

```python
# 场景切换使用淡出
self.play(FadeOut(title), FadeOut(content_group))
self.clear()

# 关键数字高亮
self.play(Indicate(key_number, color=BLUE, scale_factor=1.5))

# 公式高亮
self.play(Circumscribe(equation, color=YELLOW))
```

### 互动留白

```python
# 思考提示
prompt = Text("同学们先思考一下...", font_size=24, color=GRAY)
prompt.to_edge(DOWN)
self.play(FadeIn(prompt))
self.wait(3)  # 留白时间
```

## 依赖安装

```bash
# Python 3.11+
brew install python@3.11
python3.11 -m pip install manim

# 可选：AI配音
python3.11 -m pip install edge-tts

# 可选：视频处理
brew install ffmpeg
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `{topic}_subtitles.srt` | 标准SRT字幕文件（带时间轴） |
| `{topic}_voice.mp3` | AI配音文件 |
| `media/videos/.../xxx.mp4` | 动画视频 |

## 使用流程

1. **生成字幕和配置**
   ```bash
   python3.11 generate_video.py --topic chicken_rabbit --subtitle srt
   ```

2. **生成视频**
   ```bash
   python3.11 -m manim render --write_to_movie generate_video.py ChickenRabbitVideo
   ```

3. **导入剪映**
   - 打开视频
   - 导入SRT字幕文件
   - 使用AI配音功能
   - 导出最终视频

## 代码扩展

创建新的数学主题视频：

```python
class MyMathVideo(MathVideoTemplate):
    scenes = [
        {
            "title": "问题标题",
            "subtitle": "解说词",
            "lines": ["内容行1", "内容行2"],
        },
        # 更多场景...
    ]
    conclusion = "最终结论"
```

## 实现文件

- `generate_video.py` - Manim场景代码（含模板）
- `{topic}_subtitles.srt` - SRT字幕文件
- `media/videos/` - 生成的视频目录