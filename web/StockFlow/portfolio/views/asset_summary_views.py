from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
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


def asset_summary_ticker(request):
    # 評価額 = current_price * quantity * exchange_rate
    # F()を使用するとDB内で計算を実行する（ので高速）
    # annotate()を使用するとAssetインスタンスにvalueという仮想フィールドが追加される
    assets = Asset.objects.annotate(
        value=F('current_price') * F('quantity') * F('exchange_rate')
    )

    # ticker ごとに集計
    # assets.values('ticker)でtickerごとにレコードを取得
    # assets.valueの合計をgroupd.total_valueに設定
    grouped = assets.values('ticker').annotate(
        total_value=Sum('value')
    )

    # 全体の総額
    total = sum(item['total_value'] for item in grouped)

    # 割合を追加
    # itemは辞書なので['ratio']が見つからない場合は辞書に追加される
    for item in grouped:
        item['ratio'] = (item['total_value'] / total * 100) if total > 0 else 0

    return render(request, "portfolio/asset_summary_ticker.html", {
        "grouped": grouped,
        "total": total,
    })

