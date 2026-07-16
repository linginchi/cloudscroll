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
        'blocks': [
            {'type': 'text', 'content': 'Part II: Journeys Across China'},
            {'type': 'text', 'content': 'A Journey to Beijing — Chronicles of the Capital'},
            {'type': 'text', 'content': (
                'Beijing is an ancient capital with a history spanning more than three thousand years. '
                'Known in olden times as Yanjing and Beiping, it is the capital of the People\'s Republic of China. '
                'Since the year 1992, I have made several journeys to this storied city of emperors.'
            )},
            {'type': 'text', 'content': (
                'Album the First: In 1992, I visited the Beijing Asian Games Village. From the 22nd of September '
                'to the 7th of October, 1990, Beijing played host to the 11th Asian Games — the first comprehensive '
                'international sporting event ever held on Chinese soil.'
            )},
            {'type': 'text', 'content': (
                'The Asian Games Village was built in 1990 to welcome the event. Housing the athletic delegations '
                'from every participating nation, it lies in the north-western quarter of Beijing\'s Chaoyang District.'
            )},
            {'type': 'text', 'content': (
                'Album the Second: 1992 — A tour of Beijing\'s celebrated landmarks: Tiananmen Square, the Chairman '
                'Mao Memorial Hall, the Great Hall of the People, the Monument to the People\'s Heroes, the National '
                'Museum of Chinese History, Zhongshan Park, the Meridian Gate, the Forbidden City\'s Hall of Supreme '
                'Harmony, Hall of Central Harmony, and Hall of Preserving Harmony, the Imperial Throne, Jingshan Park, '
                'Beihai Park, the Ming Tombs, Zhaoling, Ling\'en Hall, Dingling, the Badaling Great Wall, the Stone '
                'Buddha Temple, the Mongol Genghis Khan Palace, Peking University, and Tsinghua University.'
            )},
            {'type': 'text', 'content': (
                'Album the Third: 1992 — The Summer Palace: Hall of Benevolence and Longevity, Hall of Joyful Longevity, '
                'Yiyun Hall, the Grand Theatre of the Garden of Virtuous Harmony; Yonghe Lamasery: the Tower of '
                'Buddha\'s Fragrance, the Cloud-Dispelling Gate and Hall, Longevity Hill, Kunming Lake, and the '
                'Old Summer Palace.'
            )},
            {'type': 'text', 'content': (
                'Album the Fourth: 1992 — Yonghe Lamasery (the largest lamasery in Beijing), the Hall of Yongzheng, '
                'the Temple of Heaven, Fragrant Hills, and the Azure Cloud Temple where the coffin of Dr. Sun Yat-sen '
                'rested in the shrine of "Benevolent Repose and Quiet Radiance."'
            )},
            {'type': 'text', 'content': (
                'Album the Fifth: 2002 — A return to Beijing. I visited my eldest son\'s company, Beijing SMI, and '
                'strolled through the Oriental Plaza, Tiananmen Square, and the old Beijing Railway Station.'
            )},
            {'type': 'text', 'content': (
                'Album the Sixth: 2002 — The Chinese Ethnic Culture Park. A theme park fashioned in the architectural '
                'styles of China\'s many ethnic groups, with dwellings, temples, and plazas built after their various '
                'traditions. We wandered among them, savouring the distinctive flavours of each culture.'
            )},
            {'type': 'text', 'content': (
                'Album the Seventh: 2002 — The National Museum of Modern Chinese Literature, the National Library '
                'of China, and Renmin University. The Museum of Modern Chinese Literature, founded in 1985, serves '
                'as a centre for modern and contemporary Chinese literary archives, combining the functions of an '
                'exhibition hall, a literary library, a research institute, and a forum for cultural exchange. I had '
                'the honour of being photographed beside the effigies of several modern and contemporary writers.'
            )},
            {'type': 'text', 'content': (
                'Album the Eighth: 2002 — The Lugou Bridge (Marco Polo Bridge) and the China Film and Television '
                'City of CCTV. The Lugou Bridge, begun in 1189 and completed in 1192, is Beijing\'s oldest stone '
                'arch bridge, stretching 266.5 metres in length and 7.5 metres in width, with eleven arches and '
                '501 carved stone lions in every conceivable posture. "The Morning Moon over Lugou Bridge" is '
                'renowned as one of the Eight Great Sights of Yanjing.'
            )},
            {'type': 'text', 'content': (
                'Album the Ninth: 2002 — The Grand View Garden of "The Dream of the Red Chamber," originally '
                'named Fairyland of Penglai. Among its principal structures are the Grand View Tower, the Courtyard '
                'of Pleasant Red (the abode of Jia Baoyu), the Bamboo Lodge (where Lin Daiyu dwelt as a guest '
                'of the Rongguo Mansion), the Autumn Coolness Studio, the Pavilion of Green Drops, the Fairy Isle '
                'Pavilion on the lake, the Paddy-Sweet Village, the Mansion of Prince Gong, and the garden within '
                'the garden.'
            )},
            {'type': 'text', 'content': (
                'Album the Tenth: 2002 — A return to Yonghe Lamasery, the Imperial Academy, and the Confucian '
                'Temple, where we paid homage to the Greatest Sage and Model Teacher for Ten Thousand Ages.'
            )},
            {'type': 'text', 'content': (
                'The Imperial Academy, also called the Northern Directorate or the Northern Yong, was the supreme '
                'seat of learning (the Grand Academy) and the administrative organ of education under the Yuan, '
                'Ming, and Qing dynasties — the only fully preserved campus of an ancient supreme academy in China.'
            )},
            {'type': 'text', 'content': (
                'The Beijing Confucian Temple, also known as the Temple of the First Teacher, was begun in 1302 '
                'and completed in 1306, then rebuilt in 1411. It served the Yuan, Ming, and Qing courts as the '
                'ritual site for sacrifices to Confucius. A vast complex, approached in succession through the '
                'Gate of the First Teacher, the Gate of Great Achievement, the Hall of Great Achievement, the '
                'Gate of Veneration, and the Shrine of Veneration — all principal structures crowned with yellow '
                'glazed tiles.'
            )},
            {'type': 'text', 'content': (
                'Album the Eleventh: 2002 — A visit to Beihang University and the pleasures of Beijing\'s famed '
                'eating-houses: the Grand Mansion Restaurant and the Ditan Restaurant, both establishments of '
                'the highest elegance and considerable expense, offering performances of Peking opera, comic '
                'crosstalk, and the art of face-changing.'
            )},
        ]
    },
    'v2-02': {
        'title': 'Sketches of Shanghai',
        'subtitle': 'A ramble through the Eastern Metropolis, where the Huangpu River meets the world.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Shanghai — Sketches of Shanghai'},
            {'type': 'text', 'content': (
                'Shanghai: a national central city, China\'s hub of international economics, finance, trade, '
                'shipping, and technological innovation. Since 1992, I have made three journeys to this great '
                'eastern metropolis, to visit my kin and tour its celebrated sights.'
            )},
            {'type': 'text', 'content': (
                'Album the First: In 1992, travelling from Beijing to Shanghai, I had but three days before '
                'returning to Hong Kong. I explored the city centre and visited the Shanghai Maritime Academy.'
            )},
            {'type': 'text', 'content': (
                'Album the Second: In 2005, passing through Shanghai from Korea, again I had only three days. '
                'I wandered the city centre and the Bund.'
            )},
            {'type': 'text', 'content': (
                'Album the Third: 2005 — The ancient water-town of Zhujiajiao. Known as the Venice of Shanghai, '
                'it is the best-preserved Jiangnan water-town in the city. The scenery is enchanting, giving one '
                'a vivid sense of the old folk customs and manners of this ancient settlement.'
            )},
            {'type': 'text', 'content': (
                'Album the Fourth: 2012 — I journeyed to Shanghai to visit my two nephews and their families. '
                'My nephew drove us to see the Donghai Bridge, the Yangshan Deep-Water Port, the Shanghai '
                'Maritime Academy, and the Shanghai Maritime Museum.'
            )},
            {'type': 'text', 'content': (
                'Album the Fifth: 2012 — My nephew drove us to admire the famous Expo Park of Shanghai. '
                'The Shanghai World Expo 2010 (EXPO 2010) was the 41st World Expo, held from the 1st of May '
                'to the 31st of October, 2010. Though I was unable to photograph the national pavilions, '
                'I captured the vistas of the Expo grounds.'
            )},
        ]
    },
    'v2-03': {
        'title': 'Suzhou: Hills and Towns',
        'subtitle': 'Wandering through famous mountains and ancient canal towns of Suzhou.',
        'blocks': [
            {'type': 'text', 'content': 'A Tour of Suzhou — Suzhou: Hills and Towns'},
            {'type': 'text', 'content': (
                'In 1992, flying from Beijing to Suzhou, we joined relatives from Nanping to visit Suzhou\'s '
                'renowned sights: Tiger Hill and Hanshan Temple.'
            )},
            {'type': 'text', 'content': (
                'Tiger Hill boasts a history of over two-and-a-half millennia and enjoys the reputation of '
                '"the Foremost Sight in the Land of Wu." The Sword Pool is said to be the burial site of '
                'King Helü of Wu; the leaning pagoda is Asia\'s foremost leaning tower, inclining at an angle '
                'of three degrees and fifty-nine minutes.'
            )},
            {'type': 'text', 'content': (
                'Hanshan Temple — Cold Mountain Temple — sits by the ancient town of Fengqiao in Suzhou\'s '
                'Gusu district, beside the eastern bank of the Grand Canal. A celebrated千年古刹, it is '
                'one of China\'s ten great temples, first built during the Tianjian era of the Liang dynasty '
                '(A.D. 502–519). Originally named the Miaoli Puming Pagoda Cloister, it was later renamed '
                'after the Tang-dynasty monks Hanshan and Shide, who once dwelt within its walls.'
            )},
            {'type': 'text', 'content': (
                'Yixing: a land of ceramic art and tea culture, of purple-clay master-craftsmen, and of '
                'meditative reclusion amid hills and waters.'
            )},
        ]
    },
    'v2-04': {
        'title': 'Hangzhou: A Thousand Years of Splendour',
        'subtitle': 'Exploring the timeless beauty of Hangzhou, from West Lake to its storied hills.',
        'blocks': [
            {'type': 'text', 'content': 'A Trip to Hangzhou — Hangzhou: A Thousand Years of Splendour'},
            {'type': 'text', 'content': (
                'In 1992, we flew to Hangzhou. We visited the Temple of Prince Yue and savoured the '
                'celebrated beauties of West Lake.'
            )},
            {'type': 'text', 'content': (
                'The Temple of Prince Yue (also called Yue Fei Temple) rests at the southern foot of '
                'Qixia Ridge by West Lake. It is a combined shrine and tomb commemorating the Southern '
                'Song national hero Yue Fei. The temple was formally established in 1221, with three '
                'principal precincts — the Loyalty Shrine, the Shrine of Enlightened Loyalty, and the '
                'burial grounds — all surrounded by ancient trees in an atmosphere of solemn reverence.'
            )},
            {'type': 'text', 'content': (
                'West Lake has long been extolled as "Heaven on Earth." Su Shi\'s immortal couplet — '
                '"Would that I might compare West Lake to the Lady of the West, / Whether lightly painted '
                'or richly adorned, ever is she in harmony" — perfectly captures its beauty through the '
                'changing seasons.'
            )},
        ]
    },
    'v2-05': {
        'title': 'Tianjin: The Portal of the North',
        'subtitle': 'A stroll through the old lanes and riverbanks of Tianjin.',
        'blocks': [
            {'type': 'text', 'content': 'A Tour of Tianjin — Tianjin: The Portal of the North'},
            {'type': 'text', 'content': (
                'Jinmen Guli, the Ancient Cultural Street of Tianjin, is the birthplace of the city\'s '
                'urban culture. As the old saying goes, "First came the Temple of the Heavenly Queen; '
                'only then came the Garrison of Tianjin."'
            )},
            {'type': 'text', 'content': (
                'I had long heard that Jinmen Guli held within its lanes the full panoply of old Tianjin\'s '
                'folk customs and scenes. In 2002, my eldest son drove us specially from Beijing for a '
                'ramble through its antique market and city streets; we enjoyed a gastronomic excursion, '
                'repairing to a seaside quarter for a splendid lunch of the freshest seafood; then we sought '
                'out a branch of the Goubuli steamed-bun shop, a delicacy famed throughout the land, and '
                'tasted the celebrated Goubuli buns for ourselves.'
            )},
            {'type': 'text', 'content': (
                'Upon reaching the street\'s entrance, an antique archway of grey brick and flying eaves '
                'rose before our eyes, the four characters "Jinmen Guli" carved upon it with a rugged, '
                'time-worn dignity.'
            )},
        ]
    },
    'v2-06': {
        'title': 'Sanya: Between the Mountains and the Sea',
        'subtitle': 'A southern sojourn to Sanya, where tropical seas embrace jade-green hills.',
        'blocks': [
            {'type': 'text', 'content': 'Hainan and Sanya — Sanya: Between the Mountains and the Sea'},
            {'type': 'text', 'content': (
                'Sanya lies at the southernmost tip of Hainan Island. With its peerless seaside scenery, '
                'it has become China\'s most celebrated coastal resort, enjoying the epithet of "the '
                'Oriental Hawaii." In 2001, my eldest son invited us aboard the SuperStar Leo cruise liner '
                'to visit Hainan\'s Sanya and gaze upon the beauty of "Heaven\'s Edge and the Sea\'s Corner."'
            )},
            {'type': 'text', 'content': (
                'Treading the waves of Sanya, we drank in the scenery of the southern realm. We climbed '
                'the Deer\'s Turn-Around Point to behold the vast ocean, and strolled the Sanya Coconut '
                'Dream Corridor.'
            )},
        ]
    },
    'v2-07': {
        'title': 'Three Cities of Liaoning',
        'subtitle': 'Journeying through Dalian, Lushun, and Shenyang, where history meets the sea.',
        'blocks': [
            {'type': 'text', 'content': 'Three Cities of Liaoning'},
            {'type': 'text', 'content': (
                'From the 2nd to the 9th of January, 2003, I undertook a journey to behold the Harbin '
                'Ice Lantern Exposition, that annual spectacle of frozen artistry. Being still in hearty '
                'constitution, I resolutely joined a China Travel Service tour of the three provinces and '
                'six cities of the Northeast — Liaoning, Jilin, and Heilongjiang, with stops at Dalian, '
                'Lushun, Shenyang, Changchun, Jilin, and Harbin — a circuit of eight days. In temperatures '
                'ranging from twenty-six to thirty-two degrees below zero Celsius, I persevered in visiting '
                'the sights of all six cities, feasting my eyes upon the splendours of our ancestral land.'
            )},
            {'type': 'text', 'content': 'Dalian'},
            {'type': 'text', 'content': (
                'Dalian is a coastal city born of its port and thriving towards the sea — the open gateway '
                'of the Northeast economy and the most representative leisure city of the north.'
            )},
            {'type': 'text', 'content': (
                'Arriving in Dalian, the temperature stood at minus twenty-six degrees. I beheld snowfall '
                'for the first time in my life: flakes drifting down, the earth wrapped in silver and crystal, '
                'a vision of pure beauty. We visited the largest city square in Asia — Xinghai Square — '
                'explored the city centre, and dined at the famed Yuan Taizu Grill, where one roasts and '
                'stews at table.'
            )},
            {'type': 'text', 'content': 'Lushun'},
            {'type': 'text', 'content': (
                'Lushun, the port of Lushunkou, is a district under Dalian. Its naval harbour is one of '
                'the five great naval ports of the world. As the saying goes: "One mountain bears two '
                'seas; one port writes the annals of spring and autumn. A single Lushunkou holds half '
                'the modern history of China." It is a national scenic area, a nature reserve, a forest '
                'park, and an important base for patriotic education.'
            )},
            {'type': 'text', 'content': 'Shenyang'},
            {'type': 'text', 'content': (
                'Shenyang, also called Shengjing or Fengtian, is the capital of Liaoning province — an '
                'international metropolis of the Northeast, a city of historic and cultural renown, the '
                'transportation hub of the region, and the core of the national-level Shenyang metropolitan '
                'circle. It is celebrated under four grand epithets: the Cradle of a Dynasty, the City of '
                'Two Emperors, the Eldest Son of the Republic, and the Ruhr of the Orient. We toured its '
                'famous historical sites: the Imperial Palace, the Zhao Mausoleum, the North Mausoleum, '
                'and North Mausoleum Park. Even at twenty-nine degrees below zero, with snow mantling the '
                'trees, the park was thronged with visitors.'
            )},
        ]
    },
    'v2-08': {
        'title': 'Twin Cities of the North',
        'subtitle': 'Notes on Changchun and Jilin, two cities wrapped in northern snow and memory.',
        'blocks': [
            {'type': 'text', 'content': 'Jilin Province: Changchun and Jilin — Twin Cities of the North'},
            {'type': 'text', 'content': 'Changchun'},
            {'type': 'text', 'content': (
                'Changchun, also called the "Spring City of the North," is the capital of Jilin province, '
                'a sub-provincial city and one of the central hubs of Northeast China, as well as an '
                'important industrial base. We toured its sights: the Changchun Film Studio, where we '
                'watched a Manchu wedding performance; the Museum of the Puppet Imperial Palace; and '
                'the city centre.'
            )},
            {'type': 'text', 'content': 'Jilin'},
            {'type': 'text', 'content': (
                'Jilin is the only city in China that bears the same name as its province. A sub-centre '
                'city of the province, it enjoys the name of "the River City of the North" and possesses '
                'the character of a northern tourist city. We explored its famous historical sites, but '
                'what I recall most vividly is standing on the mountaintop ski slopes, where the mercury '
                'had plunged to thirty-two below zero — bitter cold indeed. To warm myself, I stepped into '
                'a snowboard hut and paid twenty yuan for a tiny cup of tea (dearly expensive, I thought, '
                'for the year 2003). I strolled across the bridge over the Songhua River, admiring the '
                'thousand intricate shapes of the rime ice, which lent the riverbanks a unique and haunting '
                'grace.'
            )},
        ]
    },
    'v2-09': {
        'title': 'Reflections on the Ice City',
        'subtitle': 'Leisurely thoughts from Harbin, the city of ice and Russian echoes.',
        'blocks': [
            {'type': 'text', 'content': 'Reflections on the Ice City'},
            {'type': 'text', 'content': 'Harbin'},
            {'type': 'text', 'content': (
                '"A thousand layers of snow upon the frozen Songhua River; / A single city of ice '
                'congealed beneath the northern sky."'
            )},
            {'type': 'text', 'content': (
                'Harbin, known also as the "Ice City of the North," is the capital of Heilongjiang '
                'province and a sub-provincial mega-city — the political, economic, cultural, and '
                'transportation centre of the northern Northeast. It has earned the monikers of the '
                'Ice City, the Moscow of the East, and the Paris of the Orient. It is an important '
                'national manufacturing base.'
            )},
            {'type': 'text', 'content': (
                'Harbin Ice and Snow World stages an ice-sculpture exhibition each year. No sooner '
                'had we set foot in Harbin than I felt, the body not yet moving while the heart had '
                'already flown ahead, an eager longing to see the exhibition and feast my eyes upon '
                'the thousand postures and myriad expressions of the frozen carvings.'
            )},
            {'type': 'text', 'content': (
                'Part the First: The scenery of Harbin — a tour of the Ice City\'s singular cityscape.'
            )},
            {'type': 'text', 'content': (
                'Part the Second: The Harbin Ice Sculpture Exhibition — beholding ice art in every '
                'conceivable form, each piece so lifelike as to seem alive.'
            )},
        ]
    },
    'v2-10': {
        'title': 'City of the Pearl River',
        'subtitle': 'Guangzhou: one river of pearl waters, ten thousand miles of flower city.',
        'blocks': [
            {'type': 'text', 'content': 'A Trip to Guangzhou — A River of Pearl Waters, a City of Ten Thousand Flowers'},
            {'type': 'text', 'content': (
                '"Five rams brought the auspicious grain, leaving behind a paradise; / Ten thousand '
                'travellers seek its fragrance, drawn ever to Guangzhou."'
            )},
            {'type': 'text', 'content': (
                'Guangzhou, capital of Guangdong province, abbreviated as "Sui" and also known as the '
                'City of Rams and the Flower City, is a national central city, one of the first batch '
                'of National Historic and Cultural Cities, the ancient merchant capital of a thousand '
                'years, and the eastern point of departure for the Maritime Silk Road. An international '
                'hub of commerce. Since 1998, I have journeyed to the Ram City several times.'
            )},
            {'type': 'text', 'content': (
                'In 1998 and 2000, I visited the Guangzhou Oriental Paradise.'
            )},
            {'type': 'text', 'content': (
                'In 2000, I toured the Baiyun Mountain Amusement Park.'
            )},
            {'type': 'text', 'content': (
                'In May 2019, my daughter brought us once more to Guangzhou for a three-day re-visit.'
            )},
            {'type': 'text', 'content': (
                'Part the First: Beijing Road — a thoroughfare in Guangzhou\'s Yuexiu District that '
                'combines culture, entertainment, and commerce. Situated in the heart of the city, '
                'it marks the very spot where Guangzhou first came into being. We strolled the '
                'pedestrian street, viewing the thousand-year-old building foundations spanning from '
                'the Song dynasty to the modern age, explored Shufang Street — the historic locus of '
                'editing, publishing, and distribution — and visited the Dafo Ancient Temple, built '
                'between A.D. 917 and 971.'
            )},
            {'type': 'text', 'content': (
                'Part the Second: Sun Yat-sen Memorial Hall — built with funds raised by the people '
                'of Guangzhou and overseas Chinese to honour Dr. Sun Yat-sen.'
            )},
            {'type': 'text', 'content': (
                'Part the Third: Chen Clan Academy — completed in 1894, built with funds contributed '
                'by members of the Chen clan from all seventy-two counties of Guangdong province. It '
                'served as temporary lodgings for young men of the Chen lineage who came to the provincial '
                'capital to sit for the imperial examinations, await official appointments, pay taxes, '
                'or conduct legal affairs.'
            )},
            {'type': 'text', 'content': (
                'Part the Fourth: Shamian — once called Shicuizhou, lying in the south-western quarter '
                'of the city. Originally an alluvial sandbank in the Pearl River, whence its name, it '
                'served throughout the Song, Yuan, Ming, and Qing dynasties as a vital trading port and '
                'place of resort. Today it remains an important commercial quay, preserving a century-old '
                'ensemble of exotic European-style buildings — churches, mansions, consulates — and its '
                'splendid First Street of Shamian.'
            )},
            {'type': 'text', 'content': (
                'Part the Fifth: Sacred Heart Cathedral — construction began in 1863 and was completed '
                'in 1888. The cathedral is a magnificent example of Gothic architecture, the largest '
                'all-Gothic structure in China and one of only four fully Gothic cathedrals in the world '
                '(the others being Notre-Dame de Paris, Cologne Cathedral, and Westminster Abbey).'
            )},
            {'type': 'text', 'content': (
                'Part the Sixth: Xiguan Charm — Xiguan, the old name for Guangzhou\'s Liwan District '
                'and the city\'s old quarter, is a place where gastronomy, local colour, and scenery '
                'come together.'
            )},
            {'type': 'text', 'content': (
                'Part the Seventh: Yuexiu Park — the largest comprehensive park in Guangzhou and the '
                'one richest in historical relics. Among its chief sights: the Sun Yat-sen Memorial '
                'Stele, the Hall where Dr. Sun read and governed, the Zhenhai Tower (Sea-Gazing Tower), '
                'the Ming-dynasty city wall, the Sifang Fort, the Five Rams Stone Sculpture (erected in '
                '1959), and the Seamen\'s Pavilion (built to commemorate the great Hong Kong seamen\'s '
                'strike). In 2019, I revisited Yuexiu Park.'
            )},
        ]
    },
    'v2-11': {
        'title': 'Notes on Shenzhen',
        'subtitle': 'A visit to the soaring city built from a fishing village in a single generation.',
        'blocks': [
            {'type': 'text', 'content': 'Notes on Shenzhen'},
            {'type': 'text', 'content': (
                '"With a seaside heart we roamed this land of wonders; / In the Peng City we gathered our '
                'sights and wrote our wanderings."'
            )},
            {'type': 'text', 'content': (
                'Shenzhen, also called Peng Cheng — the Roc City — is a sub-provincial city under '
                'Guangdong province, a Special Economic Zone, a national economic centre, and an '
                'international metropolis. Separated from Hong Kong by merely a single river, it has '
                'been the destination of several of my journeys since 1990.'
            )},
            {'type': 'text', 'content': (
                'Part the First: Splendid China — In 1990, my family and I rambled through Splendid '
                'China, also called the Land of Lilliputians, the world\'s largest and richest miniature '
                'scenic park. Eighty-three attractions in all, divided into three categories: ancient '
                'architecture, celebrated landscapes, and folk dwellings and customs.'
            )},
            {'type': 'text', 'content': (
                'Part the Second: Window of the World — In 1994, we visited Window of the World, '
                'gazing upon condensed versions of the earth\'s most famous landscapes and feasting on '
                'the wonders of the globe. The Eiffel Tower of Paris, completed in 1889, was then the '
                'tallest structure in the world at 320 metres.'
            )},
            {'type': 'text', 'content': (
                'Part the Third: Happy Valley — In August 2000, we revelled in Happy Valley, a modern '
                'Chinese theme park combining participation, spectacle, entertainment, and delight, '
                'built in 1998.'
            )},
            {'type': 'text', 'content': (
                'Part the Fourth: A return to Splendid China in 2001, revisiting the miniature scenic area.'
            )},
            {'type': 'text', 'content': (
                'Part the Fifth: A return to Window of the World in 2001, to see the night scenery '
                'of its new attractions.'
            )},
            {'type': 'text', 'content': (
                'Part the Sixth: A tour of the Peng City in November 2019, joining the Hong Kong '
                'Alumni Association of Five-Star Middle School for a group excursion to Shenzhen. '
                'Principal sights: Nan\'ao Bay, Dapeng Fortress, Hongfa Temple, and the Wenbo Palace.'
            )},
            {'type': 'text', 'content': (
                'Nan\'ao: a stroll along Shenzhen\'s Nan\'ao Bay, a hidden paradise embraced by romantic '
                'sentiment, tucked behind the dust and clamour of the metropolis.'
            )},
            {'type': 'text', 'content': (
                'Dapeng Fortress, fully titled the Dapeng Garrison Thousand-Household Fortress, was '
                'built in 1394. It served as a crucial Ming- and Qing-dynasty coastal defence bastion, '
                'revered as "the finest fortress along the coast." It was here that the Opium Wars had '
                'their origin, and it is from this very fort that Shenzhen derives its alternate name, '
                '"Peng Cheng." We wandered through the ancient lanes of the Dapeng Fortress.'
            )},
            {'type': 'text', 'content': (
                'Hongfa Temple lies within the Xianhu Botanical Garden.'
            )},
            {'type': 'text', 'content': (
                'The Wenbo Palace is the only building complex in China that integrates the '
                'architectural styles of seven historical dynasties into a single structure.'
            )},
        ]
    },
    'v2-12': {
        'title': 'A Journey to Zhongshan',
        'subtitle': 'Travelling to the birthplace of Dr. Sun Yat-sen, amidst Lingnan charm.',
        'blocks': [
            {'type': 'text', 'content': 'A Tour of Zhongshan — A Journey to Zhongshan'},
            {'type': 'text', 'content': (
                '"A hundred years have passed, and Fragrant Hill still holds the memory of greatness; '
                '/ A river of jade-green waters encircles this city of renown."'
            )},
            {'type': 'text', 'content': (
                'Zhongshan, anciently called Xiangshan — Fragrant Hill — and also known as the Ancient '
                'Town of Zhongshan, is a prefecture-level city under Guangdong province. It is the '
                'birthplace of that great man, Dr. Sun Yat-sen. In 1998, I journeyed to this ancient '
                'town to visit the Sun Yat-sen Former Residence, the Sun Yat-sen Memorial Hall, the '
                'Zhongshan Zhan Garden, the Sunwen Memorial Park, and the scenery of the old town itself.'
            )},
        ]
    },
    'v2-13': {
        'title': 'Zhuhai by the Sea',
        'subtitle': 'Notes from Zhuhai, a coastal garden city by the South China Sea.',
        'blocks': [
            {'type': 'text', 'content': 'A Tour of Zhuhai — Zhuhai by the Sea'},
            {'type': 'text', 'content': (
                'Zhuhai is one of China\'s five Special Economic Zones. With its lovely environment, '
                'clear hills and lucid waters, and a vast maritime domain boasting more than a hundred '
                'islands, it has earned the epithet of "the City of a Hundred Isles." In 1998, I visited '
                'the New Yuanming Palace and the Nanhai Guanyin Temple.'
            )},
        ]
    },
    'v2-14': {
        'title': 'In Search of Amoy',
        'subtitle': 'Savoring the tastes and scenes of Xiamen, the Isle of Egrets.',
        'blocks': [
            {'type': 'text', 'content': 'Records of Xiamen — In Search of Amoy'},
            {'type': 'text', 'content': (
                'Xiamen, also called Amoy or the Isle of Egrets, is a sub-provincial city in Fujian '
                'province — one of China\'s earliest Special Economic Zones, a pivotal port along the '
                'south-eastern coast, and a city of international scenic tourism.'
            )},
            {'type': 'text', 'content': (
                'I. Jimei Ao Garden: Adjacent to Jimei Middle School, Ao Garden was built to '
                'commemorate the great patriotic overseas Chinese leader, Mr. Chen Jiageng.'
            )},
            {'type': 'text', 'content': 'II. Xiamen University and Nanputuo Temple:'},
            {'type': 'text', 'content': (
                'Xiamen University: My family and I frequently visited the university to call upon '
                'my cousin and his family. My cousin served as the Party secretary of the Chinese '
                'Department. In the year 2000, I went to Xiamen University to visit him and his wife.'
            )},
            {'type': 'text', 'content': (
                'Nanputuo Temple: Nestled beside Xiamen University, facing the sparkling harbour, '
                'the temple traces its origins to the late Tang dynasty. Rebuilt several times from '
                'the Ming through the Qing, it came to be called Nanputuo — "Southern Putuo" — for '
                'its location south of Mount Putuo. It remains one of the sacred Buddhist sites of '
                'southern Fujian.'
            )},
            {'type': 'text', 'content': 'III. The Xiamen Taiwan Folk Culture Village, visited in October 2001.'},
            {'type': 'text', 'content': 'IV. The Yuanbo Garden — Xiamen Horticultural Expo Garden, visited in February 2008.'},
            {'type': 'text', 'content': (
                'V. Gulangyu Islet — I have set foot on Gulangyu many times. In November 2018, I '
                'accompanied relatives from Singapore, the Philippines, Taiwan, and Xiamen on a return '
                'visit to this charmed isle.'
            )},
        ]
    },
    'v2-15': {
        'title': 'Cherishing Xiamen',
        'subtitle': 'Years of teaching in Xiamen, a city held dear in the heart.',
        'blocks': [
            {'type': 'text', 'content': 'Teaching Years and Cherished Memories of Xiamen'},
            {'type': 'text', 'content': (
                '"The scholar\'s altar keeps our passing years; / The Isle of Egrets entwines our hearts."'
            )},
            {'type': 'text', 'content': (
                'I taught at Xiamen Jimei Middle School, its branch school, and Xiamen No. 10 Middle '
                'School for over two decades. In the early 1970s, I was transferred from the Quanzhou '
                'area (Jinjiang) to Xiamen, where I spent twenty years upon the teaching dais. '
                '"Twenty autumns of sowing upon the rostrum, my heart tethered to the thriving culture '
                'of the Egret Isle; a thousand vistas of the surging sea, my affection bound to the '
                'hills and waters of Xiamen."'
            )},
            {'type': 'text', 'content': (
                'I. Jimei Middle School: In the early 1970s, I taught at Jimei Middle School.'
            )},
            {'type': 'text', 'content': (
                'II. Jimei Ao Garden (Jiageng Park): Lying near Jimei Middle School, it was built to '
                'commemorate the great patriotic overseas Chinese leader Mr. Chen Jiageng.'
            )},
            {'type': 'text', 'content': (
                'III. The first alumni-teacher reunion. Twenty-two years after teachers and students '
                'had parted from their alma mater, a grand reunion was held on the 1st and 2nd of '
                'October, 2001, at Xiamen No. 10 Middle School. Over two hundred teachers and students '
                'from overseas and across the provinces gathered for this long-awaited affair.'
            )},
            {'type': 'text', 'content': (
                'In the evening, a festive banquet was held at the Comfort Hotel in Xinglin. The day '
                'happened to coincide with the Mid-Autumn Festival, and all present indulged in the '
                'traditional game of "hitting the champion\'s cake."'
            )},
            {'type': 'text', 'content': (
                'IV. The second alumni-teacher reunion: From the 3rd to the 5th of July, 2009, a '
                'second reunion was convened, marking the thirtieth anniversary. "Long parted, now '
                'met again in joy; we set the feast beneath the arbour." Over two hundred teachers '
                'and students gathered once more. To commemorate the occasion, a memorial volume was printed.'
            )},
        ]
    },
    'v2-16': {
        'title': 'Nanping and Wuyi Mountain',
        'subtitle': 'A family visit to Nanping and a leisurely tour of the Wuyi Mountains.',
        'blocks': [
            {'type': 'text', 'content': 'Nanping and Wuyi Mountain — A Family Visit and a Mountain Ramble'},
            {'type': 'text', 'content': (
                'Nanping, commonly called Northern Fujian, lies at the junction of Fujian, Zhejiang, '
                'and Jiangxi — the source of the Min River and the largest prefecture-level city in '
                'the province. In October 2014, I travelled there to visit relatives at the Fujian '
                'Forestry Vocational Technical School.'
            )},
            {'type': 'text', 'content': (
                'In November 2018, I returned to Nanping to visit my sixth elder sister, then in her '
                'advanced years, and her family, whose household had been honoured with the title of '
                '"Outstanding Educational Family."'
            )},
            {'type': 'text', 'content': 'Wuyi Mountain'},
            {'type': 'text', 'content': (
                'The poet Zhu Xi wrote: "Upon Wuyi Mountain dwell immortal spirits; / Below, the cold, '
                'clear streams wind bend by bend." And the old saying: "Guilin\'s landscape is the '
                'finest under heaven, yet it cannot match a single hill of Wuyi."'
            )},
            {'type': 'text', 'content': (
                'In October 2014, I revelled in the beauties of Wuyi Mountain — acclaimed as Fujian\'s '
                'foremost mountain and a classic example of Danxia landform. It is the birthplace of '
                'the world-renowned Dahongpao tea.'
            )},
        ]
    },
    'v2-17': {
        'title': 'A Visit to Fujian Normal University',
        'subtitle': 'An academic journey to Fuzhou and the halls of Fujian Normal University.',
        'blocks': [
            {'type': 'text', 'content': 'Fujian Normal University — A Scholarly Visit'},
            {'type': 'text', 'content': (
                '"A hundred years have built its way of teaching; / A single campus brims with the '
                'fragrance of books."'
            )},
            {'type': 'text', 'content': (
                'Fujian Normal University has since ancient times enjoyed the epithet of "the Zou '
                'and Lu by the Sea" — a cradle of culture. It is one of the earliest-established '
                'century-old normal universities in the country. I strolled through the Youxuan '
                'Hall, quietly savouring the bookish radiance of the university, breathing in the '
                'fragrance of learning that fills its campus.'
            )},
            {'type': 'text', 'content': (
                'In October 2014, I travelled to Fujian Normal University in Fuzhou to visit my '
                'niece, who is a post-doctoral fellow and professor there.'
            )},
            {'type': 'text', 'content': (
                'Impressions: "Idly visiting the sacred halls of learning in the Fujian capital, / '
                'Where banner-like hills and misty groves bask in the spring breeze. / A lecture hall '
                'of knowledge passes on the Confucian line, / While ten thousand trees of peach and '
                'plum flourish in abundant green."'
            )},
        ]
    },
    'v2-18': {
        'title': 'Zhangjiajie and Shaoshan',
        'subtitle': 'The hidden splendour of Zhangjiajie and a pilgrimage to the birthplace of a great man.',
        'blocks': [
            {'type': 'text', 'content': 'Hunan — Zhangjiajie and Shaoshan'},
            {'type': 'text', 'content': (
                'Zhangjiajie lies in the heart of the Wuling Mountains in north-western Hunan. It is '
                'China\'s first national forest park and the global type locality for the unique '
                '"Zhangjiajie landform." In May 2015, I joined a tour organized by the Hong Kong '
                'Neikeng Town Fellowship Association to visit Zhangjiajie, the Mao Zedong Former '
                'Residence in Shaoshan, and Mao Zedong Square.'
            )},
            {'type': 'text', 'content': (
                'Zhangjiajie\'s principal sights: the National Forest Park, Suoxiyu, Tianzi Mountain, '
                'and the Grand Canyon.'
            )},
            {'type': 'text', 'content': 'The Ancient Town of Fenghuang (Phoenix).'},
            {'type': 'text', 'content': (
                '"Green tiles and yellow earth by a shallow pond — / From this corner of Hunan the '
                'hero strode forth. / A single dwelling holds the resolve of a thousand autumns, / '
                'And in its wake, the land and rivers flourish under a prosperous peace."'
            )},
            {'type': 'text', 'content': (
                '"Beneath the red sun of Shaoshan, the bronze statue gleams; / Ten thousand people '
                'bow in reverence to the great light. / A single volume of history opens the ancient '
                'nation; / A thousand autumns of merit are inscribed upon the glorious page."'
            )},
        ]
    },
    'v2-19': {
        'title': 'A Journey to Guilin',
        'subtitle': 'Travelling through Guilin and Yangshuo, where the landscape is poetry in stone.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Guilin'},
            {'type': 'text', 'content': (
                '"Guilin\'s landscape is the finest under heaven; / Its jade-green hills and gauzy '
                'mists invite contemplation."'
            )},
            {'type': 'text', 'content': (
                'Guilin is one of China\'s most celebrated scenic and historic cultural cities, '
                'enjoying the world-famous reputation of possessing the finest landscape beneath '
                'the heavens. Here the mountains rise abruptly from the plains in a thousand fantastical '
                'shapes; the waters of the Li River wind gracefully, as clear and smooth as a mirror; '
                'the hills are riddled with caves of mysterious beauty; and within those caves, '
                'strangely wrought stones bear the signature of nature\'s own cunning hand.'
            )},
            {'type': 'text', 'content': (
                'In April 2016, I joined a group tour to Guilin. After the journey, I wrote an essay '
                'entitled "A Tour of Guilin in the Locust-Blossom April."'
            )},
        ]
    },
    'v2-20': {
        'title': 'Zhengzhou and Weihui',
        'subtitle': 'Visiting the ancient Shang capital and paying homage at a loyal minister\'s temple.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Zhengzhou and Weihui'},
            {'type': 'text', 'content': (
                'Zhengzhou, anciently called the Shang Capital, is the capital of Henan province '
                'and the core city of the Central Plains.'
            )},
            {'type': 'text', 'content': (
                'On the fourth day of the fourth lunar month in 2016, marking the 3,108th anniversary '
                'of the birth of Bi Gan, the progenitor of the Lin clan, I joined a delegation to pay '
                'homage at the Bi Gan Temple in Weihui, and to tour Kaifeng, the Iron Pagoda Park, '
                'the Qingming Riverside Landscape Garden, Wanxian Mountain, and the Yandi Square by '
                'the Yellow River. In May 2018, I made a second journey.'
            )},
            {'type': 'text', 'content': (
                'I. Paying Homage at the Weihui Bi Gan Temple: The Hong Kong delegation was warmly '
                'welcomed by the local leaders. A solemn ceremony was held in the great hall of the '
                'temple to pay homage to Bi Gan, Grand Preceptor of the Yin dynasty and Loyal Duke.'
            )},
            {'type': 'text', 'content': (
                'II. The Kaifeng Prefecture Temple of Lord Bao — paying respects to the incorruptible '
                'judge Bao Zheng. Entering the Hall of Impartial Justice, we reverently bowed before '
                'the sacred image of Lord Bao, expressing our boundless admiration for this resolute '
                'man who feared no power and upheld justice for the common people, earning the '
                'reverence and love of generations.'
            )},
            {'type': 'text', 'content': (
                '"With an iron countenance he astonished both gods and ghosts; with a pure heart he '
                'governed the world. Even now he stands unafraid of the mighty, enforcing the law as '
                'unshakeable as the mountain. His integrity wins praise through the ages; his justice '
                'has won the people\'s hearts. A generation\'s merit spreads across the world; a '
                'thousand autumns\' legacy lives on among us."'
            )},
            {'type': 'text', 'content': (
                'III. The Iron Pagoda Park — beholding the world\'s foremost pagoda, nearly a thousand '
                'years old, built of brown glazed bricks that resemble iron, standing majestically '
                'at over fifty-five metres in height.'
            )},
            {'type': 'text', 'content': (
                'IV. The Qingming Riverside Landscape Garden: "With a single step one enters the '
                'scroll, and in a single day one dreams one\'s way back through a thousand years."'
            )},
            {'type': 'text', 'content': (
                'V. Wanxian Mountain and the Guo Liang Village. VI. The Yellow River Scenic Area and '
                'Yandi Square, where the grand statues of the sage-emperors face the Yellow River.'
            )},
        ]
    },
    'v2-21': {
        'title': 'Luoyang and Shangqiu',
        'subtitle': 'A dream of the River Luo, and half the history of Shangqiu in a single journey.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Henan — Luoyang and Shangqiu'},
            {'type': 'text', 'content': (
                'Luoyang lies by the River Luo in western Henan, a vital cradle of Chinese civilisation, '
                'celebrated as "the ancient capital of thirteen dynasties."'
            )},
            {'type': 'text', 'content': (
                'In May 2018, flying from Hong Kong to Zhengzhou, we toured Luoyang\'s Longmen Grottoes, '
                'the Guanlin Temple, and the White Horse Temple; joined the global commemoration of '
                'the 3,110th anniversary of Bi Gan\'s birth; paid homage to the Lin clan\'s founding '
                'ancestor Lin Jian at the Changlin Stone Chamber; and visited the Shuangzhong Temple '
                'in Shangqiu.'
            )},
            {'type': 'text', 'content': (
                'The Longmen Grottoes: the world\'s most extensive repository of stone carving art, '
                'designated by UNESCO as the pinnacle of Chinese stone carving.'
            )},
            {'type': 'text', 'content': (
                'The White Horse Temple: China\'s first ancient Buddhist monastery, founded in A.D. 68, '
                'the very first government-built temple after Buddhism entered China.'
            )},
            {'type': 'text', 'content': (
                'The Changlin Stone Chamber in Wolong Town — the birthplace of Lin Jian, founding '
                'ancestor of the Lin clan, known as the "Cavern of the Lin Origins."'
            )},
            {'type': 'text', 'content': (
                'The Shuangzhong Temple in Shangqiu honours Zhang Xun and Xu Yuan, the two loyal '
                'ministers who gave their lives suppressing the An Lushan rebellion in A.D. 757.'
            )},
        ]
    },
    'v2-22': {
        'title': 'Tulou and Yunshuiyao',
        'subtitle': 'A land of earthen fortresses and a ballad of clouds and water.',
        'blocks': [
            {'type': 'text', 'content': 'A Land of Yunshui Ballads and Ten Thousand Tulou'},
            {'type': 'text', 'content': (
                'Yongding is the ancestral home of Hakka earthen buildings, celebrated as the "Eastern '
                'Fortresses." Over twenty-three thousand tulou stand within the district — a unique '
                'architectural model that is singular in the whole world.'
            )},
            {'type': 'text', 'content': (
                'In June 2017, I toured the Yongding Tulou, marvelling at their ancient history, '
                'distinctive style, and imposing scale. Among them, the Chengqi Lou is revered as '
                'the King of Tulou.'
            )},
            {'type': 'text', 'content': (
                'The Nanjing Yunshuiyao Ancient Town: blessed with beautiful mountains and rich '
                'cultural heritage — a five-kilometre ancient post road, thousand-year-old banyan '
                'trees, and a claim to "the most marvellous building under heaven."'
            )},
        ]
    },
    'v2-23': {
        'title': 'The Charms of Zhangzhou',
        'subtitle': 'A city of warm character and abiding affection.',
        'blocks': [
            {'type': 'text', 'content': 'A City of Local Delights, a Heart Full of Warmth'},
            {'type': 'text', 'content': (
                'Zhangzhou lies at the southern end of Fujian — a National Historic and Cultural City '
                'long celebrated as the "Zou and Lu by the Sea," a city of flowers and fruit, a land '
                'of fish and rice. Its ancient quarter is a living palimpsest: Tang and Song city '
                'walls, Ming and Qing streets, Republican-era character, and southern Fujian charm.'
            )},
            {'type': 'text', 'content': (
                'In March 2019, I visited relatives and revisited the beautiful old town — its '
                'Tang-Song cityscape, the Lin Clan Ancestral Hall, the Bi Gan Temple, and the '
                'Confucian Temple.'
            )},
            {'type': 'text', 'content': (
                'Quanzhou: historically the port from which the ancient Maritime Silk Road set sail. '
                'Kaiyuan Temple, the largest Buddhist monastery in Fujian, founded in A.D. 686, is '
                'graced by its twin pagodas. Qingyuan Mountain is most famous for its Song-dynasty '
                'stone sculpture of Laozi — the largest Daoist stone carving in all of China.'
            )},
        ]
    },
    'v2-24': {
        'title': 'The Eternal City of Quanzhou',
        'subtitle': 'Where Jin River flows through a thousand years, and the city carries ten thousand lands.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Quanzhou'},
            {'type': 'text', 'content': (
                'Quanzhou, also known as the City of Carp and the City of Thorny Paulownia, lies '
                'on the south-eastern coast of Fujian. A celebrated ancestral homeland of overseas '
                'Chinese, Quanzhou was the historic port from which the ancient Maritime Silk Road '
                'set sail.'
            )},
            {'type': 'text', 'content': (
                'Kaiyuan Temple: The largest Buddhist monastery in Fujian, founded in A.D. 686. '
                'Its twin pagodas — the Zhenguo Pagoda to the east and the Renshou Pagoda to the '
                'west — have stood sentinel for centuries.'
            )},
            {'type': 'text', 'content': (
                'Qingyuan Mountain: acclaimed as the "Foremost Penglai Mountain of Fujian and the '
                'Sea." Its most celebrated treasure is the Song-dynasty stone Laozi, the largest '
                'and most artistically significant Daoist stone carving in China, popularly known '
                'as "Laozi, Foremost Under Heaven."'
            )},
        ]
    },
}

