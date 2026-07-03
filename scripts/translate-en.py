# -*- coding: utf-8 -*-
"""
scripts/translate-en.py

Generate EN translation scaffolding for each article.
Also updates master data.json with EN titles and corrects ZH subtitles (金句).
Supports both Volume 1 and Volume 2.
"""

import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK_DIR = os.path.join(ROOT, 'dist', 'book')

# ── Hand-crafted EN translations (Charles Lamb familiar essay style) ──

TRANSLATIONS = {
    '00-preface': {
        'title': 'Preface',
        'blocks': [
            {
                'type': 'text',
                'content': (
                    'I have often thought that there is no journey from which we are guaranteed to return—not the '
                    'great one we call Life, which begins with a cry and ends in silence, nor the smaller pilgrimages '
                    'we undertake between. From the first breath to the last, every road we travel is strewn with '
                    'frost and blossom alike, and the landscape, whether bleak or beautiful, is ours alone to behold.'
                )
            },
            {
                'type': 'text',
                'content': (
                    'The Master said, in that book of dialogues we call the Analects: "The wise take delight in water, '
                    'the benevolent in mountains. The wise are active, the benevolent still. The wise find joy, '
                    'and the benevolent endure." How true it is that a man of sense loves the hills and the waters, '
                    'loves Heaven itself, and in his gentleness finds both length of days and peace. For my part, '
                    'I have learned that to hear of a thing is one matter, but to see it—to let its form impress '
                    'itself upon the mind—is quite another.'
                )
            },
            {
                'type': 'text',
                'content': (
                    'It is only through travel that one may truly behold the wonders of the world, whether at home '
                    'or abroad—the exquisite scenery, the curious relics of antiquity, the strange and beautiful '
                    'shapes that Nature and Man together have wrought. The heart relaxes; the eye feasts; and the '
                    'soul, for a blessed interval, forgets its cares. The ancients had a saying: "Hear much, and '
                    'follow that which is good; see much, and keep it in remembrance." I take this as a gentle '
                    'injunction to step out of doors, to open one\'s eyes and ears, and to choose, from all that '
                    'presents itself, what is worth keeping.'
                )
            },
            {
                'type': 'text',
                'content': (
                    'Only when we have adjusted our minds to the proper contemplation of scenery—when we have '
                    'learned to be at once in the journey and of it—can we truly say that we have lived, and '
                    'felt, and enjoyed. The glory of life, methinks, lies in the travelling.'
                )
            },
            {
                'type': 'text',
                'content': (
                    'Goethe—that great German who understood these things better than most—once observed that '
                    'we love to travel not for the sake of arriving, but for the manifold pleasures of the road '
                    'itself. I confess I have found this to be true in my own humble case.'
                )
            },
            {
                'type': 'text',
                'content': (
                    'From the year 1980 to 2019, I have been a traveller upon this earth, and these pages are '
                    'the record of my wanderings.'
                )
            },
            {
                'type': 'text',
                'content': (
                    'The work is divided into two parts. The first, which I have called "To the World," gathers '
                    'my journeys abroad; the second, "Wanderings in the Divine Land," those within China. In each '
                    'I have followed, as best I could, the order of the years, setting down a brief account of '
                    'every country and city, every province and district, every road and prospect, every mountain '
                    'and stream—river, sea, lake, and all—and every temple or shrine that came within my view. '
                    'To these I have added my reflections and impressions, together with such pictures as seemed '
                    'to me worthy of preservation. The whole I have gathered into a single volume, entitled '
                    '"A Life Unfolded in Miles," in the hope that the reader, too, may find some share of the pleasure '
                    'that I have enjoyed along the way.'
                )
            },
            {
                'type': 'text',
                'content': (
                    'The collection is divided into two parts. The first, "To the World," chronicles my journeys abroad; '
                    'the second, "Wanderings in the Divine Land," those within China. Arranged in order of the years, '
                    'each entry offers a brief account of the cities and countries, provinces and districts, roads and '
                    'vistas, mountains and streams—rivers, seas, lakes, and all—and every temple or shrine that graced '
                    'my path, together with my reflections and impressions and such pictures as seemed worth preserving. '
                    'All these I have gathered into a single volume, "A Life Unfolded in Miles," that the reader too '
                    'may find some share of the pleasure I have enjoyed along the way.'
                )
            },
        ]
    },
    '01-taiwan': {
        'title': 'Wanderings in Taiwan',
        'subtitle': 'Six crossings of the Strait in search of old echoes; as many landings on that treasured isle to taste its hills and waters.',
        'subtitle_zh': '數渡海峽尋舊韻，幾登寶島嘗山河。',
        'blocks': [
            {'type': 'text', 'content': 'Part I: To the World'},
            {'type': 'text', 'content': 'A Journey to Taiwan — Wanderings in Taiwan'},
            {'type': 'text', 'content': (
                'How many times have I crossed that narrow Strait, seeking the echoes of an older time, '
                'and set foot upon that treasured isle—Formosa, as the Portuguese once called it, or simply '
                '"the Jewel"—to taste its hills and waters! From 1980 to 2010 I returned six times, a number '
                'that surprises even me. Taiwan is an island in the sea, and its cities seem to rise from the '
                'waves: Taipei, Taichung, Kaohsiung, Tainan—each a chapter in a long and pleasant story. '
                'The photographs I gathered over those years I have arranged into two collections.'
            )},
            {'type': 'text', 'content': (
                'The first album begins with Yangmingshan National Park, which lies hard by Taipei itself, '
                'a vast expanse of the Tatun Volcano Group covering some eleven thousand hectares. I visited '
                'it twice. On the first occasion, in March, the weather proved unkind: a chilling rain fell, '
                'the temperature dropped to ten degrees, and we were obliged to tour the park in raincoats, '
                'shivering yet determined. I remember thinking that there is a certain melancholy pleasure in '
                'seeing a famous landscape through a veil of cold rain.'
            )},
            {'type': 'text', 'content': (
                'At the park one finds a statue of the Ming philosopher Wang Yangming—after whom the mountain '
                'is named, for it was formerly called Grass Mountain. Then there is the celebrated Flower Clock, '
                'the great waterfall that calls to mind Li Bai\'s line about "three thousand feet of flying '
                'waterfall," and the cherry blossoms. Old Lao She once wrote: "Cherry blossoms in spring are '
                'as splendid as maple leaves in autumn; the tender green of early summer is threaded with '
                'deepest red." How true! There are also hot springs, gorges, forests, and a wealth of natural '
                'wonders to delight the eye.'
            )},
            {'type': 'text', 'content': 'Statue of Wang Yangming | Flower Clock | Waterfall | Cherry blossoms | Presidential Palace'},
            {'type': 'text', 'content': 'National Palace Museum | Chiang Kai-shek Memorial Hall | Taipei: ceremonial guards, Martyrs\' Shrine'},
            {'type': 'text', 'content': 'Taipei 101: soaring tower, its plaza and shopping arcade.'},
            {'type': 'text', 'content': 'Album Three: Chinese Folk Culture Village.'},
            {'type': 'text', 'content': (
                'Alishan lies seventy-five kilometres east of Chiayi, rising to 2,216 metres. Its wonders '
                'are five: sunrise, the sea of clouds, evening glow, the ancient forests, and the mountain '
                'railway. The sacred trees of Alishan—the Three Generations Tree, where a single root has '
                'sprung back to life after death, reborn again and again—stand in silent witness to the ages. '
                'Suspension bridges, the Sisters Lake, and a hundred other beauties make this a place to which '
                'all travellers aspire.'
            )},
            {'type': 'text', 'content': 'Welcome to Alishan | Three Generations, One Root | Crossing the Suspension Bridge'},
            {'type': 'text', 'content': 'Eternal Love Bridge | Alishan Forest Railway | Sunrise Trail to Zhushan'},
            {'type': 'text', 'content': 'Sisters Lake'},
            {'type': 'text', 'content': 'Yangmingshan Imperial Hot Spring | Beitou Geothermal Valley, Taipei'},
            {'type': 'text', 'content': 'Guanziling Hot Spring, Tainan'},
        ]
    },
    '02-philippines': {
        'title': 'The Philippine Isles: Dew and Frost',
        'subtitle': 'A son\'s journey to find his father, across decades and seas.',
        'blocks': [
            {'type': 'text', 'content': 'The Philippine Isles: Dew and Frost'},
            {'type': 'text', 'content': (
                'In the closing years of the nineteenth century, China was in turmoil. Foreign invaders pressed '
                'from without, misrule festered within, and the common people found no rest. It was to escape '
                'this chaos that my young father, following my revered uncle, left his native village and ventured '
                'across the sea—a perilous journey of a thousand miles—to seek a livelihood in the Philippines, '
                'that archipelago of seven thousand islands in Southeast Asia.'
            )},
            {'type': 'text', 'content': (
                'When at last I saw my father again, it was as though a lifetime had passed. Decades had not '
                'altered his native accent, nor diminished his fluent Chinese script, nor erased the cherished '
                'customs of our hometown. My children served as interpreters when I spoke with my Philippine relatives.'
            )},
            {'type': 'text', 'content': (
                'In September 1991, my eldest son accompanied me to the Philippines to see my father. Though '
                'I had never met my Philippine kin before, they received us with such warmth as moved me deeply.'
            )},
            {'type': 'text', 'content': (
                'In 1996, my wife and I, with our third son, made a second journey. This time we toured the '
                'islands\' famous sights: the Nayong Pilipino, the Enchanted Kingdom, the Manila Chinese Church, '
                'the Philippine Flower Exhibition, and the Pagsanjan Falls.'
            )},
            {'type': 'text', 'content': '【Nayong Pilipino — The Philippine Village】'},
            {'type': 'text', 'content': (
                'Nayong Pilipino, called the "Thousand Islands in Miniature," reflects the character of '
                'each Philippine province. Every garden showcases the native scenery and typical architecture '
                'of its region. It was a rare and precious thing to have my father with us there.'
            )},
            {'type': 'text', 'content': '【Enchanted Kingdom】'},
            {'type': 'text', 'content': (
                'My Filipino brother and his family took us to the Enchanted Kingdom, a grand amusement park. '
                'We rode an ox-cart through the grounds, admired a waterfall of several dozen metres.'
            )},
            {'type': 'text', 'content': '【Pagsanjan Falls】'},
            {'type': 'text', 'content': (
                'Pagsanjan Falls lies ninety-two kilometres south of Manila, its waterfall dropping some hundred '
                'metres, famous for thrilling boat rides. We were content to let the children play in the water '
                'and to enjoy a splendid lunch.'
            )},
            {'type': 'text', 'content': (
                'In January 2010, my wife and I, accompanied by our daughter, made a third visit.'
            )},
            {'type': 'text', 'content': '【Philippine Hilltop Park】'},
            {'type': 'text', 'content': (
                'My sister and my niece drove us to a hilltop park. We wandered among the hills and waters, '
                'and found happiness seeping into our very souls.'
            )},
            {'type': 'text', 'content': (
                'On 30 March 2010, word came that my father had passed away in the Philippines. '
                'My passport was not with me; I rushed back to Hong Kong to fetch it. Three airports in a '
                'single day—what a gruelling pilgrimage of love!'
            )},
            {'type': 'text', 'content': 'Dew and frost—the seasons of remembrance. We shall forever cherish our beloved father.'},
        ]
    },
    '03-kuala-lumpur': {
        'title': 'Cloud-Girt Genting, Twin Towers Aflame',
        'subtitle': 'A drive through the clouds to a mountain paradise, and twin towers piercing the sky.',
        'blocks': [
            {'type': 'text', 'content': 'Cloud-Girt Genting, Twin Towers Aflame'},
            {'type': 'text', 'content': 'We drove through the clouds, climbed to the summit, and beheld a fairyland.'},
            {'type': 'text', 'content': (
                'Genting Highlands is a place no visitor to Malaysia should miss. At an elevation of two thousand '
                'metres, it boasts a vast entertainment complex, grand hotels, and—most wondrous of all—a '
                'replica of the legendary Penglai Fairyland.'
            )},
            {'type': 'text', 'content': 'Genting Highlands Hotel | View from the Heights'},
            {'type': 'text', 'content': 'Penglai Fairyland at Genting | The Eight Immortals Crossing the Sea'},
            {'type': 'text', 'content': 'Petronas Twin Towers | Kuala Lumpur City Centre'},
        ]
    },
    '04-penang': {
        'title': 'A Kinsman\'s Journey to Penang',
        'subtitle': 'Travelling far to Penang for family ties, and wandering through ancient lanes to savour its charms.',
        'blocks': [
            {'type': 'text', 'content': 'A Kinsman\'s Journey to Penang'},
            {'type': 'text', 'content': 'I travelled far to Penang to renew family bonds, and roamed its ancient alleyways.'},
            {'type': 'text', 'content': (
                'Penang is one of the thirteen states of Malaysia, often called the "Oriental Garden." '
                'Here one finds the old alley where the film \'A Tale of Two Cities\' was shot, and the '
                'curious architectural wonder of houses-within-houses.'
            )},
            {'type': 'text', 'content': 'Unique Architecture | Penang City Centre | Penang City Nightscape'},
        ]
    },
    '05-vietnam': {
        'title': 'Starlit Seas: A Cruise to Vietnam',
        'subtitle': 'Riding the emerald waves beneath a starry sky, bound for the legendary bay of Ha Long.',
        'subtitle_zh': '山光明媚，水色秀麗。藍天綠島與碧海交織的人間美景。',
        'blocks': [
            {'type': 'text', 'content': 'Starlit Seas: A Cruise to Vietnam'},
            {'type': 'text', 'content': (
                'Vietnam lies on the eastern side of the Indochinese Peninsula. In 2001, my eldest son '
                'treated us to a voyage aboard the SuperStar Virgo, a colossal cruise liner bound for Ha Long Bay.'
            )},
            {'type': 'text', 'content': 'The SuperStar Virgo was then the largest cruise ship in Asia.'},
            {'type': 'text', 'content': 'Ha Long Bay — emerald islands against a sky of purest blue.'},
        ]
    },
    '06-korea': {
        'title': 'In the Footsteps of Dae Jang-geum: Korea\'s Charms',
        'subtitle': 'In search of the legendary physician\'s footsteps, roaming through Korea\'s ancient and modern wonders.',
        'blocks': [
            {'type': 'text', 'content': 'In the Footsteps of Dae Jang-geum'},
            {'type': 'text', 'content': (
                'The Republic of Korea lies on the southern half of the Korean Peninsula. Its capital is Seoul.'
            )},
            {'type': 'text', 'content': 'I went to Korea to find the filming locations of \'Dae Jang-geum.\''},
            {'type': 'text', 'content': 'Cheongwadae — The Blue House | Changdeokgung Palace | Seoul city scenes'},
        ]
    },
    '07-new-zealand': {
        'title': 'New Zealand: A Feast for the Eyes',
        'subtitle': 'A month of quiet contentment in Auckland, with wide-eyed wonder at its museums, temples, and curious local tales.',
        'blocks': [
            {'type': 'text', 'content': 'New Zealand: A Feast for the Eyes'},
            {'type': 'text', 'content': (
                'New Zealand lies in the southern Pacific Ocean, comprising two main islands. '
                'In January 2012, my wife and I travelled to Auckland to visit our third son and his family.'
            )},
            {'type': 'text', 'content': (
                'We stayed a month, living a quiet and contented life. Auckland is a coastal city '
                'consistently ranked among the world\'s most liveable cities.'
            )},
            {'type': 'text', 'content': 'Auckland War Memorial Museum | Sky Tower | Auckland Domain'},
            {'type': 'text', 'content': 'Fo Guang Shan Buddhist Temple | Chinese New Year Flower Market'},
        ]
    },
    '08-usa': {
        'title': 'Fair Sights, Soaring Spirits: Travels in America',
        'subtitle': 'Eighteen days across five great American cities, a family pilgrimage of pride and wonder.',
        'blocks': [
            {'type': 'text', 'content': 'Fair Sights, Soaring Spirits: Travels in America'},
            {'type': 'text', 'content': (
                'In 2017, my wife and I accompanied our eldest son and his family to the United States for '
                'our grandson\'s graduation from Davidson College. My son led our party on a grand tour of '
                'five great American cities: Chicago, Charlotte, Washington, Philadelphia, and New York.'
            )},
            {'type': 'text', 'content': 'It was a journey of eighteen days.'},
            {'type': 'text', 'content': '【Chicago】The Windy City on the shore of Lake Michigan.'},
            {'type': 'text', 'content': 'Cloud Gate — "The Bean," one of Chicago\'s most beloved landmarks.'},
            {'type': 'text', 'content': '【Charlotte】Attended our grandson\'s graduation from Davidson College.'},
            {'type': 'text', 'content': '【Washington, D.C.】The White House, Capitol Hill, Lincoln Memorial.'},
            {'type': 'text', 'content': '【New York】United Nations, Empire State Building, Wall Street, Columbia University.'},
        ]
    },
    '09-macau': {
        'title': 'Macau, Again and Again',
        'subtitle': 'Countless crossings of the Hong Kong-Zhuhai-Macau Bridge to a city of layered memories.',
        'blocks': [
            {'type': 'text', 'content': 'Macau, Again and Again'},
            {'type': 'text', 'content': (
                'Macau returned to Chinese sovereignty in December 1999. Since 2000, I have lost count of '
                'how many times I have crossed the Hong Kong–Zhuhai–Macau Bridge to this singular city.'
            )},
            {'type': 'text', 'content': 'Ruins of St. Paul\'s | A-Ma Temple | Hotel Lisboa | The Venetian Macau'},
        ]
    },
    '10-kinmen': {
        'title': 'Record of a Ramble in Kinmen',
        'subtitle': 'A thirty-minute ferry ride across the strait from Xiamen lands one in a different world.',
        'blocks': [
            {'type': 'text', 'content': 'Record of a Ramble in Kinmen'},
            {'type': 'text', 'content': (
                'Kinmen is an outlying island of Taiwan, known in ancient times as Wu-zhou. In 2017, '
                'my family and I took the passenger ferry from Xiamen, a mere thirty-minute crossing.'
            )},
            {'type': 'text', 'content': 'Juguang Tower | Kinmen National Park | Zhaishan Tunnel'},
        ]
    },
}

