"""模拟数据采集器 - 用模拟数据跑通全链路，后续替换为真实爬虫

先把 RAG 全链路跑通，采集模块后续再接真实爬虫
"""

from app.models.schemas import CompetitorNote
from datetime import datetime
import uuid


def generate_mock_data() -> list[CompetitorNote]:
    """生成模拟的竞品笔记数据，用于测试 RAG 全链路"""

    mock_notes = [
        CompetitorNote(
            id=str(uuid.uuid4()),
            platform="xiaohongshu",
            author="厨房小当家",
            author_followers=523000,
            title="3分钟搞定！懒人必学的酸辣粉做法",
            content="使用超市买的速食酸辣粉底料，加入自制的辣椒油和花生碎，3分钟出锅。视频时长45秒，竖屏拍摄。这款酸辣粉用了特制的辣椒油配方，比外卖还好吃！材料简单，适合上班族下班后快速搞定一餐。",
            likes=8523,
            collects=12301,
            comments=892,
            tags=["美食教程", "懒人料理", "酸辣粉"],
            publish_time="2026-03-01",
            crawl_time=datetime.now().isoformat(),
        ),
        CompetitorNote(
            id=str(uuid.uuid4()),
            platform="xiaohongshu",
            author="厨房小当家",
            author_followers=523000,
            title="老公连吃三碗饭的红烧肉，做法简单到离谱",
            content="五花肉冷水下锅焯水，冰糖炒色，加入生抽老抽料酒，小火炖45分钟。使用了电饭煲懒人版本，突出零失败卖点。这道红烧肉的秘诀在于冰糖炒色的时机，要等冰糖完全融化起大泡泡时再放肉。",
            likes=15201,
            collects=23456,
            comments=1523,
            tags=["红烧肉", "家常菜", "下饭菜"],
            publish_time="2026-03-03",
            crawl_time=datetime.now().isoformat(),
        ),
        CompetitorNote(
            id=str(uuid.uuid4()),
            platform="xiaohongshu",
            author="美食猎人小李",
            author_followers=387000,
            title="探店！人均30的宝藏小馆，比大酒楼还好吃",
            content="位于城中村的一家川菜馆，招牌菜水煮鱼只要38元。使用了对比手法（外观破旧vs菜品精致），配文走意外发现路线。水煮鱼的分量足，两个人吃都够了，麻辣鲜香，花椒是自家炒的。",
            likes=12890,
            collects=8765,
            comments=2341,
            tags=["探店", "美食推荐", "平价美食"],
            publish_time="2026-03-02",
            crawl_time=datetime.now().isoformat(),
        ),
        CompetitorNote(
            id=str(uuid.uuid4()),
            platform="xiaohongshu",
            author="美食猎人小李",
            author_followers=387000,
            title="5家必吃的深圳茶餐厅测评，第3家绝了",
            content="横向对比5家茶餐厅的菠萝包和丝袜奶茶，使用打分表格形式呈现。第一家金记85分菠萝包酥脆，第二家华姐80分奶茶浓郁，第三家肥仔90分性价比最高人均35，第四家添好运82分，第五家翠华78分。封面使用九宫格拼图。",
            likes=9234,
            collects=15678,
            comments=1876,
            tags=["深圳美食", "茶餐厅", "测评"],
            publish_time="2026-03-04",
            crawl_time=datetime.now().isoformat(),
        ),
        CompetitorNote(
            id=str(uuid.uuid4()),
            platform="xiaohongshu",
            author="旅行日记本",
            author_followers=891000,
            title="人均500！这个小众海岛美哭我了",
            content="介绍了福建平潭岛的蓝眼泪景观，详细列出了交通住宿费用。从福州出发动车1.5小时到平潭，民宿人均150一晚，吃海鲜大排档人均80。蓝眼泪最佳观赏期是4-6月，晚上8点后在龙凤头海滩最容易看到。文案风格感性，配图使用高饱和度滤镜。",
            likes=32456,
            collects=45678,
            comments=3456,
            tags=["小众旅行", "海岛", "穷游攻略"],
            publish_time="2026-03-01",
            crawl_time=datetime.now().isoformat(),
        ),
        CompetitorNote(
            id=str(uuid.uuid4()),
            platform="xiaohongshu",
            author="旅行日记本",
            author_followers=891000,
            title="千万不要在旺季去这5个景区，血泪教训",
            content="列出了黄山、张家界、故宫、西湖、凤凰古城的旺季问题。黄山国庆排队3小时看日出，张家界暑假住宿涨价300%，故宫五一人挤人拍照全是人头，西湖断桥挤到寸步难行，凤凰古城春节商业化严重物价翻倍。建议淡季出行，11月或3月最佳。使用避雷类标题引发共鸣。",
            likes=28901,
            collects=18234,
            comments=5678,
            tags=["旅行避坑", "景区", "旅游攻略"],
            publish_time="2026-03-03",
            crawl_time=datetime.now().isoformat(),
        ),
        CompetitorNote(
            id=str(uuid.uuid4()),
            platform="xiaohongshu",
            author="背包客阿南",
            author_followers=234000,
            title="一个人的西藏之旅，第3天差点哭了",
            content="自驾川藏线的日记体笔记，记录了高反经历和沿途风景。第一天成都出发经雅安到康定，第二天翻折多山看到雪山激动，第三天到理塘高反严重头疼呕吐差点放弃，吸氧后第四天恢复继续前进。风格真实不做作，评论区互动氛围好，很多人分享自己的高反经历。",
            likes=18765,
            collects=12345,
            comments=4567,
            tags=["西藏", "独自旅行", "川藏线"],
            publish_time="2026-03-02",
            crawl_time=datetime.now().isoformat(),
        ),
        CompetitorNote(
            id=str(uuid.uuid4()),
            platform="xiaohongshu",
            author="数据分析师",
            author_followers=0,
            title="本周数据总结",
            content="本周共采集笔记127条，覆盖博主23个，总互动量约458000次，平均单篇互动量3606次。赛道互动量排名：旅行赛道平均互动量5823最高，美食赛道平均互动量4156，穿搭赛道平均互动量2890，护肤赛道平均互动量2134。爆款规律：使用数字标题的笔记点赞量平均高出43%，高饱和度暖色调封面点击率比冷色调高28%，对比测评形式笔记收藏率是普通笔记的2.1倍，周一和周三18-20点发布互动量最高。",
            likes=0,
            collects=0,
            comments=0,
            tags=["数据总结", "周报"],
            publish_time="2026-03-07",
            crawl_time=datetime.now().isoformat(),
        ),
    ]

    return mock_notes
