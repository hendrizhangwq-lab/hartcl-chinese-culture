import json, os, urllib.request, urllib.parse, time

def translate(text):
    if not text.strip(): return ''
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q=' + urllib.parse.quote(text.strip())
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10)
        data = json.loads(res.read().decode('utf-8'))
        sentences = [item[0] for item in data[0] if item and item[0]]
        return ''.join(sentences)
    except Exception as e:
        return text

# Curated core insights for each of the 24 lessons to ensure deep analysis
LESSON_SUMMARIES = {
    1: {
        "gistZh": "文化并非单纯的学历或知识堆砌，而是一种沉淀为习惯的精神价值与生活方式，其最终成果是塑造一个社会的「集体人格」。",
        "gistEn": "Culture is not mere credentials or accumulated knowledge, but spiritual values and a way of life settled into daily habit—the ultimate fruit of which is shaping a society's 'collective personality'.",
        "highlights": [
            {
                "zh": "最短文化定义：一种成为习惯的精神价值和生活方式。",
                "en": "Shortest Definition of Culture: Spiritual values and a way of life that have become ingrained habits."
            },
            {
                "zh": "文化的终极成果：创造并沉淀社会的集体人格（如中国文化中的君子）。",
                "en": "Ultimate Outcome of Culture: Creating and cultivating a society's collective personality (such as the 'Junzi' or Noble Person in Chinese culture)."
            },
            {
                "zh": "知识 vs 文化：知识可以临时记忆，而文化是日常行为中不假思索的自然体现。",
                "en": "Knowledge vs. Culture: Knowledge can be temporarily memorized, whereas culture is a natural, unreflective expression in daily behavior."
            },
            {
                "zh": "集体记忆与延续性：中国文化的生命力在于数千年不曾间断的生活习惯与价值传承。",
                "en": "Collective Memory & Continuity: The vitality of Chinese culture stems from thousands of years of unbroken living habits and value transmission."
            }
        ]
    },
    2: {
        "gistZh": "庄子哲学强调突破人类自我中心主义，以万物平等的视角审视自然与人生，追求超脱世俗名利的精神自由（逍遥游）。",
        "gistEn": "Zhuangzi's philosophy emphasizes transcending human anthropocentrism, viewing nature and life through absolute equality, and pursuing spiritual freedom ('Carefree Wandering') beyond worldly fame and wealth.",
        "highlights": [
            {
                "zh": "万物平等视角：从「人的立场」转向「自然的立场」，打破人为划分的贵贱与成败。",
                "en": "Equality of All Things: Shifting from a human-centric stance to a natural stance, breaking down artificial distinctions of status and success."
            },
            {
                "zh": "老子与庄子的继承：老子讲「上善若水、滋润万物而不争」，庄子将其延伸为个体精神的绝对自由。",
                "en": "Laozi & Zhuangzi Connection: Laozi espouses 'supreme goodness is like water—nourishing all things without conflict', which Zhuangzi expands into absolute individual spiritual freedom."
            },
            {
                "zh": "逍遥游的精神境界：不受外界毁誉和实用功利的羁绊，实现心灵的彻底解放。",
                "en": "Spirit of 'Carefree Wandering': Unfettered by external praise, blame, or utilitarian gain, achieving complete liberation of the soul."
            },
            {
                "zh": "对现代人的启示：在功利竞争激烈的社会中，庄子给中国心灵提供了一剂精神解毒剂。",
                "en": "Relevance Today: In a hyper-competitive, utilitarian society, Zhuangzi offers a vital spiritual antidote for the human mind."
            }
        ]
    },
    3: {
        "gistZh": "「君子人格」是中国文化独一无二的核心集体人格，不同于西方的绅士或骑士，它注重内在道德修养、社会责任感与中庸圆融。",
        "gistEn": "The 'Junzi' (Noble Person) is Chinese culture's unique core collective personality—unlike Western gentlemen or knights, it emphasizes inner moral cultivation, social responsibility, and harmonious balance.",
        "highlights": [
            {
                "zh": "集体人格对比：对比西方绅士人格、骑士人格与日本武士人格，君子是中国文化的独特标志。",
                "en": "Collective Personality Comparison: Compared to Western gentlemen, medieval knights, or Japanese samurai, the Junzi is the indispensable symbol of Chinese civilization."
            },
            {
                "zh": "君子的核心标准：德行第一、重义轻利、文质彬彬，兼具社会担当与个修养。",
                "en": "Core Criteria of a Junzi: Virtue first, valuing righteousness over profit, cultured yet refined, combining social duty with self-cultivation."
            },
            {
                "zh": "君子与小人的界限：小人同而不和、择利而动；君子和而不同、择善而固执。",
                "en": "Junzi vs. Xiaoren (Petty Person): The petty person seeks uniformity without harmony for profit; the Junzi seeks harmony without conformity for virtue."
            },
            {
                "zh": "文化的避风港：即便历史遭遇劫难，只要君子人格尚存，中国文明的火种就不会熄灭。",
                "en": "Cultural Sanctuary: Even during historical catastrophes, as long as the Junzi ideal endures, the embers of Chinese civilization remain alive."
            }
        ]
    },
    4: {
        "gistZh": "「中庸之道」并非平庸妥协，而是数千年来中华民族在复杂历史环境下的集体生存智慧——寻找极致与偏激之间的黄金平衡点。",
        "gistEn": "The 'Doctrine of the Mean' (Zhongyong) is not mediocre compromise, but thousands of years of collective survival wisdom—seeking the golden balance between extremes and radicalism.",
        "highlights": [
            {
                "zh": "中庸的真正含义：「中」指不偏不倚的精准适度，「庸」指常态与持久，结合即为可持续的最高智慧。",
                "en": "True Meaning of Zhongyong: 'Zhong' denotes unswerving balance and appropriateness, while 'Yong' signifies constancy; combined, they form sustainable supreme wisdom."
            },
            {
                "zh": "民族集体选择：经历无数战乱与变迁后，中华文明选择中庸作为维持大一统与社会稳定的社会契约。",
                "en": "Nation's Collective Choice: Through endless conflicts, Chinese civilization adopted moderation as a social contract for unity and stability."
            },
            {
                "zh": "反极端主义：警惕极端偏执与情绪化言行，用理性中和的力量化解矛盾。",
                "en": "Anti-Extremism: Guarding against radicalism and emotional fervor, resolving conflicts through rational, harmonizing strength."
            },
            {
                "zh": "现代价值：在分化加剧的世界中，中庸之道为国际沟通与社会治理提供了宝贵的协调智慧。",
                "en": "Modern Value: In a polarized world, the Doctrine of the Mean provides invaluable wisdom for international dialogue and governance."
            }
        ]
    },
    5: {
        "gistZh": "「家国同构」解释了中国社会小秩序（家庭伦理）与大秩序（国家治理）的无缝衔接，使国家治理具备了深厚的伦理情感根基。",
        "gistEn": "'Isomorphism of Family and State' explains the seamless alignment between micro-order (family ethics) and macro-order (state governance), providing statecraft with deep ethical and emotional roots.",
        "highlights": [
            {
                "zh": "大秩序与小秩序：家庭是国家的微缩版，国家是家庭的放大版，孝亲与忠国在逻辑上高度统一。",
                "en": "Macro & Micro Orders: The family is a microcosm of the state, and the state is an expanded family; filial piety and patriotism share logical unity."
            },
            {
                "zh": "伦理作为治理工具：不同于依赖法律强制的治理，中国传统社会通过家庭伦理实现低成本的自主治安与社会凝聚。",
                "en": "Ethics as Governance: Unlike governance relying purely on legal coercion, traditional China achieved low-cost self-governance via family ethics."
            },
            {
                "zh": "家国情怀的双刃剑：赋予文明强大的凝聚力与抗风险能力，但也需要现代公民意识的调和。",
                "en": "Double-Edged Sword: It bestows immense social cohesion and resilience, yet requires balancing with modern civic awareness."
            },
            {
                "zh": "文明长寿的奥秘：家国同构让社会基本单元（家庭）在战乱中能迅速重建文明秩序。",
                "en": "Secret of Longevity: This structure allowed the basic social unit (family) to rapidly rebuild civil order even after disastrous wars."
            }
        ]
    },
    6: {
        "gistZh": "秦始皇统一文字是中国文明史上最伟大的战略决策，汉字超越了方言隔阂与时代变迁，成为凝聚数亿人的不可消灭的文化基因。",
        "gistEn": "The standardization of written Chinese by Qin Shi Huang was the single greatest strategic decision in Chinese history—written Chinese transcended dialect barriers and time, becoming an indestructible cultural gene.",
        "highlights": [
            {
                "zh": "文字超越方言：即便各地口音相隔万里无法听懂，相同的方块字让政令、思想与文化毫无障碍地交流。",
                "en": "Transcending Dialects: Even when spoken dialects are mutually incomprehensible across regions, identical written characters enable seamless communication."
            },
            {
                "zh": "跨越时空的阅读：现代中国人能直接阅读两千年前的先秦古籍，这在拼音文字文明中是难以想象的。",
                "en": "Reading Across Millennia: Modern Chinese can directly read classical texts from 2,000 years ago, a phenomenon nearly impossible in alphabetic civilizations."
            },
            {
                "zh": "大一统的文化基石：统一文字锁定了中华文明的共同心理认同，使得中国即便分崩离析也必然重新走向统一。",
                "en": "Bedrock of Unity: Standardized writing anchored a shared psychological identity, ensuring China's eventual reunification even after collapses."
            },
            {
                "zh": "汉字的审美与艺术：汉字不仅是信息载体，更是书法艺术与审美哲学的载体。",
                "en": "Aesthetics of Chinese Characters: Chinese characters serve not just as informational tools, but as vessels for calligraphy and aesthetic philosophy."
            }
        ]
    },
    7: {
        "gistZh": "凉州（西北边陲）展现了超越血缘与族群隔阂的文化胸怀，融合多民族文化与西域文明，铸就了中华文化包容吸纳的硬朗基因。",
        "gistEn": "Liangzhou (the Northwestern frontier) exemplified a cultural open-mindedness transcending bloodlines and ethnic boundaries, fusing diverse ethnic and Silk Road civilizations into a resilient cultural gene.",
        "highlights": [
            {
                "zh": "超越血缘限制：中华文化并非建立在单一族群血缘之上，而是在边陲交融中不断吸纳新鲜血液。",
                "en": "Beyond Bloodlines: Chinese culture is not built on single-ethnic bloodlines, but constantly absorbs fresh vitality from frontier exchanges."
            },
            {
                "zh": "丝绸之路的前哨：凉州作为文化交汇重镇，守护并传播了中原文化与佛教文明。",
                "en": "Frontier of the Silk Road: As a hub of cultural crossroads, Liangzhou preserved and disseminated both Central Plain and Buddhist civilizations."
            },
            {
                "zh": "强悍与儒雅的结合：凉州风范融合了边塞的雄浑豪迈与中原的文化典雅，展现了中国文化的刚柔相济。",
                "en": "Robustness & Elegance: Liangzhou style fused frontier heroism with Central Plain refined culture, displaying complementary strength and grace."
            },
            {
                "zh": "开放包容的示范：证明中国文化越在边疆越具包容性，越能展现生生不息的同化力。",
                "en": "Exemplar of Inclusivity: Proving that Chinese culture expands its inclusivity at frontiers, showcasing immortal assimilative power."
            }
        ]
    },
    8: {
        "gistZh": "唐代长安是古代世界第一座国际化大都市，以开放的胸襟吸引全球商贾、留学生与艺术家，展现了中国文化最辉煌、自信的世界性生活方式。",
        "gistEn": "Tang Dynasty Chang'an was the ancient world's premier cosmopolitan metropolis, attracting global merchants, scholars, and artists with open confidence—exemplifying Chinese culture's most brilliant international lifestyle.",
        "highlights": [
            {
                "zh": "真正的世界都市：长安人口破百万，外国人占相当比例，官员、将军甚至包括许多外族人士。",
                "en": "A True Global Metropolis: Exceeding a million residents with a large foreign population, even government officials and generals hailed from abroad."
            },
            {
                "zh": "文化自信的峰值：不惧外来文化侵蚀，反而兼收并蓄，将西域音乐、服饰与饮食融入日常生活。",
                "en": "Peak Cultural Confidence: Unafraid of foreign influence, Chang'an enthusiastically integrated Silk Road music, fashion, and cuisine into daily life."
            },
            {
                "zh": "气度与包容：对待不同宗教（佛教、景教、祆教、伊斯兰教）一视同仁，给予高度自由。",
                "en": "Magnanimity & Freedom: Treating diverse faiths (Buddhism, Nestorianism, Zoroastrianism, Islam) with equal respect and freedom."
            },
            {
                "zh": "永恒的盛唐气象：长安不仅是一座城市，更是中国文化心胸开阔、万国来朝的大国象喻。",
                "en": "Immortal Grandeur of Tang: Chang'an was more than a city; it remains a metaphor for Chinese culture's open heart and cosmic grandeur."
            }
        ]
    },
    9: {
        "gistZh": "明末传教士利玛窦在中国成功传播西方科学与基督教，其经验揭示了中国文化崇尚和平、尊重智慧、不具侵略本性的文明特质。",
        "gistEn": "The success of Jesuit Matteo Ricci in late-Ming China revealed the fundamental traits of Chinese civilization: revering peace and wisdom, with a inherently non-aggressive nature.",
        "highlights": [
            {
                "zh": "利玛窦的本土化策略：穿儒服、通汉语、尊孔孟，用科学（地图、天文学）与道德赢得中国士大夫的尊重。",
                "en": "Matteo Ricci's Localization Strategy: Wearing Confucian robes, mastering Chinese, and using science (maps, astronomy) and virtue to win scholars' respect."
            },
            {
                "zh": "非侵略性的证明：中国文化乐于接受外来的真理与科技，只要其不带有武力威胁或蛮横征服。",
                "en": "Proof of Non-Aggression: Chinese culture readily accepts foreign truth and technology as long as it arrives without military force or coercion."
            },
            {
                "zh": "东西方文明的黄金对话：利玛窦与徐光启的合作（翻译《几何原本》）树立了跨文化理性交流的典范。",
                "en": "Golden Age of East-West Dialogue: Ricci's collaboration with Xu Guangqi (translating Euclid's Elements) set a model for rational cross-cultural exchange."
            },
            {
                "zh": "包容非排他：中国文化天生具备融通其他文明成果的胸怀，而非非黑即白的文明对抗。",
                "en": "Inclusivity over Exclusivity: Chinese culture inherently possesses the capacity to integrate achievements of other civilizations."
            }
        ]
    },
    10: {
        "gistZh": "科举制度是古代中国最伟大的制度创新之一，打破了世袭贵族垄断，建立了基于才学而非血统的平民阶层上升通道与文官治理体系。",
        "gistEn": "The Imperial Examination (Keju) was one of ancient China's greatest institutional innovations, breaking noble monopolies and establishing merit-based mobility and civil service governance.",
        "highlights": [
            {
                "zh": "打破贵族世袭：取消门第限制，让寒门子弟通过读书朝为田舍郎，暮登天子堂。",
                "en": "Breaking Hereditary Aristocracy: Abolishing birthright barriers, enabling commoners to rise to state leadership through rigorous study."
            },
            {
                "zh": "科举五大优点：公平竞争、文官政治、全国文化一体化、崇尚知识的风气以及社会流动机制。",
                "en": "Five Meritocratic Advantages: Fair competition, civil governance, national cultural unification, societal reverence for learning, and upward mobility."
            },
            {
                "zh": "文官治理范式：领先西方千余年建立专业的常任文官管理体系，保障政府运转稳定。",
                "en": "Civil Governance Paradigm: Establishing a professional meritocratic bureaucracy over a millennium ahead of the West."
            },
            {
                "zh": "历史局限与启发：虽后期陷入八股僵化，但其「唯才是举、公平竞争」的核心精神依然是现代文官制度的基石。",
                "en": "Modern Resonance: Though later stifled by rigid formats, its core spirit of meritocracy and fair competition remains the bedrock of modern civil service."
            }
        ]
    },
    11: {
        "gistZh": "「君子之交淡如水」体现了中国文化中关于友谊的最高智慧，强调情感的纯粹、人格的独立与长久的相互尊重，拒绝利益交换。",
        "gistEn": "'Friendship between gentlemen is as pure as water' reflects Chinese culture's highest wisdom on friendship, emphasizing emotional purity, personal independence, and mutual respect over transactional gain.",
        "highlights": [
            {
                "zh": "淡如水 vs 甘若醴：小人之交甘若醴（因利而聚、因利而散）；君子之交淡如水（不依附、不强求、久而弥香）。",
                "en": "Pure Water vs. Sweet Wine: Shallow friendship is sweet like wine for profit; noble friendship is pure as water—unattached, enduring, and respectful."
            },
            {
                "zh": "友谊是人生难题：人际关系最易毁于过于亲密导致的界限丧失与功利索取。",
                "en": "Friendship as a Life Challenge: Human relationships crumble easily when boundaries blur into needy utility or over-entanglement."
            },
            {
                "zh": "保持独立与尊严：真正的朋友相互理解独立的人格，无需频繁客套或利益捆绑。",
                "en": "Preserving Independence & Dignity: True friends honor each other's distinct individuality without requiring empty formalities or transactional ties."
            },
            {
                "zh": "知音难觅的精神寄托：从伯牙子期到竹林七贤，中国文化将友谊提升为灵魂深处的精神共鸣。",
                "en": "Spiritual Resonance of Soulmates: From Boya and Ziqi to the Seven Sages, Chinese culture elevates friendship into deep spiritual alignment."
            }
        ]
    },
    12: {
        "gistZh": "真诚与说真话是中国传统文化中的道德底线，反对用虚伪和套话替代真实，主张求真务实与直面事实的勇气。",
        "gistEn": "Sincerity and truth-telling form the ethical baseline of traditional Chinese thought, rejecting hypocrisy and empty rhetoric in favor of seeking truth from facts.",
        "highlights": [
            {
                "zh": "反对虚假繁荣：真正的文化繁荣建立在真实之上，任何虚构的历史与饰辞终将被历史唾弃。",
                "en": "Rejecting False Prosperity: True cultural vigor rests on honesty; fabricated histories and deceptive praise are eventually discarded by time."
            },
            {
                "zh": "史官精神：从齐太史到司马迁，中国历史学家宁死不改事实，奠定了「秉笔直书」的崇高道德传统。",
                "en": "The Historian's Courage: From ancient scribes to Sima Qian, Chinese historians risked death to record unvarnished truth, forging a noble tradition."
            },
            {
                "zh": "诚意正心：儒学将「诚」作为修身齐家的根本，不诚无物，虚伪是文明腐化的开始。",
                "en": "Sincerity of Mind: Confucianism places 'Sincerity' (Cheng) as the foundation of self-cultivation; hypocrisy marks the onset of cultural decay."
            },
            {
                "zh": "现实警示：在当代公共表达中，依然需要弘扬勇于说真话、不讲假话套话的清风。",
                "en": "Modern Imperative: In contemporary public dialogue, advocating courageous truth-telling remains a vital civic virtue."
            }
        ]
    },
    13: {
        "gistZh": "中国文化重新定义了「成功」，区分了世俗的功名利禄（一时之成功）与人格道德、文明贡献的立德立言（万世之成功）。",
        "gistEn": "Chinese culture redefines 'Success', distinguishing ephemeral worldly status from eternal success achieved through moral virtue, ideas, and cultural contribution ('Three Immortalities').",
        "highlights": [
            {
                "zh": "两种成功对比：一种是权力、财富与权势（随生命消逝）；一种是思想、文章与品格（历千年而不朽）。",
                "en": "Two Types of Success: Worldly power and wealth fade with life; enduring ideas, literature, and character shine across centuries."
            },
            {
                "zh": "三不朽理念：立德、立功、立言，中国智者追求的是将个体生命融入文明的长河中。",
                "en": "The Three Immortalities: Establishing Virtue, Service, and Words—Chinese sages sought to merge individual life into civilization's river."
            },
            {
                "zh": "苏东坡与杜甫的例子：世俗命运坎坷颠沛，但因其伟大的精神与诗篇，获得了真正的终极成功。",
                "en": "Examples of Su Shi & Du Fu: Though materially tragic, their sublime spirit and poetry granted them ultimate historical victory."
            },
            {
                "zh": "破解功利焦虑：给被现代成功学困扰的人们提供了重新审视人生价值的高远视角。",
                "en": "Overcoming Modern Anxiety: Providing a elevated perspective for individuals trapped in modern hyper-utilitarian rat races."
            }
        ]
    },
    14: {
        "gistZh": "道教作为中国本土宗教，核心呼唤在于对「和平、自然、生命」的关切，主张顺应天道、尊重生命规律与身心和谐。",
        "gistEn": "As China's indigenous religion, Taoism's core calling lies in its reverence for 'Peace, Nature, and Life'—advocating alignment with the Tao, respect for vital laws, and mind-body harmony.",
        "highlights": [
            {
                "zh": "三大核心呼唤：呼唤和平（反对战争杀戮）、呼唤自然（天人合一）、呼唤生命（贵生重生）。",
                "en": "Three Core Callings: Peaceful harmony (anti-war), Natural resonance (oneness of cosmos and human), and Vitality (revering physical & spiritual life)."
            },
            {
                "zh": "本土宗教的独特性：不同于向外探索或彼岸救赎，道教极其关切当下生命的健康、长寿与身心自在。",
                "en": "Uniqueness of Local Faith: Unlike religions focused purely on afterlife redemption, Taoism deeply cares for immediate health, longevity, and freedom."
            },
            {
                "zh": "天人合一生态观：将人类视为大自然的一部分，反对过度开发与违反自然的狂妄扩张。",
                "en": "Ecological Oneness: Viewing humanity as an intrinsic part of nature, opposing arrogant over-exploitation of environmental balance."
            },
            {
                "zh": "养生与艺术灵感：道教为中国中医药学、书法、山水画及养生哲学提供了源源不断的灵感。",
                "en": "Source of Healing & Arts: Inspiring Chinese traditional medicine, calligraphy, landscape painting, and holistic wellness practices."
            }
        ]
    },
    15: {
        "gistZh": "《心经》以极其精炼的文字（260字）阐释了佛教的核心智慧「色即是空，空即是色」，引导人们放下执念、破除恐惧，获得心灵的终极平静。",
        "gistEn": "The Heart Sutra concisely (260 characters) encapsulates Buddhism's core wisdom: 'Form is Emptiness, Emptiness is Form'—guiding minds to relinquish attachments, dissolve fear, and achieve inner tranquility.",
        "highlights": [
            {
                "zh": "佛教最简明支点：仅260字，却构成了中国佛教思想史上影响力最大的精神支柱。",
                "en": "Most Concise Spiritual Pillar: At just 260 characters, it stands as the most influential spiritual anchor in East Asian Buddhism."
            },
            {
                "zh": "「色即是空，空即是色」：现象与本质互为表里，万物皆在变化流转中，不必偏执于暂时的得失。",
                "en": "'Form is Emptiness, Emptiness is Form': Appearance and essence are interdependent; all phenomena shift, so do not cling rigidly to transient gain or loss."
            },
            {
                "zh": "无挂碍故，无有恐怖：破除对名利、生死与功利的执念，才能从根本上祛除焦虑与恐惧。",
                "en": "No Impediment, No Fear: Dissolving obsession with fame, life, or death cures anxiety and fear at their root."
            },
            {
                "zh": "中国化佛教的胜利：将深奥的印度佛学转化为中国人触手可及的切爽心灵智慧。",
                "en": "Victory of Sinicized Buddhism: Transforming complex Indian metaphysics into accessible, practical inner wisdom for daily life."
            }
        ]
    },
    16: {
        "gistZh": "李清照作为中国历史上最伟大的女词人，其作品展现了绝顶的文学才华、对爱情与家国命运的深刻体验，以及不让须眉的骨气与独立人格。",
        "gistEn": "Li Qingzhao, China's greatest female poet, demonstrated unsurpassed literary genius, profound reflection on love and national fate, and extraordinary personal fortitude.",
        "highlights": [
            {
                "zh": "文学史上的奇迹：突破封建时代对女性的压抑，以极高艺术成就跻身宋词最高巅峰。",
                "en": "A Historical Miracle: Shattering feudal constraints on women, reaching the absolute pinnacle of Song Dynasty Ci poetry."
            },
            {
                "zh": "前期与后期的转折：前期闺情清丽缠绵，后期国破家亡后词风变为苍凉悲壮、沉郁顿挫。",
                "en": "Artistic Evolution: Early works capture luminous love and joy; later poetry transforms into tragic, haunting elegies after war and exile."
            },
            {
                "zh": "不让须眉的骨气：「至今思项羽，不肯过江东」，对妥协偏安的南宋统治者提出最犀利的批判。",
                "en": "Heroic Fortitude: Lines like 'Still missing Xiang Yu, who refused to retreat across the River' offered fierce criticism of cowardly court appeasement."
            },
            {
                "zh": "独立人格典范：晚年宁可坐牢也要与人品卑劣的丈夫离婚，展现了中国女性罕见的尊严与勇气。",
                "en": "Model of Independence: In old age, she endured imprisonment rather than remain married to a corrupt husband, proving rare dignity and courage."
            }
        ]
    },
    17: {
        "gistZh": "唐诗是中国人文化修养与美学启蒙的天然起点，它用凝练的韵律与意境将审美、情感、哲学与家国情怀完美融入日常记忆。",
        "gistEn": "Tang Poetry is the natural starting point for Chinese cultural literacy and aesthetics—blending music, philosophy, and emotion into timeless collective memory.",
        "highlights": [
            {
                "zh": "全民文化起点：从小背诵的唐诗构成了全球华人共同的美学基因与情感底色。",
                "en": "Universal Literacy Foundation: Verses memorized in childhood form the shared aesthetic DNA and emotional resonance of Chinese people globally."
            },
            {
                "zh": "语言的极致艺术：将汉字的声音美、意象美与节奏感发挥到极致，不可替代也不可等翻译完全替代。",
                "en": "Pinnacle of Language Art: Pushing the acoustic, visual, and rhythmic beauty of Chinese characters to its ultimate height."
            },
            {
                "zh": "博大的精神气象：从李白的雄浑浪漫到杜甫的沉郁顿挫，涵盖了人类心灵的所有情感光谱。",
                "en": "Vast Spiritual Horizons: From Li Bai's cosmic romanticism to Du Fu's tragic realism, spanning every emotional spectrum of humanity."
            },
            {
                "zh": "诗意地栖居：唐诗让中国人即使在困顿与逆境中，依然能保有诗意的心灵与高尚的情趣。",
                "en": "Living Poetically: Tang poetry enables Chinese people to maintain poetic dignity and spiritual elevated taste even amidst suffering."
            }
        ]
    },
    18: {
        "gistZh": "宋代创造了中国古代最精致、优雅、富有生活情趣的文明形态，将茶道、瓷器、金石学与文人审美推向了世界历史的巅峰。",
        "gistEn": "The Song Dynasty birthed China's most exquisite, elegant lifestyle, elevating tea rituals, ceramics, antiquarianism, and scholarly aesthetics to global historic peaks.",
        "highlights": [
            {
                "zh": "生活美学的巅峰：点茶、焚香、插花、挂画「四般闲事」，将日常平淡生活升华为艺术享受。",
                "en": "Pinnacle of Living Aesthetics: Tea whisking, incense burning, flower arranging, and art appreciation transformed mundane life into fine art."
            },
            {
                "zh": "极简与典雅的审美：宋瓷（如汝窑）追求极简、素雅与温润，领先现代极简主义设计近千年。",
                "en": "Minimalist Elegance: Song ceramics (like Ru ware) embraced serene minimalism and subtle luster, anticipating modern design by 1,000 years."
            },
            {
                "zh": "市民文化与经济繁荣：取消宵禁，夜市繁华，清明上河图展现了充满活力的城市文明。",
                "en": "Vibrant Urban Civilization: Abolishing night curfews, thriving night markets—immortalized in the 'Along the River During the Qingming Festival' scroll."
            },
            {
                "zh": "陈寅恪的评价：「华夏民族之文化，历数千载之演进，造极于赵宋之世。」",
                "en": "Historian Chen Yinke's Tribute: 'The culture of the Chinese nation, evolving over thousands of years, reached its absolute zenith in the Song Dynasty.'"
            }
        ]
    },
    19: {
        "gistZh": "英国哲学家罗素对中国文化进行了深刻客观的剖析，盛赞中国人的和平理性、幽默与忍耐，同时也尖锐指出了缺乏现代科技与效率的弱点。",
        "gistEn": "British philosopher Bertrand Russell offered a profound, objective evaluation of Chinese culture—praising its peaceful rationality and humor, while warning of deficiencies in modern science and efficiency.",
        "highlights": [
            {
                "zh": "罗素的独特视角：作为西方智者，在1920年代造访中国，写下《中国问题》，给予中国文明极高敬意。",
                "en": "Russell's Unique Vision: Visiting China in the 1920s, the Western sage authored 'The Problem of China', offering immense respect for its civilization."
            },
            {
                "zh": "中国文化的极佳优点：崇尚和平、反对侵略扩张、富有生活幽默感、对自然的尊重与深沉的耐力。",
                "en": "China's Great Virtues: Love of peace, anti-expansionism, gentle humor in daily life, reverence for nature, and immense resilience."
            },
            {
                "zh": "历史缺陷与短板：缺乏现代科学逻辑、公共效率低下、面对工业强国侵略时过于软弱。",
                "en": "Historical Deficiencies: Lack of modern scientific logic, inefficient public administration, and vulnerability when facing industrialized aggression."
            },
            {
                "zh": "跨文化互补启示：西方需要学习中国的和平生活智慧，中国需要学习西方的科技与法治，双方互为救赎。",
                "en": "Cross-Cultural Complementarity: The West needs China's wisdom of peaceful living; China needs Western science and rule of law—each complementing the other."
            }
        ]
    },
    20: {
        "gistZh": "真正的文化创新不是被动跟在科技后面，而是让人文精神与文化伦理走在科技前面，为人工智能与技术时代提供方向与良知。",
        "gistEn": "True cultural innovation does not passively trail tech; it positions humanistic ethics ahead of science, providing direction and conscience in the AI age.",
        "highlights": [
            {
                "zh": "文化与科技的关系：科技提供工具与效率，文化提供目的与灵魂；没有文化的科技可能导向毁灭。",
                "en": "Culture & Tech Synergy: Science supplies tools and speed, while culture provides purpose and soul; tech without humanities risks catastrophe."
            },
            {
                "zh": "让文化走在科技前面：在数字与AI革命中，必须先建立人文伦理规范，防范科技异化与心灵空虚。",
                "en": "Leading Science with Culture: In AI and digital revolutions, humanistic ethics must lead to prevent technological alienation."
            },
            {
                "zh": "创新不是摒弃传统：真正的创新是在深厚文明土壤上长出的新芽，而非切断历史根脉的狂妄破坏。",
                "en": "Innovation vs. Tradition: Authentic innovation is a fresh bloom from deep historical soil, not reckless destruction of cultural roots."
            },
            {
                "zh": "中华文化的当代使命：用「天人合一、中庸和谐」的东方智慧为全球科技伦理治理贡献力量。",
                "en": "China's Contemporary Mission: Contributing Eastern wisdom of harmony to global technological and ethical governance."
            }
        ]
    },
    21: {
        "gistZh": "新儒学是对传统儒学在近现代遭遇危机后的深刻反思与自我革新，试图将儒家伦理与现代民主、科学及人权价值有机融通。",
        "gistEn": "New Confucianism is a profound reflection and self-renewal of traditional Confucianism facing modernity, bridging ancient ethics with science, democracy, and human rights.",
        "highlights": [
            {
                "zh": "近现代儒学危机：面对西学东渐与新文化运动，传统儒学曾被误认为阻碍现代化的绊脚石。",
                "en": "The Crisis of Modernity: Facing Western impact, traditional Confucianism was once misdiagnosed as an obstacle to modernization."
            },
            {
                "zh": "新儒家的历史功绩：熊十力、牟宗三、唐君毅等大师证明了儒学核心精神与现代文明并不冲突。",
                "en": "New Confucian Legacy: Masters like Xiong Shili and Mou Zongsan demonstrated that Confucian ethics harmonize with modern values."
            },
            {
                "zh": "内圣开出外王：从内在心性道德（内圣）开显出现代民主与科学制度（外王），完成文明的现代转向。",
                "en": "Inner Sage to Outer King: Deriving modern democratic institutions and scientific inquiry from inner moral self-cultivation."
            },
            {
                "zh": "全球化时代的价值：为现代人破解工具理性泛滥、道德滑坡与精神无家可归提供心灵归宿。",
                "en": "Global Value: Offering a spiritual sanctuary for humanity confronting modern hyper-rationalism and moral disorientation."
            }
        ]
    },
    22: {
        "gistZh": "中华文化历史上经历过多次大迁徙（如永嘉南渡、宋室南迁），但文化不仅没有在流动中湮灭，反而在迁徙融汇中获得了更强韧的生命力。",
        "gistEn": "Chinese culture survived major historical migrations (such as the Southern retreats); rather than perishing in transit, it gained newfound vitality through movement.",
        "highlights": [
            {
                "zh": "迁徙中的文化保存：每当北方战乱，文化精英与民众将文明种子带往江南与华南，实现文明的异地繁荣。",
                "en": "Cultural Preservation in Transit: During northern wars, elites and commoners carried cultural seeds south, flourishing in new soils."
            },
            {
                "zh": "在移动中活得更好：迁徙打破了区域封闭，促成了不同方言、民俗与文明形态的深度大融合。",
                "en": "Thriving in Movement: Migration shattered regional isolation, fostering rich synthesis across dialects, customs, and civilizations."
            },
            {
                "zh": "文化基因的流动性：证明中国文化不是僵硬固定的地理名词，而是随人流动、生生不息的活态生命体。",
                "en": "Fluidity of Cultural Genes: Proving Chinese culture is not a rigid geographical label, but a living organism moving with its people."
            },
            {
                "zh": "海外华人的文明延续：如同当代全球华人移民，无论走到哪里，中国文化的生活方式与价值观依然延续。",
                "en": "Global Diaspora Resonance: Just like modern global Chinese communities, cultural values and habits endure wherever people settle."
            }
        ]
    },
    23: {
        "gistZh": "汉文化在漫长历史中遇到了两个重大「陌生」——佛教文明的融入与西方近代文明的碰撞，正是两次拥抱陌生让中华文明实现了飞跃。",
        "gistEn": "Han culture encountered two monumental 'strangers' in history—Buddhism and modern Western civilization; embracing these strangers powered civilization's leaps.",
        "highlights": [
            {
                "zh": "第一个陌生（佛教）：汉代引入印度佛教，历经数百年争论与消化，最终彻底融入中国文化（形成禅宗）。",
                "en": "The First Stranger (Buddhism): Arriving from India, centuries of dialogue fully integrated Buddhism into Chinese thought (forming Zen)."
            },
            {
                "zh": "第二个陌生（西方现代文明）：明清以来面对西洋科学、工业与民主思想，经历了震荡、反思与全面吸收。",
                "en": "The Second Stranger (Western Modernity): Facing Western science and industrialization, undergoing shock, reflection, and creative absorption."
            },
            {
                "zh": "对待陌生的正确态度：不恐惧、不排外、不盲目崇拜，而是用自身强大的消化能力取其精华。",
                "en": "Correct Stance Toward Strangers: Neither xenophobic fear nor blind worship, but digesting essential wisdom with assimilative strength."
            },
            {
                "zh": "文明因互鉴而伟大：证明一个文化越敢于面对陌生的冲击，其生命力与包容度就越发强大。",
                "en": "Greatness Through Mutual Learning: Demonstrating that the braver a culture faces the unfamiliar, the stronger its enduring vitality."
            }
        ]
    },
    24: {
        "gistZh": "全课大回顾与总结：中国文化必修课带我们走过了数千年精神之旅，核心在于建立文化自信、修养君子人格，让古老文明在当代焕发光明。",
        "gistEn": "Course Grand Finale: A millennia-long spiritual journey concluding that Chinese culture's core lies in building cultural confidence, cultivating the Junzi ideal, and illuminating modern life.",
        "highlights": [
            {
                "zh": "文化之旅的总回顾：从文化的最小定义到君子人格、中庸之道、唐诗宋词，梳理了中华文明的精神脊梁。",
                "en": "Course Retrospective: From culture's definition to Junzi ethics, the Mean, Tang poetry, and Song living art—tracing civilization's spine."
            },
            {
                "zh": "重建文化自信：既不盲目自大，也不自卑自弃，理性客观地珍视我们文化中最优秀的精神遗产。",
                "en": "Rebuilding Cultural Confidence: Neither arrogant nor self-deprecating, but cherishing our finest spiritual heritage with rational clarity."
            },
            {
                "zh": "让文化落实在每个人身上：文化的最终成果是集体人格，每一个现代中国人的品行都是中国文化的活名片。",
                "en": "Living Culture in Every Individual: Culture's fruit is collective character; every individual's conduct is the living ambassador of our culture."
            },
            {
                "zh": "面向未来的嘱托：带上这份文化底蕴与智慧，在充满不确定性的世界中坚定、优雅、有远见地生活。",
                "en": "Charge for the Future: Carrying this heritage forward to live with poise, elegance, and vision in an uncertain global landscape."
            }
        ]
    }
}

def main():
    json_path = '/Users/hendrizhang/Desktop/HartCL/lessons_data.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        lessons = json.load(f)

    for l in lessons:
        idx = l['index']
        if idx in LESSON_SUMMARIES:
            l['summary'] = LESSON_SUMMARIES[idx]
            print(f"[{idx:02d}] Added deep curated summary for {l['title']}")
        else:
            print(f"[{idx:02d}] Missing summary for {l['title']}")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)

    print("\nAll 24 deep bilingual summaries written to lessons_data.json!")

if __name__ == '__main__':
    main()
