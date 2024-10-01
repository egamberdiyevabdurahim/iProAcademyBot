from datetime import datetime

from queries.for_balance import get_all_active_balance_query, deactivate_balance_by_id_query


async def balance_calculater():
    balances_data = get_all_active_balance_query()  # assuming you have an async version
    for balance in balances_data:
        if balance['ends_at'] < datetime.now().date():
            deactivate_balance_by_id_query(balance['id'])

