from minio import Minio
import io

client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)

bucket = "test-bucket"

if not client.bucket_exists(bucket):
    client.make_bucket(bucket)

data = b"Hello from Python!"
client.put_object(
    bucket,
    "/data/hello.txt",
    io.BytesIO(data),
    length=len(data),
    content_type="text/plain",
)


for obj in client.list_objects(bucket):
    print(f"  {obj.object_name} ({obj.size} bytes)")