# ── Volume 2 EN titles and subtitles ──
V2_TRANSLATIONS = {
    'v2-01': {
        'title': 'Chronicles of the Capital',
        'subtitle': 'Many journeys to Beijing, the ancient capital, tracing its imperial past and modern pulse.',
    },
    'v2-02': {
        'title': 'Sketches of Shanghai',
        'subtitle': 'A ramble through the Eastern Metropolis, where the Huangpu River meets the world.',
    },
    'v2-03': {
        'title': 'Suzhou: Hills and Towns',
        'subtitle': 'Wandering through famous mountains and ancient canal towns of Suzhou.',
    },
    'v2-04': {
        'title': 'Hangzhou: A Thousand Years of Splendour',
        'subtitle': 'Exploring the timeless beauty of Hangzhou, from West Lake to its storied hills.',
    },
    'v2-05': {
        'title': 'Tianjin: The Portal of the North',
        'subtitle': 'A stroll through the old lanes and riverbanks of Tianjin.',
    },
    'v2-06': {
        'title': 'Sanya: Between the Mountains and the Sea',
        'subtitle': 'A southern sojourn to Sanya, where tropical seas embrace jade-green hills.',
    },
    'v2-07': {
        'title': 'Three Cities of Liaoning',
        'subtitle': 'Journeying through Dalian, Lushun, and Shenyang, where history meets the sea.',
    },
    'v2-08': {
        'title': 'Twin Cities of the North',
        'subtitle': 'Notes on Changchun and Jilin, two cities wrapped in northern snow and memory.',
    },
    'v2-09': {
        'title': 'Reflections on the Ice City',
        'subtitle': 'Leisurely thoughts from Harbin, the city of ice and Russian echoes.',
    },
    'v2-10': {
        'title': 'City of the Pearl River',
        'subtitle': 'Guangzhou: one river of pearl waters, ten thousand miles of flower city.',
    },
    'v2-11': {
        'title': 'Notes on Shenzhen',
        'subtitle': 'A visit to the soaring city built from a fishing village in a single generation.',
    },
    'v2-12': {
        'title': 'A Journey to Zhongshan',
        'subtitle': 'Travelling to the birthplace of Dr. Sun Yat-sen, amidst Lingnan charm.',
    },
    'v2-13': {
        'title': 'Zhuhai by the Sea',
        'subtitle': 'Notes from Zhuhai, a coastal garden city by the South China Sea.',
    },
    'v2-14': {
        'title': 'In Search of Amoy',
        'subtitle': 'Savoring the tastes and scenes of Xiamen, the Isle of Egrets.',
    },
    'v2-15': {
        'title': 'Cherishing Xiamen',
        'subtitle': 'Years of teaching in Xiamen, a city held dear in the heart.',
    },
    'v2-16': {
        'title': 'Nanping and Wuyi Mountain',
        'subtitle': 'A family visit to Nanping and a leisurely tour of the Wuyi Mountains.',
    },
    'v2-17': {
        'title': 'A Visit to Fujian Normal University',
        'subtitle': 'An academic journey to Fuzhou and the halls of Fujian Normal University.',
    },
    'v2-18': {
        'title': 'Zhangjiajie and Shaoshan',
        'subtitle': 'The hidden splendor of Zhangjiajie and a pilgrimage to the birthplace of a great man.',
    },
    'v2-19': {
        'title': 'A Journey to Guilin',
        'subtitle': 'Travelling through Guilin and Yangshuo, where the landscape is poetry in stone.',
    },
    'v2-20': {
        'title': 'Zhengzhou and Weihui',
        'subtitle': 'Visiting the ancient Shang capital and paying homage at a loyal minister\'s temple.',
    },
    'v2-21': {
        'title': 'Luoyang and Shangqiu',
        'subtitle': 'A dream of the River Luo, and half the history of Shangqiu in a single journey.',
    },
    'v2-22': {
        'title': 'Tulou and Yunshuiyao',
        'subtitle': 'A land of earthen fortresses and a ballad of clouds and water.',
    },
    'v2-23': {
        'title': 'The Charms of Zhangzhou',
        'subtitle': 'A city of warm character and abiding affection.',
    },
    'v2-24': {
        'title': 'The Eternal City of Quanzhou',
        'subtitle': 'Where Jin River flows through a thousand years, and the city carries ten thousand lands.',
    },
}

