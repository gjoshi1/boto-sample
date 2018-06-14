import os

import boto
from boto.s3.key import Key

def upload_to_s3(aws_access_key_id, aws_secret_access_key, file, bucket, key, callback=None, md5=None, reduced_redundancy=False, content_type=None):
    """
    Uploads the given file to the AWS S3
    bucket and key specified.

    callback is a function of the form:

    def callback(complete, total)

    The callback should accept two integer parameters,
    the first representing the number of bytes that
    have been successfully transmitted to S3 and the
    second representing the size of the to be transmitted
    object.

    Returns boolean indicating success/failure of upload.
    """
    try:
        size = os.fstat(file.fileno()).st_size
    except:
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    print(conn)
    bucket = conn.get_bucket(bucket, validate=False)
    print(bucket)
    lst = bucket.list()
    #print(lst.size())
    
    
    k = Key(bucket)
    k.key = "myspace/"+key
    
    print(k.key)
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)

    # Rewind for later use
    file.seek(0)

    if sent == size:
        return True
    return False


AWS_ACCESS_KEY="AWS_ACCESS_KEY"
AWS_ACCESS_SECRET_KEY="AWS_ACCESS_SECRET_KEY"
bucket = 'bucket-name'

file = open('sample.txt', 'r+')

key = file.name


if upload_to_s3(AWS_ACCESS_KEY, AWS_ACCESS_SECRET_KEY, file, bucket, key):
    print 'It worked!'
else:
    print 'The upload failed...'