import sys

sys.path.append('../../')

# main.py
from koml import KomlBot, CustomBag
from funcs import show_date, know


# bot = KomlBot()
# bot.learn(['section.xml', 'tags.xml', 'template.xml'])
# bot.converse()

# bag = CustomBag(funcs={'show_date': show_date, 'know': know})
bag = CustomBag(funcs={'know': know})

bot = KomlBot(bag)
bot.learn(['section.xml', 'tags.xml', 'template.xml', 'custom_function.xml'])
bot.converse()