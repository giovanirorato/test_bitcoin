# Dividend Data Fetcher

Esse é um projeto novo com o objetivo de pegar dados de ações que pagam dividendos da bolsa brasileira.

Ele utiliza a biblioteca [yfinance](https://pypi.org/project/yfinance/) para coletar informações de dividendos dos tickers da B3.

## Como usar

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Execute o script, que irá buscar automaticamente todas as ações que possuem dividend yield anual de pelo menos 6%:

   ```bash
   python dividend_fetcher.py

   Você pode utilizar os parâmetros `--max-pe` e `--max-payout` para aplicar filtros adicionais de valuation e sustentabilidade dos dividendos.
   ```
