import os
import json
import urllib.parse
import boto3
import psycopg2

from extraction import extract_text
from analysis import analyze_with_gemini

s3 = boto3.client("s3")

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]


def lambda_handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

    local_path = f"/tmp/{os.path.basename(key)}"
    s3.download_file(bucket, key, local_path)

    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()

    try:
        text = extract_text(local_path)
        result = analyze_with_gemini(text)

        cur.execute(
            "UPDATE documents SET status = %s, result = %s WHERE filename = %s",
            ("done", json.dumps(result), os.path.basename(key)),
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        cur.execute(
            "UPDATE documents SET status = %s, result = %s WHERE filename = %s",
            ("failed", json.dumps({"error": str(e)}), os.path.basename(key)),
        )
        conn.commit()
        raise

    finally:
        cur.close()
        conn.close()

    return {"statusCode": 200}