# ── Volume 3 EN titles and subtitles ──
V3_TRANSLATIONS = {
    'v3-01': {
        'title': 'Silver Hair, Lingering Grace in the Lion City',
        'subtitle': 'An elder traveller savours the sights and memories of Singapore.',
        'blocks': [
            {'type': 'text', 'content': 'Silver Hair, Lingering Grace in the Lion City'},
            {'type': 'text', 'content': (
                'From the 18th to the 22nd of November, 2023, we made another journey to Singapore. '
                'That beautiful garden city, where spring endures through all four seasons and the '
                'scenery resembles paintings, is one of the most cosmopolitan cities in all of Asia — '
                'a place where Eastern and Western cultures merge, alive with vigour and elegance, '
                'and blessed with world-renowned architecture and cuisine.'
            )},
            {'type': 'text', 'content': 'The New Modern Library of Singapore'},
            {'type': 'text', 'content': (
                'On the 18th of November, my third son led us on a visit to the newly built modern '
                'Punggol Regional Library, situated within the Punggol Community Hub. Opened on the '
                '30th of January, 2023, this magnificent edifice of five storeys encompasses a total '
                'area exceeding twelve thousand square metres, making it one of the largest public '
                'libraries in Singapore. Within its precincts, a great food court offers hundreds of '
                'dining stalls, and we chose a well-known establishment called "The Old Place" for '
                'our midday repast.'
            )},
            {'type': 'text', 'content': 'The Haw Par Villa'},
            {'type': 'text', 'content': (
                'On the 20th of November, my daughter took us to visit the Haw Par Villa. Also known '
                'as the Tiger Balm Garden, it is a singular Chinese cultural theme park — a gift from '
                'the wealthy overseas Chinese merchant Aw Boon Haw to his younger brother Aw Boon Par. '
                'Completed in 1937, it is one of three such villas in Asia (the others being in Hong '
                'Kong and Fujian province), built by the celebrated maker of Tiger Balm and opened '
                'freely to the public.'
            )},
            {'type': 'text', 'content': 'The Modern Marina Bay Shopping Mall'},
            {'type': 'text', 'content': (
                'On the 21st of November, my daughter led us through the Marina Bay Shopping Mall, '
                'one of Singapore\'s premier luxury retail destinations, situated in the heart of the '
                'central business district. With its contemporary design overlooking the magnificent '
                'skyline of Marina Bay, the mall houses a casino, an ice-skating rink, and even an '
                'artificial canal where visitors may ride in little boats. Though I had been here '
                'many times before, this year the mall was adorned with the rich colours of Christmas. '
                'How beautiful it was!'
            )},
            {'type': 'text', 'content': 'Little India'},
            {'type': 'text', 'content': (
                'On the 22nd of November, we wandered through Singapore\'s Little India district. '
                'A gathering-place for the Indian community, it is as though a miniature India has '
                'been transported to this corner of the Lion City — one of the most vibrant quarters '
                'of the nation. Of Singapore\'s 5.677 million inhabitants, some 2.79 million are '
                'ethnic Chinese, accounting for three-quarters of the population, while roughly ten '
                'percent are of Indian descent, with over four hundred and fifty thousand residing '
                'in Little India alone.'
            )},
            {'type': 'text', 'content': (
                'Little India brims with exotic charm. The Tekka Centre stands at its bustling heart, '
                'and we visited the Indian Heritage Centre and the Sri Mariamman Temple — the oldest '
                'Hindu temple in Singapore, built in 1843.'
            )},
        ]
    },
    'v3-02': {
        'title': 'A Visit to the National University of Singapore',
        'subtitle': 'Wandering the halls of NUS, a bastion of learning in the tropics.',
        'blocks': [
            {'type': 'text', 'content': 'A Casual Note on Visiting the National University of Singapore'},
            {'type': 'text', 'content': (
                'On the 19th of November, 2023, a Sunday, my granddaughter Lin Sijia — a fourth-year '
                'graduate of the National University of Singapore — led us by taxi from our residence '
                'in Sengkang to Queenstown, to visit the university. NUS is ranked eleventh in the QS '
                'World University Rankings and first in all of Asia. Possessing a richly diverse '
                'academic environment, first-rate scholarly resources and facilities, a modern library, '
                'and ample opportunities for social engagement, NUS is renowned throughout the world '
                'for its academic excellence. The visit left a profound impression upon me.'
            )},
            {'type': 'text', 'content': (
                'Part the First: We toured the beautiful NUS University Town, where I was photographed '
                'with my granddaughter in the central plaza. We then visited the administration '
                'building, the dining hall, the grand auditorium, and the modern library, and took '
                'our lunch in the campus canteen. We strolled through the residential college area, '
                'admiring more than twenty hotel-style dormitory towers, each eleven storeys high '
                'and each bearing a distinct architectural exterior — a vision of modern living.'
            )},
            {'type': 'text', 'content': (
                'Part the Second: We visited the upper-year student residences, the dining halls, '
                'the small gardens, reception rooms, laundry rooms, photocopy rooms, and communal '
                'kitchens — every convenience one could wish for. Because the NUS campus is vast and '
                'divided into two precincts, we rode the campus shuttle from University Town to the '
                'upper-year precinct to continue our exploration.'
            )},
        ]
    },
    'v3-03': {
        'title': 'Revisiting the Sights of Singapore Chinatown',
        'subtitle': 'A second tour through the bustling lanes and heritage of Chinatown.',
        'blocks': [
            {'type': 'text', 'content': 'Revisiting the Sights of Singapore\'s Chinatown'},
            {'type': 'text', 'content': (
                'Chinatown in the Kreta Ayer district boasts a long history. From 1821 onward, '
                'immigrants from southern China flooded in, most of them settling in this area '
                'in the heart of the city — one of the oldest quarters of Singapore. In those '
                'days, water was delivered by ox-drawn carts, giving the district its name: '
                'Kreta Ayer, the Water-Cart district. Some sixty-five thousand Chinese reside '
                'within this quarter alone.'
            )},
            {'type': 'text', 'content': (
                'On the 22nd of November, 2023, we rambled through Singapore\'s Chinese quarter — '
                'Kreta Ayer Chinatown — visiting the Pearl Centre, the Thian Hock Keng Temple (the '
                'temple of the Heavenly Queen, Mazu), and the clan associations of Fujian, Eng Choon, '
                'Zhangzhou, and Nan\'an.'
            )},
            {'type': 'text', 'content': (
                'Thian Hock Keng Temple, built in 1840, is the oldest and most famous Chinese '
                'temple in Singapore, graced by a plaque bearing the imperial characters "Auspicious '
                'Clouds Over the Ocean" bestowed by the Guangxu Emperor in 1899. On the 26th, my '
                'third daughter-in-law and granddaughter, taking advantage of the Sunday holiday, '
                'led us once more through the many sights of Chinatown. We explored Temple Street, '
                'with its street-side fruit stalls, durian vendors, traditional shops, tea houses, '
                'and the old custom of face-threading for ladies. On Smith Street we discovered the '
                'Singapore Association of Writers, the Xin Sheng Poetry Society, and the Dunhuang '
                'Theatre, before making our way to the Buddha Tooth Relic Temple — a sacred monument '
                'of religious art and culture.'
            )},
            {'type': 'text', 'content': 'Farewell, O ancient Kreta Ayer Chinatown of Singapore, O China Town!'},
        ]
    },
    'v3-04': {
        'title': 'Jewel Changi: A Leisurely Note',
        'subtitle': 'Strolling through the shimmering wonder of Jewel Changi Airport.',
        'blocks': [
            {'type': 'text', 'content': 'A Leisurely Note on Jewel Changi'},
            {'type': 'text', 'content': (
                'On the 2nd of December, 2023, my third daughter-in-law took us to see yet another '
                'must-visit sight of Singapore — Jewel Changi, situated at the very core of Changi '
                'Airport before Terminal One. The largest airport commercial complex in the world, '
                'Jewel Changi opened in April 2019 with five storeys of leisure, entertainment, '
                'luxury shopping, lush greenery, and a celestial garden, housing more than two hundred '
                'and eighty shops. It is at once an airport and a premier shopping destination, '
                'where a waterfall and an indoor forest have been brought into the terminal itself. '
                'This essay shall lead you through the delights of Jewel Changi.'
            )},
        ]
    },
    'v3-05': {
        'title': 'Admiring the Flora of Singapore',
        'subtitle': 'A feast of exotic flowers and rare trees in the Garden City.',
        'blocks': [
            {'type': 'text', 'content': 'Feasting on the Exotic Flowers and Fine Trees of the Lion City'},
            {'type': 'text', 'content': (
                'On the 8th of December, 2023, my granddaughter, having finished her semester '
                'examinations, led us to the Singapore Botanic Gardens — the country\'s first UNESCO '
                'World Heritage Site, on a par with the Great Wall of China as a landmark of global '
                'significance.'
            )},
            {'type': 'text', 'content': (
                'The Gardens, established in 1859, stretch across seventy-four hectares on Cluny Road. '
                'They harbour over twenty thousand species of subtropical and tropical exotic flowers '
                'and precious trees, divided into tropical, palm, bamboo, and horticultural collections. '
                'We wandered through the Leaf Garden, the Rubber Garden, and the Ethnobotany Garden, '
                'marvelling at groves of bamboo and palm, at rubber trees that provide the raw material '
                'for automobile tyres, and at the sky-shrouding forest canopy.'
            )},
        ]
    },
    'v3-06': {
        'title': 'A Night at Chiayi Culture Road Night Market',
        'subtitle': 'The sounds, smells, and tastes of Chiayi after dark.',
        'blocks': [
            {'type': 'text', 'content': 'An Evening Rhapsody at Chiayi\'s Culture Road Night Market'},
            {'type': 'text', 'content': (
                'From the 18th of December, 2023, to the 13th of January, 2024, my wife and I '
                'returned to Taiwan to visit our daughter, staying for a full month.'
            )},
            {'type': 'text', 'content': (
                'On the evening of the 19th of December, our daughter led us by car to the Culture '
                'Road Night Market in Chiayi\'s western district. Stretching some five hundred metres, '
                'the road serves as a thoroughfare by day and transforms by night into a bustling '
                'market, with food and fruit stalls lining both sides. Especially famous are its '
                'delectable snacks — sand-pot fish head, chicken rice, oyster omelettes, oyster '
                'vermicelli, offal soup, glutinous rice cakes, soup dumplings, and bubble tea. We '
                'found ourselves in a place brimming with gastronomy and revelry, thronged with '
                'locals and visitors alike, alive with the unique charm of Taiwan\'s night-market culture.'
            )},
            {'type': 'text', 'content': (
                'Naturally, we could not miss the culinary treasures of Culture Road. We made our '
                'way to No. 361 Zhongzheng Road, to the original headquarters of the world-renowned '
                '"Lin Congming Sand-Pot Fish Head," a namesake establishment of our own Lin clan. '
                'The dish was exquisitely delicious — a flavour so sublime as to defy resistance.'
            )},
        ]
    },
    'v3-07': {
        'title': 'Shadow Tower of Peach City, Under the Sun',
        'subtitle': 'The iconic tower of Chiayi and the legend of the sun-shooting hero.',
        'blocks': [
            {'type': 'text', 'content': 'The Shadow Tower of Peach City and the Sun-Shooting Lore'},
            {'type': 'text', 'content': (
                'On the 21st of December, 2023, on our journey through Chiayi — known as the Peach '
                'City — we could not omit a visit to the Sun-Shooting Tower, the very landmark of '
                'the city. Standing in Chiayi Park and built in 1911, the tower rises to sixty-two '
                'metres. Its design is inspired by the sacred trees of Alishan, its brown aluminium '
                'strips mimicking the bark of those ancient giants, and a forty-metre "slit of sky" '
                'running through its centre like a cleft in a divine tree.'
            )},
            {'type': 'text', 'content': (
                'We purchased tickets (sixty New Taiwan dollars each) to ascend to the twelve-storey '
                'observation deck. On the tenth floor, we viewed the spiritual art exhibition of the '
                'heart-painter Zeng Risheng; on the eleventh, we savoured Assam milk tea and peanut '
                'caramel latte at a charming café, each priced at one hundred and eighty dollars. '
                'Then, from the topmost floor, we beheld the splendid panorama of Chiayi. Standing '
                'at the summit, I gazed upon the city\'s forest of high-rises — a breathtaking vista '
                'unfolding before my eyes. How beautiful!'
            )},
            {'type': 'text', 'content': (
                'We also toured the Confucian Temple within Chiayi Park, built in 1964, where the '
                'sacred tablet of Confucius is enshrined in the Hall of Great Achievement.'
            )},
        ]
    },
    'v3-08': {
        'title': 'Classic Sights of Chiayi, Part One',
        'subtitle': 'A guided ramble through Chiayi\'s most treasured landmarks.',
        'blocks': [
            {'type': 'text', 'content': 'A Ramble Through the Classic Sights of Chiayi — Part the First'},
            {'type': 'text', 'content': (
                'On the 22nd of December, 2023, we pursued the beauty of sightseeing in Chiayi — '
                'exploring the Alishan Forest Railway Garage Park, riding the charming cypress-wood '
                'train, admiring the Alishan Forestry Village, and wandering through the Hinoki '
                'Village. These are sights that no visitor to Chiayi should miss.'
            )},
            {'type': 'text', 'content': (
                'The Alishan Forest Railway Garage Park, one of the most celebrated tourist '
                'attractions, is also one of the most historic forest railways, built in 1906 '
                'when it served only to transport timber and tea. Covering approximately two '
                'thousand hectares, the park displays trains and carriages, including the '
                'Zhongxing Express, numerous decommissioned locomotives, a wooden waiting room '
                'from the Japanese colonial era, and a repair workshop — a tourism destination '
                'that combines history, culture, and the scenery of Alishan.'
            )},
            {'type': 'text', 'content': (
                'The cypress-wood train operates within the park. The staff told us that the six '
                'carriages — three kept in Alishan and operated only once a year, and three in '
                'Chiayi running every weekend and holiday — were modelled after the 1925 Japanese '
                'imperial family\'s VIP car, each carriage costing fifteen million New Taiwan dollars '
                'to build and giving off a refined, delicate fragrance of cypress. We were fortunate '
                'that it was a Saturday, and we boarded carriage number two for our scenic ride.'
            )},
            {'type': 'text', 'content': (
                'The Alishan Forestry Village is an art park spanning some thirteen hectares, its '
                'centrepiece being the "Song of the Forest," a new landmark fashioned from timber, '
                'rattan, railway tracks, and stone. The Hinoki Village, covering over three hectares, '
                'is the most concentrated collection of Japanese-style wooden buildings in Taiwan — '
                'twenty-nine structures in all — and the nation\'s first forest-themed cultural and '
                'creative park.'
            )},
        ]
    },
    'v3-09': {
        'title': 'Classic Sights of Chiayi, Part Two',
        'subtitle': 'Continuing the journey through Chiayi\'s scenic and historic spots.',
        'blocks': [
            {'type': 'text', 'content': 'A Ramble Through the Classic Sights of Chiayi — Part the Second'},
            {'type': 'text', 'content': 'The Jingguo New Village'},
            {'type': 'text', 'content': (
                'On the 8th of January, 2024, we continued our exploration of Chiayi\'s classic '
                'sights, venturing into the Jingguo New Village — a military dependents\' village. '
                'After the Nationalist retreat, many soldiers and their families fled to the western '
                'district of Chiayi, settling in this very area. Today, the streets are lined with '
                'Nationalist flags, and every residential block is numbered by letters of the '
                'alphabet from A to P. Named in honour of Chiang Ching-kuo, the area has become a '
                'thriving new quarter of western Chiayi.'
            )},
            {'type': 'text', 'content': 'Urn-Baked Chicken'},
            {'type': 'text', 'content': (
                'On the 10th of January, we travelled to Wenya Road for lunch at a celebrated '
                'urn-baked-chicken restaurant. The authentic preparation uses specially chosen wood '
                'to roast the chicken, resulting in a crisp, golden skin and a succulent, aromatic '
                'interior — a singularly unique gastronomic delight.'
            )},
            {'type': 'text', 'content': 'Kaohsiung'},
            {'type': 'text', 'content': (
                'On the morning of the 11th of January, we took a taxi to Chiayi Railway Station, '
                'then a train connecting to the metro that brought us to Kaohsiung\'s Formosa Boulevard '
                'Station. Famed for its singular architectural design, the station boasts the '
                'magnificent "Dome of Light" — a cascade of flowing colours and radiant hues that '
                'is not merely an architectural marvel but a destination in its own right.'
            )},
        ]
    },
    'v3-10': {
        'title': 'Exploring the Charm of Budai Harbour',
        'subtitle': 'A day at the fishing port of Budai, where sea and sky meet.',
        'blocks': [
            {'type': 'text', 'content': 'Exploring the Charm of Budai Harbour'},
            {'type': 'text', 'content': (
                'On the 26th of December, 2023, we set out to discover the charms of Budai Harbour, '
                'lying in the north-western corner of Budai Township in Chiayi County. A fishing '
                'port of long history, it is among the most important harbours of Chiayi and one '
                'of the most popular tourist destinations. We rode bus 7209 from the Chiayi bus '
                'terminal, a journey of an hour and a half through the city centre, the county, '
                'and the township to reach this distant coastal spot.'
            )},
            {'type': 'text', 'content': (
                'At the Yunlin-Chiayi-Tainan Coastal National Scenic Area, we admired the Budai '
                'Harbour Bridge and strolled through the old streets of Budai, where we purchased '
                'fresh seafood — prawns, oysters, a large female crab, and clams — for nearly two '
                'thousand New Taiwan dollars. We also beheld the curious High-Heel Shoe Church, '
                'standing seventeen metres tall in the Budai Seaview Park, certified by Guinness '
                'World Records as the largest shoe-shaped building on earth.'
            )},
        ]
    },
    'v3-11': {
        'title': 'An Evening Stroll by the Moonlit Bridge',
        'subtitle': 'The gentle grace of a bridge bathed in twilight and moonbeams.',
        'blocks': [
            {'type': 'text', 'content': 'An Evening Stroll at the Mituo Moon-Reflecting Bridge'},
            {'type': 'text', 'content': (
                'On the evening of the 28th of December, 2023, we took a twilight ramble to the '
                'Mituo Moon-Reflecting Bridge, lingering by the stream to savour the gentle moonlight.'
            )},
            {'type': 'text', 'content': (
                'The Mituo Moon-Reflecting Bridge is an important scenic span in Chiayi — a pedestrian '
                'cable-stayed bridge with a singular illuminated night-time effect. Strolling to the '
                'Green-Reflection Waterfront Park along the Bazhang River, we beheld this bridge, '
                'also called the Chiayi Grand Bridge. Spanning two hundred and twenty-two metres, '
                'crossing the Bazhang River for a distance of one hundred and fifteen metres, and '
                'rising fifty metres high, its single-tower cable-stayed structure presents elegant '
                'lines by day. Completed after a year of construction at a cost of over one hundred '
                'million dollars, it is Chiayi\'s new landmark. The single tower is fitted with two '
                'projection mirrors that can cast images of people and buildings.'
            )},
            {'type': 'text', 'content': (
                'At night, the majestic Moon-Reflecting Bridge comes alive: a riot of five-coloured '
                'light bathes the single tower, a kaleidoscope of hues — a glowing jewel along the '
                'Bazhang River under the night sky. How beautiful it was!'
            )},
        ]
    },
    'v3-12': {
        'title': 'Moon Shadows on the Lake at Dusk',
        'subtitle': 'Reflections of the moon upon a tranquil lake at eventide.',
        'blocks': [
            {'type': 'text', 'content': 'Moon Shadows on the Lake at Dusk'},
            {'type': 'text', 'content': (
                '"The moon descends upon the Orchid Pool, spreading pale splendour; / The wind '
                'stirs the waterside pavilion, stirring a tranquil heart."'
            )},
            {'type': 'text', 'content': (
                '"The pool\'s surface spreads light, congealing the moon\'s reflected image; / The '
                'lake\'s heart, stirred into stillness, enfolds the mountain\'s mist."'
            )},
            {'type': 'text', 'content': (
                'On the evening of Friday, the 29th of December, 2023, we travelled east to the '
                'Lantan Scenic Area in Chiayi\'s Luliao Village. The "Moon Shadow Pool\'s Heart," '
                'designed by Wang Wenzhi in 2011, is a hollow, woven structure of aluminium, '
                'stainless steel, pottery, and steel — under the moonlight, its shifting light and '
                'shadows create a bird\'s-nest form poised upon the water.'
            )},
            {'type': 'text', 'content': (
                'At half past six in the evening, the musical fountain performance began. Melodies '
                'bloomed softly in the air, as though invisible threads were drawing the soul into '
                'another world. Coloured pillars of water danced and soared — a feast for eye and '
                'ear alike, carrying one into a realm of dreams. How wondrous was the musical fountain! '
                'When the performance ended, I rose with a heart both calm and full, looking back '
                'upon this beautiful scene.'
            )},
        ]
    },
    'v3-13': {
        'title': 'A Leisurely Walk Through Chiayi Mituo Night Market',
        'subtitle': 'A relaxed evening among the stalls and lights of Mituo Night Market.',
        'blocks': [
            {'type': 'text', 'content': 'An Idle Ramble Through the Chiayi Mituo Night Market'},
            {'type': 'text', 'content': (
                'On the evening of Friday, the 29th of December, 2023, after watching the musical '
                'fountain, we rode to Mituo Road to browse the Chiayi Mituo Night Market.'
            )},
            {'type': 'text', 'content': (
                'A nocturnal ramble through Chiayi, idly strolling amid the flowing lights and colours '
                'of the Mituo Night Market. Renowned for its rich variety of delicacies, it is a '
                'thriving night market that celebrates traditional cuisine and vibrant culture. '
                'Open every Wednesday and Friday, it draws surging crowds — a sea of visitors, '
                'alive with bustle and vitality.'
            )},
            {'type': 'text', 'content': (
                'Whether beef steak, pork chop, chicken fillet, turkey rice, or snacks of every '
                'description, each dish wafts an enticing aroma and flavour. Whether one favours '
                'the spicy, the sweet, the sour, or the salty, all tastes are satisfied here. We '
                'chose the "Xinye Steak Grill" for our evening repast, enjoying four types of meats '
                'with corn chowder and black tea to drink at will. Thus did we stroll, savouring '
                'both the food and the warm, lively ambience of the night market — a gentle night '
                'in a gentle city, a record of Chiayi\'s Mituo nocturne.'
            )},
        ]
    },
    'v3-14': {
        'title': 'An Unforgettable New Year\'s Eve, 2023',
        'subtitle': 'Ringing in the new year with family, warmth, and fond memories.',
        'blocks': [
            {'type': 'text', 'content': 'An Unforgettable New Year\'s Eve, 2023'},
            {'type': 'text', 'content': (
                'The unforgettable New Year\'s Eve of 2023 — a night brimming with joy and blessings.'
            )},
            {'type': 'text', 'content': (
                'On the evening of the 31st of December, 2023, to celebrate the passing of the year, '
                'we rode a taxi forty minutes from Mituo Road to Daya Road in Chiayi\'s eastern '
                'district, to the renowned Taohuayuan — the Peach Blossom Spring Restaurant — a '
                'courtyard dining-house of classical elegance whose chef, Mr. Zeng Daozheng, once '
                'served as the Presidential Palace\'s imperial cook. This was my second time enjoying '
                'its delectable cuisine. The restaurant was packed with diners, and had my daughter '
                'not booked in advance online, we would never have secured a table. We specially '
                'chose the dish that had won first prize in the national New Year\'s Eve competition — '
                '"Dried Scallops Embroidered Balls" — along with the famous Crispy Duck and '
                'Braised Pork Belly in Lotus-Leaf Buns.'
            )},
            {'type': 'text', 'content': (
                'After dinner, we rode to Chiayi Stadium to enjoy the "Welcome 2024 All-Chiayi '
                'Rise Together New Year Countdown Gala," where thousands upon thousands had gathered '
                'to count down the final moments of the year. Then we plunged into the exuberant '
                'night market in the side streets — a sea of humanity, a roar of voices, a spectacle '
                'of festivity. In short, this was our first New Year\'s Eve in Chiayi, an evening '
                'of delight and unforgettable joy.'
            )},
        ]
    },
    'v3-15': {
        'title': 'A New Year\'s Day Ramble in Chiayi',
        'subtitle': 'Welcoming the first day of the year with a gentle wander through the city.',
        'blocks': [
            {'type': 'text', 'content': 'A New Year\'s Day Nocturne in Chiayi'},
            {'type': 'text', 'content': (
                'On the first day of the year 2024, as the new year began and the evening breeze '
                'blew mild, we ventured into the city of Chiayi to share in the festive panorama. '
                'The sky was lit with fireworks, bursting in vibrant colours like a galaxy of stars '
                'suspended above, bringing richness and blessing to the city. Around five in the '
                'afternoon, we headed to Carrefour Plaza on Boai Road in the western district, '
                'which by night transforms into the famed Jialefu Night Market. We dined at the '
                '"Hefeng Teppanyaki," a restaurant with a unique concept of compound supermarket '
                'teppanyaki, where the chef performs his culinary artistry before your very eyes.'
            )},
            {'type': 'text', 'content': (
                'We ordered lamb chops, beef steak, chicken fillet, Matsusaka pork, mackerel, '
                'flounder, scallops, prawns, thick omelette, greens, bean sprouts, and zucchini. '
                'The chef, with consummate skill, produced meats of tender succulence — lamb, beef, '
                'chicken, and fish — along with the omelette and vegetables, all complemented by '
                'a secret house sauce. So delightful was the flavour that I broke my usual rule '
                'and ate two small bowls of rice. Only late at night did we return, looking back '
                'upon a city ablaze with lights, recording in these travelling notes an unforgettable '
                'New Year\'s Day in Chiayi.'
            )},
        ]
    },
    'v3-16': {
        'title': 'A Visit to National Chiayi University',
        'subtitle': 'A tour of the campus and its serene academic atmosphere.',
        'blocks': [
            {'type': 'text', 'content': 'A Record of Visiting National Chiayi University'},
            {'type': 'text', 'content': (
                'On the 5th of January, 2024, we stepped into the secret academic sanctuary of the '
                'southern realm — the Cloud-Forest Academy — and feasted on the splendour of NCYU.'
            )},
            {'type': 'text', 'content': (
                'National Chiayi University, abbreviated as NCYU, is a comprehensive university '
                'formed in the year 2000 through the merger of the National Chiayi Institute of '
                'Technology and the National Chiayi Teachers College. It encompasses four campuses: '
                'Lantan (the main campus), Minxiong, Xinmin, and Linsen, plus an experimental forest '
                'in Shekou, Zhongpu Township. Six colleges — Science and Engineering, Agriculture, '
                'Life Sciences, Management, Teacher Education, and Humanities and Arts — house '
                'thirty-six departments and forty-four graduate institutes.'
            )},
            {'type': 'text', 'content': (
                'We rode to Xuefu Road in Luliao Village to visit the beautiful Lantan main campus. '
                'Part the First: We photographed ourselves at the university gate, then moved to '
                'the campus garden, where like children we enjoyed the stone sculptures of water '
                'buffaloes, shepherd boys, and rabbits — the buffalo and shepherd representing '
                'the deep sentiment of the merger between the agricultural and teachers\' traditions.'
            )},
            {'type': 'text', 'content': (
                'Part the Second: We strolled past the sports field, swimming pool, Ruisui Hall, '
                'Jiahe Hall, student activity plaza, Zhongzheng Building, the Bell Tower, and the '
                'administration centre. Part the Third: Walking along the campus avenue, we reached '
                'the Science and Engineering Building, the Physics and Chemistry Hall, then the '
                'dining hall, where we enjoyed a delicious lunch on the second floor. Afterwards, '
                'we visited the student activity centre, the university co-operative, and the '
                'monumental natural stone — a piece of cloud-patterned marble weighing over '
                'seventy-eight tons, the oldest basement rock of Taiwan, symbolising the century-old '
                'heritage of the university. Farewell, National Chiayi University!'
            )},
        ]
    },
    'v3-17': {
        'title': 'Ten Thousand at the Lakeview Fair: Chiayi Night Market',
        'subtitle': 'A bustling night market by the lake, alive with crowds and colour.',
        'blocks': [
            {'type': 'text', 'content': 'Ten Thousand at the Lakeview Fair — the Chiayi Night Market'},
            {'type': 'text', 'content': (
                'On the 6th of January, 2024, the Chiayi City Government\'s Construction Department '
                'inaugurated the "Lakeview Fair Chiayi Night Market." Ten thousand gathered, the '
                'lights blazed brilliantly, and the crowds surged in endless streams — hence its '
                'renown as the "Ten-Thousand Lakeview Fair."'
            )},
            {'type': 'text', 'content': (
                'That day, a Saturday, was the very first day of the Lakeview Night Market\'s opening. '
                'Occupying over six thousand square metres and housing two hundred stalls divided '
                'into two zones, it operates every Wednesday, Friday, and Saturday from dusk until '
                'midnight, with free admission — one of Chiayi\'s largest and most distinctive '
                'night markets. Around four in the afternoon, we rode a taxi to the distant Humei '
                'Eighth Road, joining an estimated thirty thousand visitors. The stalls were a '
                'dazzling array of sights and smells, and we sampled many of their offerings: '
                'baked lobster pot, fresh prawn meatballs, cheese-filled potato rolls, fried '
                'oyster patties, radish cake, large-intestine-wrapped-small-intestine sausage, '
                'peanut-coated pig\'s blood cake, old-style ice cream, licorice olives, and more.'
            )},
            {'type': 'text', 'content': (
                'We roamed the ten-thousand-strong Lakeview Fair, so enchanted we forgot to leave, '
                'relishing every moment of this boisterous, fascinating, unforgettable night. '
                'Farewell, O unforgettable Lakeview Fair Chiayi Night Market!'
            )},
        ]
    },
    'v3-18': {
        'title': 'Zhentian Temple and the Oath of the Peach Garden',
        'subtitle': 'Paying homage at a temple that honours the legendary brotherhood.',
        'blocks': [
            {'type': 'text', 'content': 'A Pleasant Visit to Zhentian Temple — Paying Homage to the Peach Garden Oath'},
            {'type': 'text', 'content': (
                'On the 9th of January, 2024, my daughter led us to Fang\'an Road in Chiayi\'s '
                'eastern district, to visit Xixin Zhentian Temple and gaze upon the rare and '
                'colossal statues of the Three Sworn Brothers of the Peach Garden. Founded in 1964 '
                'as the "Zhentian Palace" and formally renamed in 1971, the temple completed its '
                'gigantic golden icons of Liu Bei, Guan Yu, and Zhang Fei in 1982, crowning the '
                'edifice itself. From afar, the imposing archway is visible, and the temple — a '
                'magnificent palace of the Peach Garden oath — radiates an aura of grandeur.'
            )},
            {'type': 'text', 'content': (
                'The right gate is the Dragon Gate, the left the Tiger Gate, each inscribed with '
                'evocative couplets. Entering the temple courtyard, we found it spacious and serene, '
                'incense smoke curling towards the heavens, conveying prayers. On the left stands '
                'the Red Hare Horse Shrine, on the right the Golden Brazier. The temple itself '
                'rises four levels. The ground-floor main hall, solemn and majestic, grand and '
                'elegant, houses a pantheon of deities whose awe-inspiring presence evokes '
                'spontaneous reverence. Ascending to the first floor, we beheld the giant golden '
                'statues of the three sworn brothers. On the second floor, the Bell and Drum Garden '
                'and the Matchmaker\'s Hall; on the third, the Hall of the Three Patriarchs.'
            )},
        ]
    },
    'v3-19': {
        'title': 'Half a Day at Ziyun Temple, Bantianyan',
        'subtitle': 'A brief but memorable visit to the cliffside temple of Purple Clouds.',
        'blocks': [
            {'type': 'text', 'content': 'Spending Half a Day at the Ziyun Temple of Bantianyan'},
            {'type': 'text', 'content': (
                '"Halfway up the peak, numinous crags spread heaven\'s splendour; / Purple vapours '
                'among the clouds diffuse the fragrance of the Buddha\'s temple."'
            )},
            {'type': 'text', 'content': (
                'The 10th of January, 2024, was our last day in Chiayi after nearly a month\'s '
                'sojourn. Seizing what could not be missed, we set out early in the morning for '
                'the Bantianyan Ziyun Temple. My daughter led us to Zhongshan Road, and from there '
                'we rode bus 7308 up the mountainside to Bantianyan in Minhe Village, Fanlu Township. '
                'Arriving around nine, we began our ramble through the temple.'
            )},
            {'type': 'text', 'content': (
                'The majestic archway captured our attention first, its couplet speaking of guiding '
                'the lost and ferrying souls to the Pure Land. Founded in 1682, Ziyun Temple has '
                'stood for over three hundred years — a temple of imposing presence and ancient, '
                'unadorned sincerity. From afar, the mountain seems to reach halfway to heaven, '
                'hence the name Bantianyan — "Half-Sky Crag" — and the purple clouds that wreathe '
                'the peak at dawn and dusk give the temple its name: Ziyun, the Purple Cloud Temple.'
            )},
            {'type': 'text', 'content': (
                'The spacious courtyard features twin bell-and-drum towers, a golden brazier with '
                'incense smoke ascending, and the dragon pearl flanked by the Eight Immortals and '
                'Arhats. The main hall is solemn and carved with intricate beauty. We entered the '
                'Guanyin Hall, where a statue of the Bodhisattva had been carved from a tree stump '
                'found on this very site — a figure of striking lifelike grace. We also tried the '
                'traditional practice of touching the silver for good fortune. In the park beyond, '
                'we paid homage to the Ascending Dragon Guanyin, a statue rising seventy-six feet, '
                'and saw the Laughing Buddha. With a heart full of peace and ease, we spent half '
                'a day exploring this ancient temple, carrying its tranquillity back with us into '
                'the world.'
            )},
        ]
    },
}

