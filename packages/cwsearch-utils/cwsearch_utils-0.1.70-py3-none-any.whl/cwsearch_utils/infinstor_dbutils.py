import sqlite3
import unicodedata
import re

def create_table(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE links(tag, name, timestamp, link, msg, embedding)")
    cur.execute("CREATE INDEX idx_links ON links(tag)")
    con.commit()    

def create_table_if_not_exists(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS links(tag, name, timestamp, link, msg, embedding)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_links ON links(tag)")
    con.commit()    

# sanitizes a tag string so that we can use it as part of a db filename
# e.g. serverlessrepo:applicationId=arn:aws:serverlessrepo:us-east-1:986605205451:applications/InfinStor-Dashboard-Lambdas
# to serverlessrepo_applicationId_arn:aws:serverlessrepo_us-east-1_986605205451_applications_InfinStor-Dashboard-Lambdas
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
