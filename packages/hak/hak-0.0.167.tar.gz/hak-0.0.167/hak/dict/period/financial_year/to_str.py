from hak.dict.period.financial_year.make import f as mkfy
from hak.pxyf import f as pxyf

# to_str
f = lambda x: f"{x['start_year']} - {x['final_year']}"

t = lambda: pxyf(mkfy({'start_year': 2022}), '2022 - 2023', f)
