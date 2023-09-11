import requests
import mysql.connector
from api_module import get_scopes
from telegram_bot import send_scopes

# get data using api HackersOne
final_handle_list,final_asset_identifier_list = get_scopes()


# ایجاد اتصال به دیتابیس MySQL
conn = mysql.connector.connect(user='root',
                               password='',
                               host='127.0.0.1',
                               database='test')
cursor = conn.cursor()

# ایجاد جداول براساس لیست final_handle_list
for table_name in final_handle_list:
    table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        asset_identifier VARCHAR(100)
    )
    """
    cursor.execute(table_query)

# لیست final_asset_identifier_list

# گرفتن نام تمام جداول موجود در دیتابیس
cursor.execute("SHOW TABLES")
tables_in_db = [table[0] for table in cursor.fetchall()]

# حذف جداولی که در دیتابیس وجود دارند اما در لیست handle نیستند
for table_name in tables_in_db:
    if table_name not in final_handle_list:
        cursor.execute(f"DROP TABLE {table_name}")

# دیکشنری برای ذخیره داده‌های جدید برای هر جدول
new_tables_data = {}

# درج داده‌های متناظر در جداول با چک کردن وجود داده تکراری
for i, table_name in enumerate(final_handle_list):
    if table_name not in new_tables_data:
        new_tables_data[table_name] = []  # ایجاد لیست جدید برای هر جدول

    for asset_identifier in final_asset_identifier_list[i]:
        # بررسی وجود داده در جدول
        cursor.execute(f"SELECT asset_identifier FROM {table_name} WHERE asset_identifier = %s", (asset_identifier,))
        existing_data = cursor.fetchone()

        # اگر داده تکراری وجود نداشته باشد، آن را درج کنید و به لیست new_tables_data اضافه کنید
        if not existing_data:
            cursor.execute(f"INSERT INTO {table_name} (asset_identifier) VALUES (%s)", (asset_identifier,))
            new_tables_data[table_name].append(asset_identifier)

# گرفتن نام تمام جداول موجود در دیتابیس
cursor.execute("SHOW TABLES")
tables_in_db = [table[0] for table in cursor.fetchall()]

# حذف داده‌هایی که در جداول وجود دارند اما در asset_identifier_list نیستند
for table_name in final_handle_list:
    if table_name in tables_in_db:
        cursor.execute(f"SELECT asset_identifier FROM {table_name}")
        data_in_db = [data[0] for data in cursor.fetchall()]

        for asset_identifier in data_in_db:
            if asset_identifier not in final_asset_identifier_list[final_handle_list.index(table_name)]:
                cursor.execute(f"DELETE FROM {table_name} WHERE asset_identifier = %s", (asset_identifier,))

# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()
# send to telegram
send_scopes(new_tables_data.items())
