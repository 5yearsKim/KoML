
funcs = {}

from .date_time import funcs as date_time_funcs
funcs.update(date_time_funcs)

from .word_relay import funcs as word_relay_funcs
funcs.update(word_relay_funcs)

from .memo_utils import funcs as memo_utils_funcs
funcs.update(memo_utils_funcs)