# ── Volume 3 EN titles and subtitles ──
V3_TRANSLATIONS = {
    'v3-01': {
        'title': 'Silver Hair, Lingering Grace in the Lion City',
        'subtitle': 'An elder traveller savours the sights and memories of Singapore.',
    },
    'v3-02': {
        'title': 'A Visit to the National University of Singapore',
        'subtitle': 'Wandering the halls of NUS, a bastion of learning in the tropics.',
    },
    'v3-03': {
        'title': 'Revisiting the Sights of Singapore Chinatown',
        'subtitle': 'A second tour through the bustling lanes and heritage of Chinatown.',
    },
    'v3-04': {
        'title': 'Jewel Changi: A Leisurely Note',
        'subtitle': 'Strolling through the shimmering wonder of Jewel Changi Airport.',
    },
    'v3-05': {
        'title': 'Admiring the Flora of Singapore',
        'subtitle': 'A feast of exotic flowers and rare trees in the Garden City.',
    },
    'v3-06': {
        'title': 'A Night at Chiayi Culture Road Night Market',
        'subtitle': 'The sounds, smells, and tastes of Chiayi after dark.',
    },
    'v3-07': {
        'title': 'Shadow Tower of Peach City, Under the Sun',
        'subtitle': 'The iconic tower of Chiayi and the legend of the sun-shooting hero.',
    },
    'v3-08': {
        'title': 'Classic Sights of Chiayi, Part One',
        'subtitle': 'A guided ramble through Chiayi\'s most treasured landmarks.',
    },
    'v3-09': {
        'title': 'Classic Sights of Chiayi, Part Two',
        'subtitle': 'Continuing the journey through Chiayi\'s scenic and historic spots.',
    },
    'v3-10': {
        'title': 'Exploring the Charm of Budai Harbour',
        'subtitle': 'A day at the fishing port of Budai, where sea and sky meet.',
    },
    'v3-11': {
        'title': 'An Evening Stroll by the Moonlit Bridge',
        'subtitle': 'The gentle grace of a bridge bathed in twilight and moonbeams.',
    },
    'v3-12': {
        'title': 'Moon Shadows on the Lake at Dusk',
        'subtitle': 'Reflections of the moon upon a tranquil lake at eventide.',
    },
    'v3-13': {
        'title': 'A Leisurely Walk Through Chiayi Mituo Night Market',
        'subtitle': 'A relaxed evening among the stalls and lights of Mituo Night Market.',
    },
    'v3-14': {
        'title': 'An Unforgettable New Year\'s Eve, 2023',
        'subtitle': 'Ringing in the new year with family, warmth, and fond memories.',
    },
    'v3-15': {
        'title': 'A New Year\'s Day Ramble in Chiayi',
        'subtitle': 'Welcoming the first day of the year with a gentle wander through the city.',
    },
    'v3-16': {
        'title': 'A Visit to National Chiayi University',
        'subtitle': 'A tour of the campus and its serene academic atmosphere.',
    },
    'v3-17': {
        'title': 'Ten Thousand at the Lakeview Fair: Chiayi Night Market',
        'subtitle': 'A bustling night market by the lake, alive with crowds and colour.',
    },
    'v3-18': {
        'title': 'Zhentian Temple and the Oath of the Peach Garden',
        'subtitle': 'Paying homage at a temple that honours the legendary brotherhood.',
    },
    'v3-19': {
        'title': 'Half a Day at Ziyun Temple, Bantianyan',
        'subtitle': 'A brief but memorable visit to the cliffside temple of Purple Clouds.',
    },
}

