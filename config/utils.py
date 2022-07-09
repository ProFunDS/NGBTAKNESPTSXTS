from collections import namedtuple

colors = {'aqua': '#00FFFF', 'black': '#000000',
        'blue': '#0000FF', 'chocolate': '#D2691E',
        'green': '#008000', 'greenyellow': '#ADFF2F',
        'lime': '#00FF00', 'magenta': '#FF00FF',
        'red': '#FF0000', 'orange': '#FFA500',
        'pink': '#FFC0CB', 'purple': '#800080',
        'skyblue': '#87CEEB', 'violet': '#EE82EE',
        'yellow': '#FFFF00', 'yellowgreen': '#9ACD32',
        'lightblue': '#ADD8E6', 'lightyellow': '#FFFFE0',
        'white': '#FFFFFF'}

Pair = namedtuple('Pair', ('id', 'emoji'))

language_roles = {
        'Filipino': Pair(962777083665346670, '🇵🇭'),
        'Chinese': Pair(962777195875553302, '🇨🇳'),
        'Japanese': Pair(962777251219406858, '🇯🇵'),
        'Indonesian': Pair(962777445843468298, '🇮🇩'),
        'Malay': Pair(962777608024625202, '🇲🇾'),
        'Hindi': Pair(962777914804437092, '🇮🇳'),
        'English': Pair(962306631432040509, '🇬🇧'),
        'Spanish': Pair(962307386922655764, '🇪🇸'),
        'Russian': Pair(962759405479292969, '🇷🇺'),
        'French': Pair(962778248880746526, '🇫🇷'),
        'Dutch': Pair(962778328970964992, '🇩🇪'),
        'Portuguese': Pair(962778532268867615, '🇵🇹')}