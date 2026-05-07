"""
Milestone 1: Extraction Template Design
=========================================
Defines prompt_description and ExampleData objects for LangExtract.
Extracts entities (person, animal, object, place, event, emotion, concept)
and causal relationships from Chinese narrative text.
"""
from __future__ import annotations
from langextract.core.data import ExampleData, Extraction, CharInterval

# ─── Prompt Description ───────────────────────────────────────────────
PROMPT_DESCRIPTION = """你是一个精确的文本信息提取专家。请从给定文本中提取以下两类信息：

## 一、实体提取
提取以下类别的实体，每个实体需要提供 extraction_class（类别）、extraction_text（实体名称）和 attributes（属性）：

### 实体类别及属性要求：
1. **person（人物）**：提取所有人名和角色称谓。
   - 属性：gender（性别）、age_group（年龄段）、role（角色/职业）、appearance（外貌特征）、personality（性格特征）
2. **animal（动物）**：提取所有动物（包括有名字的动物）。
   - 属性：species（物种）、color（颜色）、feature（特征）、name（名字，如有）
3. **object（物体）**：提取所有有名称或重要的人工/天然物品。
   - 属性：material（材质）、color（颜色）、origin（来源）、function（功能）
4. **place（地点）**：提取所有地名和场景。
   - 属性：type（类型，如村庄/山洞/城市）、feature（特征）、atmosphere（氛围）
5. **event（事件）**：提取重要的行为/事件。
   - 属性：time（时间）、participants（参与者）、outcome（结果）
6. **emotion（情绪）**：提取文中明确表达的情绪/情感状态。
   - 属性：intensity（强度：高/中/低）、bearer（承载者）、trigger（触发原因）
7. **concept（概念）**：提取抽象概念、规则、思想。
   - 属性：type（类型）、domain（领域）

## 二、因果链提取（causal_chain）
提取文本中明确的因果关系，格式为：
  "(因) 实体A —[关系描述]→ (果) 实体B"
每个因果链的 extraction_class 应为 "causal_chain"，extraction_text 为上述格式。
属性：
  - cause（原因实体）、effect（结果实体）、relation_desc（关系描述）
  - cause_type（原因实体类别）、effect_type（结果实体类别）

## 重要规则：
- 所有提取必须精确对应原文，字符位置必须准确。
- 每个实体即使多次出现也只提取一次（首次出现位置）。
- 因果关系必须是原文明确表达的，不要推断。
"""

# ─── Example 1 ─────────────────────────────────────────────────────────
EXAMPLE_1_TEXT = "小明是一个勇敢的男孩。他放飞了一只红色的风筝，风筝飞向蓝天。"

EXAMPLE_1 = ExampleData(
    text=EXAMPLE_1_TEXT,
    extractions=[
        Extraction(
            extraction_class="person",
            extraction_text="小明",
            char_interval=CharInterval(start_pos=0, end_pos=2),
            attributes={"gender": "男", "age_group": "儿童", "role": "男孩", "personality": "勇敢"},
        ),
        Extraction(
            extraction_class="object",
            extraction_text="红色的风筝",
            char_interval=CharInterval(start_pos=12, end_pos=17),
            attributes={"material": "纸/布", "color": "红色", "function": "放飞"},
        ),
        Extraction(
            extraction_class="event",
            extraction_text="放飞了一只红色的风筝",
            char_interval=CharInterval(start_pos=8, end_pos=17),
            attributes={"time": "未指定", "participants": "小明", "outcome": "风筝飞向蓝天"},
        ),
        Extraction(
            extraction_class="causal_chain",
            extraction_text="(因) 小明 —[放飞]→ (果) 红色风筝飞向蓝天",
            char_interval=CharInterval(start_pos=8, end_pos=17),
            attributes={"cause": "小明", "effect": "红色风筝飞向蓝天", "relation_desc": "放飞",
                        "cause_type": "person", "effect_type": "event"},
        ),
    ],
)

# ─── Example 2 ─────────────────────────────────────────────────────────
EXAMPLE_2_TEXT = "老渔夫在湖边捡到一块发光的石头。他把石头带回了村里的铁匠铺。铁匠用这块石头打造了一把锋利的宝剑。"

