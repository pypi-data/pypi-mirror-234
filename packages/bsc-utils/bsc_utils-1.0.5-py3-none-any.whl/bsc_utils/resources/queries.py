from typing import Literal


class ORACLE:

    @staticmethod
    def td_ago(symbol_type: Literal['EXCHANGE', 'SECURITY']):
        return f'''
            SELECT TRADE_DATE FROM {symbol_type}_DAILY
            WHERE {symbol_type}_CODE = :ec
            ORDER BY TRADE_DATE DESC
            OFFSET :os ROWS FETCH NEXT 1 ROW ONLY
        '''

    codes = {
        'SECURITY': 'SELECT DISTINCT(SECURITY_CODE) FROM SECURITIES',
        'EXCHANGE': 'SELECT DISTINCT(EXCHANGE_CODE) FROM EXCHANGE_DAILY'
    }