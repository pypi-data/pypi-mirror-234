import psycopg2
from sqlalchemy import create_engine, inspect, Table, Column, String, DateTime, MetaData, Text, TIMESTAMP
import pandas as pd
import datetime

def add_history(table_name, data, destination_conf):
    """
    This method is used to add the history of a table and its associated data.
    """
    df = data
    postgres_conn = psycopg2.connect(**destination_conf)
    dest_engine = create_engine("postgresql://", creator=lambda: postgres_conn)
    destination_inspector = inspect(dest_engine)

    metadata = MetaData()

    etl_history = Table(
        "etl_history",
        metadata,
        Column("etl_process", String(255)),
        Column("source_table", String(255)),
        Column("timestamp", DateTime),
    )

    # Check if the etl_history table exists in the destination PostgreSQL database
    if not destination_inspector.has_table("etl_history"):
        # Create the table in the destination PostgreSQL database if it doesn't exist
        etl_history.create(dest_engine)

    
    log_data = {
        "etl_process": f"Transfer data from {table_name} in MySQL to {table_name} in PostgreSQL",
        "source_table": table_name,
        "timestamp": datetime.datetime.now(),
    }
    log_df = pd.DataFrame([log_data])
    log_df.to_sql("etl_history", dest_engine, index=False, if_exists="append")


                
    # Build column-level history for each row in the current table
    for index, row in df.iterrows():
        for column_name, old_value in row.items():
            new_value = old_value  # Replace with the actual new value if needed
            column_history_table_name = f"{table_name}_column_history"

            try:
                etl_column_table_history = Table(
                    column_history_table_name,
                    metadata,
                    Column("table_name", String(255)),
                    Column("row_id", String(255)),
                    Column("column_name", String(255)),
                    Column("old_value", String(255)),
                    Column("new_value", String(255)),
                    Column("timestamp", TIMESTAMP),
                )
                # Check if the etl_history table exists in the destination PostgreSQL database
                if not destination_inspector.has_table(column_history_table_name):
                    # Create the table in the destination PostgreSQL database if it doesn't exist
                    etl_column_table_history.create(dest_engine)
            except Exception as e:
                pass
            

            column_log_data = {
                "table_name": table_name,
                "row_id": index,
                "column_name": column_name,
                "old_value": old_value,
                "new_value": new_value,
                "timestamp": datetime.datetime.now(),
            }
            column_log_df = pd.DataFrame([column_log_data])
            column_log_df.to_sql(column_history_table_name, dest_engine, index=False, if_exists="append")




def connect_to_postgresql(host, user, password, database):
    return psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def update_history_log(data, destination_config):
    
    pg_conn = connect_to_postgresql(**destination_config)
    cursor_pg = pg_conn.cursor()

    # Log changes in history table
    query = f"""
            CREATE TABLE IF NOT EXISTS history_logs (
                id SERIAL PRIMARY KEY,
                record_id INT,  -- ID of the corresponding record in the main table
                change_timestamp TIMESTAMP,
                table_name Text,
                column_name TEXT,
                old_value TEXT,
                new_value TEXT,
                record_type TEXT
            );
            """
    cursor_pg.execute(query)



    for record in data:
        change_timestamp = datetime.now()
        history_query = """
            INSERT INTO history_logs 
            (record_id, change_timestamp, table_name, column_name, old_value, new_value, record_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """


        # Example usage when executing the query:
        cursor_pg.execute(history_query, (
            record.get('record_id'),
            change_timestamp,
            record.get('table_name'),
            record.get('column_name'),
            record.get('old_value'),
            record.get('new_value'),
            record.get('record_type')
        ))
        

    pg_conn.commit()
    print("Updated")