# Merge all volumes into TRANSLATIONS for lookup
ALL_TRANSLATIONS = {}
ALL_TRANSLATIONS.update(TRANSLATIONS)
ALL_TRANSLATIONS.update(V2_TRANSLATIONS)
ALL_TRANSLATIONS.update(V3_TRANSLATIONS)


def generate_en_article(article_id, zh_data, en_data):
    """Merge ZH blocks with EN translations to produce en-{id}.json"""
    en_blocks = []
    en_texts = [b for b in en_data['blocks'] if b['type'] == 'text'] if 'blocks' in en_data else []
    en_idx = 0

    for zh_block in zh_data['blocks']:
        if zh_block['type'] == 'image':
            en_blocks.append(dict(zh_block))
        elif zh_block['type'] == 'text' and en_idx < len(en_texts):
            en_blocks.append({
                'type': 'text',
                'content': en_texts[en_idx]['content'],
            })
            en_idx += 1
        else:
            en_blocks.append(dict(zh_block))

    en_article = {
        'id': article_id,
        'zh': zh_data['zh'],
        'en': en_data['title'],
        'author': zh_data.get('author', '林樺'),
        'author_en': 'Lin Hua',
        'blocks': en_blocks,
        'stats': zh_data.get('stats', {}),
    }

    return en_article, en_data.get('subtitle', '')


