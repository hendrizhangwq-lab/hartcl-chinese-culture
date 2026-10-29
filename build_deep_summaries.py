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
                "zh": "文化是一种成为习惯的精神价值和生活方式，它的最终成果是集体人格。",
                "en": "Culture is a set of spiritual values and a way of life that have become ingrained habits, and its ultimate outcome is a collective personality."
            },
            {
                "zh": "理想集体人格：中国文化在历史沉淀中塑造出的典型集体人格是“君子”。",
                "en": "The Ideal Collective Personality: The hallmark collective personality cultivated throughout Chinese history is the 'Junzi' (Noble Person)."
            },
            {
                "zh": "知识 vs 文化：知识可以临时记忆，而文化是日常行为中不假思索的自然体现。",
                "en": "Knowledge vs. Culture: Knowledge can be temporarily memorized, whereas culture is a natural, reflexive expression in daily behavior."
            },
            {
                "zh": "集体记忆与延续性：中国文化的生命力在于数千年不曾间断的生活习惯与价值传承。",
                "en": "Collective Memory & Continuity: The vitality of Chinese culture stems from thousands of years of unbroken living habits and value transmission."
            }
        ],
        "vocabulary": [
            {
                        "word": "安身立命",
                        "pinyin": "ān shēn lì mìng",
                        "en": "To Establish Oneself & Find Spiritual Anchoring",
                        "explanationZh": "成语。安身指容身立足、解决生存；立命指精神有所寄托、确立人生信念与价值。余秋雨先生强调，跨国婚姻离异等现象折射出文化直指个体安身立命的精神根本，远比器物古董更关乎文化要害。",
                        "explanationEn": "Idiom: to find physical footing and establish spiritual/moral grounding. Yu Qiuyu stresses that culture fundamentally governs an individual's spiritual anchor and existential values, far deeper than relics or artifacts."
            },
            {
                        "word": "亲情伦理",
                        "pinyin": "qīn qíng lún lǐ",
                        "en": "Familial & Filial Ethics",
                        "explanationZh": "基于血缘亲族形成的道德准则与情感契约，强调尊祖敬宗、孝养父母、顾念手足。这是中华民族数千年沉淀出的核心精神价值之一，成为中国人最不假思索的责任本能。",
                        "explanationEn": "The moral and emotional responsibilities rooted in kinship, filial piety, and ancestral reverence—one of the foundational spiritual values deeply ingrained in the Chinese cultural psyche."
            },
            {
                        "word": "扫墓",
                        "pinyin": "sǎo mù",
                        "en": "Sweeping Ancestral Graves (Tomb Sweeping)",
                        "explanationZh": "清明节祭扫祖茔、缅怀先人的古老传统。它不仅是一种礼仪，更是一种深深嵌入中国人年历周期的习惯生活方式，承载着慎终追远、血脉延续的深厚文化情思。",
                        "explanationEn": "The ancient practice of sweeping ancestral graves during the Qingming Festival. It is both a solemn filial ritual and a habitual cultural way of life embodying lineage continuity and ancestral reverence."
            },
            {
                        "word": "主心骨",
                        "pinyin": "zhǔ xīn gǔ",
                        "en": "Core Backbone / Guiding Pillar",
                        "explanationZh": "支撑整体运转的核心支柱与内在灵魂。人类早期的生活习惯仅为求生；当人们在日常习惯中提炼出处理人与天地、家庭、同伴关系的准则时，精神价值便成为文化的坚强主心骨。",
                        "explanationEn": "The central backbone or governing core. Once spiritual values emerge from everyday survival habits, culture gains its spiritual backbone and enduring integrity."
            },
            {
                        "word": "生命幅度",
                        "pinyin": "shēng mìng fú dù",
                        "en": "Span of Life's Vitality / Cultural Breadth",
                        "explanationZh": "文化所涵盖的生动视野与包容范围。余秋雨批评部分文人既不探寻崇高的精神殿堂，又轻视民间的衣食住行日常，放弃了文化应有的阔大生命幅度，陷入孤芳自赏的泥潭。",
                        "explanationEn": "The comprehensive breadth of human vitality that culture should encompass—bridging the highest metaphysical ideals down to the lived realities of daily food, clothing, and shelter."
            },
            {
                        "word": "咬文嚼字",
                        "pinyin": "yǎo wén jiáo zì",
                        "en": "Pedantic Wordplay / Nitpicking over Diction",
                        "explanationZh": "成语。过分拘泥或卖弄词句辞藻，故作高深。作者以此警示学者不应脱离生生不息的大众实践，而应从书斋清谈走向广阔的生态之地创造活的文化。",
                        "explanationEn": "Idiom: indulging in pedantic wordplay or overly precious textual nitpicking, divorcing cultural inquiry from the pulsating realities of living human experience."
            },
            {
                        "word": "集体人格",
                        "pinyin": "jí tǐ rén gé",
                        "en": "Collective Personality",
                        "explanationZh": "余秋雨文化定义的核心关键词与落脚点。指一种文化历经千百年沉淀，在全体族群成员中结晶出来的共同生命格调、行为规约与潜意识默契，也是文化的最终成果。",
                        "explanationEn": "The paramount concept in Yu Qiuyu's definition: the shared disposition, moral habits, and behavioral blueprint crystallized across generations within a civilization—the ultimate fruit of culture."
            },
            {
                        "word": "格调",
                        "pinyin": "gé diào",
                        "en": "Moral Style / Spiritual Caliber",
                        "explanationZh": "人格的精神境界、风骨气度与审美品位。人格不仅表现为外在的行为规范，更体现为内在精神格调的高下与纯粹。",
                        "explanationEn": "Spiritual demeanor, moral poise, and aesthetic caliber governing how an individual or group carries themselves in thought and action."
            },
            {
                        "word": "默契",
                        "pinyin": "mò qì",
                        "en": "Tacit Understanding / Unspoken Consensus",
                        "explanationZh": "无需外在律令明文约定、却在群体间心照不宣的情感与认知共识。集体人格深入族群潜意识中，化作日常举手投足间的自然默契与本能反应。",
                        "explanationEn": "An intuitive, unspoken alignment in values and conduct that lives naturally within a people's collective subconscious without needing formal codification."
            },
            {
                        "word": "荣格",
                        "pinyin": "Róng gé",
                        "en": "Carl Gustav Jung",
                        "explanationZh": "瑞士著名心理学家，分析心理学创始者。他提出“集体无意识”与“文化最终成果是人格”的学说，强调各民族文化的深层积淀必然具象化为该民族的集体人格。",
                        "explanationEn": "Swiss psychiatrist and psychoanalyst who founded analytical psychology. Jung posited that the ultimate fruit of culture is personality, and that every civilization crystallizes a distinct collective psyche."
            },
            {
                        "word": "浮士德",
                        "pinyin": "Fú shì dé",
                        "en": "Faust (Literary Archetype)",
                        "explanationZh": "德国文豪歌德笔下的悲剧主角。荣格指出，并非歌德凭空创造了浮士德，而是德意志民族积淀的集体人格借歌德之笔将浮士德这一无尽求索的象征体具象化。",
                        "explanationEn": "The protagonist of Goethe's magnum opus. Jung famously argued that Goethe did not merely invent Faust; rather, the centuries of German cultural sediment created Faust, who in turn shaped Goethe."
            },
            {
                        "word": "国民性",
                        "pinyin": "guó mín xìng",
                        "en": "National Character",
                        "explanationZh": "一个国家或民族在思想意识与行为方式上的普遍特征。20世纪初鲁迅吸纳荣格等现代心理学思想，将其译为“国民性”，并以文学手术刀解剖中国传统人格的病态。",
                        "explanationEn": "The shared psychological character of a nation's people. Early 20th-century writer Lu Xun adopted this concept to diagnose and reform the deep-seated spiritual maladies in traditional Chinese society."
            },
            {
                        "word": "阿Q / 孔乙己",
                        "pinyin": "Ā Q / Kǒng Yǐ jǐ",
                        "en": "Ah Q & Kong Yiji (Cultural Archetypes)",
                        "explanationZh": "鲁迅塑造的标志性人物原型。阿Q以“精神胜利法”遮蔽屈辱，孔乙己以迂腐自矜掩饰无能，二者皆为旧文化沉淀出的负面集体人格结晶，体现了改造国民性的紧迫性。",
                        "explanationEn": "Archetypal characters in Lu Xun's fiction: Ah Q embodies rationalized self-delusion ('spiritual victory'), while Kong Yiji embodies tragic intellectual pedantry under decaying feudal examinations."
            },
            {
                        "word": "君子之道",
                        "pinyin": "jūn zǐ zhī dào",
                        "en": "The Way of the Junzi (Exemplary Person)",
                        "explanationZh": "中国儒家文化对集体人格设立的最高理想模型。君子胸怀仁德、克己复礼、胸襟坦荡，孔子将做君子视为中国文化实践的起点与终点，是中华文明的道德灵魂。",
                        "explanationEn": "The quintessential personality ideal cultivated by Confucianism: a person of moral excellence, benevolence, integrity, and social duty—the central moral pillar of Chinese civilization."
            },
            {
                        "word": "小人",
                        "pinyin": "xiǎo rén",
                        "en": "Petty Person / Moral Opportunist",
                        "explanationZh": "儒家语境中与“君子”对立的集体人格模型。指心胸狭隘、惟利是图、见利忘义、谄上欺下之人。孔子以“君子怀德，小人怀土；君子喻于义，小人喻于利”厘清二者界限。",
                        "explanationEn": "The antithesis of the Junzi in Confucian thought: an unprincipled, self-serving individual who prioritizes immediate gain over justice, integrity, and ethical duty."
            },
            {
                        "word": "觉者",
                        "pinyin": "jué zhě",
                        "en": "The Awakened One (Buddhist Ideal)",
                        "explanationZh": "中国佛家文化的理想人格模型。“觉”即明心见性、破除执念无明、彻悟宇宙生命真相。觉者超脱贪嗔痴与尘世束缚，展现大慈大悲的情怀。",
                        "explanationEn": "Buddhism's ideal personality archetype: an enlightened being who has awakened from worldly delusions, transcending suffering with profound wisdom and boundless compassion."
            },
            {
                        "word": "真人",
                        "pinyin": "zhēn rén",
                        "en": "The Authentic Person (Daoist Ideal)",
                        "explanationZh": "中国道家（老庄）哲学的理想人格模型。指体悟大道、顺应造化、不为世俗功利名教所拘、保持天真本色的通达超凡者，与儒家君子、佛家觉者形成互补。",
                        "explanationEn": "Daoism's ideal personality archetype: an authentic individual living in complete harmony with Nature (the Dao), free from artificial social dogma, pretension, and worldly vanity."
            },
            {
                        "word": "全球视野",
                        "pinyin": "quán qiú shì yě",
                        "en": "Global Perspective",
                        "explanationZh": "跨越单一文明维度的宏观审视视角。余秋雨强调讲述中国文化必须站在全人类多元文明的对照坐标系中，既领会中国君子之道的独特性，又与西方骑士、绅士等文化模型交相辉映。",
                        "explanationEn": "A broad, comparative vantage point situating Chinese civilization alongside other world cultures, evaluating ideals like the Junzi in fruitful dialogue with global archetypes like the gentleman or philosopher."
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
        ],
        "vocabulary": [
            {
                "word": "物物者非物",
                "pinyin": "wù wù zhě fēi wù",
                "en": "The Creator of Things Is Not a Thing",
                "explanationZh": "《庄子·知北游》及《秋水》中的核心命题。前一个“物”为动词（创造物、使物成其为物），后两个“物”为名词。意指让万物生成、运转的终极法则或精神力量（道与造物精神），其本身绝非受制于形器的物质。人作为能参赞化育的精神主体，不可降格为被物质奴役的器物。",
                "explanationEn": "A foundational metaphysical proposition from Zhuangzi. The first 'wu' functions as a transitive verb ('to create things' / 'to render things as things'), while the subsequent instances are nouns. It posits that the ultimate creative force and animating consciousness behind material phenomena is not itself a material object. Humans, as spiritual creators, must not degrade themselves into mere instruments dominated by material possessions."
            },
            {
                "word": "上善若水",
                "pinyin": "shàng shàn ruò shuǐ",
                "en": "Supreme Good Is Like Water",
                "explanationZh": "老子《道德经》第八章名言。水滋润天下万物而与世无争，甘居于众生不愿处的低洼下流。余秋雨强调，上善若水是中国哲学最高的至善道德与处世境界，与权术阴谋截然对立，是生命最温和却最顽强的精神支柱。",
                "explanationEn": "A core maxim from Chapter 8 of Laozi's Daodejing. Water nourishes all living things without contending, willingly resting in the lowly places that humans disfavor. Yu Qiuyu underscores that this represents the pinnacle of moral excellence and existential quietude in Chinese philosophy—the exact antithesis of calculated conspiracy."
            },
            {
                "word": "迎刃而解",
                "pinyin": "yíng rèn ér jiě",
                "en": "To Split Effortlessly Before the Blade / Readily Solved",
                "explanationZh": "成语，出自《晋书·杜预传》。劈竹子时只要劈开前面几节，下面就顺着刀刃破裂开来；比喻抓住了根本关键，主要问题解决了，其他许多矛盾与困惑便随之自然化解。",
                "explanationEn": "Idiom: splitting like bamboo before the blade. When the blade cleaves the first few joints, the rest splinters open effortlessly. Metaphorically signifies that when the foundational philosophical truth is grasped, myriad confusions and life dilemmas dissolve naturally."
            },
            {
                "word": "水滴石穿",
                "pinyin": "shuǐ dī shí chuān",
                "en": "Water Drops Piercing Stone",
                "explanationZh": "成语。滴水不息，历经岁月终能穿透坚石。余秋雨先生在此做了独到的哲学辨析：常人误以为这是滴水向石头宣战的坚韧谋略，但老庄哲学中水从未视石头为敌人，石穿并非蓄谋设计的胜负征服，而是天体自然的道法演进。",
                "explanationEn": "Idiom: dripping water wears away stone. Yu Qiuyu offers a profound philosophical distinction: conventional thinking views this as an adversarial siege where water conquers rock through grit. In Daoist philosophy, however, water harbors no enmity; piercing stone is not a premeditated conquest, but an effortless manifestation of natural law (Dao)."
            },
            {
                "word": "行于大道",
                "pinyin": "xíng yú dà dào",
                "en": "Walking upon the Great Dao",
                "explanationZh": "遵循天地自然与宇宙生灭的根本法则行事。老子倡导人应顺应规律、返璞归真，不以人为的机巧私欲去破坏万物的自然秩序。",
                "explanationEn": "Walking in alignment with the Great Way (Dao)—the underlying celestial principle governing nature and the cosmos. It implies living in harmony with cosmic rhythms without artificial cunning or selfish contrivance."
            },
            {
                "word": "相反相成",
                "pinyin": "xiāng fǎn xiāng chéng",
                "en": "Opposites Complement and Fulfill Each Other",
                "explanationZh": "指矛盾对立的双方在深刻的哲理层面上互为前提、相互依存、相互促成。老子以此揭示有无相生、难易相成、长短相形、高下相倾的宇宙辩证法。",
                "explanationEn": "The dialectical truth that contradictory opposites mutually define, rely upon, and complete each other—such as presence and absence, difficulty and ease, lightness and shadow. This forms the heart of Daoist cosmic balance."
            },
            {
                "word": "无为而治",
                "pinyin": "wú wéi ér zhì",
                "en": "Governance Through Non-Action (Wu Wei)",
                "explanationZh": "道家根本政治与人生哲学。“无为”并非消极不作为，而是不违背自然规律、不妄加人为苛扰与过度干预，使万物与百姓能够充分自主生长、各得其所。",
                "explanationEn": "The classical Daoist philosophy of governance and living. 'Non-action' (Wu Wei) does not mean passive indolence; rather, it denotes avoiding arbitrary meddling, excessive coercion, and artificial disruptions against natural spontaneity, enabling society and nature to flourish self-organizingly."
            },
            {
                "word": "和光同尘",
                "pinyin": "hé guāng tóng chén",
                "en": "Softening One's Glare and Merging with Dust",
                "explanationZh": "出自《道德经》。和其光，同其尘。收敛刺目的锋芒与光芒，与纷扰平易的尘俗世间融为一体。形容具有极高精神修为者不矜才使气，温润含蓄，超然物外。",
                "explanationEn": "From Chapter 56 of the Daodejing: tempering one's blinding brilliance and blending peacefully with the dust of the mundane world. It describes the enlightened sage who disdains arrogance and ostentation, living serenely with humility and inner light."
            },
            {
                "word": "韬光养晦",
                "pinyin": "tāo guāng yǎng huì",
                "en": "Concealing One's Brilliance to Cultivate Strength",
                "explanationZh": "比喻隐匿光芒、收束锋芒，在静默安详中积蓄修养与内力。常人常将此误读为潜伏伺机的险恶权谋，而余秋雨指出老子的本意是甘居低下、安顿性命的纯粹至善。",
                "explanationEn": "Concealing one's brilliance to cultivate quiet inner depth. While often misunderstood in vulgar politics as tactical scheming, Yu Qiuyu explains that in Laozi's original vision, it reflects a genuine embrace of tranquility, humility, and moral integrity without aggressive rivalry."
            },
            {
                "word": "大伪",
                "pinyin": "dà wěi",
                "en": "Supreme Hypocrisy / Great Artifice",
                "explanationZh": "人为刻意矫饰所造成的虚伪与伪饰。《道德经》云：“智慧出，有大伪。” 余秋雨警示世人切勿将老子崇高纯粹的大善曲解附会为深藏不露的大伪或官场厚黑术。",
                "explanationEn": "The superficial pretense and deceit born of contrived cleverness. As the Daodejing notes, 'When artificial cunning appears, great hypocrisy arises.' The lecture cautions against corrupting Laozi's sublime benevolence into hypocritical statecraft or political manipulation."
            },
            {
                "word": "老滑头",
                "pinyin": "lǎo huá tóu",
                "en": "Sly Old Fox / Crafty Opportunist",
                "explanationZh": "俗语，指处世油滑、善于见风使舵、不肯承担责任之人。部分近代学者将老子的玄妙隐忍曲解为世故圆滑的老滑头，余秋雨对此提出严厉驳斥，正本清源。",
                "explanationEn": "A colloquial term for a slick, opportunistic person adept at evasion. Some modern commentators have mislabeled Laozi as a cynical, worldly schemer—a gross misunderstanding that Yu Qiuyu passionately refutes."
            },
            {
                "word": "老庄哲学",
                "pinyin": "lǎo zhuāng zhé xué",
                "en": "Lao-Zhuang Philosophy",
                "explanationZh": "先秦道家思想的统称，由老子奠基、庄子发扬光大。老子偏重于形而上的宇宙根本之道与治道境界，庄子则进一步转向个体精神的绝对自由、审美品味与逍遥解脱。",
                "explanationEn": "The collective philosophy of Laozi and Zhuangzi, the foundational twin masters of Daoism. Laozi laid down the metaphysical cosmic Dao and principles of non-contention, while Zhuangzi expanded these into individual spiritual emancipation, boundless imagination, and aesthetic freedom."
            },
            {
                "word": "逍遥游",
                "pinyin": "xiāo yáo yóu",
                "en": "Carefree Wandering (Xiaoyaoyou)",
                "explanationZh": "《庄子》首篇兼其哲学巅峰之作。通过鲲鹏展翅九万里与小雀斥鴳的对比，阐述超越肉体受限、世俗名誉与物质束缚，达到乘天地之正、御六气之辩的终极精神自由。",
                "explanationEn": "The opening and crowning chapter of the Zhuangzi. Through the contrast of the colossal Peng bird soaring 90,000 li against petty sparrows, Zhuangzi portrays the ultimate state of spiritual liberation—transcending physical limits, worldly accolades, and self-centered anxieties."
            },
            {
                "word": "先秦诸子",
                "pinyin": "xiān qín zhū zǐ",
                "en": "Pre-Qin Masters / Hundred Schools of Thought",
                "explanationZh": "春秋战国时期中国思想文化的黄金时代，以孔子、老子、庄子、孟子、墨子等为代表的百家学派。余秋雨从文学审美品味的角度将其排名为：庄子第一、孟子第二、老子第三、孔子第四。",
                "explanationEn": "The diverse intellectual masters of the Spring and Autumn and Warring States periods (Confucianism, Daoism, Mohism, Legalism). From a literary aesthetics standpoint, Yu Qiuyu famously ranks Zhuangzi first, followed by Mencius, Laozi, and Confucius."
            },
            {
                "word": "寓言",
                "pinyin": "yù yán",
                "en": "Allegory / Philosophical Parable",
                "explanationZh": "寄寓哲理于具体生动故事之中的文学表现手法。《庄子》全书寓言十九，庄子如同拥有孩童般纯真清澈的眼光，不立威严说教，而是以奇幻瑰丽的神话寓言启发心灵。",
                "explanationEn": "Literary parables embodying profound metaphysical insights. Nearly ninety percent of Zhuangzi's writings are allegories; rather than lecturing dogmatically from an ivory tower, Zhuangzi approaches the cosmos with the curious, unclouded gaze of an artist and child."
            },
            {
                "word": "秋水篇",
                "pinyin": "qiū shuǐ piān",
                "en": "The 'Autumn Floods' Chapter (Qiu Shui)",
                "explanationZh": "《庄子·外篇》名篇。以河伯欣然自喜顺流东行、望见无边北海而叹服的对话，论证视角的相对性，揭示跳出有限认知、以无限宏阔的“道”审视万物的哲学方法。",
                "explanationEn": "A celebrated chapter from the Zhuangzi. Through the parable of the River God (Hebo) marveling at his own vastness until meeting the infinite Northern Sea (Beihai Ruo), it expounds epistemic humility and the necessity of viewing reality through cosmic relativism."
            },
            {
                "word": "以人论物",
                "pinyin": "yǐ rén lùn wù",
                "en": "Appraising Things from the Human & Dao Perspective",
                "explanationZh": "庄子关于人与物质关系的核心命题。主张从人的崇高精神尊严与天道本质来审度万物，让物质为人服务，而非让物质反客为主成为评判人类生命价值与尊严的尺度。",
                "explanationEn": "Zhuangzi's profound criterion regarding human relationship with the material world. It insists that things must be evaluated through the lens of human spiritual dignity and the Dao, rather than allowing external objects to define a human being's worth."
            },
            {
                "word": "以物论物",
                "pinyin": "yǐ wù lùn wù",
                "en": "Measuring Worth Purely by Material Quantity",
                "explanationZh": "以物质多寡、财产数目或外在器物的等级来判定人的高低贵贱（如以存款三百万或四百万来衡量人）。庄子严厉批评这种见物不见人的异化现象，告诫人不要沦为物质的奴隶。",
                "explanationEn": "The alienated practice of measuring human beings solely by their material possessions, monetary balances, or commercial assets. Zhuangzi critiques this commodification of human identity, warning that measuring humanity by material criteria reduces human beings to mere things."
            }
        ]
    },
    "02-01": {
        "gistZh": "庄子哲学以“物物者非物”揭示人与宇宙的生命法则，倡导打破以物观物的狭隘局限，通过“无待”与“无己”的超越境界，追求超越世俗束缚的绝对精神自由与“真人”的人格理想。",
        "gistEn": "Zhuangzi's philosophy establishes that 'the creator of things is not a thing', urging humanity to transcend material-centric perception. Through 'Wu Dai' (non-dependence) and 'Wu Ji' (selflessness), it pursues absolute spiritual liberation and the ideal of the 'Zhenren' (Real Person).",
        "highlights": [
            {
                "zh": "物物者非物：造物者与生命主体绝非受制于形器的物质，应以道观物而非以物观物。",
                "en": "The Creator of Things Is Not a Thing: The creative subject is not a material object; one must view reality through the Dao rather than through materialism."
            },
            {
                "zh": "超越世俗羁绊：打破分数、财富、名利等功利评价体系，追求生命本真的自由与内心的平静。",
                "en": "Transcending Worldly Fret: Shattering utilitarian metrics like grades, wealth, and status to embrace authentic inner peace and spiritual freedom."
            },
            {
                "zh": "无待与无己：“无待”即摆脱外在依赖与被迫等待，“无己”即破除自我执念与功利计较。",
                "en": "Non-Dependence & Selflessness: 'Wu Dai' frees the soul from external dependencies, while 'Wu Ji' dismantles self-centered anxieties and competitive vanity."
            },
            {
                "zh": "道家真人理想：相较于儒家“君子”、佛家“觉者”，道家“真人”顺应天道、回归天然，实现生命根气的通达。",
                "en": "The Ideal of the Zhenren: Distinct from the Confucian 'Junzi' or Buddhist 'Awakened One', Daoism's 'Real Person' lives in effortless accord with nature."
            }
        ],
        "vocabulary": [
            {
                "word": "物物者非物",
                "pinyin": "wù wù zhě fēi wù",
                "en": "The Creator of Things Is Not a Thing",
                "explanationZh": "庄子哲学最核心的命题之一。前一个“物”为动词（创造物、支配物），后两个“物”为名词。指主导万物化育的力量与人自身的精神主体绝非形器物质本身。人若被物质与名利奴役，便丧失了创造者的神圣地位。",
                "explanationEn": "A foundational Daoist proposition: the animating power that creates and governs objects is not itself a material object. Human consciousness must not be enslaved by the very possessions and accolades it creates."
            },
            {
                "word": "以物观物",
                "pinyin": "yǐ wù guān wù",
                "en": "Viewing Things Through Materialism",
                "explanationZh": "陷在物质、功利与世俗指标里相互攀比的认知方式。如比拼房产、车子、存款或名次，这种局限视角会将人的精神主体埋没于功利俗套之中。",
                "explanationEn": "A reductionist, material-centric mindset trapped in comparing possessions, wealth, and social rankings, thereby burying human spiritual dignity under utilitarian anxieties."
            },
            {
                "word": "以道观物",
                "pinyin": "yǐ dào guān wù",
                "en": "Viewing Things Through the Lens of the Dao",
                "explanationZh": "站在宇宙大道与生命全局的高度审视万物的宏阔视角。如同登临山顶俯瞰纷扰红尘，能深刻洞察世俗名利的短暂与虚妄，赋予心灵超然与从容。",
                "explanationEn": "Surveying existence from the lofty vantage point of cosmic harmony (the Dao). Like standing on a mountain peak viewing the valley below, it dissolves mundane rivalries into serene clarity."
            },
            {
                "word": "逍遥游",
                "pinyin": "xiāo yáo yóu",
                "en": "Carefree Wandering (Xiaoyaoyou)",
                "explanationZh": "庄子代表作与哲学巅峰境界。指心灵完全摆脱世俗功利、名誉约束与肉体困顿，在天地宇宙间获得无拘无束、纵横驰骋的绝对精神自由。",
                "explanationEn": "Zhuangzi's hallmark concept: ultimate spiritual emancipation wherein the soul soars unimpeded across the cosmic expanse, entirely free from utilitarian coercion and social pretension."
            },
            {
                "word": "无待",
                "pinyin": "wú dài",
                "en": "Non-Dependence / Absolute Freedom",
                "explanationZh": "逍遥游的核心条件之一。“待”即等待、依赖与条件限制。无待意味着生命不依赖外在的风力、时势或他人脸色，摆脱被动与被控，达到自足自主的彻底自由。",
                "explanationEn": "A prerequisite for Carefree Wandering: transcending reliance on external conditions, praise, or favorable winds, thereby attaining self-contained autonomy without passive subordination."
            },
            {
                "word": "无己",
                "pinyin": "wú jǐ",
                "en": "Selflessness / Transcending Self-Obsession",
                "explanationZh": "逍遥游的另一核心条件。破除以自我为中心的狭隘执念、成败得失与功利虚荣。只有放下“我”的困顿与计较，才能融于天地自然，获得无边广阔的心灵空间。",
                "explanationEn": "Dissolving egocentric anxiety, competitive pride, and self-serving vanity. By shedding narrow self-obsession, the individual merges seamlessly with the boundless rhythm of the universe."
            },
            {
                "word": "真人",
                "pinyin": "zhēn rén",
                "en": "The Real Person / Authentic Sage",
                "explanationZh": "庄子及道家所立的理想人格模型。指返璞归真、体悟大道、不欺弱、不自雄、不计谋，超脱生死毁誉与外在束缚的纯粹真诚之士。",
                "explanationEn": "Daoism's ideal personality archetype: an authentic human being who eschews deceit, arrogance, and manipulative schemes, living with spontaneous sincerity in harmony with nature."
            },
            {
                "word": "君子",
                "pinyin": "jūn zǐ",
                "en": "The Exemplary Person (Confucian Ideal)",
                "explanationZh": "中国儒家文化塑造的理想人格。强调修己安人、践行仁义礼智信、具有社会担当与道德自律，与道家的“真人”、佛家的“觉者”交相辉映。",
                "explanationEn": "The Confucian personality ideal: a person of supreme moral integrity, benevolence, social responsibility, and self-cultivation who anchors ethical social order."
            },
            {
                "word": "觉者",
                "pinyin": "jué zhě",
                "en": "The Awakened One (Buddhist Ideal)",
                "explanationZh": "中国佛家文化的理想人格。指破除执念无明、彻悟生命真相、超脱贪嗔痴束缚并怀大慈大悲之心的觉悟者（佛陀与菩萨境界）。",
                "explanationEn": "The Buddhist ideal: an enlightened being who has awakened from illusion and karmic suffering, embodying profound transcendent wisdom and universal compassion."
            },
            {
                "word": "不逆寡",
                "pinyin": "bù nì guǎ",
                "en": "Not Overpowering the Vulnerable",
                "explanationZh": "《庄子·大宗师》描述古代真人的品质。指不凭借强权去背逆或欺压弱小者，不以大欺小、不以强凌弱，体现了道家温和宽厚的生命慈悲。",
                "explanationEn": "A virtue of the ancient Zhenren in Zhuangzi: refusing to coerce or overpower the weak and vulnerable, embodying Daoist compassion and non-aggressive gentleness."
            },
            {
                "word": "不雄成",
                "pinyin": "bù xióng chéng",
                "en": "Not Flaunting Success",
                "explanationZh": "古之真人的品质。指有了成功与成就也不自恃英雄、不炫耀夸耀，保持谦逊沉静，不把功名当作傲视他人的资本。",
                "explanationEn": "A trait of the authentic sage: not boasting of personal triumphs or parading accomplishments, remaining humble and grounded amidst success."
            },
            {
                "word": "不谟士",
                "pinyin": "bù mó shì",
                "en": "Free from Devious Schemes",
                "explanationZh": "古之真人的品质。指不耍阴谋诡计、不上心机权术、不搞利益算计，坦荡光明，如日月朗照般自然纯粹。",
                "explanationEn": "Refraining from manipulative contrivance, political plotting, or calculated duplicity; conducting oneself with unclouded transparency and authentic purity."
            },
            {
                "word": "真人之息以踵",
                "pinyin": "zhēn rén zhī xī yǐ zhǒng",
                "en": "The True Person Breathes from the Heels",
                "explanationZh": "庄子对真人生命根气与呼吸境界的深刻比喻。真人的呼吸通达深入至脚跟，代表生命能量充盈通畅；而常人浮躁浅薄，呼吸仅滞留于喉咙。",
                "explanationEn": "Zhuangzi's visceral metaphor for spiritual vitality: the authentic sage's breath reaches deep down to the heels, while ordinary people breathe shallowly from the throat."
            },
            {
                "word": "天机",
                "pinyin": "tiān jī",
                "en": "Heavenly Capacity / Natural Vitality",
                "explanationZh": "生命与生俱来的天然灵性与内在根器。庄子云：“其耆欲深者，其天机浅。”如果一个人被世俗欲望与物欲深深奴役，其天赋予的灵性与智慧就会日渐枯竭。",
                "explanationEn": "The innate spiritual capacity and wisdom granted by Nature. As Zhuangzi warns, 'He whose worldly desires are deep has shallow natural wisdom.'"
            },
            {
                "word": "屈服者其嗌言若哇",
                "pinyin": "qū fú zhě qí yì yán ruò wā",
                "en": "Subservient Words Are Choked and Obstructed",
                "explanationZh": "庄子警句。指一个人若屈服于他人权势或世俗欲望，说话就会委曲谄媚、吞吞吐吐，无法坦荡直言，丧失了生命的独立尊严。",
                "explanationEn": "Zhuangzi's observation: when a person surrenders to external coercion or base desires, their speech becomes choked, timid, and servile, forfeiting authentic expression."
            },
            {
                "word": "不以心捐道",
                "pinyin": "bù yǐ xīn juān dào",
                "en": "Not Impairing the Dao with Human Intellect",
                "explanationZh": "真人的修为原则。“心”指人类私意、妄想与狡黠的智巧。不用人为的狭隘私心去损害、扭曲天然崇高的宇宙大道，顺应自然规律。",
                "explanationEn": "A core principle of the Zhenren: refraining from using narrow human contrivance, artificial cleverness, or arrogant ego to distort natural cosmic truth."
            },
            {
                "word": "不以人助天",
                "pinyin": "bù yǐ rén zhù tiān",
                "en": "Not Replacing Nature with Human Artifice",
                "explanationZh": "真人的修为原则。不用人为强加的干预、矫饰或破坏去替加天然造化，保持事物的自然本色与生生不息的活态。",
                "explanationEn": "Avoiding artificial over-engineering or coercive meddling with nature, allowing all beings to flourish according to their spontaneous inherent qualities."
            },
            {
                "word": "解放",
                "pinyin": "jiě fàng",
                "en": "Spiritual Liberation",
                "explanationZh": "余秋雨总结庄子哲学的核心功能。庄子思想是给人类心灵的一剂解毒剂，将现代人从名利竞争、焦虑比较与物质包围的牢笼中彻底解放出来。",
                "explanationEn": "The ultimate therapeutic value of Zhuangzi's philosophy: liberating the human mind from the suffocating prisons of rat-race competition, materialism, and existential anxiety."
            }
        ]
    },
    "02-02": {
        "gistZh": "《逍遥游》是中国思想、文学与艺术的总体概括。通过典雅畅达的现代今译，融汇经典的神韵与气韵，展示大鹏图南、至人无己、神人无功、圣人无名及无用之用等崇高意境，为现代人通往古典提供了美文跳板。",
        "gistEn": "'Xiaoyaoyou' serves as the ultimate summary of Chinese thought, literature, and art. Through standard, beautiful modern translation preserving original spirit and vitality, it reveals cosmic allegories like the soaring Peng bird, selflessness, and the utility of uselessness.",
        "highlights": [
            {
                "zh": "文学与思想的总概括：“逍遥游”三字不仅是庄子哲学的精髓，更是中国文学与艺术从内容到形式的最高概括。",
                "en": "Overall Summary of Art & Thought: 'Xiaoyaoyou' is not only the essence of Zhuangzi's philosophy, but the supreme summary of Chinese literature and art."
            },
            {
                "zh": "今译的价值与使命：今译旨在通达古今，以散文的美感与学术的严谨保留典雅气韵，成为读者通往原文的桥梁与跳板。",
                "en": "Purpose of Modern Translation: Bridging past and present with literary elegance and scholarly precision, offering a captivating springboard to classical originals."
            },
            {
                "zh": "自由与无待的崇高意境：通过大鹏与蜩鸠的对比、列子御风的局限，揭示至人无己、神人无功、圣人无名的终极境界。",
                "en": "Sublime Realm of Unfettered Freedom: Contrasting the colossal Peng with sparrows, and Liezi's wind-reliance with absolute selflessness, meritlessness, and namelessness."
            },
            {
                "zh": "无用之用的大智慧：打破世俗功利对价值的狭隘限定，让灵魂在旷野大树下获得无牵无挂的舒展与栖居。",
                "en": "Wisdom of the Useless: Shattering pragmatic utilitarianism to allow the human soul serene rest and expansive freedom under the shade of the 'useless' tree."
            }
        ],
        "vocabulary": [
            {
                "word": "今译",
                "pinyin": "jīn yì",
                "en": "Modern Literary Translation",
                "explanationZh": "将古代文言经典忠实且富有美感地翻译为现代散文的创作过程。余秋雨强调今译既要有严格的学术准确性，又要有流畅优雅的散文气韵，唤醒古典生命力。",
                "explanationEn": "The art of translating ancient classical texts into refined modern prose, balancing rigorous academic accuracy with fluid aesthetic elegance to revive classical vitality."
            },
            {
                "word": "气韵",
                "pinyin": "qì yùn",
                "en": "Spiritual Rhythm and Vitality",
                "explanationZh": "古典文学与艺术作品中贯穿始终的内在生命力与美感节奏。如果仅靠逐字繁琐注释，文章完整的“气”就会被打断，而今译能保持气韵连贯。",
                "explanationEn": "The unified spiritual rhythm and living aesthetic pulse of a masterpiece. Modern translation preserves this living pulse, preventing it from being fractured by pedantic footnotes."
            },
            {
                "word": "基础记忆与扩大记忆",
                "pinyin": "jī chǔ jì yì yǔ kuò dà jì yì",
                "en": "Core Canon Memory vs. Broad Memory",
                "explanationZh": "余秋雨提出的文化阅读分类法。“基础记忆”指必须精读熟诵的核心经典（如《逍遥游》《论语》精选）；“扩大记忆”指泛读博览、耳顺了解的书目。",
                "explanationEn": "Yu Qiuyu's canon methodology: 'Core Memory' comprises foundational texts to be deeply memorized and internalized, while 'Broad Memory' encompasses supplementary reading for broad acquaintance."
            },
            {
                "word": "跳板",
                "pinyin": "tiào bǎn",
                "en": "Springboard / Gateway to Classics",
                "explanationZh": "比喻今译的功能。现代翻译并非要替代古代原文，而是作为一个富有吸引力的诱惑与过渡跳板，引导现代读者满怀兴趣地走向原文阅读。",
                "explanationEn": "Metaphor for modern translation: not a replacement for ancient texts, but an inviting springboard enabling modern readers to leap into the rich ocean of classical originals."
            },
            {
                "word": "鲲鹏",
                "pinyin": "kūn péng",
                "en": "The Kun and the Peng (Cosmic Allegory)",
                "explanationZh": "《逍遥游》开篇的巨型神兽意象。北海之鱼为鲲，化而为鸟为鹏，背若泰山，翼若垂天之云，象征着浩瀚无比、气势磅礴的精神格局与生命境界。",
                "explanationEn": "The iconic cosmic creatures in Xiaoyaoyou: the giant fish Kun transforming into the colossal bird Peng, whose wings resemble storm clouds—symbolizing vast spiritual vision and grand scope."
            },
            {
                "word": "野马与尘埃",
                "pinyin": "yě mǎ yǔ chén āi",
                "en": "Shimmering Mists and Dust Specks",
                "explanationZh": "大鹏高空俯瞰人间所见到的景象。“野马”指游动的雾气。比喻世俗红尘中万物的生灭纷扰与渺小，在宏观宇宙视角下皆如微尘飘忽。",
                "explanationEn": "The view from 90,000 li above: galloping mists ('ye ma') and floating dust. It symbolizes how mortal affairs and anxieties appear as fleeting specks in cosmic perspective."
            },
            {
                "word": "扶摇而上九万里",
                "pinyin": "fú yáo ér shàng jiǔ wàn lǐ",
                "en": "Soaring Ninety Thousand Li on Whirling Winds",
                "explanationZh": "描述大鹏乘着旋风直冲九霄雲天的壮丽诗意画面。比喻生命打破低空盘旋的束缚，跃升至极致高远的精神维度。",
                "explanationEn": "The poetic description of the Peng soaring skyward on spiraling cyclones, metaphorically representing the human soul breaking everyday limits to attain towering spiritual height."
            },
            {
                "word": "蜩与学鸠",
                "pinyin": "tiáo yǔ xué jiū",
                "en": "The Cicada and Little Dove (Narrow-Mindedness)",
                "explanationZh": "在榆树檀枝间低空飞翔的小虫与小鸟，嘲笑大鹏九万里图南的壮举。比喻目光短浅、自以为是、无法理解宏大境界与崇高理想的世俗平庸者。",
                "explanationEn": "Small creatures fluttering low among trees who mock the Peng's grand migration. They embody petty, self-satisfied narrow-mindedness incapable of comprehending noble ideals."
            },
            {
                "word": "宋荣子",
                "pinyin": "Sòng Róng zǐ",
                "en": "Song Rongzi (Indifference to Praise and Blame)",
                "explanationZh": "战国思想家。举世赞誉他不会加劲，举世非难他也不会沮丧，能定乎内外之分、辩乎荣辱之境。虽超脱毀誉，但庄子指出他仍未树立最崇高的立身标杆。",
                "explanationEn": "An ancient philosopher impervious to worldly applause or condemnation. Though adept at separating praise from blame, Zhuangzi notes he still fell short of ultimate transcendent freedom."
            },
            {
                "word": "列子御风",
                "pinyin": "Liè zǐ yù fēng",
                "en": "Liezi Riding the Wind (Conditional Freedom)",
                "explanationZh": "道家大师列子能乘风而行，轻盈从容。但庄子指出列子“犹有所待者也”——他依然依赖风吹，无风则无法飞行，因此仍属于有条件的局限自由。",
                "explanationEn": "The Daoist master Liezi traveling effortlessly upon the wind. However, Zhuangzi observes that Liezi remained dependent on the wind; lacking absolute autonomy, his freedom was still conditional."
            },
            {
                "word": "至人无己",
                "pinyin": "zhì rén wú jǐ",
                "en": "The Ultimate Person Has No Self",
                "explanationZh": "《逍遥游》核心结论之一。达到修养顶峰的“至人”彻底消解了自我执念与功利私心，不守己、不固执，与天地万物融为一体。",
                "explanationEn": "One of Xiaoyaoyou's foundational maxims: the supreme person completely dissolves self-centered ego and personal anxiety, merging seamlessly with universal nature."
            },
            {
                "word": "神人无功",
                "pinyin": "shén rén wú gōng",
                "en": "The Divine Person Pursues No Merit",
                "explanationZh": "《逍遥游》核心结论。精神超凡入圣的“神人”不追求外在的世俗功绩与事业资本，不把功勋作为自我依靠的张本，获得纯粹的解脱。",
                "explanationEn": "The spiritual sage avoids anchoring their self-worth on mundane achievements or societal merit, operating above the rat race of recognition."
            },
            {
                "word": "圣人无名",
                "pinyin": "shèng rén wú míng",
                "en": "The Sage Seeks No Fame",
                "explanationZh": "《逍遥游》核心结论。德合天地的“圣人”不追逐世俗名声与毁誉赞夸。“名”仅为“实”之宾客，不让名气羁绊心灵的自在。",
                "explanationEn": "The true sage refrains from chasing earthly fame, viewing reputation as a mere secondary shadow that must never fetter inner autonomy."
            },
            {
                "word": "许由让王",
                "pinyin": "Xǔ Yóu ràng wáng",
                "en": "Xu You Rejecting Emperor Yao's Throne",
                "explanationZh": "高士许由拒绝尧帝禅让天下的典故。许由以“鹪鹩巢于深林，不过一枝；偃鼠饮河，不过满腹”为答，揭示人对物质名位的需求极有限，绝不作虚名的附庸。",
                "explanationEn": "The story of hermit Xu You declining the imperial throne from Emperor Yao. Noting that a bird nesting in a forest occupies but one twig, he rejected imperial power as superfluous vanity."
            },
            {
                "word": "藐姑射之山",
                "pinyin": "miǎo gū yè zhī shān",
                "en": "Mount Guye (Realm of Divine Spirits)",
                "explanationZh": "庄子塑造的神话仙山。山上有神人居住，肌肤如冰雪，风姿像处女，不食五谷，吸风饮露，凝聚元神即可使万物无灾、五谷丰登，象征超尘脱俗的至纯境界。",
                "explanationEn": "The mythical mountain in Xiaoyaoyou inhabited by divine beings with skin like snow, who ingest air and dew, embodying pristine spiritual purity and effortless harmony with cosmos."
            },
            {
                "word": "形体之盲与智力之盲",
                "pinyin": "xíng tǐ zhī máng yǔ zhì lì zhī máng",
                "en": "Physical Blindness vs. Intellectual/Spiritual Blindness",
                "explanationZh": "连叔开导肩吾的辩证哲理。不仅肉体有盲人聋子无法欣赏文采鼓乐，智力与心灵上亦有“盲”与“聋”，无法领悟超越世俗常理的宏大哲理。",
                "explanationEn": "A philosophical distinction: just as physical blindness prevents seeing colors, intellectual and spiritual blindness prevents small minds from perceiving cosmic truths beyond dogmatic common sense."
            },
            {
                "word": "无用之用",
                "pinyin": "wú yòng zhī yòng",
                "en": "The Utility of Uselessness",
                "explanationZh": "庄子反功利主义的深邃辩证法。世人眼中的“有用”（如野猫黄鼠狼之能捕鼠）往往招致网罗祸患；而“无用”的大树（樗树）反而不受刀斧砍伐，得以终享天年。",
                "explanationEn": "Zhuangzi's profound paradox: pragmatic 'usefulness' often invites danger and destruction, whereas apparent 'uselessness' protects life from exploitation, achieving ultimate preservation and peace."
            },
            {
                "word": "无何有之乡",
                "pinyin": "wú hé yǒu zhī xiāng",
                "en": "The Land of Nothingness / Realm of Pure Freedom",
                "explanationZh": "庄子设想的没有功利纷扰、没有等级压迫的精神原乡。将“无用”的大树种于广袤无垠的无何有之乡，人可逍遥自在地躺卧其下，获得心灵的终极栖居。",
                "explanationEn": "Zhuangzi's utopian realm of absolute spiritual serenity—free from utilitarian striving—where one can wander carefree and rest peacefully beneath the branches of cosmic peace."
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
        ],
        "vocabulary": [
            {
                "word": "君子人格",
                "pinyin": "jūn zǐ rén gé",
                "en": "Junzi (Noble Person) Collective Personality",
                "explanationZh": "中国文化独一无二的核心集体人格。不同于西方的骑士或绅士，君子注重内在道德修养、社会担当与中庸圆融，是中国文明延续数千年的理想人格标杆。",
                "explanationEn": "The core collective personality unique to Chinese civilization. Unlike Western knights or gentlemen, the Junzi emphasizes inner moral refinement, social duty, and harmonious moderation—serving as the ideal benchmark of Chinese humanity."
            },
            {
                "word": "集体无意识",
                "pinyin": "jí tǐ wú yì shí",
                "en": "Collective Unconscious",
                "explanationZh": "心理学概念，由瑞士心理学家荣格提出。指不依赖于个人经验而由遗传继承下来的群体精神结构，深藏于文化族群的潜意识之中，塑造着群体的心理本能与行为习惯。",
                "explanationEn": "A psychological concept introduced by Carl Jung. It refers to the inherited mental structures shared across a culture, residing deep within the subconscious and shaping collective instincts and behavioral patterns."
            },
            {
                "word": "暗礁与海床",
                "pinyin": "àn jiāo yǔ hǎi chuáng",
                "en": "Reefs & the Seabed",
                "explanationZh": "学术界对心理学大师理论的生动比喻：弗洛伊德找到了人类心理海浪波涛下的「暗礁」（个体潜意识），而荣格找到了暗礁底下的「海床」（集体无意识）。余秋雨借此说明君子人格是深沉稳固的文化海床。",
                "explanationEn": "A vivid psychological metaphor: Freud discovered the 'reefs' beneath the ocean waves (individual subconscious), while Jung uncovered the deeper 'seabed' (collective unconscious). Yu Qiuyu highlights Junzi personality as this deep, rock-solid cultural seabed."
            },
            {
                "word": "心理故乡",
                "pinyin": "xīn lǐ gù xiāng",
                "en": "Psychological Homeland / Soul Sanctuary",
                "explanationZh": "一个民族文化心理与灵魂依托的源头。由远古神话、原始意象与历史记忆共同构筑，即便历经岁月变迁，依然是全体族群成员心灵归宿与精神依恋的深层故乡。",
                "explanationEn": "The foundational spiritual sanctuary of a nation, forged by primordial myths and archetype memories that provide an enduring emotional refuge and sense of belonging for a people."
            },
            {
                "word": "原始意象",
                "pinyin": "yuán shǐ yì xiàng",
                "en": "Primordial Archetype / Archetypal Images",
                "explanationZh": "荣格心理学核心词。远古时代遗留下来并深植于人类群体潜意识中的象征性心理构件（如女娲补天、夸父逐日），跨越时空反复出现在民族的文化梦境与艺术创作中。",
                "explanationEn": "A central Jungian term denoting symbolic psychological constructs embedded in a culture's collective unconscious from ancient mythologies, resurfacing endlessly in national art, literature, and dreams."
            },
            {
                "word": "自画像",
                "pinyin": "zì huà xiàng",
                "en": "National Self-Portrait",
                "explanationZh": "指一个民族在千百年集体心理活动中组合构建出的自我象征画像。中国人深层的自我画像即是包含仁爱、重义、坚韧与温良的「君子」形象。",
                "explanationEn": "The symbolic self-image forged across centuries of collective psychological life. The deep self-portrait embedded within the Chinese psyche is the image of the Junzi—embodying benevolence, integrity, and quiet fortitude."
            },
            {
                "word": "因果律",
                "pinyin": "yīn guǒ lǜ",
                "en": "Law of Causality",
                "explanationZh": "西方现代科学与机械唯物主义的基础逻辑，强调原因与结果之间的确定性因果链条。荣格指出，相比西方依赖统计学的因果律，中国古代智慧（如《易经》）展示了更高维度的整体联系与变化法则。",
                "explanationEn": "The foundational logic of modern Western science emphasizing deterministic cause-and-effect chains. Jung noted that ancient Chinese wisdom (such as the I Ching) offers a higher holistic paradigm beyond linear statistical causality."
            },
            {
                "word": "物极必反",
                "pinyin": "wù jí bì fǎn",
                "en": "Things Bound to Turn Around at Extremes",
                "explanationZh": "成语。指事物发展到极点就会向相反的方向转化。《易经》与道家哲学的重要法则，展示了辩证包容的动态平衡智慧，超越了以自我为中心、单向固执的西方人格结构。",
                "explanationEn": "Idiom: When things reach an extreme, they inevitably reverse direction. A core principle in I Ching and Daoist philosophy, offering a dynamic dialectical balance that transcends rigid, self-centered individualistic mindsets."
            },
            {
                "word": "王道与霸道",
                "pinyin": "wáng dào yǔ bà dào",
                "en": "Kingly Way (Benevolence) vs. Hegemonic Way (Force)",
                "explanationZh": "中国传统政治伦理的一对核心范畴。王道指以道德感化、仁政与礼义治理天下；霸道指以武力威慑、权谋与功利扩张秩序。孙中山曾劝告邻国警惕霸道，恪守东方的王道文化。",
                "explanationEn": "Two contrasting governance paradigms in Chinese philosophy: the 'Kingly Way' rules through moral example, benevolence, and ethics; the 'Hegemonic Way' relies on coercion, power politics, and force."
            },
            {
                "word": "和而不同",
                "pinyin": "hé ér bù tóng",
                "en": "Harmony Without Uniformity",
                "explanationZh": "出自《论语》。君子在人际交往与社会治理中追求内在秩序与多元包容的和谐（和），而不盲目苟同或强求一律（不同）；反之，「小人同而不和」，追求形式上的结党苟同却破坏内在和谐。",
                "explanationEn": "From the Analects: The Junzi seeks deep organic harmony while respecting diverse perspectives ('harmony without uniformity'), whereas the petty person demands rigid conformity while breeding underlying friction."
            },
            {
                "word": "择善而固执",
                "pinyin": "zé shàn ér gù zhí",
                "en": "Choosing the Good & Holding Fast to It",
                "explanationZh": "出自《礼记·中庸》。指通过理性辨析选择正确的道德善道，然后坚守信念、矢志不渝。这是君子人格在复杂变局与道义关头展现出的独立人格与精神定力。",
                "explanationEn": "From the Doctrine of the Mean: Discriminating the moral good with wisdom and steadfastly holding to it with unwavering conviction—the hallmark of moral resolve in a noble character."
            },
            {
                "word": "文质彬彬",
                "pinyin": "wén zhì bīn bīn",
                "en": "Cultured Elegance Balanced with Inner Substance",
                "explanationZh": "出自《论语》。「文」指外在礼仪、学识与文化教养；「质」指内在朴实、真诚的道德质朴。外在文化修养与内在道德质朴达到完美平衡，方为真正的君子。",
                "explanationEn": "From the Analects: 'Wen' represents refined culture and demeanor; 'Zhi' denotes inner moral substance. True nobility requires a harmonious balance where external refinement matches internal integrity."
            },
            {
                "word": "重义轻利",
                "pinyin": "zhòng yì qīng lì",
                "en": "Valuing Righteousness Over Personal Profit",
                "explanationZh": "儒家理想人格的核心价值取向。「君子喻于义，小人喻于利」。在面临道德公义与个人私利的抉择时，君子坚持恪守道义尊严，不为一时功利而违背良知底线。",
                "explanationEn": "A defining value of Confucian ethics: 'The noble person comprehends righteousness; the petty person comprehends profit.' When faced with choices, the Junzi upholds moral integrity over self-serving gain."
            },
            {
                "word": "修己安人",
                "pinyin": "xiū jǐ ān rén",
                "en": "Self-Cultivation for the Peace of Others",
                "explanationZh": "出自《论语》。君子修养道德人格不单是为了自我超脱，更是为了造福他人、安定社会。将个人的内在道德修养与天下苍生的社会责任紧密相连。",
                "explanationEn": "From the Analects: Cultivating one's character not for selfish enlightenment, but to bring peace, order, and well-being to society—connecting personal ethics directly with broader human duty."
            },
            {
                "word": "君子之道",
                "pinyin": "jūn zǐ zhī dào",
                "en": "The Way of the Junzi",
                "explanationZh": "中华文化千百年来提炼出的理想人格生活准则与实践路径。涵盖仁爱、忠恕、知耻、尊礼等范畴，是儒家思想归结出的最高生命实践学问。",
                "explanationEn": "The practical spiritual path and ethical code refined over millennia in China, encompassing benevolence, empathy, integrity, and propriety—the ultimate fruit of Confucian life philosophy."
            },
            {
                "word": "夸父逐日",
                "pinyin": "kuā fù zhú rì",
                "en": "Kuafu Chasing the Sun (Mythic Archetype)",
                "explanationZh": "中国远古神话代表。表达了古代先民对于光明与真理不屈不挠、死而后已的宏大追求，化作中华民族精神深处英勇执着、义无反顾的心理基因。",
                "explanationEn": "A classic Chinese myth embodying humanity's heroic, relentless pursuit of light, truth, and greatness—embedded deep within the national subconscious as an archetype of persistent courage."
            },
            {
                "word": "女娲补天",
                "pinyin": "nǚ wā bǔ tiān",
                "en": "Nuwa Mending the Heavens (Mythic Resilience)",
                "explanationZh": "中国远古上古创世神话。象征着中华文明在面对天塌地陷级的巨灾劫难时，所展现出的强大拯救意志、母性慈爱与重建秩序的文明抗逆力。",
                "explanationEn": "An ancient creation myth symbolizing Chinese civilization's maternal compassion, heroic agency, and invincible resilience in repairing societal order after apocalyptic catastrophes."
            },
            {
                "word": "德行第一",
                "pinyin": "dé xíng dì yī",
                "en": "Virtue & Moral Integrity Above All",
                "explanationZh": "君子人格的首要评判标准。在中国文化中，才干、学问与财富皆位居次席，唯有道德操守与良知品格是衡量一个人高下与尊严的根本准则。",
                "explanationEn": "The primary criterion for the Junzi. In Chinese tradition, intellect, wealth, and status remain secondary to moral integrity, which serves as the supreme measure of human dignity."
            }
        ]
    },
    "03-01": {
        "gistZh": "余秋雨从孔子对君子与小人的对比思维切入，提出“研究小人是为了更好地认识君子”的核心论点。深刻剖析了小人琢磨不定、善于伪装、消解历史与正义的特殊本质，揭示了直面文化负面人格对完善君子修养的重大意义。",
        "gistEn": "Yu Qiuyu explores the Confucian dichotomy between Junzi and Xiaoren, establishing that 'studying the petty person is essential to fully understanding the exemplary person.' He dissects the elusive, camouflaged, and corrosive nature of Xiaoren, illustrating why confronting this dark side of cultural character is vital for authentic virtue.",
        "highlights": [
            {
                "zh": "反面映衬法：“想知道君子是什么样的吗？看小人就知道了。”通过划清与小人的界限，反向确立君子的人格高标。",
                "en": "Contrastive Definition: 'Want to know what a Junzi is like? Just look at a Xiaoren.' By defining boundaries against Xiaoren, the lofty benchmark of Junzi is clearly delineated."
            },
            {
                "zh": "小人的特质：不是元凶巨恶，却琢磨不定；没有明确政见，却能让鲜明形象瘫软、祥和关系险恶、响亮命题荒唐。",
                "en": "Traits of the Xiaoren: Not overt monsters, but elusive and shifting; lacking clear convictions, yet paralyzing noble figures, poisoning relationships, and debasing grand ideals."
            },
            {
                "zh": "伪装与消解：小人最擅长伪装成君子，甚至在面临问责时与愤怒的大众站在一起，使正义失去攻击的目标。",
                "en": "Disguise and Dissolution: Xiaoren disguise themselves as Junzi and even echo righteous fury when challenged, effectively depriving justice of a clear target."
            },
            {
                "zh": "文化批判的勇气：克服君子对泥潭的回避，敢于探究中华文化深层的负面人格结构（《历史的暗角》/《大地小人》）。",
                "en": "Courage for Cultural Critique: Overcoming the instinct to avoid murky subjects, daring to probe the subterranean negative personality of Chinese culture."
            }
        ],
        "vocabulary": [
            {
                "word": "君子与小人",
                "pinyin": "jūn zǐ yǔ xiǎo rén",
                "en": "Junzi and Xiaoren (Exemplary Person vs. Petty Person)",
                "explanationZh": "中国传统伦理中最核心的一对二元对立人格范畴。孔子与儒家几乎每条关于君子的论述都以小人作对比，确立道德与人品的正反两极标尺。",
                "explanationEn": "The foundational dualistic archetype in traditional Chinese ethics. Confucius contrasted Junzi with Xiaoren in almost every teaching, establishing positive and negative moral benchmarks."
            },
            {
                "word": "对立面",
                "pinyin": "duì lì miàn",
                "en": "Antithesis / Opposing Counterpart",
                "explanationZh": "事物发展中相互排斥又互为映衬的相反方面。余秋雨指出讲完君子之道的九项要点与四大难点后，必须直面其对立面小人，整个君子学问才算完整闭环。",
                "explanationEn": "The diametrical counterpart essential for systemic understanding. Studying the Xiaoren as the antithesis completes the intellectual and moral portrait of the Junzi."
            },
            {
                "word": "小人天地",
                "pinyin": "xiǎo rén tiān dì",
                "en": "The Realm of Xiaoren (The Petty Domain)",
                "explanationZh": "余秋雨对中华文化负面人格生态的概括性称谓。指由无原则、善伪装、利己害群的各种小人行为构成的隐蔽而庞大的社会心理网络。",
                "explanationEn": "Yu Qiuyu's collective term for the cultural pathology of negative archetypes: a pervasive social and psychological undercurrent woven by unprincipled, parasitic opportunists."
            },
            {
                "word": "边际修剪",
                "pinyin": "biān jì xiū jiǎn",
                "en": "Marginal Trimming (Definition via Negation)",
                "explanationZh": "哲学与逻辑学上的“排除法”定义方式。在正面难以穷尽描述高尚理想时，通过剔除所有非君子、反道德的污浊杂质，让君子的纯粹形象自然凸显。",
                "explanationEn": "A philosophical definition method through negation: when a sublime ideal defies easy positive specification, trimming away negative traits brings the noble form into sharp relief."
            },
            {
                "word": "琢磨不定",
                "pinyin": "zuó mo bù dìng",
                "en": "Elusive, Indeterminate, and Shifting",
                "explanationZh": "小人群体最致命的特征之一。无明确立场、无固定形态，如同空气与流水般四处渗透，使得学者难以研究、正派人士难以防范与正面交锋。",
                "explanationEn": "The most dangerous hallmark of the Xiaoren: devoid of rigid convictions or identifiable stances, fluidly infiltrating social fabrics, evading both academic capture and moral accountability."
            },
            {
                "word": "伪装",
                "pinyin": "wěi zhuāng",
                "en": "Camouflage / Moral Disguise",
                "explanationZh": "小人借用君子的道德话语与崇高言辞包装自己的手段。结果导致圣贤的名言警句反而常从小人口中说出，使大众真伪难辨。",
                "explanationEn": "The art of co-opting virtuous rhetoric to mask insidious intentions, resulting in classic moral aphorisms ironically flowing from the lips of hypocrites to confuse the public."
            },
            {
                "word": "群众眼睛未必雪亮",
                "pinyin": "qún zhòng yǎn jing wèi bì xuě liàng",
                "en": "The Public Eye Is Not Infallible",
                "explanationZh": "余秋雨对传统“众人无可欺”观念的清醒反思。由于小人擅长伪装与煽动，普通大众在多数历史时期极易被表象蒙蔽，无法迅速辨清大忠大奸。",
                "explanationEn": "A sober critique of the naive belief that the masses are invariably discerning. Master manipulators frequently bamboozle public sentiment, confounding moral clarity."
            },
            {
                "word": "历史的暗角",
                "pinyin": "lì shǐ de àn jiǎo",
                "en": "Dark Corners of History",
                "explanationZh": "余秋雨收录于《山居笔记》的著名文化散文篇名。首次系统性地从文化学与心理学角度剖析中国历史上小人的生成机制与巨大破坏力，引发华人世界极大轰动。",
                "explanationEn": "The title of Yu Qiuyu's celebrated essay in 'Notes from Mountain Dwelling', which pioneered the cultural-psychological dissection of Xiaoren in Chinese dynastic history."
            },
            {
                "word": "大地小人",
                "pinyin": "dà dì xiǎo rén",
                "en": "Xiaoren Across the Earth",
                "explanationZh": "《历史的暗角》扩充后的文章名称。“大地”与“小人”形成宏阔空间与猥琐人格的强烈对仗，揭示小人群体在广袤国土上普遍滋生、阴魂不散的普遍性。",
                "explanationEn": "The expanded title contrasting the vast earth with petty humans, highlighting how the scourge of unprincipled opportunism has populated every corner of civilization."
            },
            {
                "word": "元凶巨恶",
                "pinyin": "yuán xiōng jù è",
                "en": "Arch-Criminals and Heinous Villains",
                "explanationZh": "公开作恶、罪行昭彰的首要恶徒。小人不同于元凶巨恶，他们往往没有滔天罪行或鲜明暴行，而是以微小而持续的侵蚀瓦解道德与事业。",
                "explanationEn": "Notorious, overt master villains. Xiaoren differ fundamentally from blatant criminals in that they operate through stealthy, incremental rot rather than conspicuous monstrosity."
            },
            {
                "word": "混沌暧昧",
                "pinyin": "hùn dùn ài mèi",
                "en": "Chaotic, Ambiguous, and Sordid",
                "explanationZh": "小人对清晰历史事件的消解效应。由于他们的挑拨、曲解与谣言，原本黑白分明的事理慢慢变得浑浊不清、是非难分、龌龊肮脏。",
                "explanationEn": "The muddying effect of petty politics: sowing rumor and malice until originally transparent truths become ambiguous, sordid, and indecipherable."
            },
            {
                "word": "腐浊之气",
                "pinyin": "fǔ zhuó zhī qì",
                "en": "A Murky, Putrid Atmosphere / Corrosive Influence",
                "explanationZh": "余秋雨对小人氛围的通感比喻。小人如同一团驱之不散、不见痕迹的腐臭浊气，让人心生厌恶却又抓不到实体，时刻侵蚀着周遭的清爽与宁静。",
                "explanationEn": "A sensory metaphor for toxic micro-politics: an inescapable, shapeless smog of corruption that asphyxiates moral integrity without leaving tangible fingerprints."
            },
            {
                "word": "飘忽不定",
                "pinyin": "piāo hū bù dìng",
                "en": "Evanescent and Flickering / Mercurial",
                "explanationZh": "形容小人的言谈与神态变化莫测。他们没有原则，见风使舵，随环境与利益的变动而随意切换面孔，使人防不胜防。",
                "explanationEn": "Mercurial shifts in demeanor and tone: altering smiles, glances, and loyalties at a moment's notice to align with shifting winds of convenience."
            },
            {
                "word": "万钧雷霆",
                "pinyin": "wàn jūn léi tíng",
                "en": "Thunderous Might / Crushing Retribution",
                "explanationZh": "比喻正义之士积聚的强大怒火与打击力量。当正义之士准备雷霆出击时，小人往往早已换上一副同样愤怒的面具混在阵营中，使正义打击落空。",
                "explanationEn": "Overwhelming righteous wrath. When poised to strike down malice with crushing force, the pursuer finds the Xiaoren masquerading amidst the angry crowd."
            },
            {
                "word": "不绝如缕",
                "pinyin": "bù jué rú lǚ",
                "en": "Lingering Inescapably / Tenacious Continuity",
                "explanationZh": "原指声音或气息微弱而连绵不断。此处指即使你掉过头去不理会小人，那股阴暗猥琐的气息依然像细丝一样紧紧缠绕、挥之不去。",
                "explanationEn": "Lingering persistently like an unbroken thread: describing the insidious tenacity of petty slander and toxicity that clings despite attempts to ignore it."
            },
            {
                "word": "钢铸铁浇",
                "pinyin": "gāng zhù tiě jiāo",
                "en": "Forged of Iron and Steel / Unyielding Titans",
                "explanationZh": "形容历史上那些意志坚如钢铁、经受过无数风浪考验的杰出政治家与军事家。他们能战胜千军万马，却往往被身边微小的小人暗算致死。",
                "explanationEn": "Metaphor for iron-willed historical titans and generals who conquered formidable battlefields, yet ultimately succumbed to the covert poisoning of petty courtiers."
            },
            {
                "word": "和颜悦色",
                "pinyin": "hé yán yuè sè",
                "en": "Genial Smiles and Courteous Countenances",
                "explanationZh": "形容和蔼喜悦的神色。小人在依附强者时往往展现出最无可挑剔的温顺和颜，而这种甜蜜的表象下往往隐藏着最致命的见风使舵与背刺背叛。",
                "explanationEn": "Amiable expressions and courteous veneer: the deceptive mask worn by sycophants to ingratiate themselves with power before delivering the fatal betrayal."
            },
            {
                "word": "弥留之际",
                "pinyin": "mí liú zhī jì",
                "en": "On One's Deathbed / Dying Breath",
                "explanationZh": "生命垂危、行将离世的最后时刻。余秋雨描写钢铁般的领袖在临终弥留之际，最刻骨铭心的遗恨不是敌人，而是颤抖着吐出的两个字——“小人”。",
                "explanationEn": "The threshold of final expiration. Historical commanders on their deathbeds carry lingering trauma not toward worthy rivals, but toward the elusive Xiaoren."
            }
        ],
        "ninePoints": [
            {
                "titleZh": "君子怀德",
                "titleEn": "Junzi Cherishes Virtue",
                "pinyin": "jūn zǐ huái dé",
                "quote": "君子怀德，小人怀土；君子怀刑，小人怀惠。",
                "descZh": "有道德才有真正的人。道德是君子安身立命、区别于禽兽与小人的第一精神支柱。小人所思所虑皆是田宅、家业、宗族乡土等现实利益（“怀土”），而君子心中始终装着道义原则、良知操守与精神高度（“怀德”）。君子重视的是超越物质利益的精神人格追求。",
                "descEn": "Virtue is what makes an authentic human being. Confucius establishes virtue as the primary spiritual pillar of an exemplary life ('The Junzi cherishes virtue; the petty person cherishes land and comfort'). While the Xiaoren fixates on immediate material gains, clan real estate, and physical security, the Junzi anchors life in moral conscience, lofty spiritual values, and principled righteousness beyond worldly attachments."
            },
            {
                "titleZh": "君子之德风",
                "titleEn": "Virtue of the Junzi is Like Wind",
                "pinyin": "jūn zǐ zhī dé fēng",
                "quote": "君子之德风，小人之德草。草上之风，必偃。",
                "descZh": "君子独善其身是不够的。真正的道德必须具备化育社会、引领风尚的强大辐射力与示范效应。君子的道德如同无形拂过的春风，具有强大的社会感染力；当德风吹过，普通民众与社会大众如草受风抚，自然向善倾服。君子必须承担起推动社会向善的道义责任。",
                "descEn": "Solitary self-cultivation alone is insufficient. Drawing on Confucius's insight ('The virtue of the Junzi is like the wind, and that of the petty person is like grass; when the wind blows across the grass, it cannot but bend'), Yu Qiuyu highlights that genuine virtue must possess radiant social influence. An exemplary person does not retreat into sterile aloofness, but actively inspires and elevates the moral climate of the broader community."
            },
            {
                "titleZh": "君子成人之美",
                "titleEn": "Junzi Brings Out the Best in Others",
                "pinyin": "jūn zǐ chéng rén zhī měi",
                "quote": "君子成人之美，不成人之恶。小人反是。",
                "descZh": "向他人投向真诚祝贺的目光。君子怀有博大仁厚的心胸，看到他人有所成就、有美德善举，会打心底里感到欢喜并真诚施以援手，促其圆满；而绝不像小人那样嫉贤妒能、见不得别人好、暗中下绊甚至落井下石（“成人之恶”）。成人之美是衡量一个人是否具有君子器量最直观的试金石。",
                "descEn": "Gazing upon others with eyes of sincere celebration. The Analects teaches: 'The Junzi fosters the good in others, not what is base; the petty person does the opposite.' Possessing a generous and benevolent soul, the Junzi rejoices in and aids the noble achievements of fellow human beings, rather than succumbing to envy, sabotage, or kicking others while they are down."
            },
            {
                "titleZh": "君子周而不比",
                "titleEn": "Junzi is Harmonious Without Colluding",
                "pinyin": "jūn zǐ zhōu ér bù bǐ",
                "quote": "君子周而不比，小人比而不周。",
                "descZh": "做光明的大团结，不做卑劣的私勾结。“周”是出于公理、道义的普遍包容与坦诚团结；“比”是拉帮结派、朋党营私的利益勾结。君子以天下公心待人接物，求同存异，凝聚共识；小人则以狭隘的私人算计拉小圈子、排斥异己。君子之聚是光明磊落的大团结，小人之聚是卑劣算计的私下勾结。",
                "descEn": "Genuine public solidarity over factional conspiracy. In Confucius's words: 'The Junzi is all-embracing and does not form cliques; the petty person colludes and is not all-embracing.' Yu Qiuyu explains that the Junzi fosters broad, principled solidarity rooted in public good and moral fellowship, strictly rejecting nepotism, clannish cabals, and conspiratorial factionalism driven by selfish interest."
            },
            {
                "titleZh": "君子坦荡荡",
                "titleEn": "Junzi is Serene and Open-Hearted",
                "pinyin": "jūn zǐ tǎn dàng dàng",
                "quote": "君子坦荡荡，小人长戚戚。",
                "descZh": "不忧不惧，心胸如青天白日。君子内心平坦宽广、光明磊落，行事无不可对人言，因此没有患得患失的阴暗心理，达到了“仁者不忧，勇者不惧”的精神境界；相反，小人因满腹算计、心怀鬼胎、总在追逐私利与担忧败露中挣扎，因而终日神思惶恐、战战兢兢、“长戚戚”。",
                "descEn": "Untroubled and fearless like a clear sky. As recorded in the Analects: 'The Junzi is serene and open-hearted; the petty person is forever anxious and restless.' Because the Junzi conducts their life with absolute transparency and clear conscience, they are untroubled by selfish scheming and dwell in calm fortitude; the Xiaoren, racked with deceit and greed, lives in perpetual dread."
            },
            {
                "titleZh": "君子中庸",
                "titleEn": "Junzi Holds to the Golden Mean",
                "pinyin": "jūn zǐ zhōng yōng",
                "quote": "君子中庸，小人反中庸。君子之中庸也，君子而时中。",
                "descZh": "在复杂矛盾中把握动态的黄金平衡点。《中庸》强调“君子而时中”。中庸绝非毫无原则的和稀泥、随波逐流或平庸，而是在洞悉极复杂、极微妙的矛盾关系后，能够准确把握事物最适宜的“度”，在极端偏激之间精准拿捏分寸与尺度的高超生存智慧。",
                "descEn": "Mastering the dynamic golden balance amidst polarized extremes. The Doctrine of the Mean stresses 'embodying the Mean at the fitting moment' (时中). Zhongyong is neither lukewarm compromise nor mediocre passivity; it is the supreme art of dynamic calibration—finding the precise, harmonious equilibrium in complex human affairs while resisting fanatical polarization."
            },
            {
                "titleZh": "君子有礼",
                "titleEn": "Junzi Cultivates Propriety",
                "pinyin": "jūn zǐ yǒu lǐ",
                "quote": "不学礼，无以立。",
                "descZh": "礼是敬意的生命形式，礼与美融为一体。《论语》云：“不学礼，无以立。”礼节不仅仅是外在的社交规矩或繁文缛节，更是将内在对生命、他人与文明的敬畏，化为体面、优雅、克制、优美的仪轨与风度。通过礼让与界限感，君子维系了文明交往的尊严与温暖。",
                "descEn": "Reverence as a living form, uniting ritual with aesthetic grace. Reflecting Confucius's dictum 'Without mastering propriety, one cannot establish oneself' (不学礼，无以立), Yu Qiuyu underscores that Li (propriety) is the externalization of profound inner reverence. Far from empty etiquette, it preserves personal dignity, mutual boundaries, and civil decency in social life."
            },
            {
                "titleZh": "君子不器",
                "titleEn": "Junzi is Not a Mere Utensil",
                "pinyin": "jūn zǐ bù qì",
                "quote": "君子不器。",
                "descZh": "不做功利工具与权力的奴仆。器物只有单一、固定的工具用途。君子坚决反对将自我降格为某种狭隘的功利工具、技术零件或权力的奴仆，始终保持博大的人文情怀、独立自由的灵魂与终极关怀，做有完整人格的人。",
                "descEn": "Refusing utilitarian reduction and instrumental servitude. Drawn from the classic aphorism 'The Junzi is not a utensil' (君子不器), Yu Qiuyu asserts that tools exist only for single utilitarian functions. A true Junzi refuses to become a disposable cog or a slave to utilitarian greed, maintaining an expansive humanistic soul, broad-minded insight, and intellectual freedom."
            },
            {
                "titleZh": "君子知耻",
                "titleEn": "Junzi Possesses a Sense of Shame",
                "pinyin": "jūn zǐ zhī chǐ",
                "quote": "行己有耻；知耻近乎勇。",
                "descZh": "耻和不耻是君子人格最低的阀门与底线。中国文化是典型的“耻感文化”，真正的勇敢不是匹夫之勇，而是敢于正视自身的过失与丑陋（“知耻近乎勇”）。知耻意味着内在拥有清晰的良知标尺，坚守道德红线；一旦丧失耻感，人便会堕入肆无忌惮的小人深渊。",
                "descEn": "Shame as the essential bottom threshold of human character. Citing 'Conducting oneself with a sense of shame' (行己有耻) and 'To know shame is close to courage' (知耻近乎勇), Yu Qiuyu explains that an acute sense of shame serves as the bottom safety valve of Confucian personality. Real courage begins with confronting one's moral flaws; an acute sense of shame anchors moral self-discipline and prevents humanity from descending into uninhibited depravity."
            }
        ]
    },

    "03-02": {
        "gistZh": "面对小人的纠缠，争吵只会让小人借势膨胀，研究与冷落才能使其失重瓦解；真正的君子不仅要以制度与整体漠视将其边缘化，更要在文化健全后以博大情怀实现社会的最终超越与救赎。",
        "gistEn": "Confronting petty exploiters (Xiaoren) through direct quarreling only grants them illicit leverage, while academic dissection and cold detachment rob them of social gravity; true Junzi marginalize malice through cultural health and systemic indifference, ultimately transcending petty strife with boundless magnanimity.",
        "highlights": [
            {
                "zh": "冷落与搁置：争吵使小人加重，研究使小人失重。小人的能量源自被关注，唯有彻底冷落才能瓦解其话语权。",
                "en": "Cold Detachment & Disregard: Friction empowers malice, analysis dissolves it. Sidelining opportunists strips them of leverage."
            },
            {
                "zh": "扩大君子队伍：抵御小人最根本的路径，是不断通过自我修养与教育扩大君子队伍，压缩恶的寄生空间。",
                "en": "Cultivating the Junzi Community: Expanding the noble ranks through self-cultivation creates a dominant culture that compresses malevolence."
            },
            {
                "zh": "问鼎伟大的时代：一个健康的社会并非完全没有小人，而是全社会充满创造力，谁也不把小人放在眼里。",
                "en": "A Truly Great Era: A confident, thriving civilization is engrossed in noble creation, rendering malicious antics powerless and ignored."
            },
            {
                "zh": "终极超越与救赎：君子之道最终抱持“大雄”气魄，在筑牢防御之后，反思小人根源，给予文化救赎与人格唤醒。",
                "en": "Ultimate Transcendence & Redemption: Possessing 'Da Xiong' magnanimity, the Junzi seeks systemic healing and cultural redemption for collective trauma."
            }
        ],
        "vocabulary": [
            {
                "word": "大雄",
                "pinyin": "dà xióng",
                "en": "Supreme Heroism / Da Xiong",
                "explanationZh": "佛家语，意指具备大力量、大智慧、能降伏一切烦恼与邪恶的至高人格（常用于佛陀尊号，如“大雄宝殿”）。余秋雨借此形容能以浩瀚包容的胸襟去拯救与化解小人恶意的最高精神境界。",
                "explanationEn": "Buddhist concept denoting 'Supreme Heroism' or moral strength capable of subjugating all afflictions (as in 'Mahavira'). Used here to portray the highest spiritual summit capable of embracing and redeeming petty antagonists."
            },
            {
                "word": "众口铄金",
                "pinyin": "zhòng kǒu shuò jīn",
                "en": "Clamorous Slander Melts Metal",
                "explanationZh": "众人的言论能够熔化金属。比喻舆论力量强大，也形容小人们集体造谣中伤足以颠倒黑白、毁灭一个人。",
                "explanationEn": "Literally 'public clamor can melt metal': an idiom warning that collective slander and fabricated gossip have the terrifying power to dissolve reputations and destroy innocent lives."
            },
            {
                "word": "招腥惹臭",
                "pinyin": "zhāo xīng rě chòu",
                "en": "Attracting Putrid Stench and Foul Parasites",
                "explanationZh": "比喻因为不慎介入污浊纷争或与品格卑劣者纠缠，从而惹火上身、沾染满身恶名与污秽。",
                "explanationEn": "Metaphor for courting reputational ruin and foul toxicity by foolishly wading into dirty disputes with disreputable individuals."
            },
            {
                "word": "群蝇成阵",
                "pinyin": "qún yíng chéng zhèn",
                "en": "Swarming Flies Massing in Formation",
                "explanationZh": "形容卑劣丑陋的小人群体像苍蝇般聚集结阵，喧嚣刺耳、逐臭而生。",
                "explanationEn": "Vivid imagery depicting petty opportunists swarming together like a battalion of blowflies, driven by an appetite for decay and mutual validation."
            },
            {
                "word": "大而无当",
                "pinyin": "dà ér wú dàng",
                "en": "Ostentatious but Devoid of Substance",
                "explanationZh": "出自《庄子》，指言辞或事物表面宏大却脱离实际、不着边际。余秋雨借以提醒探讨文化与对策时不可沦为空洞大话，而要切实落地。",
                "explanationEn": "Originating from Zhuangzi, meaning grand and sweeping in appearance but impractical and empty in reality; hollow pretentiousness."
            },
            {
                "word": "问鼎伟大",
                "pinyin": "wèn dǐng wěi dà",
                "en": "Ascending to the Pinnacle of Historical Greatness",
                "explanationZh": "“问鼎”原指图谋夺取天下王权，后泛指攀登至最高殿堂。此处指一个文明在精神和制度上达到成熟从容、无视低劣杂音的崇高境界。",
                "explanationEn": "'Wen Ding' originally signified aspiring to imperial sovereignty; here it denotes a civilization ascending to its highest historical summit, immune to petty sabotage."
            },
            {
                "word": "双向冷落",
                "pinyin": "shuāng xiàng lěng luò",
                "en": "Reciprocal Alienation / Mutual Sidelining",
                "explanationZh": "指双方互不搭理、完全断绝关注的状态。在对付小人时，唯有全社会主动实施冷落，才能打碎其以碰瓷君子为荣的单向吸血链条。",
                "explanationEn": "A mutual severing of interaction. Against petty agitators, society's deliberate, universal disregard severs the parasite's lifeblood of unreciprocated provocations."
            },
            {
                "word": "喝了“狼奶”",
                "pinyin": "hē le láng nǎi",
                "en": "Weaned on Wolves' Milk / Conditioned to Brutality",
                "explanationZh": "文化批评常用语，指在特殊极端历史或家庭环境中长大，从小浸染斗争哲学、仇恨思维与残忍心性的人格扭曲现象。",
                "explanationEn": "A critical metaphor for individuals nurtured in extreme social pathology or cruelty, whose early psychological conditioning steeped them in ruthlessness, paranoia, and spite."
            },
            {
                "word": "文痞",
                "pinyin": "wén pǐ",
                "en": "Cultural Ruffians / Pseudo-Intellectual Hooligans",
                "explanationZh": "指那些掌握文字与舆论工具，却丧失道德底线，依附权贵、罗织罪名、构陷良善的文化流氓。",
                "explanationEn": "Literary thugs or pseudo-intellectual opportunists who weaponize pens and media platforms to fabricate charges, flatter patrons, and assassinate characters."
            },
            {
                "word": "失重",
                "pinyin": "shī zhòng",
                "en": "Loss of Social Weight / Gravitational Deprivation",
                "explanationZh": "借物理学概念，指小人一旦被剥夺了争论和注意力的平台，失去了道德争端作为支撑，其言行便毫无社会价值，在公众视野中彻底失去分量。",
                "explanationEn": "Borrowed from physics: once petty agitators are denied the platform of argument and spotlight, their provocations collapse into total societal insignificance."
            },
            {
                "word": "冷落与搁置",
                "pinyin": "lěng luò yǔ gē zhì",
                "en": "Cold Indifference and Shelving / Deliberate Marginalization",
                "explanationZh": "余秋雨提出的应对小人的核心策略：不给关注、不与论辩，将其行为永久搁置在边缘角落，令其自生自灭。",
                "explanationEn": "Yu Qiuyu's strategic prescription: granting zero reaction or validation, decisively shelving malicious antics into social irrelevance."
            },
            {
                "word": "拯救与关爱",
                "pinyin": "zhěng jiù yǔ guān ài",
                "en": "Transcendental Redemption and Compassion",
                "explanationZh": "历经波折后文化主体对劣质人性的终极关怀。在筑牢防御之后，从悲剧根源上理解并拯救被异化的人格，彰显文明的终极温度。",
                "explanationEn": "The ultimate ethical summit where, having erected systemic boundaries, the noble mind perceives the tragic pathology of the fallen and seeks holistic societal healing."
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
        ],
        "vocabulary": [
            {
                        "word": "科举制度",
                        "pinyin": "kē jǔ zhì dù",
                        "en": "Imperial Examination System",
                        "explanationZh": "中国古代通过分科考试选拔文官的根本制度。始于隋唐，延续1300余年，以统一考试取代门阀贵族血缘世袭，是中华文化长寿的重要制度保障。",
                        "explanationEn": "The nationwide imperial civil service examination system established in the Sui and Tang dynasties and persisting for over 1,300 years. It replaced aristocratic bloodline succession with merit-based selection."
            },
            {
                        "word": "文官",
                        "pinyin": "wén guān",
                        "en": "Civil Official / Civil Servant",
                        "explanationZh": "掌管国家政务、礼乐、民政与司法的行政官员，与武官（执掌军旅征战）相对。科举选拔的核心在于为庞大帝国构建专业且有文化底蕴的常任文官体系。",
                        "explanationEn": "Civilian administrative officials responsible for governance, civil affairs, and state administration, as distinguished from military officers (武官). The core objective of the exams was cultivating an administrative corps."
            },
            {
                        "word": "保全",
                        "pinyin": "bǎo quán",
                        "en": "To Preserve / Safeguard Intact",
                        "explanationZh": "维护完整、使不受破坏。余秋雨先生指出，即使政权更替或国土受创，全国统一的文官知识分子队伍亦能保全中华文化的深厚土壤，使其历经浩劫而不散。",
                        "explanationEn": "To preserve and keep intact. The lecture underscores that even amid dynastic upheavals, a unified civil bureaucracy protected the social and intellectual soil of Chinese civilization."
            },
            {
                        "word": "一代雄主",
                        "pinyin": "yī dài xióng zhǔ",
                        "en": "Formidable / Heroic Monarch of an Era",
                        "explanationZh": "具有宏大魄力与雄才大略的杰出君主。早期文明往往依赖雄主的个人魅力聚合战友，但若缺乏制度化体系，雄主离世后帝国极易瓦解。",
                        "explanationEn": "A visionary, powerful monarch with exceptional leadership. Early civilizations often relied on heroic rulers, but without institutionalized succession, empires fractured upon the monarch's demise."
            },
            {
                        "word": "自成格局",
                        "pinyin": "zì chéng gé jú",
                        "en": "Forming an Independent Enclave",
                        "explanationZh": "地方官员在各自领地内形成封闭、自主的小天地或割据势力。古代版图辽阔，若无中央统一选拔流转机制，各地管理者便会自成格局并最终导致分裂。",
                        "explanationEn": "Developing isolated regional power bases or autonomous fiefdoms. Given China's vast geography, regional administrators naturally drifted into localized fiefdoms without a standardized civil service."
            },
            {
                        "word": "太守",
                        "pinyin": "tài shǒu",
                        "en": "Commandery Governor / Prefect",
                        "explanationZh": "古代郡级行政区的最高军政长官。若各郡太守依个人好恶私自任免官吏，所选官员便无法跨区域任职，导致各地政令阻隔、互不承认。",
                        "explanationEn": "The chief administrative governor of a commandery (prefecture) in ancient China. If each prefect appointed local protégés at will, governance standards would collapse across jurisdictions."
            },
            {
                        "word": "各自为政",
                        "pinyin": "gè zì wéi zhèng",
                        "en": "Each Pursuing Their Own Course / Fragmented Rule",
                        "explanationZh": "成语。各自按照自己的意愿和主张行事，缺乏统一部署。科举以全国统一的标准、统一的机构，彻底消除了地方官僚各自为政、互不认可的隐患。",
                        "explanationEn": "Idiom: each ruling according to their own agenda without central coordination. The unified examination dismantled this regional parochialism by establishing nationwide equivalence of credentials."
            },
            {
                        "word": "层层叠叠",
                        "pinyin": "céng céng dié dié",
                        "en": "Tier upon Tier / Multi-Layered",
                        "explanationZh": "形容层次丰富繁密。指古代从中央部院到道、府、州、县绵密分布的多层级行政管理结构，需要大量合格人才常年充实其中。",
                        "explanationEn": "Layer upon layer; referring to the multi-tiered administrative hierarchy stretching from imperial ministries down to prefectures and counties across a vast subcontinent."
            },
            {
                        "word": "源源不断",
                        "pinyin": "yuán yuán bù duàn",
                        "en": "In an Unbroken / Endless Stream",
                        "explanationZh": "成语。形容接连不断地涌来。科举制度固定每三年举行一次大考，为朝廷稳定输送取之不竭、品学兼优的年轻文官队伍。",
                        "explanationEn": "Idiom: a constant, unceasing stream. The triennial examination cycle guaranteed a regular, renewable replenishment of qualified scholar-bureaucrats across dynasties."
            },
            {
                        "word": "心血来潮",
                        "pinyin": "xīn xuè lái cháo",
                        "en": "On a Sudden Whim / Impulsive Caprice",
                        "explanationZh": "成语。指一时冲动、毫无定规的举措。科举制度的严格周期性杜绝了君主凭心血来潮隔十几年才临时选官的弊端，使国家管理具有可预期的稳定性。",
                        "explanationEn": "Idiom: acting on a capricious impulse. The institutional rhythm of scheduled exams prevented imperial regimes from capriciously suspending or improvising official recruitment."
            },
            {
                        "word": "门庭",
                        "pinyin": "mén tíng",
                        "en": "Clan Pedigree / Family Social Status",
                        "explanationZh": "指家族门第与阀阅出身。魏晋南北朝时期仕途全凭家世门第垄断；科举制度打破门庭藩篱，不分贵贱贫富，唯才华与试卷定高下。",
                        "explanationEn": "Ancestral lineage, clan pedigree, or aristocratic pedigree. The exam bypassed aristocratic gatekeeping, democratizing bureaucratic entry for ordinary commoners."
            },
            {
                        "word": "动员",
                        "pinyin": "dòng yuán",
                        "en": "Mobilization",
                        "explanationZh": "发动调动全体社会成员的积极性。科举促成了全社会文化生命力的大动员，使全国各阶层男性终生向学，铸就了中华文明尊师重教的深厚传统。",
                        "explanationEn": "Mobilization; rousing and activating the intellectual energies and social aspirations of the entire populace toward learning and statecraft."
            },
            {
                        "word": "屡败屡考",
                        "pinyin": "lǚ bài lǚ kǎo",
                        "en": "Persistently Re-Sitting Exams Despite Repeated Failures",
                        "explanationZh": "哪怕屡试不中依然矢志不渝、继续备考。科举为士人提供了终生的合法希望，将社会精英的不满与能量导向学术钻研而非破坏性暴动。",
                        "explanationEn": "Persistently re-taking the exams despite repeated failures. It provided a permanent legitimate avenue for ambition, transforming potential social rebellion into constructive scholarly discipline."
            },
            {
                        "word": "安全系数",
                        "pinyin": "ān quán xì shù",
                        "en": "Safety Margin / Societal Stability Factor",
                        "explanationZh": "维护社会安定秩序的保障程度。年轻男性最具躁动与叛逆倾向，科举成功将他们的大半精力引导在书卷文墨与考场竞争中，显著提升了社会稳定。",
                        "explanationEn": "Societal safety margin. By channeling restless, energetic young men into scholarly pursuit and civil service ambitions, the system neutralized destructive unrest in a cultural atmosphere."
            },
            {
                        "word": "进士",
                        "pinyin": "jìn shì",
                        "en": "Jinshi / Metropolitan Graduate",
                        "explanationZh": "科举殿试录取的最高等第，亦为古代知识分子的至高荣誉。余秋雨先生在著名文化散文《十万进士》中深入剖析了这一群体对中国历史与文化的深刻塑造。",
                        "explanationEn": "The highest degree awarded in the imperial civil examination system. Yu Qiuyu explored this elite intellectual group extensively in his acclaimed cultural essay 'A Hundred Thousand Jinshi'."
            },
            {
                        "word": "《女驸马》",
                        "pinyin": "Nǚ Fù Mǎ",
                        "en": "'The Female Imperial Son-in-Law' (Huangmei Opera)",
                        "explanationZh": "著名传统戏剧。讲述才女冯素珍为解救蒙冤未婚夫，女扮男装赴京考中状元并被选为驸马的奇闻。此剧折射出古代女性才识虽不让须眉，却被阻挡在科举门外的历史遗憾。",
                        "explanationEn": "A celebrated classic Chinese opera recounting how Feng Suzhen disguised herself as a man, topped the imperial exam, and was betrothed as the imperial son-in-law, reflecting women's exclusion from the exams."
            },
            {
                        "word": "提纲",
                        "pinyin": "tí gāng",
                        "en": "Thesis Outline / Structural Synopsis",
                        "explanationZh": "文章的论点脉络与框架架构。科考策论极其讲究起承转合与破题提纲，展现应试者剖析国家治理问题时的周密逻辑与行政思路。",
                        "explanationEn": "The thematic outline and structural blueprint of an essay, essential in imperial examinations for demonstrating logical rigor and administrative insight."
            },
            {
                        "word": "文采",
                        "pinyin": "wén cǎi",
                        "en": "Literary Flair / Ornate Stylistic Eloquence",
                        "explanationZh": "文字的辞藻与文学修辞。余秋雨先生强调，科举选拔的终极落脚点并非纯粹的诗赋文采，而是具备全局眼光、务实操盘能力的治国管理人才。",
                        "explanationEn": "Ornate poetic talent and literary rhetoric. The author underscores that the primary goal of the exam was practical administrative competence rather than pure poetry."
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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'lessons_data.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        lessons = json.load(f)

    # Check if 03-01 is present; if not, insert it after 03
    has_03_01 = any(l.get('index') == '03-01' for l in lessons)
    if not has_03_01:
        folder_03_01 = "lessons/03-01_君子的反面：研究小人是为了更好地认识君子"
        zh_path = os.path.join(base_dir, folder_03_01, "transcript.md")
        en_path = os.path.join(base_dir, folder_03_01, "english_transcript.md")
        zh_txt = open(zh_path, encoding='utf-8').read() if os.path.exists(zh_path) else ""
        en_txt = open(en_path, encoding='utf-8').read() if os.path.exists(en_path) else ""
        
        lesson_03_01 = {
            "index": "03-01",
            "title": "君子的反面：研究小人是为了更好地认识君子",
            "trackId": 139794735,
            "folderName": folder_03_01,
            "audioPath": f"./{folder_03_01}/audio.m4a",
            "quoteCardPath": f"./{folder_03_01}/quote_card_1.jpg",
            "transcriptZh": zh_txt,
            "transcriptEn": en_txt,
            "duration": 685.71
        }
        # Find position after 03
        pos = -1
        for i, l in enumerate(lessons):
            if str(l.get('index')) in ['3', '03']:
                pos = i + 1
                break
        if pos != -1:
            lessons.insert(pos, lesson_03_01)
        else:
            lessons.append(lesson_03_01)
        print("Inserted lesson 03-01 into lessons list")

    # Ensure 03-02 exists and is properly configured
    folder_03_02 = "lessons/03-02_如何应对小人？冷落、搁置并最终拯救他们"
    zh_path_02 = os.path.join(base_dir, folder_03_02, "transcript.md")
    en_path_02 = os.path.join(base_dir, folder_03_02, "english_transcript.md")
    zh_txt_02 = open(zh_path_02, encoding='utf-8').read() if os.path.exists(zh_path_02) else ""
    en_txt_02 = open(en_path_02, encoding='utf-8').read() if os.path.exists(en_path_02) else ""

    existing_03_02 = next((l for l in lessons if l.get('index') == '03-02'), None)
    if existing_03_02:
        existing_03_02['folderName'] = folder_03_02
        existing_03_02['audioPath'] = f"./{folder_03_02}/audio.m4a"
        existing_03_02['quoteCardPath'] = f"./{folder_03_02}/quote_card_1.jpg"
        existing_03_02['transcriptZh'] = zh_txt_02
        existing_03_02['transcriptEn'] = en_txt_02
        existing_03_02['duration'] = 953.55
        existing_03_02['title'] = "如何应对小人？冷落、搁置并最终拯救他们"
        existing_03_02['trackId'] = 143426937
    else:
        lesson_03_02 = {
            "index": "03-02",
            "title": "如何应对小人？冷落、搁置并最终拯救他们",
            "trackId": 143426937,
            "folderName": folder_03_02,
            "audioPath": f"./{folder_03_02}/audio.m4a",
            "quoteCardPath": f"./{folder_03_02}/quote_card_1.jpg",
            "transcriptZh": zh_txt_02,
            "transcriptEn": en_txt_02,
            "duration": 953.55
        }
        # Find position after 03-01
        pos = -1
        for i, l in enumerate(lessons):
            if str(l.get('index')) == '03-01':
                pos = i + 1
                break
        if pos != -1:
            lessons.insert(pos, lesson_03_02)
        else:
            lessons.append(lesson_03_02)
        print("Inserted lesson 03-02 into lessons list")

    for l in lessons:
        idx = l['index']
        if idx in LESSON_SUMMARIES or (isinstance(idx, int) and idx in LESSON_SUMMARIES) or (isinstance(idx, str) and idx.isdigit() and int(idx) in LESSON_SUMMARIES):
            summary_key = idx if idx in LESSON_SUMMARIES else (int(idx) if isinstance(idx, str) and idx.isdigit() else idx)
            l['summary'] = LESSON_SUMMARIES[summary_key]
            print(f"[{idx}] Added deep curated summary for {l['title']}")
        else:
            print(f"[{idx}] Missing summary for {l['title']}")

        folder = l.get('folderName', '')
        timed_file = os.path.join(base_dir, folder, 'timed_transcript.json')
        if os.path.exists(timed_file):
            with open(timed_file, 'r', encoding='utf-8') as tf:
                l['timedTranscript'] = json.load(tf)
            print(f"[{idx}] Synced timedTranscript ({len(l['timedTranscript'])} items) from {folder}")

        # Ensure transcriptZh and transcriptEn are synced from markdown files if they exist
        zh_f = os.path.join(base_dir, folder, 'transcript.md')
        en_f = os.path.join(base_dir, folder, 'english_transcript.md')
        if os.path.exists(zh_f):
            l['transcriptZh'] = open(zh_f, encoding='utf-8').read()
        if os.path.exists(en_f):
            l['transcriptEn'] = open(en_f, encoding='utf-8').read()

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)

    print("\nAll deep bilingual summaries written to lessons_data.json!")

if __name__ == '__main__':
    main()
