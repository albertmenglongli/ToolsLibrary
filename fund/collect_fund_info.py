import asyncio
import json
import re
from functools import cmp_to_key
from typing import List

import aiohttp
import uvloop
from funcy import lmap, lsplit
from prettytable import PrettyTable


def cmp_by_gszzl(a: dict, b: dict):
    try:
        a_gszzl = float(a.get('gszzl', '0')) or 0
        b_gszzl = float(b.get('gszzl', '0')) or 0
        if a_gszzl < b_gszzl:
            return -1
        if a_gszzl > b_gszzl:
            return 1
    except (TypeError, Exception) as e:
        # unable to compare
        pass
    return 0


def pretty_print_fund_data(fund_data: List[dict]):
    def parse_to_chinese_readable(_data):
        res: dict = {
            '估算增量': _data['gszzl'],
            '基金编码': _data['fundcode'],
            '基金名称': _data['name'],
            '单位净值': _data['dwjz'],
            '净值日期': _data['jzrq'],
            '估算值': _data['gsz'],
            '估值时间': _data['gztime'],
        }
        return res

    fund_data = lmap(parse_to_chinese_readable, fund_data)

    table_decrease = PrettyTable()
    table_increase = PrettyTable()
    if fund_data:
        for _data in fund_data:
            if _data['估算增量'].startswith('-'):
                if not table_decrease.field_names:
                    table_decrease.field_names = list(_data.keys())
                table_decrease.add_row(_data.values())
            else:
                if not table_increase.field_names:
                    table_increase.field_names = list(_data.keys())
                table_increase.add_row(_data.values())
    table_decrease.align = table_increase.align = 'l'
    if table_decrease.rowcount > 0:
        print(table_decrease)
    if table_decrease.rowcount > 0 and table_increase.rowcount > 0:
        print()  # print a blank line as separator
    if table_increase.rowcount > 0:
        print(table_increase)


async def fetch_data(session, code):
    url = 'http://fundgz.1234567.com.cn/js/%s.js' % code
    res = {}

    timeout = aiohttp.ClientTimeout(total=2)
    try:
        async with session.get(url, ssl=False, timeout=timeout) as resp:
            if resp.status == 200:
                text = await resp.text()
                data = json.loads(re.match(".*?({.*}).*", text, re.S).group(1))
                res = data
    except TimeoutError:
        raise TimeoutError(f'{code}(Timeout)')
    except Exception:
        raise Exception(code)
    if not res:
        raise Exception(code)
    return res


async def main(codes: List[str]):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        fetch_datas = [fetch_data(session, _code) for _code in codes]
        results = await asyncio.gather(*fetch_datas, return_exceptions=True)

    fund_data, exceptions = lsplit(lambda x: not isinstance(x, Exception), results)
    if exceptions:
        print('Failed to get data for', ','.join(map(str, exceptions)))

    pretty_print_fund_data(fund_data=sorted(fund_data, key=cmp_to_key(cmp_by_gszzl)))


if __name__ == '__main__':
    codes = ['002207', '003834', '004241', '005918', '006128',
             '009026', '010685', '161005', '161721', '161724',
             '161725', '163402', '165520', '180012', '400015']

    uvloop.install()
    asyncio.run(main(codes=codes), debug=True)