def create_v2_en_placeholder(article_id, zh_data, en_data):
    """Create a basic EN article JSON for V2 (no full block translation yet).
    Uses ZH blocks as placeholder."""
    en_article = {
        'id': article_id,
        'zh': zh_data['zh'],
        'en': en_data['title'],
        'author': zh_data.get('author', '林樺'),
        'author_en': 'Lin Hua',
        'blocks': zh_data['blocks'],
        'stats': zh_data.get('stats', {}),
    }

    return en_article, en_data.get('subtitle', '')


def update_master_en_info(book_dir):
    """patch data.json with EN titles so toc.js can show them"""
    data_path = os.path.join(book_dir, 'data.json')
    if not os.path.exists(data_path):
        print('  WARNING: data.json not found, skipping master update')
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        master = json.load(f)

    updated = 0
    for art in master['articles']:
        aid = art['id']
        if aid in ALL_TRANSLATIONS:
            art['en'] = ALL_TRANSLATIONS[aid]['title']
            updated += 1
            # Also update chapter articles
            for ch in master.get('chapters', []):
                for ca in ch.get('articles', []):
                    if ca['id'] == aid:
                        ca['en'] = ALL_TRANSLATIONS[aid]['title']
                        if 'subtitle' in ALL_TRANSLATIONS[aid]:
                            ca['en_subtitle'] = ALL_TRANSLATIONS[aid]['subtitle']

    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    print(f'  Updated {updated} EN titles in data.json')


