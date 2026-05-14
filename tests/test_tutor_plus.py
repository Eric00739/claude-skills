import contextlib
import io
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "tutor-plus"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TutorPlusTests(unittest.TestCase):
    def test_skill_folder_and_frontmatter_use_hyphen_case_name(self):
        self.assertTrue(SKILL.exists())
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: tutor-plus", skill_text)


    def test_generate_tts_defaults_to_warm_slow_female_teacher_voice(self):
        module = load_module(SKILL / "scripts" / "generate_tts.py", "tutor_plus_generate_tts_defaults")

        args = module.parse_cli_args(["audio_list.csv"])

        self.assertEqual(args.voice, "xiaoxiao")
        self.assertEqual(args.rate, "-8%")
        self.assertEqual(args.volume, "+0%")
        self.assertEqual(args.pitch, "+0Hz")


    def test_generate_tts_cli_accepts_rate_option_and_help(self):
        module = load_module(SKILL / "scripts" / "generate_tts.py", "tutor_plus_generate_tts_cli")

        args = module.parse_cli_args(["audio_list.csv", "./audio", "--rate", "-8%"])

        self.assertEqual(args.rate, "-8%")
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as exit_context:
                module.parse_cli_args(["--help"])
        self.assertEqual(exit_context.exception.code, 0)


    def test_generate_all_records_tts_style_parameters(self):
        module = load_module(SKILL / "scripts" / "generate_tts.py", "tutor_plus_generate_tts_manifest")
        calls = []

        async def fake_generate_audio(text, output_path, voice="xiaoxiao", rate="-8%", volume="+0%", pitch="+0Hz"):
            calls.append(
                {
                    "text": text,
                    "output_path": str(output_path),
                    "voice": voice,
                    "rate": rate,
                    "volume": volume,
                    "pitch": pitch,
                }
            )
            Path(output_path).write_bytes(b"fake audio")
            return True, 3.21

        module.generate_audio = fake_generate_audio

        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "audio_list.csv"
            audio_dir = Path(tmp) / "audio"
            csv_path.write_text(
                'filename,text\n'
                'audio_001_开场.wav,"我们先看看题目里告诉了什么。"\n',
                encoding="utf-8",
            )

            success = module.asyncio.run(module.generate_all(csv_path, audio_dir))
            manifest = json.loads((audio_dir / "audio_info.json").read_text(encoding="utf-8"))

        self.assertTrue(success)
        self.assertEqual(calls[0]["voice"], "xiaoxiao")
        self.assertEqual(calls[0]["rate"], "-8%")
        self.assertEqual(calls[0]["volume"], "+0%")
        self.assertEqual(calls[0]["pitch"], "+0Hz")
        self.assertEqual(manifest["voice"], "xiaoxiao")
        self.assertEqual(manifest["rate"], "-8%")
        self.assertEqual(manifest["volume"], "+0%")
        self.assertEqual(manifest["pitch"], "+0Hz")


    def test_skill_references_child_friendly_narration_guidance(self):
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        reference_path = SKILL / "references" / "narration_style.md"

        self.assertTrue(reference_path.exists())
        reference_text = reference_path.read_text(encoding="utf-8")
        self.assertIn("references/narration_style.md", skill_text)
        self.assertIn("亲和女老师", reference_text)
        self.assertIn("小学生", reference_text)
        self.assertIn("不要", reference_text)


    def test_generate_tts_parses_storyboard_audio_table(self):
        module = load_module(SKILL / "scripts" / "generate_tts.py", "tutor_plus_generate_tts")
        with tempfile.TemporaryDirectory() as tmp:
            storyboard = Path(tmp) / "storyboard.md"
            storyboard.write_text(
                """
# 分镜脚本

## 音频生成清单

| 幕号 | 文件名 | 读白文本 | 时长 | 说话人 | 情感 |
|------|--------|----------|------|--------|------|
| 1 | audio_001_开场.wav | "大家好，今天讲这道题。" | | xiaoxiao | 平和 |
| 2 | audio_002_证明.wav | "接着看证明过程。" | | yunyang | 稳重 |
""",
                encoding="utf-8",
            )

            entries = module.parse_input_file(storyboard)

        self.assertEqual(
            entries,
            [
                {"filename": "audio_001_开场.wav", "text": "大家好，今天讲这道题。"},
                {"filename": "audio_002_证明.wav", "text": "接着看证明过程。"},
            ],
        )


    def test_scaffold_passes_builtin_structure_check_without_warnings(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SKILL / "scripts" / "check.py"),
                str(SKILL / "templates" / "script_scaffold.py"),
            ],
            cwd=SKILL,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("警告", result.stdout)
        self.assertNotIn("未检测到 add_sound", result.stdout)
        self.assertNotIn("Subtitle 类", result.stdout)


    def test_init_copies_runtime_files_into_project(self):
        module = load_module(SKILL / "init.py", "tutor_plus_init")
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "lesson"
            project.mkdir()

            module.create_directory_structure(project)
            module.copy_runtime_files(project)
            module.copy_templates(project)
            module.generate_csv_template(project)

            self.assertTrue((project / "script.py").exists())
            self.assertTrue((project / "requirements.txt").exists())
            self.assertTrue((project / "scripts" / "render.py").exists())
            self.assertTrue((project / "scripts" / "check.py").exists())
            self.assertTrue((project / "scripts" / "generate_tts.py").exists())
            self.assertTrue((project / "scripts" / "validate_audio.py").exists())


    def test_render_pipeline_uses_current_project_as_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "lesson"
            shutil.copytree(SKILL, project)
            module = load_module(project / "scripts" / "render.py", "tutor_plus_render")

            pipeline = module.RenderPipeline(script_file="script.py", preview=False)

            self.assertEqual(pipeline.project_dir, project)
            self.assertEqual(pipeline.check_script, project / "scripts" / "check.py")


if __name__ == "__main__":
    unittest.main()
