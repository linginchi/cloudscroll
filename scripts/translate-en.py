# -*- coding: utf-8 -*-
"""
scripts/translate-en.py

Generate EN translation scaffolding for each article.
Also updates master data.json with EN titles and corrects ZH subtitles (金句).
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
            {'type': 'text', 'content': 'Statue of Wang Yangming | Flower Clock | Waterfall—"three thousand feet of flying water" | Cherry blossoms in autumn hues | Presidential Palace'},
            {'type': 'text', 'content': 'National Palace Museum | Chiang Kai-shek Memorial Hall | Museum | Taipei album: solemn ceremonial guards, Martyrs\' Shrine'},
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
                'that archipelago of seven thousand islands in Southeast Asia. There, in the Philippine Isles, '
                'my father and uncle built their lives from nothing, hewing a path through thorns and brambles.'
            )},
            {'type': 'text', 'content': (
                'The old saying has it that "a stranger in a strange land thinks twice as much of home during '
                'the festivals." When at last I saw my father again, it was as though a lifetime had passed. '
                'Each time I visited him in the Philippines, my children came with me. Decades had not altered '
                'his native accent, nor diminished his fluent Chinese script, nor erased the cherished customs '
                'of our hometown. For my part, I know no English, so my children served as interpreters when '
                'I spoke with my Philippine relatives.'
            )},
            {'type': 'text', 'content': (
                'In September 1991, my eldest son accompanied me to the Philippines to see my father. Though '
                'I had never met my Philippine kin before, they received us with such warmth and sincerity as '
                'moved me deeply. But my son had to return to Hong Kong to attend to business, and we could '
                'stay only three days—too brief a time to see the islands. My Filipino brother and his family '
                'treated us to a splendid dinner at a fine restaurant.'
            )},
            {'type': 'text', 'content': (
                'In 1996, my wife and I, with our third son, made a second journey to see my father. This time '
                'we had the chance to tour the islands\' famous sights, guided by my Filipino brother and sister: '
                'the Nayong Pilipino, the Enchanted Kingdom, the Manila Chinese Church, the Philippine Flower '
                'Exhibition, and the Pagsanjan Falls.'
            )},
            {'type': 'text', 'content': '【Nayong Pilipino — The Philippine Village】'},
            {'type': 'text', 'content': (
                'Nayong Pilipino, also called the "Thousand Islands in Miniature," reflects the character of '
                'each Philippine province. Here one gains an understanding of the country\'s geography and culture. '
                'Every garden showcases the native scenery and typical architecture of its region—nipa huts, '
                'ethnic houses, all scaled to miniature perfection. It was a rare and precious thing to have my '
                'father with us in that place, and we captured the moment in photographs.'
            )},
            {'type': 'text', 'content': '【Enchanted Kingdom】'},
            {'type': 'text', 'content': (
                'My Filipino brother and his family took us to the Enchanted Kingdom, a grand amusement park. '
                'We rode an ox-cart through the grounds, admired a waterfall of several dozen metres—I composed '
                'a little verse: "A hundred feet of flying water, the thunder of waves across five slopes." '
                'My third son rode a pedal boat and drifted with the current. A bit dangerous, I thought, but '
                'he was thrilled.'
            )},
            {'type': 'text', 'content': (
                'I sat on a bamboo raft and watched the park\'s beauty glide by. I murmured: "On a bamboo raft '
                'above the blue waves, a man wanders through a painting."'
            )},
            {'type': 'text', 'content': (
                'There was a vast swimming pool filled with crystal-clear water that glittered under the sun. '
                'My third son, like a flying fish, splashed and swam to his heart\'s content. Watching him dart '
                'hither and thither, I felt a vicarious joy. Afterwards, we had our picture taken with the staff.'
            )},
            {'type': 'text', 'content': '【Manila Chinese Church】'},
            {'type': 'text', 'content': '【Philippine Flower Exhibition】'},
            {'type': 'text', 'content': (
                'Manila is a city of tropical gardens, bright and beautiful. We visited a flower exhibition '
                'full of local character. Flowers in the houses, houses among the flowers—how delightful!'
            )},
            {'type': 'text', 'content': '【Pagsanjan Falls】'},
            {'type': 'text', 'content': (
                '"A little boat enters the perilous rapids, / A hundred turns through the rushing torrent. / '
                'A hundred-foot waterfall plunges down; / My heart tightens as I grip the rail." Pagsanjan Falls '
                'lies ninety-two kilometres south of Manila, its waterfall dropping some hundred metres, famous '
                'for thrilling boat rides. My Filipino sister and cousin drove us there. We were content merely '
                'to let the children play in the water—pedal boats, swimming, and the like—and to enjoy a '
                'splendid lunch.'
            )},
            {'type': 'text', 'content': '【A Bountiful Dinner】'},
            {'type': 'text', 'content': (
                'Our Filipino mother laboured in the kitchen to prepare a feast of exquisite delicacies—carved '
                'clams and ornate seafood that tasted of the sea itself. It was a dinner seasoned with love. '
                'How we honoured her!'
            )},
            {'type': 'text', 'content': '【Water Play】'},
            {'type': 'text', 'content': (
                'For the children\'s safety, we kept to the gentler activities: pedal boats, swimming, gazing '
                'at the beauty of Pagsanjan under a warm sun and a blue sky.'
            )},
            {'type': 'text', 'content': (
                'In January 2010, my wife and I, accompanied by our daughter, made a third visit to see my '
                'father and my Filipino brother and sister, and to meet my niece and nephew. The couple received '
                'us with such gracious hospitality as I cannot adequately express.'
            )},
            {'type': 'text', 'content': '1.  2.'},
            {'type': 'text', 'content': '3.'},
            {'type': 'text', 'content': (
                'A rare and unexpected honour: I had the chance to converse with a Chinese-Filipino who had run '
                'for the presidency of the Philippines (he wore a green shirt). I was beside myself with joy.'
            )},
            {'type': 'text', 'content': '【Philippine Hilltop Park】'},
            {'type': 'text', 'content': (
                'One day we were in the water; the next, we climbed a mountain. My sister (a cardiologist) and '
                'my niece (a company director) drove us to a hilltop park. We wandered among the hills and '
                'waters, and found happiness seeping into our very souls. As the old saying goes: "When you '
                'climb a mountain, your heart fills with the mountain; when you gaze at the sea, your spirit '
                'overflows with the sea." We took many photographs.'
            )},
            {'type': 'text', 'content': (
                'On 30 March 2010, while my wife and I were on our way to our ancestral village of Jinjiang '
                'to tend the family graves, word came that my father had passed away in the Philippines. '
                'My passport was not with me; I rushed back to Hong Kong to fetch it. My father was gone—'
                'he had lived ninety-seven years (1913–2010). Desperate to see him one last time, I tried '
                'on 1 April to buy a ticket to the Philippines from Hong Kong, but every airline was sold out. '
                'I made a snap decision: fly to Xiamen instead, and ask relatives there to secure a ticket. '
                'We waited in the airport VIP lounge until nearly five in the afternoon. By eight that evening '
                'we landed in Manila, but we speak no English and could not reach my brother and sister. '
                'Fortunately, a kind young woman lent us her phone. In the confusion of arrival—there was no '
                'arrival hall to speak of—we spent over an hour finding my relatives. They drove us first to '
                'a restaurant for a late meal; we reached their home past midnight. Three airports in a single '
                'day—what a gruelling pilgrimage of love!'
            )},
            {'type': 'text', 'content': (
                'On 3 April, we set up a mourning hall at home and paid our respects. The following day, '
                'many relatives and friends attended the funeral, and we followed the cortege to the crematorium, '
                'where a memorial service was held in the church.'
            )},
            {'type': 'text', 'content': 'Dew and frost—the seasons of remembrance. We shall forever cherish our beloved father.'},
            {'type': 'text', 'content': (
                'Afterwards, my niece arranged for a company driver to take us to a place called "Cha Tsai Bat" '
                'in the Philippines—the very spot where my revered uncle had once run a sundry shop. It was '
                'there that he had blazed his trail through the wilderness.'
            )},
            {'type': 'text', 'content': 'I honour my uncle\'s simple, frugal life and his hard-won success. Though he is gone, he lives in our memory.'},
            {'type': 'text', 'content': (
                'We then visited the cemetery where my elder cousin lies buried—a site of good feng shui, '
                'as it turned out, for his children and grandchildren have prospered, their fortunes rising '
                'like the tide.'
            )},
            {'type': 'text', 'content': 'My cousin, too, has departed. May he rest in peace. We shall not forget him.'},
            {'type': 'text', 'content': (
                'Several times I travelled to the Philippines to visit my family—a land of grace and love, '
                'of kindness and blessing. These are my reflections:'
            )},
            {'type': 'text', 'content': 'The song of the Philippine Isles spreads to the four corners.'},
            {'type': 'text', 'content': 'The coconut groves cast their shadows upon the heart like the tide.'},
            {'type': 'text', 'content': '(Note: The Philippine Isles—an archipelago of more than seven thousand islands.)'},
            {'type': 'text', 'content': '(Coconut groves: the emblematic trees of the Philippines, found along every coast, their presence a symbol of island beauty.)'},
            {'type': 'text', 'content': '(7)'},
        ]
    },
    '03-kuala-lumpur': {
        'title': 'Cloud-Girt Genting, Twin Towers Aflame',
        'subtitle': 'A drive through the clouds to a mountain paradise, and twin towers piercing the sky.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Malaysia — Cloud-Girt Genting, Twin Towers Aflame'},
            {'type': 'text', 'content': 'We drove through the clouds, climbed to the summit, and there beheld a fairyland. The twin towers, soaring across the sky, glittered with silver light—a scene that lingers still in my mind\'s eye.'},
            {'type': 'text', 'content': 'Kuala Lumpur is the capital and largest city of Malaysia, a metropolis of great influence in Southeast Asia.'},
            {'type': 'text', 'content': (
                'Genting Highlands is a place no visitor to Malaysia should miss. At an elevation of two thousand '
                'metres, it boasts a vast entertainment complex, grand hotels, every manner of dining and gaming, '
                'and—most wondrous of all—a replica of the legendary Penglai Fairyland, a paradise of Taoist '
                'immortals amid the clouds. In 2001, a relative drove us up to this celestial retreat.'
            )},
            {'type': 'text', 'content': 'Genting Highlands Hotel | Our Relative\'s Car | View from the Heights'},
            {'type': 'text', 'content': 'Penglai Fairyland at Genting | The Eight Immortals Crossing the Sea | The Character "Longevity"'},
            {'type': 'text', 'content': '"Destiny" | "Guan Yin" (Goddess of Mercy)'},
            {'type': 'text', 'content': 'Petronas Twin Towers | Twin Towers District | Kuala Lumpur City Centre'},
        ]
    },
    '04-penang': {
        'title': 'A Kinsman\'s Journey to Penang',
        'subtitle': 'Travelling far to Penang for family ties, and wandering through ancient lanes to savour its charms.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Penang — A Kinsman\'s Journey to Penang'},
            {'type': 'text', 'content': 'I travelled far to Penang to renew family bonds, and roamed its ancient alleyways to drink in its unique character.'},
            {'type': 'text', 'content': (
                'Penang is one of the thirteen states of Malaysia, lying off the northwest coast of the peninsula. '
                'It is the country\'s third largest city. Betel-nut palms grow everywhere on the island, giving '
                'it both its name and its character. It is a place of singular charm—a city of captivating beauty, '
                'often called the "Oriental Garden." Here one finds the old alley where the film \'A Tale of Two '
                'Cities\' was shot, and the curious architectural wonder of houses-within-houses.'
            )},
            {'type': 'text', 'content': 'In 2014, my family and I visited Penang for the first time, to see relatives and to explore this remarkable city.'},
            {'type': 'text', 'content': 'Unique Architecture | Penang City Centre | City Centre Hotel'},
            {'type': 'text', 'content': 'House-within-a-House | Penang City Centre | Penang City Nightscape'},
            {'type': 'text', 'content': 'Film Set Alley — "A Tale of Two Cities" | Penang\'s Characterful Little Streets'},
            {'type': 'text', 'content': 'An Artisan Bakery'},
            {'type': 'text', 'content': '.'},
        ]
    },
    '05-vietnam': {
        'title': 'Starlit Seas: A Cruise to Vietnam',
        'subtitle': 'Riding the emerald waves beneath a starry sky, bound for the legendary bay of Ha Long.',
        'subtitle_zh': '山光明媚，水色秀麗。藍天綠島與碧海交織的人間美景。',
        'blocks': [
            {'type': 'text', 'content': 'A Voyage to Vietnam — Starlit Seas, a Cruise to Vietnam'},
            {'type': 'text', 'content': (
                'Vietnam lies on the eastern side of the Indochinese Peninsula in Southeast Asia, its coast '
                'washed by the South China Sea. It is a multi-ethnic nation whose principal people are the Kinh. '
                'In 2001, my eldest son treated us to a voyage aboard the SuperStar Virgo, a colossal cruise '
                'liner bound for Ha Long Bay.'
            )},
            {'type': 'text', 'content': (
                'The SuperStar Virgo was then the largest cruise ship in Asia—thirteen decks high, covering the '
                'area of twelve football fields, and able to accommodate 2,800 passengers. She belonged to '
                'Star Cruises of Singapore and enjoyed a splendid reputation the world over.'
            )},
            {'type': 'text', 'content': 'The SuperStar Virgo | A Photograph with the Cruise Line\'s Senior Officer'},
            {'type': 'text', 'content': 'Sixth-Floor Lobby Lifts | Sixth-Floor Lobby Lifts | Ninth-Floor German Bar'},
            {'type': 'text', 'content': 'Tenth-Floor Observation Deck | Twelfth-Floor Swimming Pool | Thirteenth-Floor Children\'s Pool'},
            {'type': 'text', 'content': (
                'The chefs performed culinary feats before our eyes; I had breakfast with my little granddaughter. '
                'And then we reached Ha Long Bay, in northern Vietnam, and I understood at once why it is called '
                'the "Bay of the Descending Dragon." The hills rise from the water in exquisite shapes, the '
                'colours are soft and luminous—emerald islands against a sky of purest blue. They say it rivals '
                'Guilin\'s landscape. I believe it.'
            )},
            {'type': 'text', 'content': (
                'Ha Long Bay belongs to the city of Ha Long in Quang Ninh Province. We watched performances '
                'of Vietnamese folk customs and a delightful show by local musicians and dancers.'
            )},
            {'type': 'text', 'content': 'Ha Long Bay | Ha Long Park | Vietnamese Folk Scene'},
            {'type': 'text', 'content': 'Ha Long Street View | A Corner of the Street | Ha Long — "Guilin on the Sea"'},
            {'type': 'text', 'content': 'Guilin-like Landscape | Splendid Performances | Solo Singer | Instrumental Solo'},
        ]
    },
    '06-korea': {
        'title': 'In the Footsteps of Dae Jang-geum: Korea\'s Charms',
        'subtitle': 'In search of the legendary physician\'s footsteps, roaming through Korea\'s ancient and modern wonders.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Korea — In the Footsteps of Dae Jang-geum'},
            {'type': 'text', 'content': 'The Republic of Korea, commonly called South Korea, lies on the southern half of the Korean Peninsula in East Asia. Its capital is Seoul—a vibrant, modern city and a thriving capitalist democracy.'},
            {'type': 'text', 'content': 'I went to Korea to find the actual filming locations of \'Dae Jang-geum,\' and to wander through the country\'s ancient and modern marvels.'},
            {'type': 'text', 'content': 'Part One: Visiting the filming set of the Korean drama \'Dae Jang-geum.\''},
            {'type': 'text', 'content': 'The drama was directed by Lee Byung-hoon—a stirring historical epic about a royal physician. Lee Young-ae played the lead,'},
            {'type': 'text', 'content': 'and Ji Jin-hee the male lead. The series became a sensation across Asia, winning the highest ratings in Korea and captivating audiences in China, Hong Kong, Macau, Taiwan, Singapore, and beyond. And so,'},
            {'type': 'text', 'content': 'in 2005, I joined a tour group to Seoul and visited the film set. To stand on the very ground where the drama was shot—to see it with one\'s own eyes—is to believe.'},
            {'type': 'text', 'content': 'Fellow Tourists at the Palace Gate | Lee Young-ae as the Female Lead'},
            {'type': 'text', 'content': 'Tourists in Traditional Hanbok Costume | Ji Jin-hee as the Male Lead'},
            {'type': 'text', 'content': '1. Hanbok 2. Palace & Courtyard 3. Grand Hall 4. Royal Kitchen | 1. Fish Gate 2. Archery Ground 3. Taepyeong Hall | (Part Two) Presidential Office, Changdeok Palace, Seoul city scenes'},
            {'type': 'text', 'content': 'Cheongwadae — The Blue House (Presidential Office of South Korea)'},
            {'type': 'text', 'content': 'Roofed in blue-grey tiles, backed by Bukaksan Mountain, it blends the dignity of a traditional palace with the bearing of a modern seat of power.'},
            {'type': 'text', 'content': 'Cheongwadae (Blue House) | Changdeokgung (Secret Garden Palace)'},
            {'type': 'text', 'content': '1. Presidential Office 2. Grand Drum Pavilion 3–4. City Centre  | 1. The "Clear Heart, Righteous Conduct" Pavilion 2. Cherry Blossoms 3–4. Ferry Terminal'},
        ]
    },
    '07-new-zealand': {
        'title': 'New Zealand: A Feast for the Eyes',
        'subtitle': 'A month of quiet contentment in Auckland, with wide-eyed wonder at its museums, temples, and curious local tales.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Auckland, New Zealand — A Feast for the Eyes'},
            {'type': 'text', 'content': (
                'New Zealand lies in the southern Pacific Ocean, between the Antarctic and the Equator, '
                'comprising two main islands and a scattering of smaller ones. Its climate is temperate maritime, '
                'with modest seasonal variation.'
            )},
            {'type': 'text', 'content': (
                'The seasons are the reverse of those in Hong Kong, being in the Southern Hemisphere. A twelve-hour '
                'flight from Hong Kong brings one to Auckland.'
            )},
            {'type': 'text', 'content': (
                'In January 2012, my wife and I travelled to Auckland, on the North Island, to visit our third son '
                'and his family. We stayed a month, living a quiet and contented life. Auckland is a coastal city '
                'consistently ranked among the world\'s three most liveable cities. It is New Zealand\'s largest '
                'city and port, the nation\'s economic and cultural heart. The Chinese have been settling here for '
                'over 160 years, and Auckland now holds the largest Chinese population in the country.'
            )},
            {'type': 'text', 'content': (
                'Our daughter-in-law drove us to the Auckland War Memorial Museum, often called simply the '
                'Auckland Museum. It stands on a vast lawn like a great green carpet. The museum is one of the '
                'country\'s most important cultural institutions—a "touchstone of New Zealand\'s spirit and culture," '
                'as it has been described. Opened in 1929, it houses a remarkable collection spanning military '
                'history, natural history, and cultural artefacts across three floors.'
            )},
            {'type': 'text', 'content': (
                'Next we saw the Sky Tower, built in 1996—an observation and broadcast tower rising 328 metres, '
                'the tallest structure in the Southern Hemisphere and the thirteenth tallest in the world. '
                'It has become Auckland\'s iconic landmark. A revolving restaurant crowns the tower. Every Christmas, '
                'dazzling fireworks light up the sky above the Sky Tower—truly a scene of "fire trees and silver '
                'flowers lighting up the night." What a spectacle!'
            )},
            {'type': 'text', 'content': (
                'The Auckland Domain is the city\'s oldest and most historic park, lying in the heart of the '
                'city, a peaceful retreat for its citizens. Lush lawns, ancient trees, and blooming flowers '
                'greet every visitor, and few can resist the serene, unhurried atmosphere.'
            )},
            {'type': 'text', 'content': (
                'The Domain covers eight hundred hectares (some eighty thousand mu) right in Auckland\'s heart. '
                'It offers flower gardens (including a remarkable cactus collection), a botanical garden, rest '
                'areas, and a children\'s playground. I was amused to photograph a huge water tank—over two '
                'metres tall—for visitors to wash their hands, a sign that the park takes hygiene seriously. '
                'I also noticed a volunteer tirelessly trimming the plants, asking nothing in return.'
            )},
            {'type': 'text', 'content': (
                'We also visited the Fo Guang Shan Buddhist Temple in North Auckland. Our daughter-in-law drove '
                'us to East Tamaki to see this magnificent monastery—the largest Buddhist temple in New Zealand. '
                'Built in the Tang Dynasty style, with grey-green glazed tiles, deep red stone pillars, and '
                'latticed windows, it radiates solemn grandeur and quiet dignity. The complex includes the Great '
                'Hero Hall, the Great Compassion Hall, a bell tower, a drum tower, meditation halls, and '
                'expansive courtyard gardens.'
            )},
            {'type': 'text', 'content': (
                'In 1991, the Venerable Master Hsing Yun, founder of the Fo Guang Shan order, was invited to '
                'New Zealand. His vision of a temple in Auckland was finally realised in 2007.'
            )},
            {'type': 'text', 'content': 'I gathered many interesting observations during my stay in Auckland. Let me share a few tales:'},
            {'type': 'text', 'content': '【Of Police and Thieves】'},
            {'type': 'text', 'content': (
                'First, the police: you rarely see them anywhere in Auckland—perhaps they have no foot patrols. '
                'My son managed a petrol station, and people repeatedly drove off without paying. He reported '
                'it to the police, who said they would look into it within a week. A week passed—and nothing '
                'came of it. Another family reported a missing child, but after a week the police had still not '
                'found her. Filing a report, it seems, is often an exercise in futility.'
            )},
            {'type': 'text', 'content': (
                'As for thieves: they steal in every imaginable way. But if you so much as threaten a thief with '
                'a weapon, you may be charged with intimidation. One Indian shopkeeper who tried to defend his '
                'property was arrested for assault. And so on…'
            )},
            {'type': 'text', 'content': '【Moving Houses】'},
            {'type': 'text', 'content': (
                'Had I not seen it with my own eyes, I would not have believed it possible: houses that can be '
                'moved. Outside Auckland\'s high-rise core, the towns and countryside consist entirely of single-story '
                'dwellings. These can be shifted relatively easily—a feat of modern engineering that I found '
                'utterly fascinating.'
            )},
            {'type': 'text', 'content': '【Mailboxes by the Roadside】'},
            {'type': 'text', 'content': (
                'Auckland\'s population is about 4.3 million. Since houses in the towns and countryside are all '
                'single-story, and each area is sparsely populated and spread out, the postal service places rows '
                'of mailboxes along the roadside for each neighbourhood.'
            )},
            {'type': 'text', 'content': '【Chinese New Year Flower Market and Street Bazaar】'},
            {'type': 'text', 'content': (
                'There are about 247,000 Chinese in Auckland, making up 69.1% of the city\'s Chinese population. '
                'Though there is no official Chinatown, the community organizes festive events. Our daughter-in-law '
                'took us to the annual Chinese New Year Flower Market—a sea of people, with a festive din filling '
                'the air. We also visited the weekend markets in the towns and countryside: bustling, lively, '
                'and full of character.'
            )},
            {'type': 'text', 'content': (
                'There is a China Town supermarket in Auckland, and every department store carries a full range '
                'of Chinese goods.'
            )},
        ]
    },
    '08-usa': {
        'title': 'Fair Sights, Soaring Spirits: Travels in America',
        'subtitle': 'Eighteen days across five great American cities, from Chicago to New York, a family pilgrimage of pride and wonder.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to America — Fair Sights, Soaring Spirits'},
            {'type': 'text', 'content': (
                'The Master said in the Analects: "The wise are active, the benevolent still; the wise find joy, '
                'and the benevolent endure." How this rang true when, in 2017, my wife and I accompanied our eldest '
                'son and his family to the United States for our grandson\'s graduation from Davidson College in '
                'North Carolina. Seizing the occasion, my son led our party of seven on a grand tour of five great '
                'American cities: Chicago, Charlotte, Washington, Philadelphia, and New York.'
            )},
            {'type': 'text', 'content': 'It was a journey of eighteen days.'},
            {'type': 'text', 'content': '【Chicago】'},
            {'type': 'text', 'content': (
                'We flew Cathay Pacific and landed in Chicago, the "Windy City," situated on the southern shore of '
                'Lake Michigan. It is America\'s third largest city, a global financial centre, and a crucible of '
                'culture and education, home to the world-class University of Chicago. We visited Lake Michigan, '
                'Grant Park, the Cloud Gate, the Art Institute, and the city centre.'
            )},
            {'type': 'text', 'content': u'\u200b'},
            {'type': 'text', 'content': 'Cloud Gate — "The Bean"'},
            {'type': 'text', 'content': (
                'Cloud Gate is a marvel of ingenuity: 168 stainless steel plates welded together, measuring '
                '10 by 20 by 13 metres and weighing 100 tons. Its mirror-polished surface reflects the surrounding '
                'buildings, people, and sky—a "magic mirror" and one of Chicago\'s most beloved landmarks.'
            )},
            {'type': 'text', 'content': u'\u200b\u200b'},
            {'type': 'text', 'content': '【Charlotte】'},
            {'type': 'text', 'content': (
                'From Chicago we flew to Charlotte, the largest city in and the capital of North Carolina. '
                'Here we attended our grandson\'s graduation from Davidson College, founded in 1837 and one of '
                'the finest liberal arts colleges in America. This was the chief purpose of our journey. Davidson '
                'ranks ninth among national liberal arts colleges—a small, elite institution that attracts the '
                'brightest students. It is also the alma mater of NBA star Stephen Curry. Our grandson had already '
                'been admitted to Columbia University\'s financial engineering master\'s programme. We swelled '
                'with pride at the diligence and ambition of the younger generation.'
            )},
            {'type': 'text', 'content': '【Washington, D.C.】'},
            {'type': 'text', 'content': (
                'Washington, District of Columbia—the capital of the United States, named for George Washington, '
                'the first president. We visited the White House, Capitol Hill, the Lincoln Memorial (built in '
                'honour of the sixteenth president), the Washington Monument (for the first president), the '
                'Washington Obelisk, the Department of Agriculture, the National Mall, Washington\'s Chinatown, '
                'and the venerable George Washington University (alma mater of China\'s Foreign Minister Wang Yi).'
            )},
            {'type': 'text', 'content': 'The White House | Lincoln Memorial | Washington Monument'},
            {'type': 'text', 'content': 'The Capitol | Department of Agriculture | Washington Obelisk'},
            {'type': 'text', 'content': 'National Mall | Washington Chinatown | Historic George Washington University'},
            {'type': 'text', 'content': 'George Washington University Campus | The Stone Steps Where a Film Was Shot'},
            {'type': 'text', 'content': 'Philadelphia Cityscape | Philadelphia City Hall | Philadelphia City Hall'},
            {'type': 'text', 'content': 'Liberty Bell Centre | Liberty Bell Centre | Philadelphia City Centre'},
            {'type': 'text', 'content': 'Beautiful City | City Centre | Beautiful City'},
            {'type': 'text', 'content': '【New York】'},
            {'type': 'text', 'content': (
                'New York lies at the mouth of the Hudson River in southeastern New York State, on the Atlantic '
                'coast. It is the largest city and port in the United States,'
            )},
            {'type': 'text', 'content': (
                'a global centre of economics, commerce, finance, media, politics, education, and entertainment.'
            )},
            {'type': 'text', 'content': (
                'It is America\'s financial capital and the world\'s; it is the diplomatic capital of the world, '
                'home to the United Nations headquarters.'
            )},
            {'type': 'text', 'content': (
                'We spent four days in New York. We toured the United Nations, visited the Empire State Building, '
                'Wall Street, the Manhattan financial district, Chinatown, and Brookfield Place. We took a ferry '
                'to see the Statue of Liberty, and made a point of visiting Columbia University.'
            )},
            {'type': 'text', 'content': 'Visiting the United Nations: founded in 1945, its headquarters in New York'},
            {'type': 'text', 'content': (
                'was completed in 1952. One must register in advance, present a passport and visa, and pass '
                'security before entering the grand UN plaza, the exhibition halls, the General Assembly, and '
                'the Security Council. To sit in the very seats of the United Nations was an unforgettable honour.'
            )},
            {'type': 'text', 'content': 'UN Building | UN Headquarters Entrance | UN Plaza | UN Plaza'},
            {'type': 'text', 'content': 'United Nations Headquarters | UN Security Council Chamber'},
            {'type': 'text', 'content': 'In the General Assembly Seats | At the Security Council | The Five-Star Red Flag of China at the UN'},
            {'type': 'text', 'content': '(Part Two) The Empire State Building and Liberty Island'},
            {'type': 'text', 'content': 'Wall Street | Global Financial Centre | Manhattan Financial District'},
            {'type': 'text', 'content': 'Manhattan Financial District | Manhattan | Times Square | A New York Street'},
            {'type': 'text', 'content': '(Part Four) New York\'s Chinatown: now spreading across 45 streets, covering over four square kilometres, home to some 800,000 Chinese, with four Chinatowns and ten Chinese communities.'},
            {'type': 'text', 'content': 'New York Chinatown | Chinatown | The Fujian Association Building on This Street'},
            {'type': 'text', 'content': '(Part Five) The World Trade Center Twin Towers. These 110-storey giants, called the "Twin Stars," once dominated the financial district. The memorial site, called Ground Zero, marks where the towers fell on 9/11—two vast, square reflecting pools with cascading water, their rims inscribed with the names of the fallen.'},
            {'type': 'text', 'content': 'World Trade Center Twin Towers | The 9/11 Attack'},
            {'type': 'text', 'content': 'Ground Zero — The sites of Towers A and B, now two vast square pools with flowing water.'},
            {'type': 'text', 'content': 'The names of the victims are inscribed around the pools.'},
            {'type': 'text', 'content': '【Columbia University】'},
            {'type': 'text', 'content': (
                'Columbia University, founded in 1756, is the fifth oldest university in the United States and '
                'fifth in national ranking—one of the most prestigious in the world (16th globally in 2019). '
                'It counts 98 Nobel laureates among its alumni; its engineering school alone has produced 22.'
            )},
            {'type': 'text', 'content': (
                'Our grandson Lin Manshan earned a Master of Science from Columbia\'s Engineering School. '
                'In 2017, he published a paper in IEEE titled "Applying Sports Analytics to Financial Trading."'
            )},
            {'type': 'text', 'content': (
                'On 11 December 2017, the IEEE invited him to present at the Global IEEE 2017 Financial Data '
                'Application Forum in Taiwan. All other presenters held doctorates. When the moderator announced '
                'the youngest speaker of the conference, the hall erupted in applause.'
            )},
            {'type': 'text', 'content': 'Columbia University Campus | The Global Financial Data Application Forum Presentation'},
            {'type': 'text', 'content': 'University Auditorium | Columbia Engineering School | Law School'},
        ]
    },
    '09-macau': {
        'title': 'Macau, Again and Again',
        'subtitle': 'Countless crossings of the Hong Kong-Zhuhai-Macau Bridge to a city of layered memories.',
        'blocks': [
            {'type': 'text', 'content': 'A Journey to Macau — Macau, Again and Again'},
            {'type': 'text', 'content': (
                'Macau lies on the western shore of the Pearl River Delta in southern China. It returned to '
                'Chinese sovereignty in December 1999, becoming the Macau Special Administrative Region. '
                'The territory comprises the Macau Peninsula, Taipa, and Coloane (the latter two now joined as '
                'one island). It is a free port, a world tourism and leisure centre, and one of the world\'s '
                'four great gambling destinations. Its light industries, tourism, hotels, and casinos have kept '
                'it prosperous and vibrant.'
            )},
            {'type': 'text', 'content': 'Since 2000, I have lost count of how many times I have crossed the Hong Kong–Zhuhai–Macau Bridge to this singular city.'},
            {'type': 'text', 'content': (
                'I have visited with family, accompanied relatives, travelled with students and friends, led '
                'groups on study tours, and attended festive celebrations of local associations. Before the '
                'bridge was built, we always went by ferry—a very convenient passage.'
            )},
            {'type': 'text', 'content': (
                'Part One: Sightseeing in Macau—the Legislative Assembly Building, the Office of the Ministry '
                'of Foreign Affairs, the Lotus Flower gifted by the State Council, the Provisional Municipal '
                'Council, the Kun Iam statue, the new harbour observation deck, the Macau–Taipa Bridge, '
                'the wrought-iron sculpture, the Ruins of St. Paul\'s, A-Ma Temple, the ferry pier, the '
                'churches, the Maritime Museum, and the Taipa Exhibition Centre.'
            )},
            {'type': 'text', 'content': 'Hong Kong–Zhuhai–Macau Bridge Port | Legislative Assembly | Office of the Ministry of Foreign Affairs'},
            {'type': 'text', 'content': 'Lotus Square (2000) | Ministry of Foreign Affairs (2000) | Provisional Municipal Council (2000)'},
            {'type': 'text', 'content': 'Macau–Taipa Bridge (2000) | Observation Deck (2000) | The Iron Sculpture Commissioned by the Governor for MOP 6 Million (2000)'},
            {'type': 'text', 'content': ','},
            {'type': 'text', 'content': 'Ruins of St. Paul\'s (2000) | City Centre (2000) | Lotus Square'},
            {'type': 'text', 'content': 'Ruins of St. Paul\'s | A-Ma Temple | Macau Ferry Pier'},
            {'type': 'text', 'content': 'Church | Maritime Museum | Taipa Exhibition Centre | (Part Two) The magnificent Lisboa, Venetian, and MGM hotels; a group visit to the Macau Nei Keng Village Association.'},
            {'type': 'text', 'content': 'Hotel Lisboa | Hotel Lisboa | The Venetian Macau'},
            {'type': 'text', 'content': 'The Venetian | MGM Macau | Nei Keng Village Association Group Visit'},
            {'type': 'text', 'content': '(Part Three) Visiting Macau Zhongya International Travel Ltd. and Baise Jinlian Real Estate Development Ltd.'},
            {'type': 'text', 'content': (
                'We were graciously hosted by Managing Director Xu Fengqing and his wife (Xu was once my student). '
                'They showed us the newer attractions of Macau. In the evening, we admired the beautiful lights '
                'of the bustling Sands Plaza. The Xus treated us to dinner at a famous restaurant, "Chen Old '
                'Lady\'s Shunde Cuisine."'
            )},
            {'type': 'text', 'content': 'Zhongya International Travel Ltd. | Dinner Hosted by Xu Fengqing | Sands Plaza'},
            {'type': 'text', 'content': 'Sands Plaza Night View | Sands Plaza | Sands Casino'},
            {'type': 'text', 'content': '(Part Four) A group of teachers and alumni from Xiamen No.10 High School, led by a local host, visited the magnificent A-Ma Temple (also called the Goddess Temple). Perched on Diecshitang Mountain in Coloane, it covers 7,000 square metres—the largest temple in Macau, built at a cost of MOP 200 million in the southern Fujian style. Its grand staircase, magnificent ornamental gate, white jade altar, dressing pavilion, bell and drum towers, and the imposing main hall with carved dragons and golden tiles—all bear witness to a splendid heritage.'},
            {'type': 'text', 'content': 'Within, the temple is a blaze of carved beams and gilded pillars. A three-metre statue of the Goddess Mazu, in phoenix crown and embroidered cape, gazes with serene compassion.'},
            {'type': 'text', 'content': 'The Majestic A-Ma Temple | The Grand Staircase, Over Sixty Metres Long | The Main Hall'},
            {'type': 'text', 'content': 'Dragon-Carved Pillars | The Ornate Interior | Lunch Hosted by Classmate Xu Fengqing for Teachers and Students'},
        ]
    },
    '10-kinmen': {
        'title': 'Record of a Ramble in Kinmen',
        'subtitle': 'A thirty-minute ferry ride across the strait from Xiamen lands one in a different world—Kinmen, the ancient isle of Wu-zhou.',
        'blocks': [
            {'type': 'text', 'content': 'A Ramble in Kinmen — Record of a Ramble in Kinmen'},
            {'type': 'text', 'content': 'Kinmen is an outlying island of Taiwan, known in ancient times as Wu-zhou. It lies to the east of Xiamen. In 2017,'},
            {'type': 'text', 'content': (
                'my family and I took the passenger ferry from Xiamen\'s Wutong Port to Kinmen, a mere '
                'thirty-minute crossing across the narrow strait.'
            )},
            {'type': 'text', 'content': (
                'When you step into the Kinmen Shuitiong Passenger Service Centre, the first thing that greets '
                'you is the sign: "Kinmen Welcomes You!" We visited Juguang Tower, the island\'s landmark—a '
                'three-storey pavilion modelled after the ancient Qilin Pavilion, majestic and imposing. We also '
                'toured Kinmen National Park and took in the island\'s characteristic sights.'
            )},
            {'type': 'text', 'content': 'Xiamen Wutong Port Passenger Centre | Kinmen Shuitiong Port Centre | Kinmen\'s Famous Kaoliang Liquor'},
            {'type': 'text', 'content': 'Watchtower | Kinmen Landmark: Juguang Tower | Juguang Tower'},
            {'type': 'text', 'content': 'Kinmen National Park | Zhaishan Tunnel | Kinmen Air-Raid Shelter'},
            {'type': 'text', 'content': 'Aircraft Display | Artillery Cluster One | Artillery Cluster Two'},
        ]
    },
}


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
        'author': zh_data['author'],
        'author_en': 'Lin Hua',
        'blocks': en_blocks,
        'stats': zh_data['stats'],
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
        if aid in TRANSLATIONS:
            art['en'] = TRANSLATIONS[aid]['title']
            updated += 1
            # Also update chapter articles
            for ch in master.get('chapters', []):
                for ca in ch.get('articles', []):
                    if ca['id'] == aid:
                        ca['en'] = TRANSLATIONS[aid]['title']
                        if 'subtitle' in TRANSLATIONS[aid]:
                            ca['en_subtitle'] = TRANSLATIONS[aid]['subtitle']

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

        if article_id in TRANSLATIONS:
            en_translation = TRANSLATIONS[article_id]
            en_data, en_sub = generate_en_article(article_id, zh_data, en_translation)
            en_path = os.path.join(BOOK_DIR, f'en-{article_id}.json')
            with open(en_path, 'w', encoding='utf-8') as f:
                json.dump(en_data, f, ensure_ascii=False, indent=2)

            # Update zh_data EN title and subtitle
            zh_data['en'] = en_translation['title']
            if en_sub:
                zh_data['en_subtitle'] = en_sub[:60]
            # Also patch ZH subtitle (金句) if provided
            if 'subtitle_zh' in en_translation:
                zh_data['subtitle'] = en_translation['subtitle_zh'][:60]

            with open(zh_path, 'w', encoding='utf-8') as f:
                json.dump(zh_data, f, ensure_ascii=False, indent=2)

            print(f'  ✓ en-{article_id}.json — {en_translation["title"]}')
        else:
            print(f'  - {article_id}: translation pending')

    # Update master data.json with EN info
    update_master_en_info(BOOK_DIR)

    print(f'\nDone. {len([k for k in TRANSLATIONS])} articles with EN info.')


if __name__ == '__main__':
    main()
