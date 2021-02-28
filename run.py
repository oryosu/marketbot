# coding: utf-8

import os
import slackweb
from information import get_moving_average, golden_crossover, dead_crossover, get_fundametals, get_data

def main():
    slack = slackweb.Slack(url=os.environ['SLACKWEB_ANDDATA_MARKETBOT'])
    with open('tosho.list', 'r') as f:
        codes = f.read().splitlines()
    for code in codes:
        attachments = []
        print(code)
        company_name, infos = get_fundametals(code)
        try:
            data = get_data(code)
        except:
            print("ETF?")
            continue
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