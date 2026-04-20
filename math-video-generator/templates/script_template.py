"""
苹果销售问题 - 数学教学视频完整实现
根据分镜脚本实现每一幕动画，确保音画同步
"""

from manim import *
import json
import os


class AppleProblemScene(Scene):
    """苹果销售问题教学视频"""

    # ========== 1. 配置 ==========
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    COLORS = {
        'background': '#1a1a2e',
        'primary': '#4ecca3',      # 第一天（青色）
        'secondary': '#e94560',    # 第二天（红色）
        'highlight': '#ffc107',    # 剩余（黄色）
        'text': '#ffffff',
        'text_secondary': '#aaaaaa',  # 次要文字
        'success': '#28a745',      # 答案（绿色）
        'title': '#667eea',
    }

    # ========== 2. 幕信息 ==========
    SCENES = [
        (1, "开场", "audio_001_开场.wav", 10.08),
        (2, "已知条件", "audio_002_已知条件.wav", 10.72),
        (3, "等量关系", "audio_003_等量关系.wav", 8.88),
        (4, "设未知数", "audio_004_设未知数.wav", 7.68),
        (5, "建立方程", "audio_005_建立方程.wav", 11.28),
        (6, "步骤1", "audio_006_步骤1.wav", 7.76),
        (7, "步骤2", "audio_007_步骤2.wav", 10.80),
        (8, "步骤3", "audio_008_步骤3.wav", 9.20),
        (9, "验证", "audio_009_验证.wav", 16.72),
        (10, "总结", "audio_010_总结.wav", 12.08),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_dir = "audio"

    # ========== 3. 音频管理 ==========
    def add_scene_audio(self, scene_num):
        """添加指定幕的音频"""
        for sn, name, audio_file, duration in self.SCENES:
            if sn == scene_num:
                audio_path = os.path.join(self.audio_dir, audio_file)
                if os.path.exists(audio_path):
                    self.add_sound(audio_path)
                    return duration
                else:
                    print(f"Warning: Audio not found: {audio_path}")
                    return duration
        return 0

    # ========== 4. 主流程 ==========
    def construct(self):
        """主构造流程"""
        self.camera.background_color = self.COLORS['background']

        # 执行每一幕
        for scene_num, scene_name, audio_file, duration in self.SCENES:
            print(f"\n=== Scene {scene_num}: {scene_name} ({duration}s) ===")
            self.play_scene(scene_num, scene_name, duration)

    # ========== 5. 每幕动画实现 ==========
    def play_scene(self, scene_num, scene_name, duration):
        """播放单幕动画"""

        # 添加音频
        audio_duration = self.add_scene_audio(scene_num)

        # 根据幕号实现不同动画
        if scene_num == 1:
            self.play_scene_1(duration)
        elif scene_num == 2:
            self.play_scene_2(duration)
        elif scene_num == 3:
            self.play_scene_3(duration)
        elif scene_num == 4:
            self.play_scene_4(duration)
        elif scene_num == 5:
            self.play_scene_5(duration)
        elif scene_num == 6:
            self.play_scene_6(duration)
        elif scene_num == 7:
            self.play_scene_7(duration)
        elif scene_num == 8:
            self.play_scene_8(duration)
        elif scene_num == 9:
            self.play_scene_9(duration)
        elif scene_num == 10:
            self.play_scene_10(duration)

        # 确保画面时长 >= 音频时长
        if duration > audio_duration:
            self.wait(duration - audio_duration)

    # ========== 幕动画详细实现 ==========
    def play_scene_1(self, duration):
        """第1幕：开场引入"""
        # 标题
        title = Text("苹果销售问题", font_size=64, color=self.COLORS['title'])
        title.move_to(UP * 2)

        # 题目
        problem = Text(
            "第一天卖出30%，第二天卖出120kg，还剩160kg",
            font_size=42,
            color=self.COLORS['text']
        )
        problem.move_to(DOWN * 0.5)

        # 关键数字高亮
        keywords = VGroup(
            Text("30%", font_size=48, color=self.COLORS['primary']),
            Text("120kg", font_size=48, color=self.COLORS['secondary']),
            Text("160kg", font_size=48, color=self.COLORS['highlight']),
        )
        keywords.arrange(RIGHT, buff=1.5)
        keywords.move_to(DOWN * 2)

        # 动画
        self.play(FadeIn(title), run_time=1)
        self.play(FadeIn(problem), run_time=1.5)
        self.play(
            keywords[0].animate.scale(1.2),
            keywords[1].animate.scale(1.2),
            keywords[2].animate.scale(1.2),
            run_time=2
        )

        self.wait(duration - 4.5)

        # 退场
        self.play(FadeOut(title), FadeOut(problem), FadeOut(keywords))

    def play_scene_2(self, duration):
        """第2幕：已知条件"""
        # 标题
        subtitle = Text("已知条件分析", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 3)

        # 三条条件
        cond1 = Text("① 第一天：总数的 30%", font_size=42, color=self.COLORS['primary'])
        cond2 = Text("② 第二天：120 kg", font_size=42, color=self.COLORS['secondary'])
        cond3 = Text("③ 剩余：160 kg", font_size=42, color=self.COLORS['highlight'])

        conditions = VGroup(cond1, cond2, cond3)
        conditions.arrange(DOWN, buff=0.5)
        conditions.move_to(UP * 0.5)

        # 动画：逐条显示
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(cond1), run_time=2)
        self.play(FadeIn(cond2), run_time=2)
        self.play(FadeIn(cond3), run_time=2)

        self.wait(duration - 7)

        # 退场
        self.play(FadeOut(subtitle), FadeOut(conditions))

    def play_scene_3(self, duration):
        """第3幕：等量关系"""
        # 标题
        subtitle = Text("等量关系", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 2)

        # 等量关系公式
        relation = Text(
            "总量 = 第一天 + 第二天 + 剩余",
            font_size=42,
            color=self.COLORS['text']
        )
        relation.move_to(UP * 0.5)

        # 条形图示意
        bar_total = Rectangle(width=10, height=0.5, color=self.COLORS['title'])
        bar_day1 = Rectangle(width=3, height=0.5, color=self.COLORS['primary'])
        bar_day2 = Rectangle(width=3, height=0.5, color=self.COLORS['secondary'])
        bar_remain = Rectangle(width=4, height=0.5, color=self.COLORS['highlight'])

        bar_total.move_to(DOWN * 1)
        bar_day1.move_to(DOWN * 2)
        bar_day2.next_to(bar_day1, RIGHT, buff=0)
        bar_remain.next_to(bar_day2, RIGHT, buff=0)

        # 动画
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(relation), run_time=1.5)
        self.play(FadeIn(bar_total), run_time=1)
        self.play(
            Transform(bar_total.copy(), bar_day1),
            Transform(bar_total.copy(), bar_day2),
            Transform(bar_total.copy(), bar_remain),
            run_time=3
        )

        self.wait(duration - 6.5)

        # 退场
        self.play(
            FadeOut(subtitle), FadeOut(relation),
            FadeOut(bar_total), FadeOut(bar_day1),
            FadeOut(bar_day2), FadeOut(bar_remain)
        )

    def play_scene_4(self, duration):
        """第4幕：设未知数"""
        # 标题
        subtitle = Text("设未知数", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 2)

        # 设x
        x_text = Text("设原有苹果有 x 千克", font_size=48, color=self.COLORS['text'])
        x_symbol = Text("x", font_size=72, color=self.COLORS['primary'])
        x_unit = Text("千克", font_size=42, color=self.COLORS['text'])

        x_text.move_to(UP * 0.5)
        x_symbol.move_to(DOWN * 1)
        x_unit.next_to(x_symbol, RIGHT)

        # 动画
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(x_text), run_time=2)
        self.play(FadeIn(x_symbol), FadeIn(x_unit), run_time=1.5)
        self.play(x_symbol.animate.scale(1.3), run_time=1)

        self.wait(duration - 5.5)

        # 退场
        self.play(FadeOut(subtitle), FadeOut(x_text), FadeOut(x_symbol), FadeOut(x_unit))

    def play_scene_5(self, duration):
        """第5幕：建立方程"""
        # 标题
        subtitle = Text("建立方程", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 3)

        # 方程
        equation = Text("x = 0.3x + 120 + 160", font_size=56, color=self.COLORS['text'])

        # 高亮项
        eq_03x = Text("0.3x", font_size=56, color=self.COLORS['primary'])
        eq_120 = Text("120", font_size=56, color=self.COLORS['secondary'])
        eq_160 = Text("160", font_size=56, color=self.COLORS['highlight'])

        equation.move_to(UP * 0.5)

        # 动画
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(equation), run_time=2)

        # 高亮闪烁
        self.play(equation.animate.set_color(self.COLORS['primary']), run_time=1)
        self.play(equation.animate.set_color(self.COLORS['secondary']), run_time=1)
        self.play(equation.animate.set_color(self.COLORS['text']), run_time=1)

        self.wait(duration - 6)

        # 退场
        self.play(FadeOut(subtitle), FadeOut(equation))

    def play_scene_6(self, duration):
        """第6幕：解方程步骤1"""
        # 标题
        subtitle = Text("步骤1：移项整理", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 3)

        # 原方程
        original = Text("x = 0.3x + 120 + 160", font_size=42, color=self.COLORS['text'])
        original.move_to(UP * 1)

        # 移项后
        new_eq = Text("x - 0.3x = 280", font_size=42, color=self.COLORS['text'])
        new_eq.move_to(DOWN * 0.5)

        # 箭头
        arrow = Arrow(UP * 0.8, DOWN * 0.3, color=self.COLORS['highlight'])

        # 动画
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(original), run_time=2)
        self.play(FadeIn(arrow), run_time=1)
        self.play(FadeIn(new_eq), run_time=2)

        self.wait(duration - 6)

        # 退场
        self.play(FadeOut(subtitle), FadeOut(original), FadeOut(arrow), FadeOut(new_eq))

    def play_scene_7(self, duration):
        """第7幕：解方程步骤2"""
        # 标题
        subtitle = Text("步骤2：合并同类项", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 3)

        # 上一步方程
        previous = Text("x - 0.3x = 280", font_size=42, color=self.COLORS['text'])
        previous.move_to(UP * 1)

        # 计算过程
        calc = Text("(1 - 0.3)x = 0.7x", font_size=36, color=self.COLORS['text_secondary'])
        calc.move_to(DOWN * 0.5)

        # 新方程
        new_eq = Text("0.7x = 280", font_size=56, color=self.COLORS['highlight'])
        new_eq.move_to(DOWN * 2)

        # 动画
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(previous), run_time=2)
        self.play(FadeIn(calc), run_time=2)
        self.play(FadeIn(new_eq), run_time=2)
        self.play(new_eq.animate.scale(1.2), run_time=1)

        self.wait(duration - 8)

        # 退场
        self.play(
            FadeOut(subtitle), FadeOut(previous),
            FadeOut(calc), FadeOut(new_eq)
        )

    def play_scene_8(self, duration):
        """第8幕：解方程步骤3"""
        # 标题
        subtitle = Text("步骤3：求解x", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 3)

        # 上一步方程
        previous = Text("0.7x = 280", font_size=42, color=self.COLORS['text'])
        previous.move_to(UP * 1)

        # 计算
        calc = Text("x = 280 ÷ 0.7", font_size=36, color=self.COLORS['text_secondary'])
        calc.move_to(DOWN * 0.5)

        # 最终答案
        result = Text("x = 400 千克", font_size=72, color=self.COLORS['success'])
        result.move_to(DOWN * 2)

        # 动画
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(previous), run_time=2)
        self.play(FadeIn(calc), run_time=1)
        self.play(FadeIn(result), run_time=2)
        self.play(result.animate.scale(1.3), run_time=1)

        self.wait(duration - 7)

        # 退场
        self.play(FadeOut(subtitle), FadeOut(previous), FadeOut(calc))
        # result保留到下一幕

    def play_scene_9(self, duration):
        """第9幕：验证答案"""
        # 标题
        subtitle = Text("验证答案", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 3)

        # 答案（从上一幕保留）
        result = Text("x = 400 千克", font_size=48, color=self.COLORS['success'])
        result.move_to(UP * 1)

        # 验证过程
        check1 = Text("第一天：400×30% = 120kg ✓", font_size=36, color=self.COLORS['primary'])
        check2 = Text("第二天：120kg ✓", font_size=36, color=self.COLORS['secondary'])
        check3 = Text("剩余：400-120-120 = 160kg ✓", font_size=36, color=self.COLORS['highlight'])

        checks = VGroup(check1, check2, check3)
        checks.arrange(DOWN, buff=0.5)
        checks.move_to(DOWN * 0.5)

        # 动画
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(result), run_time=1.5)
        self.play(FadeIn(check1), run_time=2)
        self.play(FadeIn(check2), run_time=2)
        self.play(FadeIn(check3), run_time=2)

        self.wait(duration - 8.5)

        # 退场
        self.play(FadeOut(subtitle), FadeOut(result), FadeOut(checks))

    def play_scene_10(self, duration):
        """第10幕：总结答案"""
        # 标题
        subtitle = Text("最终答案", font_size=48, color=self.COLORS['title'])
        subtitle.move_to(UP * 2)

        # 大答案框
        answer_box = Rectangle(width=10, height=2, color=self.COLORS['success'])
        answer_text = Text("原有 400 千克苹果", font_size=72, color=self.COLORS['success'])
        answer_box.move_to(UP * 0.5)
        answer_text.move_to(answer_box.get_center())

        # 解题技巧
        tips = Text(
            "解题关键：建立等量关系 → 设未知数 → 解方程",
            font_size=36,
            color=self.COLORS['text']
        )
        tips.move_to(DOWN * 2)

        # 动画
        self.play(FadeIn(subtitle), run_time=1)
        self.play(FadeIn(answer_box), FadeIn(answer_text), run_time=2)
        self.play(answer_text.animate.scale(1.2), run_time=1.5)
        self.play(FadeIn(tips), run_time=2)

        self.wait(duration - 6.5)

        # 最终退场
        self.play(
            FadeOut(subtitle), FadeOut(answer_box),
            FadeOut(answer_text), FadeOut(tips),
            run_time=1.5
        )


# ========== 运行提示 ==========
if __name__ == "__main__":
    print("\n使用 Manim 渲染视频：")
    print("cd ~/Documents/apple_problem_project")
    print("manim -pqh script.py AppleProblemScene")
    print("\n参数说明：")
    print("-p: 渲染后自动播放")
    print("-q: 质量等级 (l=480p, m=720p, h=1080p, k=4K)")
    print("-qh: 1080p60 高清")