"""
Generate realistic sample extraction data for the butterfly story.
This creates extraction_results.jsonl and highlight.html without needing an API key.
"""
from __future__ import annotations
import pathlib
from langextract.core.data import (
    AnnotatedDocument, Extraction, CharInterval, AlignmentStatus
)
import langextract as lx

TEXT = pathlib.Path("sample_text.txt").read_text(encoding="utf-8")

def pos(start: int, end: int) -> CharInterval:
    return CharInterval(start_pos=start, end_pos=end)

def ext(cls: str, text: str, start: int, end: int, **attrs) -> Extraction:
    return Extraction(
        extraction_class=cls,
        extraction_text=text,
        char_interval=pos(start, end),
        alignment_status=AlignmentStatus.MATCH_EXACT,
        attributes=attrs,
    )

# All extractions ordered by position in text
EXTRACTIONS = [
    # ── 人物 (person) ────────────────────────────────────────
    ext("person", "林溪", 18, 20,
        gender="女", age_group="年轻", role="村民/女孩",
        appearance="明亮的蓝色眼睛", personality="温柔、好奇、勇敢"),

    ext("person", "张伯", 358, 360,
        gender="男", age_group="老年", role="老樵夫",
        appearance="", personality="勤劳"),

    ext("person", "陈老", 377, 379,
        gender="男", age_group="老年", role="族长",
        appearance="", personality="智慧、稳重"),

    ext("person", "王铁锤", 494, 497,
        gender="男", age_group="成年", role="工匠/铁匠",
        appearance="", personality="手巧"),

    ext("person", "小山", 685, 687,
        gender="男", age_group="儿童", role="矿工之子",
        appearance="", personality=""),  # Note: this is 小山 who is trapped

    ext("person", "赵远", 543, 545,
        gender="男", age_group="成年", role="商队队长",
        appearance="", personality="精明"),

    ext("person", "孙明远", 571, 574,
        gender="男", age_group="成年", role="富商",
        appearance="", personality="富有、果断"),

    ext("person", "李玄", 769, 771,
        gender="男", age_group="成年", role="道人/修士",
        appearance="", personality="慈悲、智慧"),

    # ── 动物 (animal) ────────────────────────────────────────
    ext("animal", "雪翅", 102, 104,
        species="蝴蝶", color="白色带金色斑点", feature="翅膀金色斑点", name="雪翅"),

    ext("animal", "白色蝴蝶", 101, 105,
        species="蝴蝶", color="白色", feature="金色斑点翅膀", name="雪翅"),

    ext("animal", "金色蜜蜂", 224, 228,
        species="蜜蜂", color="金色", feature="正在采蜜", name=""),

    ext("animal", "翠鸟", 246, 248,
        species="翠鸟", color="翠绿", feature="饥饿", name=""),

    # ── 物体 (object) ────────────────────────────────────────
    ext("object", "枯枝", 275, 277,
        material="木头", color="枯黄", origin="老树", function=""),

    ext("object", "黑石", 330, 332,
        material="石头", color="黑色", origin="山涧溪边", function="刻有符文"),

    ext("object", "《山河志》", 390, 395,
        material="纸", color="", origin="陈老收藏", function="记载地理历史"),

    ext("object", "荧光矿石", 446, 450,
        material="矿石", color="淡蓝色荧光", origin="龙隐洞", function="发光"),

    ext("object", "星辉灯", 503, 506,
        material="荧光矿石", color="淡蓝色", origin="翠云村打造", function="照亮山谷"),

    ext("object", "青山约", 902, 905,
        material="纸", color="", origin="陈老制定", function="村规/环保条约"),

    # ── 地点 (place) ─────────────────────────────────────────
    ext("place", "翠云村", 10, 13,
        type="村庄", feature="宁静、山间", atmosphere="平和→繁荣→反思"),

    ext("place", "老榕树", 63, 66,
        type="古树", feature="村口", atmosphere="宁静、怀念"),

    ext("place", "山谷", 185, 187,
        type="自然地形", feature="有野花田", atmosphere="生机勃勃"),

    ext("place", "野花田", 190, 193,
        type="花田", feature="山谷中", atmosphere="美丽"),

    ext("place", "山涧", 284, 286,
        type="溪流", feature="枯枝落入处", atmosphere="清幽"),

    ext("place", "小溪", 289, 291,
        type="溪流", feature="水流被改变", atmosphere=""),

    ext("place", "龙隐洞", 432, 435,
        type="山洞", feature="被遗忘、有荧光矿石", atmosphere="神秘"),

    ext("place", "平阳城", 554, 557,
        type="城市", feature="繁华", atmosphere="热闹、商业"),

    ext("place", "玉峰山", 753, 756,
        type="山", feature="修道之地", atmosphere="清修"),

    # ── 事件 (event) ─────────────────────────────────────────
    ext("event", "林溪对蝴蝶吹了一口气", 106, 115,
        time="某天早晨", participants="林溪", outcome="蝴蝶飞向天空"),

    ext("event", "蝴蝶扇动翅膀飞向天空", 119, 128,
        time="紧接着", participants="蝴蝶(雪翅)", outcome="气流形成"),

    ext("event", "气流穿过野花田惊醒蜜蜂", 153, 163,
        time="紧随其后", participants="气流、蜜蜂", outcome="蜜蜂愤怒飞起"),

    ext("event", "翠鸟俯冲撞到枯枝", 256, 264,
        time="紧随蜜蜂飞起", participants="翠鸟", outcome="枯枝断裂落入山涧"),

    ext("event", "枯枝落入山涧改变溪水方向", 278, 290,
        time="枯枝断裂后", participants="枯枝、溪水", outcome="泥土松动黑石滚落"),

    ext("event", "张伯发现刻有符文的黑石", 349, 358,
        time="黑石滚落后", participants="张伯", outcome="将符文告知陈老"),

    ext("event", "陈老发现龙隐洞", 420, 426,
        time="张伯告知后", participants="陈老", outcome="发现荧光矿石"),

    ext("event", "村民在龙隐洞发现荧光矿石", 438, 450,
        time="陈老发现后", participants="林溪、村民", outcome="打造星辉灯"),

    ext("event", "王铁锤打造星辉灯", 497, 505,
        time="发现矿石后", participants="王铁锤", outcome="灯光照亮山谷"),

    ext("event", "赵远将星辉灯带到平阳城", 536, 546,
        time="灯造成后", participants="赵远", outcome="引起富商孙明远注意"),

    ext("event", "孙明远决定投资开发矿脉", 582, 593,
        time="见到星辉灯后", participants="孙明远", outcome="翠云村变为矿业重镇"),

    ext("event", "龙隐洞发生严重塌方", 826, 834,
        time="三天后的雨夜", participants="矿工", outcome="矿工被困洞中"),

    ext("event", "林溪举星辉灯入洞救援", 717, 726,
        time="塌方后", participants="林溪", outcome="成功找到被困者"),

    ext("event", "全村成功救出被困矿工", 799, 808,
        time="林溪入洞后", participants="林溪、村民、商队", outcome="全部获救"),

    ext("event", "陈老制定青山约", 894, 900,
        time="灾难过后", participants="陈老", outcome="限制开采、植树造林"),

    ext("event", "孙明远资助建立星辉书院", 950, 961,
        time="青山约制定后", participants="孙明远", outcome="孩子们学习自然智慧"),

    ext("event", "蝴蝶再次落在林溪指尖", 985, 994,
        time="来年春天", participants="林溪、蝴蝶", outcome="林溪微笑守护"),

    # ── 情绪 (emotion) ────────────────────────────────────────
    ext("emotion", "好奇", 46, 48,
        intensity="中", bearer="林溪", trigger="对世界的探索欲"),

    ext("emotion", "愤怒", 233, 235,
        intensity="高", bearer="金色蜜蜂", trigger="被气流惊醒"),

    ext("emotion", "忧郁", 660, 662,
        intensity="中", bearer="林溪", trigger="怀念白色蝴蝶雪翅"),

    ext("emotion", "忧伤", 715, 717,
        intensity="中", bearer="林溪", trigger="唱歌怀念蝴蝶"),

    ext("emotion", "哀愁", 783, 785,
        intensity="中", bearer="李玄", trigger="被林溪的歌声触动"),

    ext("emotion", "恐慌", 843, 845,
        intensity="高", bearer="村民", trigger="龙隐洞塌方矿工被困"),

    ext("emotion", "勇气", 731, 733,
        intensity="高", bearer="林溪", trigger="需要救援被困矿工"),

    ext("emotion", "怀念", 671, 673,
        intensity="中", bearer="林溪", trigger="蝴蝶雪翅消失"),

    # ── 概念 (concept) ────────────────────────────────────────
    ext("concept", "贪婪", 897, 899,
        type="负面品质", domain="人性"),

    ext("concept", "自然与平衡", 980, 984,
        type="哲学理念", domain="生态智慧"),

    ext("concept", "蝴蝶效应", 118, 124,
        type="科学概念/隐喻", domain="混沌理论"),

    # ── 因果链 (causal_chain) ─────────────────────────────────
    # Chain 1: 林溪吹气 → 蝴蝶飞
    ext("causal_chain",
        "(因) 林溪吹气 —[引发]→ (果) 蝴蝶扇动翅膀飞向天空",
        106, 128,
        cause="林溪吹气", effect="蝴蝶扇动翅膀飞向天空",
        relation_desc="引发", cause_type="event", effect_type="event"),

    # Chain 2: 蝴蝶翅膀 → 气流形成
    ext("causal_chain",
        "(因) 蝴蝶扇动翅膀 —[搅动空气产生]→ (果) 微小气流形成",
        129, 152,
        cause="蝴蝶扇动翅膀", effect="微小气流形成",
        relation_desc="搅动空气产生", cause_type="event", effect_type="event"),

    # Chain 3: 气流 → 惊醒蜜蜂
    ext("causal_chain",
        "(因) 气流穿过野花田 —[惊醒]→ (果) 金色蜜蜂愤怒飞起",
        153, 235,
        cause="气流穿过野花田", effect="金色蜜蜂愤怒飞起",
        relation_desc="惊醒", cause_type="event", effect_type="event"),

    # Chain 4: 蜜蜂嗡嗡声 → 引来翠鸟
    ext("causal_chain",
        "(因) 蜜蜂嗡嗡声 —[引来]→ (果) 翠鸟俯冲捕食",
        237, 255,
        cause="蜜蜂嗡嗡声", effect="翠鸟俯冲捕食",
        relation_desc="引来", cause_type="event", effect_type="event"),

    # Chain 5: 翠鸟 → 撞断枯枝
    ext("causal_chain",
        "(因) 翠鸟俯冲 —[撞到]→ (果) 枯枝断裂落入山涧",
        256, 280,
        cause="翠鸟俯冲", effect="枯枝断裂落入山涧",
        relation_desc="撞到", cause_type="event", effect_type="event"),

    # Chain 6: 枯枝 → 改变水流 → 黑石滚落
    ext("causal_chain",
        "(因) 枯枝落入山涧 —[改变水流]→ (果) 黑石滚落出来",
        278, 332,
        cause="枯枝落入山涧", effect="黑石滚落出来",
        relation_desc="改变水流导致", cause_type="event", effect_type="event"),

    # Chain 7: 黑石 → 张伯发现 → 告知陈老
    ext("causal_chain",
        "(因) 黑石滚落 —[被张伯发现告知]→ (果) 陈老翻阅《山河志》",
        330, 395,
        cause="黑石滚落", effect="陈老翻阅《山河志》",
        relation_desc="被张伯发现告知", cause_type="event", effect_type="event"),

    # Chain 8: 山河志 → 发现龙隐洞
    ext("causal_chain",
        "(因) 陈老查阅《山河志》 —[发现线索指向]→ (果) 发现龙隐洞",
        395, 435,
        cause="陈老查阅《山河志》", effect="发现龙隐洞",
        relation_desc="发现线索指向", cause_type="event", effect_type="event"),

    # Chain 9: 荧光矿石 → 星辉灯
    ext("causal_chain",
        "(因) 发现荧光矿石 —[被王铁锤打造为]→ (果) 星辉灯照亮山谷",
        438, 510,
        cause="发现荧光矿石", effect="星辉灯照亮山谷",
        relation_desc="被王铁锤打造为", cause_type="event", effect_type="event"),

    # Chain 10: 星辉灯 → 带到平阳城 → 投资
    ext("causal_chain",
        "(因) 星辉灯被带到平阳城 —[引起孙明远注意导致]→ (果) 投资开发矿脉",
        536, 593,
        cause="星辉灯被带到平阳城", effect="投资开发矿脉",
        relation_desc="引起孙明远注意导致", cause_type="event", effect_type="event"),

    # Chain 11: 开发 → 翠云村变迁 → 林溪忧郁
    ext("causal_chain",
        "(因) 矿脉过度开发 —[导致]→ (果) 林溪感到忧郁怀念蝴蝶",
        598, 673,
        cause="矿脉过度开发", effect="林溪感到忧郁怀念蝴蝶",
        relation_desc="导致", cause_type="event", effect_type="emotion"),

    # Chain 12: 林溪歌声 → 触动李玄
    ext("causal_chain",
        "(因) 林溪唱忧伤歌谣 —[触动]→ (果) 李玄下山帮助林溪",
        705, 777,
        cause="林溪唱忧伤歌谣", effect="李玄下山帮助林溪",
        relation_desc="触动", cause_type="event", effect_type="event"),

    # Chain 13: 过度开采 → 塌方
    ext("causal_chain",
        "(因) 过度开采荧光矿石 —[导致]→ (果) 龙隐洞塌方矿工被困",
        809, 850,
        cause="过度开采荧光矿石", effect="龙隐洞塌方矿工被困",
        relation_desc="导致", cause_type="event", effect_type="event"),

    # Chain 14: 林溪勇气 → 救援成功
    ext("causal_chain",
        "(因) 林溪举灯勇敢救援 —[感召众人协作]→ (果) 成功救出所有被困矿工",
        717, 808,
        cause="林溪举灯勇敢救援", effect="成功救出所有被困矿工",
        relation_desc="感召众人协作", cause_type="event", effect_type="event"),

    # Chain 15: 灾难 → 反思 → 青山约
    ext("causal_chain",
        "(因) 塌方灾难 —[促使反思]→ (果) 陈老制定青山约",
        826, 905,
        cause="塌方灾难", effect="陈老制定青山约",
        relation_desc="促使反思", cause_type="event", effect_type="event"),

    # Chain 16: 青山约 → 书院
    ext("causal_chain",
        "(因) 青山约制定 —[促使孙明远]→ (果) 建立星辉书院",
        902, 961,
        cause="青山约制定", effect="建立星辉书院",
        relation_desc="促使孙明远", cause_type="event", effect_type="event"),

    # Chain 17: 自然恢复 → 蝴蝶归来
    ext("causal_chain",
        "(因) 自然平衡恢复 —[迎来]→ (果) 蝴蝶雪翅归来",
        965, 994,
        cause="自然平衡恢复", effect="蝴蝶雪翅归来",
        relation_desc="迎来", cause_type="concept", effect_type="event"),
]

def main():
    doc = AnnotatedDocument(
        document_id="butterfly_echo_v1",
        extractions=EXTRACTIONS,
        text=TEXT,
    )

    # Save JSONL
    out_dir = pathlib.Path(".")
    lx.io.save_annotated_documents(
        iter([doc]),
        output_dir=str(out_dir),
        output_name="extraction_results.jsonl",
    )
    print(f"Saved {len(EXTRACTIONS)} extractions to extraction_results.jsonl")

    # Count by class
    from collections import Counter
    counts = Counter(e.extraction_class for e in EXTRACTIONS)
    print("\nExtraction summary:")
    for cls, cnt in counts.most_common():
        print(f"  {cls}: {cnt}")

    # Generate highlight HTML
    html = lx.visualize(doc, animation_speed=1.5, gif_optimized=True)
    html_path = out_dir / "highlight.html"
    full_html = f"<!DOCTYPE html>\n<html lang='zh-CN'>\n<head>\n<meta charset='utf-8'>\n<title>文本提取高亮验证 - 蝴蝶回声</title>\n</head>\n<body>\n{html}\n</body>\n</html>"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Highlight HTML saved to: {html_path}")


if __name__ == "__main__":
    main()
