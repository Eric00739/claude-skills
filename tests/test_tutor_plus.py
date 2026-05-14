import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "Tutor_Plus"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TutorPlusTests(unittest.TestCase):
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
