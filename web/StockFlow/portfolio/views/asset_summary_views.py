from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce
from portfolio.models import Asset

# 資産クラスごとの円グラフ
def asset_summary_class(request):
    assets = Asset.objects.all()

    # 表示順（日本語の自然な順）
    ORDER = [
        'US_STOCK',
        'US_BND',
        'US_MMF',
        'US_CASH',
        'JP_STOCK',
        'JP_FUND',
        'JP_BND',
        'JP_CASH',
    ]

    # 資産クラスごとに評価額(JPY)を集計
    totals = {key: 0 for key in ORDER}
    for a in assets:
        totals.setdefault(a.asset_class, 0)
        totals[a.asset_class] += float(a.valuation_jpy)

    # 英語コード → 日本語ラベル
    LABEL_MAP = {
        'US_STOCK': '外国株',
        'US_BND':   '外国債券',
        'US_MMF':   '外貨建てMMF',
        'US_CASH':  '外貨建て現金',
        'JP_STOCK': '日本株',
        'JP_FUND':  '投資信託',
        'JP_BND':   '国内債券',
        'JP_CASH':  '現金',
    }

    # Chart.js用データ
    labels = [LABEL_MAP[k] for k in ORDER]
    values = [totals[k] for k in ORDER]
    context = {
        'labels': labels,
        'values': values,
    }
    return render(request, 'portfolio/asset_summary_class.html', context)

# 銘柄ごとの集計
def asset_summary_ticker(request):

    # 銘柄ごとに集計
    grouped = {}    # {ticker: {name:"name", "value: 0, "class": "US_STOCK"}}
    total_value = 0
    assets = Asset.objects.all()
    for a in assets:
        grouped.setdefault(a.ticker, {"name":"", "value":0, "class": a.asset_class})
        grouped[a.ticker]["value"] += float(a.valuation_jpy)
        if not grouped[a.ticker].get("name"):
            grouped[a.ticker]["name"] = a.name
        total_value += float(a.valuation_jpy)

    # 割合を追加
    for ticker, data in grouped.items():
        value = data["value"]
        data["ratio"] = (value / total_value * 100) if total_value > 0 else 0
        # {ticker: {name: "name", value: 0, class: "US_STOCK", ratio:10}}

    # 資産クラスごとにソート
    ORDER = [
        'US_STOCK',
        'US_BND',
        'US_MMF',
        'US_CASH',
        'JP_STOCK',
        'JP_FUND',
        'JP_BND',
        'JP_CASH',
    ]
    sorted_items = sorted(
        grouped.items(),
        key = lambda x: ORDER.index(x[1]["class"])
    )
    new_grouped = dict(sorted_items)
    print(new_grouped)

    # Chart.js用にラベルと値のリストを作る
    #labels = list(new_grouped.keys())
    labels = [data["name"] for data in new_grouped.values()]
    values = [data["value"] for data in new_grouped.values()]

    return render(request, "portfolio/asset_summary_ticker.html", {
        "grouped": new_grouped,
        "total": total_value,
        "labels": labels,
        "values": values,
    })


