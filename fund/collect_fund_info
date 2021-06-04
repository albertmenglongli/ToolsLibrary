import asyncio
import json
import pprint
import re
from functools import cmp_to_key

import aiohttp
import requests
from funcy import first, keep, lmap

code_name_mapping = {
    '005918': "天弘沪深300ETF联接C",
    '002207': "前海开源金银珠宝混合C",
}


def get_code_by_name(search):
    global url, response, data, code
    url = 'http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchAPI.ashx?m=1&key=' + search  #
    response = requests.post(url)
    data = response.json()
    if data['ErrCode'] != 0:
        raise Exception('Bad request')
    datas = data.get('Datas', [])
    item = first(datas)
    if item is None:
        raise Exception(f'Not found for {search}')
    code = item['CODE']
    return code


def cmp_by_gszzl(a: dict, b: dict):
    try:
        a_gszzl = float(a.get('gszzl', '0'))
        b_gszzl = float(b.get('gszzl', '0'))
        if a_gszzl < b_gszzl:
            return -1
        if a_gszzl > b_gszzl:
            return 1
    except Exception:
        # unable to compare
        pass


def parse_to_chinese_readable(data):
    res = {
        '估算增量': "%s%%" % format(data['gszzl']),
        '基金编码': data['fundcode'],
        '基金名称': data['name'],
        '单位净值': data['dwjz'],
        '净值日期': data['jzrq'],
        '估算值': data['gsz'],
        '估值时间': data['gztime'],
    }
    return res


async def get_data(code, future):
    """
    通过基金编码获取估值
    """
    url = 'http://fundgz.1234567.com.cn/js/%s.js' % code
    res = {}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url, ssl=False) as resp:
            try:
                if resp.status == 200:
                    text = await resp.text()
                    data = json.loads(re.match(".*?({.*}).*", text, re.S).group(1))
                    res = data
                elif resp.status == 404:
                    pass
                else:
                    pass
            except Exception as e:
                print(f'failed get estimation for code {code}, {e}')

            future.set_result(res)


async def main():
    # collect all 基金估算数据
    fund_data = []

    tasks = []
    codes = code_name_mapping.keys()
    for _code in codes:
        _future = asyncio.Future()
        _future.add_done_callback(lambda f: fund_data.append(f.result()))
        _task = asyncio.ensure_future(get_data(_code, _future))
        tasks.append(_task)

    for t in asyncio.as_completed(tasks):
        await t

    fund_data = lmap(parse_to_chinese_readable,  # parse to more readable
                     sorted(keep(fund_data),  # remove falsy values, sort by gszzl asc
                            key=cmp_to_key(cmp_by_gszzl)))

    for d in fund_data:
        pprint.pprint(d)


# {'估值时间': '2021-06-04 13:06',
#  '估算值': '1.2319',
#  '估算增量': '-0.82%',
#  '净值日期': '2021-06-03',
#  '单位净值': '1.2420',
#  '基金名称': '前海开源金银珠宝混合C',
#  '基金编码': '002207'}
# {'估值时间': '2021-06-04 13:04',
#  '估算值': '1.4678',
#  '估算增量': '0.48%',
#  '净值日期': '2021-06-03',
#  '单位净值': '1.4607',
#  '基金名称': '天弘沪深300ETF联接C',
#  '基金编码': '005918'}

if __name__ == '__main__':
    asyncio.set_event_loop(None)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = loop.create_future()
    try:
        loop.run_until_complete(main())
    finally:
        try:
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            loop.close()
