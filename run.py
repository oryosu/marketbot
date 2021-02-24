# coding: utf-8

import slackweb
from information import get_moving_average, golden_crossover, dead_crossover, get_fundametals, get_datas

def main():
    slack = slackweb.Slack(url=os.environ['SLACKWEB_ANDDATA_MARKETBOT'])
    with open('tosho.list', 'r') as f:
        codes = f.read().splitlines()
    datas = get_datas(codes)
    for code, data in zip(codes, datas):
        print(code, data)
        attachments = []
        company_name, infos = get_fundametals(code)
        series1, series2, series3 = get_moving_average(data)
        if golden_crossover(series1, series2, series3):
            attachment = {"title": company_name,
                          "color": "good",
                          "title_link": "https://stocks.finance.yahoo.co.jp/stocks/detail/?code={}".format(code),
                          "text": "{}".format("\n".join(infos))}
            attachments.append(attachment)
        elif dead_crossover(series1, series2, series3):
            attachment = {"title": company_name,
                          "color": "danger",
                          "title_link": "https://stocks.finance.yahoo.co.jp/stocks/detail/?code={}".format(code),
                          "text": "{}".format("\n".join(infos))}
            attachments.append(attachment)
        else:
            pass
            #attachment = {"title": company_name,
            #              "color": "warning",
            #              "title_link": "https://stocks.finance.yahoo.co.jp/stocks/detail/?code={}".format(code),
            #              "text": "{}".format("\n".join(infos))}
            #attachments.append(attachment)
        if attachments:
            slack.notify(attachments=attachments)
    print("all {} companies were analized".format(len(codes)))


if __name__ == "__main__":
    print('start slackbot')
    main()