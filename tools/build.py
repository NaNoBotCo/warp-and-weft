# -*- coding: utf-8 -*-
"""build.py: write docs/index.html (English), docs/th/ (Thai) and docs/km/ (Khmer) from one source.

All copy lives here, three languages side by side. docs/weave.js draws everything that moves.
    python3 tools/build.py
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), "docs")
SITE = "https://nanobotco.github.io/warp-and-weft/"
LANGS = ("en", "th", "km")
L = "en"


def e(x):
    return html.escape("" if x is None else str(x))


def t(en, th, km):
    return {"en": en, "th": th, "km": km}[L]


def te(en, th, km):
    return e(t(en, th, km))


NAV = [("loom-sec", "Loom", "กี่", "កី"), ("math", "Math", "คณิต", "គណិត"), ("ikat", "Ikat", "มัดหมี่", "ចងជ្រលក់"),
       ("shawl", "Shawl", "ผ้าคลุมไหล่", "កន្សែង"), ("cambodia", "Cambodia", "กัมพูชา", "កម្ពុជា"),
       ("thailand", "Thailand", "ไทย", "ថៃ"), ("worm", "Silkworm", "หนอนไหม", "ដង្កូវនាង"),
       ("road", "Silk Road", "เส้นทางสายไหม", "ផ្លូវសូត្រ"), ("draw", "Draw", "วาด", "គូរ"),
       ("sources", "Sources", "แหล่งข้อมูล", "ប្រភព")]

SLAB = [("2", "sets of thread in every woven cloth", "ชุดเส้นด้ายในผ้าทอทุกผืน", "សំណុំអំបោះក្នុងក្រណាត់ត្បាញ"),
        ("1/2", "hol twill: the warp shows at one crossing in three", "ลายสองของผ้าโฮล เส้นยืนโผล่หนึ่งในสามจุด", "ត្បាញទ្រេតហូល៖ អំបោះបញ្ឈរលេចមួយក្នុងបី"),
        ("~900 m", "of silk in one cocoon", "เส้นไหมในรังเดียว", "សរសៃសូត្រក្នុងសំបុកមួយ"),
        ("7", "ways to repeat a border", "วิธีทำซ้ำลายขอบ", "របៀបធ្វើក្បាច់គែមឡើងវិញ"),
        ("1804", "Jacquard's punched-card loom", "กี่บัตรเจาะรูของฌากการ์", "កីកាតចោះរន្ធរបស់ហ្សាកា"),
        ("c. 552", "silkworm eggs reach Constantinople", "ไข่ไหมถึงคอนสแตนติโนเปิล", "ពងដង្កូវនាងដល់កុងស្តង់ទីណូប្លឺ")]

CAMBODIA = [
    ("Sampot hol", "สมปตโฮล", "សំពត់ហូល",
     "The weft-ikat silk wrap worn for weddings and Buddhist ceremonies. It is woven in an uneven 1/2 twill on three shafts, so one colour rules the face and another the back. More than 200 hol patterns have names.",
     "ผ้านุ่งไหมมัดหมี่เส้นพุ่ง ใส่ในงานแต่งงานและงานบุญ ทอลายสองไม่เท่ากันแบบ 1/2 บนสามตะกอ สีหนึ่งจึงเด่นด้านหน้า อีกสีเด่นด้านหลัง ลายโฮลที่มีชื่อเรียกมีมากกว่า 200 ลาย",
     "សំពត់សូត្រចងអំបោះទទឹង ស្លៀកក្នុងពិធីរៀបការ និងពិធីបុណ្យ។ ត្បាញទ្រេតមិនស្មើ 1/2 លើស៊ុមលើកបី ដូច្នេះពណ៌មួយលេចខាងមុខ ពណ៌មួយទៀតលេចខាងក្រោយ។ ក្បាច់ហូលដែលមានឈ្មោះ មានជាង 200។"),
    ("Pidan", "ปิดาน", "ពិដាន",
     "Pictorial hol hung above altars and offerings: temples, Buddhas, nagas, elephants, lions, rows of figures. The name is the Khmer word for ceiling.",
     "ผ้าโฮลภาพเล่าเรื่อง แขวนเหนือแท่นบูชาและเครื่องบูชา มีลายปราสาท พระพุทธรูป นาค ช้าง สิงห์ และแถวผู้คน ชื่อนี้คือคำเขมรที่แปลว่าเพดาน",
     "ហូលរូបភាព ព្យួរពីលើអាសនៈ និងគ្រឿងបូជា៖ ប្រាសាទ ព្រះពុទ្ធ នាគ ដំរី សិង្ហ និងជួរមនុស្ស។ ឈ្មោះនេះមកពីពិដាន ដែលវាព្យួរនៅពីក្រោម។"),
    ("Golden silk", "ไหมทอง", "សូត្រមាស",
     "Cambodia's native silkworms spin yellow cocoons. In 1996 Kikuo Morimoto, a kimono dyer from Kyoto, founded the Institute for Khmer Traditional Textiles, gathered older weavers who still held the craft, and planted mulberry and dye trees. It works from Siem Reap.",
     "หนอนไหมพื้นเมืองของกัมพูชาปั่นรังสีเหลือง ปี 1996 คิคุโอะ โมริโมโตะ ช่างย้อมกิโมโนจากเกียวโต ก่อตั้งสถาบันสิ่งทอพื้นเมืองเขมร รวบรวมช่างทอสูงวัยที่ยังรู้วิชา แล้วปลูกหม่อนกับต้นไม้ให้สีย้อม สถาบันทำงานอยู่ที่เสียมราฐ",
     "ដង្កូវនាងពូជខ្មែរបញ្ចេញសំបុកពណ៌លឿង។ នៅឆ្នាំ 1996 លោក គីគូអូ ម៉ូរីម៉ូតូ ជាងជ្រលក់ពណ៌គីម៉ូណូមកពីក្យូតូ បានបង្កើតវិទ្យាស្ថានវាយនភណ្ឌប្រពៃណីខ្មែរ ប្រមូលអ្នកត្បាញចាស់ៗដែលនៅចេះជំនាញ ហើយដាំមន និងដើមឈើសម្រាប់ធ្វើពណ៌។ វិទ្យាស្ថាននេះធ្វើការនៅសៀមរាប។"),
    ("Weaving villages", "หมู่บ้านทอผ้า", "ភូមិត្បាញ",
     "Takeo province, south of Phnom Penh, is known for its silk. Koh Dach, an island in the Mekong just upstream of the city, keeps looms under the houses.",
     "จังหวัดตาแก้ว ทางใต้ของพนมเปญ ขึ้นชื่อเรื่องผ้าไหม ส่วนเกาะดาจ เกาะกลางแม่น้ำโขงเหนือตัวเมืองขึ้นไปไม่ไกล มีกี่ทอผ้าอยู่ใต้ถุนบ้าน",
     "ខេត្តតាកែវ ខាងត្បូងភ្នំពេញ ល្បីខាងសូត្រ។ កោះដាច់ ជាកោះក្នុងទន្លេមេគង្គ ខាងលើទីក្រុងបន្តិច មានកីត្បាញនៅក្រោមផ្ទះ។"),
]

THAILAND = [
    ("Mudmee", "มัดหมี่", "ម៉ាត់មី",
     "Isan's weft ikat, in silk and in cotton, from fine silk for ceremonies to the everyday cotton pha sin, the tube skirt. Patterns are tied in bundles, and many have names: naga, hook, tree.",
     "มัดหมี่ของอีสาน มีทั้งไหมและฝ้าย ตั้งแต่ผ้าไหมเนื้อดีสำหรับงานพิธี ไปจนถึงผ้าซิ่นฝ้ายใส่ทุกวัน ลายมัดเป็นปอย และหลายลายมีชื่อ เช่น ลายนาค ลายขอ ลายต้นสน",
     "ម៉ាត់មីនៃអ៊ីសាន ចងអំបោះទទឹង មានទាំងសូត្រ និងកប្បាស ចាប់ពីសូត្រល្អសម្រាប់ពិធី ដល់សំពត់ស៊ីនកប្បាសស្លៀករាល់ថ្ងៃ។ ក្បាច់ចងជាបាច់ ហើយក្បាច់ជាច្រើនមានឈ្មោះ ដូចជា នាគ ទំពក់ ដើមឈើ។"),
    ("Khit", "ขิด", "ខិត",
     "Continuous supplementary weft: an extra thread runs selvedge to selvedge over the ground weave, lifted by pattern sticks into diamonds, hooks and nagas. The triangular mon khit pillows of Isan are the best-known pieces.",
     "การเสริมเส้นพุ่งแบบต่อเนื่อง ด้ายพิเศษวิ่งจากริมผ้าด้านหนึ่งไปอีกด้านบนเนื้อผ้าพื้น ยกด้วยไม้เก็บขิดให้เป็นลายข้าวหลามตัด ขอ และนาค หมอนขิดสามเหลี่ยมของอีสานคือชิ้นที่คุ้นตาที่สุด",
     "ការបន្ថែមអំបោះទទឹងជាប់គ្នា៖ អំបោះបន្ថែមរត់ពីគែមម្ខាងទៅគែមម្ខាងទៀតលើក្រណាត់ផ្ទៃ លើកដោយឈើរើសក្បាច់ ទៅជាក្បាច់ពេជ្រ ទំពក់ និងនាគ។ ខ្នើយខិតរាងត្រីកោណនៃអ៊ីសាន ជារបស់ដែលគេស្គាល់ច្រើនជាងគេ។"),
    ("Jok", "จก", "ចក",
     "Discontinuous supplementary weft, picked in by fingertip or a small pick, one patch of colour at a time. The teen jok, the worked hem of a Tai Yuan tube skirt, is the pride of Mae Chaem in Chiang Mai province.",
     "การเสริมเส้นพุ่งแบบไม่ต่อเนื่อง ใช้ปลายนิ้วหรือขนเม่นควักด้ายสีเข้าทีละหย่อม ตีนจก คือเชิงผ้าซิ่นไทยวนที่ทอลายจก เป็นความภูมิใจของแม่แจ่ม จังหวัดเชียงใหม่",
     "ការបន្ថែមអំបោះទទឹងមិនជាប់គ្នា ប្រើចុងម្រាមដៃ ឬឈើចកតូច ជីកអំបោះពណ៌ចូលម្តងមួយដុំ។ ទីនចក ជាជាយសំពត់ស៊ីនថៃយួន ដែលត្បាញក្បាច់ចក ជាមោទនភាពនៃម៉ែចែម ខេត្តឈៀងម៉ៃ។"),
    ("Prae wa", "แพรวา", "ផ្រែវ៉ា",
     "The Phu Tai weavers of Kalasin make this shoulder cloth of dense supplementary-weft patterns on a red ground. Thais call it the queen of silks.",
     "ผ้าสไบของชาวผู้ไทกาฬสินธุ์ ลายเสริมเส้นพุ่งแน่นเต็มผืนบนพื้นสีแดง คนไทยเรียกว่าราชินีแห่งผ้าไหม",
     "ក្រណាត់ស្ពាយស្មារបស់អ្នកត្បាញភូថៃ នៅកាឡាស៊ីន មានក្បាច់បន្ថែមអំបោះទទឹងក្រាស់ពេញផ្ទាំង លើផ្ទៃពណ៌ក្រហម។ ជនជាតិថៃហៅវាថា មហាក្សត្រីនៃសូត្រ។"),
    ("Peacock marks", "ตรานกยูง", "ត្រាក្ងោក",
     "Four peacock marks grade Thai silk. Gold: native silk, handmade start to finish, natural dyes. Silver: handmade with some modern steps. Blue: pure silk, made any way. Green: silk blends.",
     "ตรานกยูงสี่สีแบ่งชั้นผ้าไหมไทย สีทอง ไหมพันธุ์พื้นบ้าน ทำมือทุกขั้นตอน ย้อมสีธรรมชาติ สีเงิน ทำมือแต่ใช้เครื่องมือสมัยใหม่บางขั้น สีน้ำเงิน ไหมแท้ ทำด้วยวิธีใดก็ได้ สีเขียว ไหมผสม",
     "ត្រាក្ងោកបួនពណ៌ ចាត់ថ្នាក់សូត្រថៃ។ មាស៖ សូត្រពូជក្នុងស្រុក ធ្វើដោយដៃគ្រប់ដំណាក់កាល ជ្រលក់ពណ៌ធម្មជាតិ។ ប្រាក់៖ ធ្វើដោយដៃ តែប្រើឧបករណ៍ទំនើបខ្លះ។ ខៀវ៖ សូត្រសុទ្ធ ធ្វើតាមវិធីណាក៏បាន។ បៃតង៖ សូត្រលាយ។"),
    ("Revival", "ฟื้นฟู", "ការស្តារ",
     "After the Second World War the American Jim Thompson built Thai silk into an export known abroad; he vanished in Malaysia's Cameron Highlands in 1967. In 1976 Queen Sirikit founded the SUPPORT Foundation, which trains village weavers and buys their cloth.",
     "หลังสงครามโลกครั้งที่สอง จิม ทอมป์สัน ชาวอเมริกัน ทำให้ผ้าไหมไทยเป็นสินค้าส่งออกที่มีชื่อในต่างประเทศ เขาหายตัวไปที่คาเมรอนไฮแลนด์ ประเทศมาเลเซีย ในปี 1967 ปี 1976 (พ.ศ. 2519) สมเด็จพระนางเจ้าสิริกิติ์ พระบรมราชินีนาถ พระบรมราชชนนีพันปีหลวง ทรงก่อตั้งมูลนิธิส่งเสริมศิลปาชีพ ฝึกช่างทอในหมู่บ้านและรับซื้อผ้า",
     "ក្រោយសង្គ្រាមលោកលើកទីពីរ ជនជាតិអាមេរិក ជីម ថមសុន បានធ្វើឱ្យសូត្រថៃក្លាយជាទំនិញនាំចេញដែលល្បីនៅបរទេស។ គាត់បានបាត់ខ្លួននៅខ្ពង់រាបខេមេរុន ប្រទេសម៉ាឡេស៊ី ក្នុងឆ្នាំ 1967។ នៅឆ្នាំ 1976 ព្រះមហាក្សត្រីសិរីកិត្តិ៍ បានបង្កើតមូលនិធិ SUPPORT ដែលបណ្តុះបណ្តាលអ្នកត្បាញតាមភូមិ និងទិញក្រណាត់របស់ពួកគេ។"),
]

LIFE = [("~10 days", "ราว 10 วัน", "ប្រហែល 10 ថ្ងៃ", "Egg", "ไข่", "ពង"),
        ("~25 days, 4 moults", "ราว 25 วัน ลอกคราบ 4 ครั้ง", "ប្រហែល 25 ថ្ងៃ សកស្បែក 4 ដង", "Caterpillar, mulberry only", "หนอน กินแต่ใบหม่อน", "ដង្កូវ ស៊ីតែស្លឹកមន"),
        ("2–3 days", "2–3 วัน", "2–3 ថ្ងៃ", "Spinning the cocoon", "ชักใยทำรัง", "បញ្ចេញសរសៃធ្វើសំបុក"),
        ("~2 weeks", "ราว 2 สัปดาห์", "ប្រហែល 2 សប្តាហ៍", "Pupa, inside", "ดักแด้ อยู่ข้างใน", "ដង្កូវក្នុងសំបុក"),
        ("a few days", "ไม่กี่วัน", "ពីរបីថ្ងៃ", "Moth: mates, lays hundreds of eggs, cannot fly", "ผีเสื้อ ผสมพันธุ์ วางไข่หลายร้อยฟอง บินไม่ได้", "មេអំបៅ៖ បង្កាត់ពូជ ពងរាប់រយ ហើរមិនរួច")]

SOURCES = [
    ("Pidan (textile) — Wikipedia", "https://en.wikipedia.org/wiki/Pidan_(textile)"),
    ("Sampot — Wikipedia", "https://en.wikipedia.org/wiki/Sampot"),
    ("Cambodian kiet — Asian Textile Studies", "http://www.asiantextilestudies.com/kiet.html"),
    ("What is Khmer ikat? — IKTT", "https://www.ikttearth.org/what-is-khmer-ikatt"),
    ("Saving Cambodia's ancient silk legacy — National Geographic", "https://www.nationalgeographic.com/culture/article/kikuo-morimoto-explorer-moments-reviving-silk-production-cambodia"),
    ("Thai silk: elegance in threads — Thailand Foundation", "https://thailandfoundation.or.th/thai-silk-elegance-in-threads/"),
    ("Phrae wa, the queen of Thai silk — Thailand Foundation", "https://thailandfoundation.or.th/phrae-wa-the-queen-of-thai-silk/"),
    ("Thai silk peacock marks — Silkket", "https://silkket.com/blogs/blog/thai-silk-product-standard-certification-mark-royally-bestowed-peacock-symbol"),
    ("Teen jok from Mae Chaem — Tribal Trappings", "https://tribaltrappings.com/teen-jok-from-mae-chaem-thailand/"),
    ("Silkworm moth — Britannica", "https://www.britannica.com/animal/silkworm-moth"),
    ("Cocoon spinning behavior in the silkworm — Zoological Science", "https://bioone.org/journals/zoological-science/volume-16/issue-2/zsj.16.215/Cocoon-Spinning-Behavior-in-the-Silkworm-Bombyx-mori/10.2108/zsj.16.215.full"),
    ("Jacquard machine — Wikipedia", "https://en.wikipedia.org/wiki/Jacquard_machine"),
    ("Ada Lovelace, Notes on the Analytical Engine (1843) — Wikisource", "https://en.wikisource.org/wiki/Scientific_Memoirs/3/Sketch_of_the_Analytical_Engine_invented_by_Charles_Babbage,_Esq."),
    ("Frieze group — Wikipedia", "https://en.wikipedia.org/wiki/Frieze_group"),
    ("Satin weave — Wikipedia", "https://en.wikipedia.org/wiki/Satin_weave"),
    ("Silk Road — Wikipedia", "https://en.wikipedia.org/wiki/Silk_Road"),
    ("Óc Eo — Wikipedia", "https://en.wikipedia.org/wiki/%C3%93c_Eo"),
    ("Sericulture — Wikipedia", "https://en.wikipedia.org/wiki/Sericulture"),
    ("Natural Earth 1:110m land", "https://www.naturalearthdata.com/"),
    ("Noto Sans Khmer — Google Fonts", "https://fonts.google.com/noto/specimen/Noto+Sans+Khmer"),
]

CSS = r"""
:root{--bg:#f6efe3;--card:#fffaf1;--ink:#2a1a12;--mute:#6d5646;--line:#e3d5c0;--gold:#b97a1c;--teal:#137a71;--pink:#c24a82;--dark:#1a100b;
 --f:system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans Thai","Noto Sans Khmer","Khmer Sangam MN",sans-serif;--s:Georgia,"Noto Serif Thai","Noto Serif Khmer",serif}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#1c120d;--card:#26190f;--ink:#f0e6d6;--mute:#bba58f;--line:#3d2b1f;--gold:#e9a53c;--teal:#3fb3a6;--pink:#e377a9}}
:root[data-theme=dark]{--bg:#1c120d;--card:#26190f;--ink:#f0e6d6;--mute:#bba58f;--line:#3d2b1f;--gold:#e9a53c;--teal:#3fb3a6;--pink:#e377a9}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 var(--f);-webkit-text-size-adjust:100%}
:lang(th) body,body:lang(th){line-height:1.8}:lang(km) body,body:lang(km){line-height:1.9}
a{color:var(--teal)}h2,h3{font-family:var(--s);line-height:1.2}
header.top{position:sticky;top:0;z-index:20;background:rgba(20,11,7,.92);backdrop-filter:blur(6px);color:#f4ead8;transition:transform .25s}
body.nav-away header.top{transform:translateY(-100%)}
header.top .in{display:flex;gap:14px;align-items:center;max-width:1180px;margin:0 auto;padding:8px 16px}
.brand{color:#f4ead8;text-decoration:none;font-weight:700;white-space:nowrap;display:flex;gap:8px;align-items:center}
.brand svg{width:26px;height:26px}
header.top nav{display:flex;gap:12px;overflow-x:auto;flex:1;scrollbar-width:none;font-size:14px}
header.top nav::-webkit-scrollbar{display:none}
header.top nav a,.langsw a{color:#e7d6bd;text-decoration:none;white-space:nowrap}
header.top nav a:hover{color:#fff}
.langsw{display:flex;gap:8px;font-size:14px}.langsw a[aria-current]{color:#e9a53c;font-weight:700}
.hero{position:relative;background:#0d0705;color:#f4ead8}
#loom{display:block;width:100%;height:560px}
.hero .over{position:absolute;left:0;right:0;top:0;padding:28px 16px 0;pointer-events:none}
.hero .over .in{max-width:1180px;margin:0 auto}
.hero h1{font-family:var(--s);font-size:clamp(34px,6.4vw,76px);margin:0;line-height:1.02;text-shadow:0 2px 18px #000}
.hero .sub{font-size:clamp(15px,2vw,20px);max-width:640px;margin:10px 0 0;color:#ecdcc4;text-shadow:0 1px 10px #000}
.hero .langs{font-size:clamp(15px,2vw,19px);color:#e9a53c;margin-top:8px;text-shadow:0 1px 10px #000}
main{max-width:1060px;margin:0 auto;padding:0 16px}
.slab{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:28px 0}
.slab div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.slab b{display:block;font:700 28px/1.1 var(--s);color:var(--gold)}.slab span{font-size:14px;color:var(--mute)}
section.sec{padding:34px 0;border-top:1px solid var(--line)}
section.sec>h2{font-size:clamp(28px,4vw,42px);margin:0 0 6px}
.kick{color:var(--gold);font-weight:700;letter-spacing:.02em;margin:0}
.lede{max-width:720px}
.toy{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin:18px 0}
.toy canvas{display:block;width:100%;border-radius:8px;touch-action:manipulation}
.ctl{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0 0;font-size:15px}
.ctl button{font:inherit;font-size:14px;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:999px;padding:6px 13px;cursor:pointer}
.ctl button:hover{border-color:var(--gold)}
.ctl label{display:flex;gap:6px;align-items:center}
.ctl input[type=range]{width:130px;accent-color:var(--gold)}
.ctl select,.ctl input[type=text]{font:inherit;font-size:15px;padding:5px 8px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink)}
.out{font-size:15px;color:var(--mute);margin:10px 0 0;min-height:1.6em}
.formula{font-family:ui-monospace,Menlo,monospace;font-size:14px;color:var(--mute);overflow-wrap:anywhere}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.pair figure{margin:0}.pair img{width:100%;border-radius:8px;display:block}
figcaption{font-size:13px;color:var(--mute);margin-top:6px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:18px 0}
.cards article{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.cards h3{margin:0 0 2px;font-size:22px}.cards .alt{color:var(--gold);font-size:15px;margin:0 0 6px}
.cards p{margin:0;font-size:16px}
blockquote{margin:18px 0;padding:10px 18px;border-left:4px solid var(--gold);font-family:var(--s);font-size:20px}
.life{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}
.life li{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;font-size:15px}
.life b{display:block;color:var(--teal)}
.two{display:grid;grid-template-columns:200px 1fr;gap:14px;align-items:start}
#motif{max-width:168px;cursor:pointer}
.legend{font-size:13px;color:var(--mute)}
.sources li{margin:4px 0;font-size:15px}
footer.bot{border-top:1px solid var(--line);margin-top:30px;padding:20px 16px;font-size:14px;color:var(--mute);text-align:center}
@media (max-width:640px){.pair,.two{grid-template-columns:1fr}.slab b{font-size:24px}header.top nav{display:none}}
body.card header.top,body.card main,body.card footer{display:none}
body.card .over{padding:60px 64px 0}body.card #loom{height:100vh}
"""


def ver():
    import hashlib
    return hashlib.sha1(open(os.path.join(DOCS, "weave.js"), "rb").read()).hexdigest()[:8]


def cards(rows):
    return "".join(f'<article><h3>{te(a, b, c)}</h3><p class="alt">{e(" · ".join(x for x in (a, b, c) if x != t(a, b, c)))}</p><p>{te(d, f, g)}</p></article>'
                   for a, b, c, d, f, g in rows)


def page():
    VER = ver()
    up = "" if L == "en" else "../"
    here = SITE + ("" if L == "en" else L + "/")
    title = t("Warp and Weft", "เส้นยืน เส้นพุ่ง", "អំបោះបញ្ឈរ អំបោះទទឹង")
    desc = t("Silk, weaving and the arithmetic inside cloth: a loom weaving a Khmer silk shawl, the weaving draft as a matrix product, ikat tie-and-dye, seven borders, satins by number theory, a silkworm's figure-eight cocoon, and the Silk Road. English, Thai and Khmer.",
             "ผ้าไหม การทอ และเลขคณิตในเนื้อผ้า กี่ที่กำลังทอผ้าไหมเขมร แบบทอที่เป็นการคูณเมทริกซ์ มัดหมี่ ลายขอบเจ็ดแบบ ผ้าต่วนด้วยทฤษฎีจำนวน รังไหมที่หนอนชักใยเป็นเลขแปด และเส้นทางสายไหม ภาษาอังกฤษ ไทย และเขมร",
             "សូត្រ ការត្បាញ និងលេខនព្វន្តក្នុងក្រណាត់៖ កីកំពុងត្បាញកន្សែងសូត្រខ្មែរ ប្លង់ត្បាញជាផលគុណម៉ាទ្រីស ការចងជ្រលក់ ក្បាច់គែមប្រាំពីរ សាតាំងតាមទ្រឹស្តីចំនួន សំបុកដង្កូវនាងរាងលេខប្រាំបី និងផ្លូវសូត្រ។ អង់គ្លេស ថៃ និងខ្មែរ។")
    fonts = ("https://fonts.googleapis.com/css2?family=Noto+Sans+Khmer:wght@400;700&family=Noto+Serif+Khmer:wght@700&display=swap" if L == "km"
             else "https://fonts.googleapis.com/css2?family=Noto+Sans+Khmer:wght@700&display=swap&text=" + "គោ")
    navh = "".join(f'<a href="#{a}">{te(b, c, d)}</a>' for a, b, c, d in NAV)
    langsw = " ".join(f'<a href="{up}{"" if k == "en" else k + "/"}" hreflang="{k}" lang="{k}"{" aria-current=page" if k == L else ""}>{n}</a>'
                      for k, n in (("en", "EN"), ("th", "ไทย"), ("km", "ខ្មែរ")))
    alts = "".join(f'<link rel="alternate" hreflang="{k}" href="{SITE}{"" if k == "en" else k + "/"}">' for k in LANGS)
    slab = "".join(f'<div><b>{e(n)}</b><span>{te(a, b, c)}</span></div>' for n, a, b, c in SLAB)
    life = "".join(f'<li><b>{te(a, b, c)}</b>{te(d, f, g)}</li>' for a, b, c, d, f, g in LIFE)
    srcs = "".join(f'<li><a href="{e(u)}">{e(n)}</a></li>' for n, u in SOURCES)
    other = [x for x in ("Warp and Weft", "เส้นยืน เส้นพุ่ง", "អំបោះបញ្ឈរ អំបោះទទឹង") if x != title]
    return f"""<!doctype html>
<html lang="{L}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="google" content="notranslate">
<title>{e(title)} · {te("silk, drawn by arithmetic", "ผ้าไหม วาดด้วยเลขคณิต", "សូត្រ គូរដោយលេខនព្វន្ត")}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#1a100b">
<link rel="canonical" href="{here}">{alts}<link rel="alternate" hreflang="x-default" href="{SITE}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Warp and Weft · เส้นยืน เส้นพุ่ง · អំបោះបញ្ឈរ អំបោះទទឹង">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{here}">
<meta property="og:image" content="{SITE}card.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{te("A loom weaving a Khmer silk ikat of gold cattle, drawn by arithmetic", "กี่กำลังทอผ้าไหมมัดหมี่เขมรลายวัวสีทอง วาดด้วยเลขคณิต", "កីកំពុងត្បាញហូលសូត្រខ្មែរ ក្បាច់គោពណ៌មាស គូរដោយលេខនព្វន្ត")}">
<meta property="og:locale" content="{t("en_US", "th_TH", "km_KH")}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}card.jpg">
<link rel="icon" href="{up}icon.svg" type="image/svg+xml">
<link rel="alternate" type="text/plain" href="{SITE}llms.txt" title="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<style>{CSS}</style>
<script>if(/[?&]card\\b/.test(location.search))document.documentElement.classList.add("card-mode")</script>
</head><body>
<script>if(document.documentElement.classList.contains("card-mode"))document.body.classList.add("card")</script>
<header class="top"><div class="in">
<a class="brand" href="{up}{"" if L == "en" else L + "/"}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 2v20M9 2v20M14 2v20M19 2v20M2 7h20M2 12h20M2 17h20" stroke="#e9a53c" stroke-width="1.6" fill="none"/></svg>{e(title)}</a>
<nav aria-label="{te("Sections", "หัวข้อ", "ផ្នែក")}">{navh}</nav>
<span class="langsw">{langsw}</span>
</div></header>

<div class="hero"><canvas id="loom" role="img" aria-label="{te("A loom weaving NaN's Khmer silk shawl, pick by pick", "กี่กำลังทอผ้าไหมเขมรของแนน ทีละเส้นพุ่ง", "កីកំពុងត្បាញកន្សែងសូត្រខ្មែររបស់ណាន ម្តងមួយជួរ")}"></canvas>
<div class="over"><div class="in"><h1>{e(title)}</h1>
<p class="langs">{e(" · ".join(other))}</p>
<p class="sub">{te("Silk, weaving and the arithmetic inside cloth. The loom is weaving NaN's Khmer silk shawl, one weft thread at a time, from a plan drawn in code.",
 "ผ้าไหม การทอ และเลขคณิตในเนื้อผ้า กี่นี้กำลังทอผ้าไหมเขมรของแนน ทีละเส้นพุ่ง จากแบบที่วาดด้วยโค้ด",
 "សូត្រ ការត្បាញ និងលេខនព្វន្តក្នុងក្រណាត់។ កីនេះកំពុងត្បាញកន្សែងសូត្រខ្មែររបស់ណាន ម្តងមួយសរសៃ ពីប្លង់ដែលគូរដោយកូដ។")}</p></div></div></div>

<main>
<div class="slab">{slab}</div>

<section class="sec" id="loom-sec">
<p class="kick">{te("Loom", "กี่", "កី")}</p>
<h2>{te("Two threads, over and under", "สองเส้น ขึ้นกับลง", "អំបោះពីរ ឡើងនិងចុះ")}</h2>
<p class="lede">{te("Warp threads run the length of the loom, stretched tight. The weft crosses them, over some and under others. Which ones rise is up to the shafts: frames that each lift a set of warps when the weaver steps on a treadle.",
 "เส้นยืนขึงตึงตามความยาวของกี่ เส้นพุ่งสอดขวางผ่าน ข้ามบางเส้น ลอดบางเส้น เส้นไหนจะยกขึ้นขึ้นอยู่กับตะกอ คือกรอบที่ยกเส้นยืนชุดหนึ่งขึ้นเมื่อช่างทอเหยียบไม้เหยียบ",
 "អំបោះបញ្ឈរលាតសន្ធឹងតឹងតាមបណ្តោយកី។ អំបោះទទឹងឆ្លងកាត់វា ពីលើខ្លះ ពីក្រោមខ្លះ។ សរសៃណាឡើង គឺអាស្រ័យលើស៊ុមលើក ដែលលើកអំបោះបញ្ឈរមួយក្រុម ពេលអ្នកត្បាញជាន់ឈើជាន់។")}</p>
<p class="lede">{te("A weaving draft writes this down as three grids. Top: which shaft each warp is threaded through. Top right: which shafts each treadle lifts. Right: which treadle each pick uses. The cloth is their product: the warp shows wherever the treadle lifts that warp's shaft. Tap any square to change it.",
 "แบบทอเขียนเรื่องนี้เป็นตารางสามชุด ด้านบน: เส้นยืนแต่ละเส้นร้อยผ่านตะกอไหน มุมขวาบน: ไม้เหยียบแต่ละอันยกตะกอไหน ด้านขวา: เส้นพุ่งแต่ละเส้นใช้ไม้เหยียบอันไหน ผ้าคือผลคูณของทั้งสาม เส้นยืนโผล่ตรงที่ไม้เหยียบยกตะกอของเส้นนั้น แตะช่องไหนก็ได้เพื่อเปลี่ยน",
 "ប្លង់ត្បាញកត់ត្រារឿងនេះជាតារាងបី។ ខាងលើ៖ អំបោះបញ្ឈរនីមួយៗចងកាត់ស៊ុមណា។ ជ្រុងស្តាំខាងលើ៖ ឈើជាន់នីមួយៗលើកស៊ុមណា។ ខាងស្តាំ៖ ជួរទទឹងនីមួយៗប្រើឈើជាន់ណា។ ក្រណាត់គឺជាផលគុណរបស់វាទាំងបី៖ អំបោះបញ្ឈរលេចឡើងនៅកន្លែងដែលឈើជាន់លើកស៊ុមរបស់វា។ ចុចលើក្រឡាណាមួយ ដើម្បីប្តូរ។")}</p>
<div class="toy"><canvas id="draft" aria-label="{te("Weaving draft", "แบบทอ", "ប្លង់ត្បាញ")}"></canvas>
<p class="formula">cloth[pick][warp] = tie-up[shaft(warp)][treadle(pick)]</p>
<canvas id="draft-cloth" aria-hidden="true"></canvas>
<div class="ctl">
<button data-draft="plain">{te("Plain", "ลายขัด", "ត្បាញធម្មតា")}</button><button data-draft="basket">{te("Basket", "ลายตะกร้า", "ក្បាច់កន្ត្រក")}</button>
<button data-draft="hol">{te("Hol 1/2", "โฮล 1/2", "ហូល 1/2")}</button><button data-draft="twill">{te("Twill 2/2", "ลายสอง 2/2", "ទ្រេត 2/2")}</button>
<button data-draft="twill31">{te("Twill 3/1", "ลายสอง 3/1", "ទ្រេត 3/1")}</button><button data-draft="diamond">{te("Diamond", "ข้าวหลามตัด", "ក្បាច់ពេជ្រ")}</button>
<button data-draft="colour">{te("Colours", "สี", "ពណ៌")}</button><button data-draft="random">{te("Surprise", "สุ่ม", "ចៃដន្យ")}</button>
</div></div>
</section>

<section class="sec" id="math">
<p class="kick">{te("Math", "คณิต", "គណិត")}</p>
<h2>{te("Cloth that computes", "ผ้าที่คำนวณ", "ក្រណាត់ដែលគណនា")}</h2>
<p class="lede">{te("In 1804 Joseph Marie Jacquard hung a chain of punched cards on a loom: one card per pick, one hole for each warp to lift. Charles Babbage borrowed the cards for his Analytical Engine, and in 1843 Ada Lovelace wrote that the engine",
 "ปี 1804 โจเซฟ มารี ฌากการ์ แขวนสายบัตรเจาะรูไว้บนกี่ บัตรหนึ่งใบต่อเส้นพุ่งหนึ่งเส้น รูหนึ่งรูต่อเส้นยืนที่ต้องยก ชาลส์ แบบเบจ ยืมบัตรนี้ไปใช้กับเครื่องวิเคราะห์ของเขา และปี 1843 เอดา เลิฟเลซ เขียนว่าเครื่องนั้น",
 "នៅឆ្នាំ 1804 ហ្សូសែប ម៉ារី ហ្សាកា បានព្យួរខ្សែកាតចោះរន្ធលើកី៖ កាតមួយសម្រាប់ជួរទទឹងមួយ រន្ធមួយសម្រាប់អំបោះបញ្ឈរនីមួយៗដែលត្រូវលើក។ ឆាលស៍ បាបេច បានខ្ចីកាតទាំងនេះទៅប្រើក្នុងម៉ាស៊ីនវិភាគរបស់គាត់ ហើយនៅឆ្នាំ 1843 អាដា ឡាវឡេស បានសរសេរថា ម៉ាស៊ីននោះ")}</p>
<blockquote lang="en">“weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves.”</blockquote>
{"" if L == "en" else f'<p class="lede">{te("", "“ทอลวดลายพีชคณิต เหมือนกี่ฌากการ์ทอดอกไม้และใบไม้”", "«ត្បាញក្បាច់ពិជគណិត ដូចកីហ្សាកាត្បាញផ្កា និងស្លឹកឈើ»")}</p>'}
<p class="lede">{te("Weavers in Thailand, Laos and Cambodia store patterns too. For supplementary-weft cloth a weaver picks the pattern out once with a stick, then saves each row as a string heddle hung above the loom. Lift them in order and the pattern repeats; hand them to another weaver and it travels.",
 "ช่างทอในไทย ลาว และกัมพูชา ก็เก็บลายไว้เหมือนกัน สำหรับผ้าขิดและผ้าเสริมเส้นพุ่ง ช่างทอเก็บลายครั้งแรกด้วยไม้เก็บลาย แล้วบันทึกแต่ละแถวเป็นเขาเชือกแขวนเหนือกี่ ยกตามลำดับ ลายก็ซ้ำ ส่งต่อให้ช่างทอคนอื่น ลายก็เดินทางไปด้วย",
 "អ្នកត្បាញនៅថៃ ឡាវ និងកម្ពុជា ក៏រក្សាទុកក្បាច់ដែរ។ សម្រាប់ក្រណាត់បន្ថែមអំបោះទទឹង អ្នកត្បាញរើសក្បាច់ម្តងដោយប្រើឈើ រួចរក្សាទុកជួរនីមួយៗជាខ្សែព្យួរពីលើកី។ លើកតាមលំដាប់ ក្បាច់ក៏កើតឡើងវិញ ហុចឱ្យអ្នកត្បាញម្នាក់ទៀត ក្បាច់ក៏ធ្វើដំណើរទៅជាមួយ។")}</p>
<h3>{te("Satin, by number theory", "ผ้าต่วน ด้วยทฤษฎีจำนวน", "សាតាំង តាមទ្រឹស្តីចំនួន")}</h3>
<p class="lede">{te("A satin ties each warp down once every n threads, stepping k places each row, so the ties never touch and the long floats shine. It works when k shares no factor with n and is not 1 or n−1. Try 4 and 6: no step works.",
 "ผ้าต่วนขัดเส้นยืนแต่ละเส้นหนึ่งครั้งในทุก n เส้น ขยับไป k ช่องทุกแถว จุดขัดจึงไม่ติดกัน เส้นที่ลอยยาวจึงเป็นมันวาว ใช้ได้เมื่อ k กับ n ไม่มีตัวหารร่วม และ k ไม่ใช่ 1 หรือ n−1 ลอง 4 กับ 6 ดู ไม่มีก้าวไหนใช้ได้เลย",
 "សាតាំងចងអំបោះបញ្ឈរនីមួយៗម្តងក្នុងរាល់ n សរសៃ ដោយរំកិល k ក្រឡារាល់ជួរ ដូច្នេះចំណុចចងមិនប៉ះគ្នា ហើយសរសៃអណ្តែតវែងៗភ្លឺរលោង។ វាដំណើរការពេល k និង n គ្មានតួចែករួម ហើយ k មិនមែន 1 ឬ n−1។ សាកល្បង 4 និង 6៖ គ្មានជំហានណាដំណើរការទេ។")}</p>
<div class="toy"><canvas id="satin" aria-label="{te("Satin weave", "ผ้าต่วน", "សាតាំង")}"></canvas>
<div class="ctl"><label>{te("threads", "จำนวนเส้น", "ចំនួនសរសៃ")} n <input id="satin-n" type="range" min="3" max="12" value="8"> <b id="satin-nv">8</b></label>
<label>{te("step", "ก้าว", "ជំហាន")} k <input id="satin-k" type="range" min="1" max="11" value="3"> <b id="satin-kv">3</b></label></div>
<p class="out" id="satin-out"></p></div>
<h3>{te("Seven borders", "ลายขอบเจ็ดแบบ", "ក្បាច់គែមប្រាំពីរ")}</h3>
<p class="lede">{te("A border repeats one motif along a line. Counting slides, flips and half-turns, there are exactly seven ways to do it. John Conway named them for footprints: hop, step, sidle, jump and their spinning kin. Draw a motif in the square and all seven follow.",
 "ลายขอบคือการซ้ำลายหนึ่งไปตามแนวเส้น นับการเลื่อน การพลิก และการหมุนครึ่งรอบ มีวิธีทำได้เจ็ดแบบพอดี จอห์น คอนเวย์ ตั้งชื่อตามรอยเท้า: กระโดด ก้าวเดิน ก้าวข้าง กระโดดสองเท้า และแบบหมุน วาดลายในช่องสี่เหลี่ยม ลายขอบทั้งเจ็ดจะเปลี่ยนตาม",
 "ក្បាច់គែមគឺការធ្វើក្បាច់មួយឡើងវិញតាមបន្ទាត់។ រាប់ទាំងការរំកិល ការត្រឡប់ និងការបង្វិលពាក់កណ្តាលជុំ មានរបៀបធ្វើបានប្រាំពីរយ៉ាងគត់។ ចន ខនវេ បានដាក់ឈ្មោះតាមស្នាមជើង៖ លោត ដើរ ដើរចំហៀង លោតជើងពីរ និងប្រភេទបង្វិល។ គូរក្បាច់ក្នុងការ៉េ ហើយក្បាច់គែមទាំងប្រាំពីរនឹងប្តូរតាម។")}</p>
<div class="toy"><div class="two"><div><canvas id="motif" aria-label="{te("Motif editor", "ช่องวาดลาย", "ប្រអប់គូរក្បាច់")}"></canvas>
<div class="ctl"><button data-motif="hook">{te("Hook", "ขอ", "ទំពក់")}</button><button data-motif="clear">{te("Clear", "ล้าง", "លុប")}</button><button data-motif="random">{te("Surprise", "สุ่ม", "ចៃដន្យ")}</button></div></div>
<canvas id="friezes" aria-label="{te("The seven frieze patterns", "ลายขอบทั้งเจ็ด", "ក្បាច់គែមទាំងប្រាំពីរ")}"></canvas></div></div>
</section>

<section class="sec" id="ikat">
<p class="kick">{te("Ikat", "มัดหมี่", "ចងជ្រលក់")}</p>
<h2>{te("Dye the picture into the thread", "ย้อมลายลงในเส้นด้าย", "ជ្រលក់ក្បាច់ចូលក្នុងអំបោះ")}</h2>
<p class="lede">{te("Ikat, from the Malay and Indonesian word for tie, dyes the pattern before weaving. Bundles of thread are bound tight where colour must stay out, dipped, untied, bound again and dipped again. In Cambodia the tying is chong kiet, “tying strings”, and the weft-ikat silk is hol; in Thailand it is mudmee, “tie the bundle”. Woven, each dyed thread lands a hair off its neighbour, and the edges feather.",
 "อิกัต มาจากคำมลายูและอินโดนีเซียที่แปลว่ามัด คือการย้อมลายก่อนทอ มัดปอยด้ายให้แน่นตรงที่ไม่ให้สีเข้า จุ่มย้อม แก้มัด มัดใหม่ แล้วย้อมอีก ในกัมพูชาเรียกการมัดว่า จองเกียต แปลว่า “มัดเชือก” และเรียกผ้าไหมมัดเส้นพุ่งว่าโฮล ในไทยเรียกว่ามัดหมี่ พอทอ เส้นที่ย้อมแล้วแต่ละเส้นเหลื่อมจากเส้นข้าง ๆ นิดหนึ่ง ขอบลายจึงฟุ้งเหมือนขนนก",
 "ពាក្យ អ៊ីកាត់ មកពីភាសាម៉ាឡេ និងឥណ្ឌូណេស៊ី មានន័យថា ចង។ គេជ្រលក់ក្បាច់មុនពេលត្បាញ៖ ចងបាច់អំបោះឱ្យណែននៅកន្លែងដែលមិនចង់ឱ្យពណ៌ចូល ជ្រលក់ ស្រាយ ចងម្តងទៀត ហើយជ្រលក់ម្តងទៀត។ នៅកម្ពុជា សូត្រចងអំបោះទទឹងហៅថា ហូល នៅថៃហៅថា ម៉ាត់មី។ ពេលត្បាញ អំបោះនីមួយៗរំកិលពីសរសៃជិតខាងបន្តិច គែមក្បាច់ក៏ព្រាលដូចរោមសត្វស្លាប។")}</p>
<div class="toy"><canvas id="ikat-cv" aria-label="{te("Tie, dye and weave", "มัด ย้อม ทอ", "ចង ជ្រលក់ ត្បាញ")}"></canvas>
<p class="out" id="ikat-cap"></p>
<div class="ctl"><button data-ikat="prev" aria-label="{te("back", "ย้อนกลับ", "ថយក្រោយ")}">◀</button><button data-ikat="play" aria-label="{te("play or pause", "เล่นหรือหยุด", "ចាក់ ឬផ្អាក")}">⏯</button><button data-ikat="next" aria-label="{te("next", "ถัดไป", "បន្ទាប់")}">▶</button>
<button data-ikat="cow">{te("Cow", "วัว", "គោ")}</button><button data-ikat="stars">{te("Stars and flowers", "ดาวกับดอกไม้", "ផ្កាយ និងផ្កា")}</button><button data-ikat="kou">{te("The word គោ", "คำว่า គោ", "ពាក្យ គោ")}</button>
<label><input id="ikat-fold" type="checkbox"> {te("tie it folded", "มัดตอนพับ", "ចងពេលបត់")}</label>
<label>{te("drift", "เหลื่อม", "រំកិល")} <input id="ikat-bleed" type="range" min="0" max="4" step="0.5" value="1.5"></label></div>
<p class="legend">{te("Weavers often tie a folded bundle once and get both halves of a mirrored pattern.", "ช่างทอมักมัดปอยที่พับไว้ครั้งเดียว ได้ลายสมมาตรทั้งสองซีก", "អ្នកត្បាញច្រើនចងបាច់ដែលបត់ម្តង ហើយបានក្បាច់ឆ្លុះទាំងសងខាង។")}</p></div>
</section>

<section class="sec" id="shawl">
<p class="kick">{te("Shawl", "ผ้าคลุมไหล่", "កន្សែង")}</p>
<h2>{te("NaN's shawl", "ผ้าคลุมไหล่ของแนน", "កន្សែងសូត្ររបស់ណាន")}</h2>
<p class="lede">{te("A Khmer silk hol, ikat through and through: every colour was tied and dyed into the weft before weaving. The silk has a shantung texture, the nubbly hand of thread with thick and thin places. On it: gold humped cattle, pink and teal flowers, and rows of woven Khmer letters; the gold word reads គោ, kou, “cow”. The redrawing is a plan of 72 × 104 squares. Pull drift to zero for the plan as it was tied; push it up for the tie-dye blur. Slubs adds the thick-and-thin thread.",
 "ผ้าโฮลไหมเขมร เป็นมัดหมี่ทั้งผืน ทุกสีมัดและย้อมลงในเส้นพุ่งก่อนทอ เนื้อไหมเป็นแบบซานตุง ผิวสัมผัสเป็นปุ่มปมจากเส้นด้ายที่มีช่วงหนาช่วงบาง บนผ้ามีวัวมีหนอกสีทอง ดอกไม้ชมพูกับเขียวหัวเป็ด และแถวอักษรเขมรที่ทอไว้ คำสีทองอ่านว่า គោ (โก) แปลว่า “วัว” ภาพวาดใหม่คือแบบขนาด 72 × 104 ช่อง เลื่อน “เหลื่อม” ไปที่ศูนย์ จะเห็นแบบตอนมัด เลื่อนขึ้นจะเห็นขอบฟุ้งของการมัดย้อม “ปุ่มปม” เพิ่มเส้นด้ายหนาบาง",
 "ហូលសូត្រខ្មែរ ជាក្រណាត់ចងជ្រលក់ទាំងស្រុង៖ ពណ៌នីមួយៗត្រូវបានចង និងជ្រលក់ចូលក្នុងអំបោះទទឹង មុនពេលត្បាញ។ សូត្រមានវាយនភាពដូចសានទុង គឺផ្ទៃរដុបៗពីអំបោះដែលមានកន្លែងក្រាស់ កន្លែងស្តើង។ លើក្រណាត់មាន គោមានបូកពណ៌មាស ផ្កាពណ៌ផ្កាឈូក និងបៃតងខៀវ និងជួរអក្សរខ្មែរដែលត្បាញ។ ពាក្យពណ៌មាសអានថា គោ។ រូបគូរថ្មីគឺជាប្លង់ 72 × 104 ក្រឡា។ ទាញ «រំកិល» ទៅសូន្យ ដើម្បីមើលប្លង់ពេលចង ទាញឡើង ដើម្បីមើលគែមព្រាលនៃការចងជ្រលក់។ «ក្រាស់ស្តើង» បន្ថែមអំបោះក្រាស់ស្តើង។")}</p>
<div class="toy"><div class="pair">
<figure><img src="{up}img/shawl.jpg" width="900" height="1199" loading="lazy" alt="{te("NaN's Khmer silk shawl: gold humped cattle on a dark ground, pink and teal flowers, rows of Khmer letters", "ผ้าไหมเขมรของแนน วัวสีทองบนพื้นเข้ม ดอกไม้ชมพูกับเขียว แถวอักษรเขมร", "កន្សែងសូត្រខ្មែររបស់ណាន៖ គោពណ៌មាសលើផ្ទៃពណ៌ចាស់ ផ្កាពណ៌ផ្កាឈូក និងបៃតង ជួរអក្សរខ្មែរ")}">
<figcaption>{te("Photo", "ภาพถ่าย", "រូបថត")} · NaN</figcaption></figure>
<figure><canvas id="shawl-draw" aria-label="{te("The shawl redrawn by arithmetic", "ผ้าผืนเดียวกัน วาดด้วยเลขคณิต", "កន្សែងដដែល គូរដោយលេខនព្វន្ត")}"></canvas>
<figcaption>{te("Drawn by arithmetic", "วาดด้วยเลขคณิต", "គូរដោយលេខនព្វន្ត")}</figcaption></figure></div>
<div class="ctl"><label>{te("drift", "เหลื่อม", "រំកិល")} <input id="shawl-bleed" type="range" min="0" max="4" step="0.25" value="1.5"></label>
<label>{te("slubs", "ปุ่มปม", "ក្រាស់ស្តើង")} <input id="shawl-slub" type="range" min="0" max="2" step="0.1" value="1"></label>
<label>{te("zoom", "ขยาย", "ពង្រីក")} <input id="shawl-zoom" type="range" min="2" max="12" step="1" value="5"></label></div></div>
</section>

<section class="sec" id="cambodia">
<p class="kick">{te("Cambodia", "กัมพูชา", "កម្ពុជា")}</p>
<h2>{te("Hol, pidan and golden silk", "โฮล ปิดาน และไหมทอง", "ហូល ពិដាន និងសូត្រមាស")}</h2>
<div class="cards">{cards(CAMBODIA)}</div>
</section>

<section class="sec" id="thailand">
<p class="kick">{te("Thailand", "ไทย", "ថៃ")}</p>
<h2>{te("Its own looms, its own names", "กี่ของตัวเอง ชื่อลายของตัวเอง", "កីរបស់ខ្លួន ឈ្មោះក្បាច់របស់ខ្លួន")}</h2>
<div class="cards">{cards(THAILAND)}</div>
</section>

<section class="sec" id="worm">
<p class="kick">{te("Silkworm", "หนอนไหม", "ដង្កូវនាង")}</p>
<h2>{te("One thread, in figure eights", "เส้นเดียว วนเป็นเลขแปด", "សរសៃតែមួយ ជារាងលេខប្រាំបី")}</h2>
<p class="lede">{te("Bombyx mori has lived with people for thousands of years and no longer lives wild. The caterpillar eats only mulberry leaves and grows about ten thousand times heavier in under a month. Then it spins for two or three days, swinging its head in figure eights, and lays down one unbroken thread, often around 900 m. Its moth cannot fly.",
 "หนอนไหม (Bombyx mori) อยู่กับมนุษย์มาหลายพันปี จนไม่มีในป่าแล้ว หนอนกินแต่ใบหม่อน และหนักขึ้นราวหนึ่งหมื่นเท่าในเวลาไม่ถึงเดือน จากนั้นชักใยสองถึงสามวัน ส่ายหัวเป็นเลขแปด วางเส้นใยเส้นเดียวไม่ขาด ยาวราว 900 เมตร ผีเสื้อไหมบินไม่ได้",
 "ដង្កូវនាង (Bombyx mori) រស់នៅជាមួយមនុស្សរាប់ពាន់ឆ្នាំ រហូតលែងមាននៅក្នុងព្រៃ។ វាស៊ីតែស្លឹកមន ហើយធ្ងន់ឡើងប្រហែលមួយម៉ឺនដង ក្នុងរយៈពេលមិនដល់មួយខែ។ បន្ទាប់មក វាបញ្ចេញសរសៃពីរបីថ្ងៃ ដោយគ្រវីក្បាលជារាងលេខប្រាំបី ហើយដាក់សរសៃតែមួយមិនដាច់ ជាញឹកញាប់ប្រហែល 900 ម៉ែត្រ។ មេអំបៅរបស់វាហើរមិនរួច។")}</p>
<div class="toy"><canvas id="cocoon" aria-label="{te("A cocoon being spun", "รังไหมกำลังถูกชักใย", "សំបុកដង្កូវនាងកំពុងបញ្ចេញសរសៃ")}"></canvas>
<p class="out" id="cocoon-m"></p>
<div class="ctl"><button data-cocoon="fast">{te("Finish it", "ข้ามไปจบ", "ទៅចប់")}</button><button data-cocoon="reel">{te("Reel it", "สาวไหม", "ទាញសរសៃ")}</button>
<button data-cocoon="gold">{te("Gold / white", "ทอง / ขาว", "មាស / ស")}</button><button data-cocoon="again">{te("Again", "ใหม่", "ម្តងទៀត")}</button></div></div>
<ul class="life">{life}</ul>
<p class="lede">{te("Thai and Khmer native silkworms are small breeds that spin gold cocoons and hatch several generations a year. Reeled by hand, their thread comes out thick and uneven.",
 "หนอนไหมพันธุ์พื้นบ้านไทยและเขมรตัวเล็ก ชักใยเป็นรังสีทอง และเลี้ยงได้หลายรุ่นต่อปี สาวด้วยมือ ได้เส้นไหมเส้นโตไม่สม่ำเสมอ",
 "ដង្កូវនាងពូជក្នុងស្រុកថៃ និងខ្មែរមានខ្លួនតូច បញ្ចេញសំបុកពណ៌មាស និងញាស់បានច្រើនជំនាន់ក្នុងមួយឆ្នាំ។ ទាញដោយដៃ បានសរសៃធំៗ មិនស្មើគ្នា។")}</p>
<p class="lede">{te("Chinese legend credits Leizu, wife of the Yellow Emperor, with finding silk when a cocoon fell into her tea and unravelled.",
 "ตำนานจีนเล่าว่า เหลยจู่ ชายาของจักรพรรดิเหลือง พบไหมเมื่อรังไหมตกลงในถ้วยชาแล้วคลายออกเป็นเส้น",
 "រឿងព្រេងចិនថា ឡីជូ ភរិយាអធិរាជលឿង បានរកឃើញសូត្រ ពេលសំបុកដង្កូវនាងធ្លាក់ចូលពែងតែរបស់នាង ហើយស្រាយចេញជាសរសៃ។")}</p>
</section>

<section class="sec" id="road">
<p class="kick">{te("Silk Road", "เส้นทางสายไหม", "ផ្លូវសូត្រ")}</p>
<h2>{te("Caravans west, ships through the south", "คาราวานไปตะวันตก เรือผ่านทางใต้", "ក្បួនអូដ្ឋទៅលិច នាវាកាត់ខាងត្បូង")}</h2>
<p class="lede">{te("Silk went west by caravan from Chang'an through the oasis towns, and by sea past the ports of Southeast Asia. Oc Eo, a Funan port in today's Mekong Delta, has given up Roman coins and Indian beads. The German geographer Ferdinand von Richthofen named the Silk Road in 1877. Around 552, monks carried silkworm eggs to Constantinople hidden in hollow canes, and Byzantium began making its own silk.",
 "ผ้าไหมเดินทางไปตะวันตกกับกองคาราวานจากฉางอาน ผ่านเมืองโอเอซิส และทางทะเลผ่านเมืองท่าของเอเชียตะวันออกเฉียงใต้ ออกแอว เมืองท่าของฟูนันในสามเหลี่ยมปากแม่น้ำโขงปัจจุบัน ขุดพบเหรียญโรมันและลูกปัดอินเดีย แฟร์ดีนันท์ ฟอน ริชท์โฮเฟิน นักภูมิศาสตร์ชาวเยอรมัน ตั้งชื่อเส้นทางสายไหมในปี 1877 ราวปี 552 นักบวชซ่อนไข่ไหมในไม้เท้ากลวงนำไปถึงคอนสแตนติโนเปิล ไบแซนไทน์จึงเริ่มผลิตไหมเอง",
 "សូត្របានធ្វើដំណើរទៅទិសខាងលិច តាមក្បួនអូដ្ឋពីឆាងអាន កាត់ទីក្រុងអូអាស៊ីស និងតាមសមុទ្រ កាត់កំពង់ផែនៃអាស៊ីអាគ្នេយ៍។ អូរកែវ កំពង់ផែនៃនគរហ្វូណន ក្នុងតំបន់ដីសណ្តទន្លេមេគង្គសព្វថ្ងៃ គេបានជីករកឃើញកាក់រ៉ូម៉ាំង និងអង្កាំឥណ្ឌា។ អ្នកភូមិសាស្ត្រអាល្លឺម៉ង់ ហ្វឺឌីណង់ ហ្វុន រីចថូហ្វេន បានដាក់ឈ្មោះផ្លូវសូត្រ ក្នុងឆ្នាំ 1877។ ប្រហែលឆ្នាំ 552 បព្វជិតបានលាក់ពងដង្កូវនាងក្នុងឈើច្រត់ប្រហោង យកទៅដល់កុងស្តង់ទីណូប្លឺ ហើយប៊ីហ្សង់ទីនចាប់ផ្តើមផលិតសូត្រខ្លួនឯង។")}</p>
<div class="toy"><canvas id="road-cv" aria-label="{te("Map of the Silk Road", "แผนที่เส้นทางสายไหม", "ផែនទីផ្លូវសូត្រ")}"></canvas>
<p class="out" id="road-out"></p>
<p class="legend">{te("Gold: the caravan road. Pale blue: the sea road. Pink: Chiang Mai.", "สีทอง: เส้นทางคาราวาน สีฟ้าอ่อน: เส้นทางทะเล สีชมพู: เชียงใหม่", "ពណ៌មាស៖ ផ្លូវក្បួនអូដ្ឋ។ ពណ៌ខៀវស្រាល៖ ផ្លូវសមុទ្រ។ ពណ៌ផ្កាឈូក៖ ឈៀងម៉ៃ។")}</p></div>
</section>

<section class="sec" id="draw">
<p class="kick">{te("Draw", "วาด", "គូរ")}</p>
<h2>{te("Draw with math", "วาดลายด้วยคณิต", "គូរក្បាច់ដោយគណិត")}</h2>
<p class="lede">{te("Each pattern is one formula over the grid of crossings, woven with the same drift as the ikat. Diamond measures distance the way a taxi drives a street grid. Naga folds the rows into zigzags. Pascal's triangle, kept only where it is odd, draws Sierpiński's triangle. Or type a name.",
 "แต่ละลายคือสูตรเดียวบนตารางจุดขัด ทอด้วยการเหลื่อมแบบเดียวกับมัดหมี่ ข้าวหลามตัดวัดระยะแบบรถแท็กซี่วิ่งตามถนนตาราง นาคพับแถวเป็นซิกแซก สามเหลี่ยมปาสกาลที่เก็บเฉพาะเลขคี่วาดเป็นสามเหลี่ยมเซียร์ปินสกี หรือพิมพ์ชื่อ",
 "ក្បាច់នីមួយៗគឺរូបមន្តតែមួយលើតារាងចំណុចឆ្លាស់ ត្បាញជាមួយការរំកិលដូចហូល។ ក្បាច់ពេជ្រវាស់ចម្ងាយតាមរបៀបតាក់ស៊ីបើកតាមផ្លូវជាការ៉ូ។ នាគបត់ជួរជាក្បាច់រលក។ ត្រីកោណប៉ាស្កាល់ដែលទុកតែលេខសេស គូរជាត្រីកោណស៊ែរពីនស្គី។ ឬវាយឈ្មោះ។")}</p>
<div class="toy"><canvas id="mcloth" aria-label="{te("Cloth drawn from a formula", "ผ้าที่วาดจากสูตร", "ក្រណាត់គូរពីរូបមន្ត")}"></canvas>
<div class="ctl"><select id="mc-f" aria-label="{te("formula", "สูตร", "រូបមន្ត")}">
<option value="diamond">{te("Diamond", "ข้าวหลามตัด", "ពេជ្រ")}</option><option value="naga">{te("Naga", "นาค", "នាគ")}</option>
<option value="rings">{te("Rings", "วงแหวน", "រង្វង់")}</option><option value="xor">XOR</option>
<option value="pascal">{te("Pascal, odd only", "ปาสกาล เฉพาะเลขคี่", "ប៉ាស្កាល់ តែលេខសេស")}</option><option value="name">{te("A name", "ชื่อ", "ឈ្មោះ")}</option></select>
<label hidden><input id="mc-name" type="text" maxlength="14" placeholder="{te("type a name", "พิมพ์ชื่อ", "វាយឈ្មោះ")}"></label>
<label>{te("size", "ขนาด", "ទំហំ")} <input id="mc-p" type="range" min="4" max="24" value="9"></label>
<label>{te("colours", "จำนวนสี", "ចំនួនពណ៌")} <input id="mc-k" type="range" min="2" max="6" value="4"></label>
<label>{te("drift", "เหลื่อม", "រំកិល")} <input id="mc-b" type="range" min="0" max="4" step="0.5" value="1"></label>
<button id="mc-pal">{te("Palette", "ชุดสี", "ពណ៌")}</button><button id="mc-save">{te("Save picture", "บันทึกภาพ", "រក្សាទុករូប")}</button></div></div>
</section>

<section class="sec" id="sources">
<p class="kick">{te("Sources", "แหล่งข้อมูล", "ប្រភព")}</p>
<ul class="sources">{srcs}</ul>
<p class="legend">{te("Map: Natural Earth. Photo of the shawl: NaN. Every cloth on this page is drawn in the browser by docs/weave.js.",
 "แผนที่: Natural Earth ภาพผ้าคลุมไหล่: แนน ผ้าทุกผืนบนหน้านี้วาดในเบราว์เซอร์ด้วย docs/weave.js",
 "ផែនទី៖ Natural Earth។ រូបថតកន្សែង៖ ណាន។ ក្រណាត់ទាំងអស់លើទំព័រនេះ គូរក្នុងកម្មវិធីរុករកដោយ docs/weave.js។")}</p>
</section>
</main>
<footer class="bot">{te("Text CC BY 4.0, NaNoBotCo. Code MIT.", "ข้อความ CC BY 4.0 NaNoBotCo โค้ด MIT", "អត្ថបទ CC BY 4.0 NaNoBotCo។ កូដ MIT។")} · <a href="https://github.com/NaNoBotCo/warp-and-weft">GitHub</a></footer>
<script src="{up}weave.js?v={VER}" defer></script><script src="{up}top.js" defer></script>
</body></html>
"""


ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#2e1c14"/>
<g stroke-width="3"><path d="M7 4v24M13 4v24M19 4v24M25 4v24" stroke="#17897f"/><path d="M4 9h24M4 16h24M4 23h24" stroke="#e9a53c"/></g></svg>
"""

LLMS = """# Warp and Weft · เส้นยืน เส้นพุ่ง · អំបោះបញ្ឈរ អំបោះទទឹង

> Silk, weaving and the arithmetic inside cloth, drawn in the browser. A loom weaves a Khmer silk hol (weft ikat, 1/2 twill: warp up where (warp + pick) mod 3 = 0) of gold humped cattle and the Khmer word គោ (cow) from a 72 × 104 plan, with per-pick misregistration giving the ikat blur. Toys: a four-shaft weaving draft (cloth[pick][warp] = tie-up[shaft(warp)][treadle(pick)]); tie-and-dye ikat in seven steps; the seven frieze groups (Conway's hop, step, sidle, spinning hop, spinning sidle, jump, spinning jump) from a drawable 7 × 7 motif; satin steps (k coprime to n, k not 1 or n-1; none exist for n = 4 or 6); formula cloth (taxicab diamond, naga zigzag, rings, xor, Pascal's triangle mod 2); a silkworm spinning in figure eights (about 900 m) and reeling; a Silk Road map with great-circle distances in camel days (30 km/day) and monsoon sea days (5 knots). Sections on Cambodian hol, pidan and golden silk, and on Thai mudmee, khit, jok, prae wa and the peacock silk marks. English, Thai and Khmer.

- [English](https://nanobotco.github.io/warp-and-weft/)
- [ไทย](https://nanobotco.github.io/warp-and-weft/th/)
- [ខ្មែរ](https://nanobotco.github.io/warp-and-weft/km/)
- Sections: #loom-sec #math #ikat #shawl #cambodia #thailand #worm #road #draw #sources
- Text CC BY 4.0, NaNoBotCo. Code MIT.
"""


def main():
    global L
    for L in LANGS:
        d = DOCS if L == "en" else os.path.join(DOCS, L)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page())
    open(os.path.join(DOCS, "icon.svg"), "w").write(ICON)
    open(os.path.join(DOCS, "llms.txt"), "w").write(LLMS)
    open(os.path.join(DOCS, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    urls = "".join(f'<url><loc>{SITE}{"" if k == "en" else k + "/"}</loc><lastmod>2026-09-30</lastmod>'
                   + "".join(f'<xhtml:link rel="alternate" hreflang="{o}" href="{SITE}{"" if o == "en" else o + "/"}"/>' for o in LANGS if o != k)
                   + "</url>\n" for k in LANGS)
    open(os.path.join(DOCS, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
    print("built", ", ".join(LANGS))


if __name__ == "__main__":
    main()
