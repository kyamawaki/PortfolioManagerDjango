from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Asset

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

