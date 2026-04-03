"""
Скрипт полной очистки данных: SQLite + Google Sheets.
Сбрасывает счётчик ордеров на 1000 (первый ордер будет ORD-1001).
"""

import sqlite3
import gspread

DATABASE_FILE = "orders.db"

TABLES_TO_CLEAR = [
    "orders",
    "users",
    "payments",
    "action_log",
    "reviews",
    "pending_states",
    "referrals",
    "bonus_balance",
    "bonus_transactions",
]


def reset_sqlite():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    for table in TABLES_TO_CLEAR:
        c.execute(f"DELETE FROM {table}")
        print(f"  ✅ {table}: удалено {c.rowcount} строк")
    # Сброс счётчика — следующий ордер будет ORD-1001
    c.execute("UPDATE counters SET value = 1000 WHERE name = 'order_number'")
    print(f"  ✅ counters: order_number = 1000")
    # Сброс автоинкрементов
    c.execute("DELETE FROM sqlite_sequence")
    print(f"  ✅ sqlite_sequence сброшены")
    conn.commit()
    conn.close()
    print("SQLite очищен.\n")


def reset_sheets():
    client = gspread.service_account(filename="service_account.json")
    sheet = client.open("popolnyaska_bot").sheet1
    rows = sheet.row_count
    if rows > 1:
        # Удаляем все строки кроме заголовка
        sheet.delete_rows(2, rows)
        print(f"  ✅ Google Sheets: удалено {rows - 1} строк (заголовок сохранён)")
    else:
        print("  ✅ Google Sheets: данных нет")
    print("Google Sheets очищен.\n")


if __name__ == "__main__":
    print("=== СБРОС ДАННЫХ ===\n")
    print("[1/2] SQLite...")
    reset_sqlite()
    print("[2/2] Google Sheets...")
    reset_sheets()
    print("=== ГОТОВО. Следующий ордер: ORD-1001 ===")
