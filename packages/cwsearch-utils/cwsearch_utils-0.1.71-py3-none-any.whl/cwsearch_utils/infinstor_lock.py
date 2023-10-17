import datetime
import tempfile
import json
import os
from cwsearch_utils import infinstor_dbutils
import gzip
import shutil
import base64
import numpy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
else:
    S3Client = object
    
def set_start(s3client, bucket, prefix, infinstor_time_spec):
    import botocore
    # this is not really a locking mechanism
    status_object_name = f"{prefix}/index/{infinstor_time_spec}/names.csv.creating"
    try:
        metadata = s3client.head_object(Bucket=bucket, Key=status_object_name)
        creation_time = metadata['LastModified']
        tnow = datetime.datetime.utcnow()
        delta = tnow - creation_time
        if delta.total_seconds() > 900:
            print(f"Status object {creation_time} older than 900 seconds {tnow} for {infinstor_time_spec}. This invocation continuing ..")
            return True
        else:
            print(f"Status object {creation_time} less than 900 seconds old {tnow} for {infinstor_time_spec}. This invocation exiting ..")
            return False
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"{status_object_name} does not exist. This invocation creating status object and continuing..")
        else:
            print(f"Caught {e} while reading {status_object_name}. This invocation exiting..")
            return False

    fd, tfile = tempfile.mkstemp()
    try:
        response = s3client.upload_file(tfile, bucket, status_object_name)
        print(f"{status_object_name} does not exist. This invocation successfully created status object {status_object_name} and continuing..")
        return True
    except botocore.exceptions.ClientError as e:
        print(f"Caught {e} while creating status file {status_object_name}. This invocation exiting..")
        return False

def process_full_req(sl, rv):
    # fullreq,{dt.timestamp()},{username},{rest},{cw_url},{emsg}
    name = sl[2].strip()
    dmsg = base64.b64decode(sl[5].strip()).decode('ascii')
    if name in rv:
        rv[name].append((sl[1], sl[3], sl[4], dmsg))
    else:
        rv[name] = [(sl[1], sl[3], sl[4], dmsg)]

def process_embedding(sl, names_rv, embeddings_rv):
    import pickle
    # embedding,{dt.timestamp()},{username},{cw_url},{eann},{emsg},{eem}
    print(f"process_embedding: Entered. len(sl)={len(sl)}", flush=True)
    dann = base64.b64decode(sl[4].strip()).decode('ascii') # annotation
    dmsg = base64.b64decode(sl[5].strip()).decode('ascii') # message
    demb = pickle.loads(base64.b64decode(sl[6].strip())) # embedding
    name = sl[2].strip()
    embeddings_rv.append((sl[1], name, dann, dmsg, sl[3], demb))
    if name in names_rv:
        names_rv[name].append((sl[1], dann, dmsg, sl[3]))
    else:
        names_rv[name] = [(sl[1], sl[3], sl[4], dmsg)]

def load_from_db(fn):

    fnu = fn[:-3]
    with gzip.open(fn, 'rb') as f_in:
        with open(fnu, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"load_from_db: Decompressed {fn} to {fnu}")

    rv = {}
    rv1 = []
    with open(fnu, 'r') as f_in:
        for line in f_in:
            sl = line.split(',')
            line_type = sl[0].strip()
            if line_type == 'fullreq':
                process_full_req(sl, rv)
            elif line_type == 'embedding':
                process_embedding(sl, rv, rv1)
            else:
                print(f"load_from_db: Error. Unknown line_type {line_type}", flush=True)
            print(f"load_from_db: len rv {len(rv)}, len rv1 {len(rv1)}", flush=True)
    return rv, rv1

# returns 'NotPresent'|'Creating'|'Ready'|'CreationFailed'
def get_cache_entry(bucket, prefix, infinstor_time_spec, tag, head_only):
    rv1, rv2, _ = get_cache_entry_ext(bucket, prefix, infinstor_time_spec, tag, head_only)
    return rv1, rv2

# returns 'NotPresent'|'Creating'|'Ready'|'CreationFailed', names|None, embeddings|None
def get_cache_entry_ext(bucket, prefix, infinstor_time_spec, tag, head_only):
    import boto3
    import botocore
    from infinstor import infinsnap
    s3client:S3Client = boto3.client('s3', infinstor_time_spec=infinsnap())
    if tag:
        sluggified = infinstor_dbutils.slugify(tag)
        tfname = f"names-{sluggified}.csv.gz"
    else:
        tfname = f"names.csv.gz"
    object_name = f"{prefix}/index/{infinstor_time_spec}/{tfname}"

    print(f'get_cache_entry: object={object_name}, head_only={head_only}')

    if head_only:
        try:
            # The HEAD action retrieves metadata from an object without returning the object itself.
            metadata = s3client.head_object(Bucket=bucket, Key=object_name)
            return 'Ready', {}, []
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print(f"{object_name} does not exist. Trying status object")
            else:
                print(f"Caught {e} while reading {object_name}. Returning NotPresent")
                return 'NotPresent', None, []
    else:
        lfn = f"/tmp/{tfname}" # lfn == local file name
        try:
            s3client.download_file(bucket, object_name, lfn)
            dct, embs = load_from_db(lfn)
            os.remove(lfn)
            return 'Ready', dct, embs
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print(f"{object_name} does not exist. Trying status object")
            else:
                print(f"Caught {e} while reading {object_name}. Returning NotPresent")
                return 'NotPresent', None, []

    status_object_name = f"{prefix}/index/{infinstor_time_spec}/names.csv.creating"
    try:
        # The HEAD action retrieves metadata from an object without returning the object itself.
        metadata = s3client.head_object(Bucket=bucket, Key=status_object_name)
        creation_time = metadata['LastModified']
        tnow = datetime.datetime.utcnow()
        delta = creation_time - tnow
        if delta.total_seconds() > 900:
            print(f"Status object {creation_time} older than 900 seconds {tnow} for {infinstor_time_spec}. CreationFailed..")
            return 'CreationFailed', None, []
        else:
            print(f"Status object {creation_time} less than 900 seconds old {tnow} for {infinstor_time_spec}. waiting..")
            return 'Creating', None, []
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"{status_object_name} does not exist. Returning NotPresent")
            return 'NotPresent', None, []
        else:
            print(f"Caught {e} while reading {status_object_name}. Returning CreationFailed")
            return 'CreationFailed', None, []