EXAMPLE_2 = ExampleData(
    text=EXAMPLE_2_TEXT,
    extractions=[
        Extraction(
            extraction_class="person",
            extraction_text="老渔夫",
            char_interval=CharInterval(start_pos=0, end_pos=3),
            attributes={"gender": "男", "age_group": "老年", "role": "渔夫"},
        ),
        Extraction(
            extraction_class="person",
            extraction_text="铁匠",
            char_interval=CharInterval(start_pos=23, end_pos=25),
            attributes={"gender": "男", "age_group": "成年", "role": "铁匠"},
        ),
        Extraction(
            extraction_class="place",
            extraction_text="湖边",
            char_interval=CharInterval(start_pos=4, end_pos=6),
            attributes={"type": "自然水体", "feature": "湖"},
        ),
        Extraction(
            extraction_class="place",
            extraction_text="铁匠铺",
            char_interval=CharInterval(start_pos=21, end_pos=24),
            attributes={"type": "工坊", "feature": "打铁"},
        ),
        Extraction(
            extraction_class="object",
            extraction_text="发光的石头",
            char_interval=CharInterval(start_pos=9, end_pos=14),
            attributes={"material": "矿石", "feature": "发光", "origin": "湖边"},
        ),
        Extraction(
            extraction_class="object",
            extraction_text="锋利的宝剑",
            char_interval=CharInterval(start_pos=29, end_pos=34),
            attributes={"material": "金属", "feature": "锋利", "function": "武器"},
        ),
        Extraction(
            extraction_class="causal_chain",
            extraction_text="(因) 老渔夫捡到发光石头 —[交给铁匠]→ (果) 铁匠打造宝剑",
            char_interval=CharInterval(start_pos=16, end_pos=30),
            attributes={"cause": "老渔夫捡到发光石头", "effect": "铁匠打造宝剑",
                        "relation_desc": "交给铁匠", "cause_type": "event", "effect_type": "event"},
        ),
    ],
)

# ─── Example 3 ─────────────────────────────────────────────────────────
EXAMPLE_3_TEXT = "暴雨连下三天，山洪冲毁了村庄的木桥。村民们感到极度恐慌，纷纷逃往后山。族长下令修建石坝以阻挡洪水。"

EXAMPLE_3 = ExampleData(
    text=EXAMPLE_3_TEXT,
    extractions=[
        Extraction(
            extraction_class="event",
            extraction_text="暴雨连下三天",
            char_interval=CharInterval(start_pos=0, end_pos=6),
            attributes={"time": "三天", "outcome": "山洪暴发"},
        ),
        Extraction(
            extraction_class="event",
            extraction_text="山洪冲毁了村庄的木桥",
            char_interval=CharInterval(start_pos=7, end_pos=16),
            attributes={"participants": "山洪", "outcome": "木桥被毁"},
        ),
        Extraction(
            extraction_class="place",
            extraction_text="村庄",
            char_interval=CharInterval(start_pos=12, end_pos=14),
            attributes={"type": "聚居地", "feature": "有木桥"},
        ),
        Extraction(
            extraction_class="place",
            extraction_text="后山",
            char_interval=CharInterval(start_pos=25, end_pos=27),
            attributes={"type": "山体", "feature": "避难所"},
        ),
        Extraction(
            extraction_class="emotion",
            extraction_text="极度恐慌",
            char_interval=CharInterval(start_pos=18, end_pos=22),
            attributes={"intensity": "高", "bearer": "村民", "trigger": "山洪冲毁木桥"},
        ),
        Extraction(
            extraction_class="person",
            extraction_text="族长",
            char_interval=CharInterval(start_pos=28, end_pos=30),
            attributes={"gender": "男", "age_group": "老年", "role": "族长"},
        ),
        Extraction(
            extraction_class="object",
            extraction_text="石坝",
            char_interval=CharInterval(start_pos=34, end_pos=36),
            attributes={"material": "石头", "function": "阻挡洪水"},
        ),
        Extraction(
            extraction_class="causal_chain",
            extraction_text="(因) 暴雨 —[引发]→ (果) 山洪冲毁木桥",
            char_interval=CharInterval(start_pos=0, end_pos=16),
            attributes={"cause": "暴雨", "effect": "山洪冲毁木桥", "relation_desc": "引发",
                        "cause_type": "event", "effect_type": "event"},
        ),
        Extraction(
            extraction_class="causal_chain",
            extraction_text="(因) 山洪冲毁木桥 —[导致村民恐慌]→ (果) 村民逃往后山",
            char_interval=CharInterval(start_pos=7, end_pos=27),
            attributes={"cause": "山洪冲毁木桥", "effect": "村民逃往后山", "relation_desc": "导致村民恐慌",
                        "cause_type": "event", "effect_type": "event"},
        ),
        Extraction(
            extraction_class="causal_chain",
            extraction_text="(因) 村民恐慌逃往后山 —[促使族长决策]→ (果) 修建石坝阻挡洪水",
            char_interval=CharInterval(start_pos=18, end_pos=40),
            attributes={"cause": "村民恐慌逃往后山", "effect": "修建石坝阻挡洪水",
                        "relation_desc": "促使族长决策", "cause_type": "event", "effect_type": "event"},
        ),
    ],
)

# ─── Aggregated Examples ───────────────────────────────────────────────
EXAMPLES = [EXAMPLE_1, EXAMPLE_2, EXAMPLE_3]
