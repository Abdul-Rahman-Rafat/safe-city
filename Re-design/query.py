import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect(r'C:\Users\yassi\Desktop\safecity site new\safe-city\Re-design\instance\SafeCity.db')
cursor = conn.cursor()



# Retrieve the last img_ref from the snapshots table
def re_image_name():
    cursor.execute('SELECT Detection_img_ref FROM snapshots ORDER BY ROWID DESC LIMIT 1')
    last_img_ref = cursor.fetchone()

    if last_img_ref:
        last_img_ref = last_img_ref[0]  # Extract the img_ref value from the tuple
    else:
        last_img_ref = 0  # Set last_img_ref to 0 if it's None (table is empty)

    print("Last img_ref:", last_img_ref)

    # Close the connection
    conn.close()
    return last_img_ref