V4_TRANSLATIONS = {
    'v4-01': {
        'title': 'Alumni Reunion in Pengcheng',
        'subtitle': 'Gathering of old schoolmates in Shenzhen, celebrating friendship and shared memories.',
    },
    'v4-02': {
        'title': 'A Gala of Homecoming and Honour',
        'subtitle': 'Celebrating the return, renewing bonds of kinship, and honouring elders and scholars.',
    },
    'v4-03': {
        'title': 'Erudition: Bridging Past and Present',
        'subtitle': 'Through wide learning and deep enquiry, one may know the ancient and the new.',
    },
    'v4-04': {
        'title': 'Sketches of Chancheng and Fengcheng',
        'subtitle': 'Casual notes from a ramble through the cities of the Zen and the Phoenix.',
    },
    'v4-05': {
        'title': 'Revisiting Kaiyuan Temple, Quanzhou',
        'subtitle': 'A return to the ancient monastery of Kaiyuan, and a second contemplation of a thousand years of Quanzhou.',
    },
    'v4-06': {
        'title': 'A Stroll by the Tianyan, Tea at Fanlou',
        'subtitle': 'A leisurely walk to behold the Eye of Heaven, and a cup of clear tea in the tower of plenty.',
    },
    'v4-07': {
        'title': 'New Year\'s Eve Gala in Shenzhen',
        'subtitle': 'Welcoming the new year in Pengcheng, amid ten thousand scenes of joy and festivity.',
    },
}

# Merge all volumes into TRANSLATIONS for lookup
ALL_TRANSLATIONS = {}
ALL_TRANSLATIONS.update(TRANSLATIONS)
ALL_TRANSLATIONS.update(V2_TRANSLATIONS)
ALL_TRANSLATIONS.update(V3_TRANSLATIONS)
ALL_TRANSLATIONS.update(V4_TRANSLATIONS)


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
            else:
                en_data, en_sub = create_v2_en_placeholder(article_id, zh_data, en_translation)

            en_path = os.path.join(BOOK_DIR, f'en-{article_id}.json')
            with open(en_path, 'w', encoding='utf-8') as f:
                json.dump(en_data, f, ensure_ascii=False, indent=2)
            print(f'  ✓ en-{article_id}.json — {en_translation["title"]}')

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
    v4_count = len([k for k in V4_TRANSLATIONS if k in ALL_TRANSLATIONS])
    print(f'\nDone. {v1_count} V1 + {v2_count} V2 + {v3_count} V3 + {v4_count} V4 articles with EN info.')


if __name__ == '__main__':
    main()