def main():
    article_files = sorted([
        f for f in os.listdir(BOOK_DIR)
        if f.endswith('.json') and f != 'data.json' and not f.startswith('en-')
    ])

    print(f'Found {len(article_files)} articles for EN translation')

    for fname in article_files:
        article_id = os.path.splitext(fname)[0]
        zh_path = os.path.join(BOOK_DIR, fname)

        with open(zh_path, 'r', encoding='utf-8') as f:
            zh_data = json.load(f)

        if article_id in ALL_TRANSLATIONS:
            en_translation = ALL_TRANSLATIONS[article_id]

            # V1 articles have full block translations; V2/V3 only title/subtitle
            if 'blocks' in en_translation:
                en_data, en_sub = generate_en_article(article_id, zh_data, en_translation)
                en_path = os.path.join(BOOK_DIR, f'en-{article_id}.json')
                with open(en_path, 'w', encoding='utf-8') as f:
                    json.dump(en_data, f, ensure_ascii=False, indent=2)
                print(f'  ✓ en-{article_id}.json — {en_translation["title"]}')
            else:
                # V2/V3: only EN title available, no full translation yet
                en_sub = en_translation.get('subtitle', '')
                print(f'  - {article_id}: EN title only — {en_translation["title"]}')

            # Update zh_data EN title and subtitle
            zh_data['en'] = en_translation['title']
            if en_sub:
                zh_data['en_subtitle'] = en_sub[:60]
            # Also patch ZH subtitle (金句) if provided
            if 'subtitle_zh' in en_translation:
                zh_data['subtitle'] = en_translation['subtitle_zh'][:60]

            with open(zh_path, 'w', encoding='utf-8') as f:
                json.dump(zh_data, f, ensure_ascii=False, indent=2)

        else:
            print(f'  - {article_id}: translation pending')

    # Update master data.json with EN info
    update_master_en_info(BOOK_DIR)

    v1_count = len([k for k in TRANSLATIONS if k in ALL_TRANSLATIONS])
    v2_count = len([k for k in V2_TRANSLATIONS if k in ALL_TRANSLATIONS])
    v3_count = len([k for k in V3_TRANSLATIONS if k in ALL_TRANSLATIONS])
    print(f'\nDone. {v1_count} V1 + {v2_count} V2 + {v3_count} V3 articles with EN info.')


if __name__ == '__main__':
    main()
