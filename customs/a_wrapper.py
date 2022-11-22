
funcs = {}

from .date_time import funcs as date_time_funcs
funcs.update(date_time_funcs)

from .memo_utils import funcs as memo_utils_funcs
funcs.update(memo_utils_funcs)