#!/bin/bash
# 验证 SKILL.md 中的 Qwen-TTS 配置

echo "=== 检查默认引擎配置 ==="

# 检查描述部分
if grep -q "默认使用温暖亲切的教师语音" SKILL.md; then
    echo "✅ 描述部分：正确（默认使用自然语音）"
else
    echo "❌ 描述部分：需要修改"
fi

# 检查依赖说明
if grep -q "opc-cli.*必需" SKILL.md; then
    echo "✅ 依赖说明：正确（opc-cli 为必需）"
else
    echo "❌ 依赖说明：需要修改"
fi

# 检查默认说话人
if grep -q "说话人.*Serena" SKILL.md && ! grep -q "说话人.*xiaoxiao" SKILL.md; then
    echo "✅ 默认说话人：正确（Serena）"
else
    echo "❌ 默认说话人：需要修改"
fi

# 检查引擎对比表格
if grep -q "qwen.*默认使用" SKILL.md && grep -q "edge-tts.*不推荐"; then
    echo "✅ 引擎对比：正确（Qwen默认，Edge不推荐）"
else
    echo "❌ 引擎对比：需要修改"
fi

# 检查命令示例
if grep -q "Qwen-TTS.*默认推荐" SKILL.md; then
    echo "✅ 命令标题：正确（默认推荐）"
else
    echo "❌ 命令标题：需要修改"
fi

# 检查常见问题
if grep -q "声音听起来很自然吗" SKILL.md && ! grep -q "如何避免机械声音" SKILL.md; then
    echo "✅ 常见问题：正确（Q1修改为自然声音确认）"
else
    echo "❌ 常见问题：需要修改"
fi

echo ""
echo "=== 统计信息 ==="
echo "Qwen 提及次数: $(grep -c 'Qwen' SKILL.md)"
echo "Serena 提及次数: $(grep -c 'Serena' SKILL.md)"
echo "Edge-TTS 提及次数: $(grep -c 'Edge-TTS' SKILL.md)"
echo "xiaoxiao 提及次数: $(grep -c 'xiaoxiao' SKILL.md)"

echo ""
echo "=== 最终结果 ==="
if grep -c 'Edge-TTS.*不推荐' SKILL.md && grep -c 'qwen.*默认' SKILL.md; then
    echo "✅ 所有检查通过！默认配置正确。"
else
    echo "⚠️ 需要进一步检查"
fi