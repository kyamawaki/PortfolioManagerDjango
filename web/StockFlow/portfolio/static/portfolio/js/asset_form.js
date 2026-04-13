// 資産ごとの非表示項目
const HIDE_FIELDS = {
  'US_STOCK': ['average_price_jpy', "average_exchange_rate"],
  'US_BND'  : ['ticker', 'account_type', 'average_price_usd', 'average_price_jpy'],
  'US_MMF'  : ['ticker', 'account_type', 'average_price_usd', 'average_price_jpy'],
  'US_CASH' : ['ticker', 'account_type', 'average_price_usd', 'average_price_jpy', 'average_exchange_rate'],
  'JP_STOCK': ['average_price_usd', 'average_exchange_rate'],
  'JP_FUND' : ['average_price_usd', 'average_exchange_rate'],
  'JP_BND'  : ['ticker', 'account_type', 'average_price_usd', 'average_price_jpy', 'average_exchange_rate'],
  'JP_CASH' : ['ticker', 'account_type', 'average_price_usd', 'average_price_jpy', 'average_exchange_rate'],
};

// アセットクラス変更時の処理
function toggleFieldsByAssetClass() {
  var sel = document.getElementById('id_asset_class');
  if (!sel) return;

  //console.log(sel.value)
  
  var assetClass = sel.value;
  var hideFields = HIDE_FIELDS[assetClass] || [];
  
  // 対象フィールドすべて
  var allFields = [
    "name", 
    "asset_class", 
    "owner", 
    "financial_institution", 
    "account_type", 
    "ticker", 
    "quantity", 
    "average_price_usd", 
    "average_price_jpy", 
    "average_exchange_rate"
  ]
  
  // 各フィールドの表示/非表示を切り替え
  allFields.forEach(function(field) {
    console.log(field);
    var elem = document.getElementById('id_' + field);
    if (elem && elem.closest('p')) {
      var shouldHide = hideFields.includes(field);
      if (shouldHide) {
        elem.closest('p').style.display = 'None';
        elem.readOnly = true;
      }
      else {
        elem.closest('p').style.display = '';
        elem.readOnly = false;
      }
    }
  });

  // ラベルを切り替え
  const assetClassField = document.getElementById('id_asset_class');
  const tickerLabel = document.querySelector("label[for='id_ticker']")
  const quantitylabel = document.querySelector("label[for='id_quantity']")
  const averageExchangeRatelabel = document.querySelector("label[for='id_average_exchange_rate']")
  if(assetClassField.value === "US_BND") {
    quantitylabel.textContent = "保有額面"
    averageExchangeRatelabel.textContent = "取得為替";
  } else if (assetClassField.value === "US_MMF") {
    averageExchangeRatelabel.textContent = "取得為替";
  } else if (assetClassField.value === "JP_STOCK" || assetClassField.value === "JP_FUND") {
    tickerLabel.textContent = "証券コード";
  } else {
    quantitylabel.textContent = "数量"
    averageExchangeRatelabel.textContent = "取得時平均為替レート";
  }
}

// イベントリスナーの追加
document.addEventListener('DOMContentLoaded', function() {
  console.log("come")
  var sel = document.getElementById('id_asset_class');
  if (sel) {
    sel.addEventListener('change', toggleFieldsByAssetClass);
    toggleFieldsByAssetClass();
  }

  //const nameField = document.getElementById('id_name');
  //if (nameField) nameField.focus();
});

