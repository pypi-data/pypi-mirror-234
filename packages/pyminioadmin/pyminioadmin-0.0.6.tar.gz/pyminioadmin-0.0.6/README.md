# MinIO Admin Client

**pyminioadmin** is a Python Wrapper for the MinIO client (mc) that provides admin operations and other functionalities not supported by the official Minio SDK. Please note that this wrapper requires the MinIO client (mc) to be installed on the machine.

## Requirements

- Python and pip installed.
- MinIO client installed on the machine with the path environment added as `mc`.

## Usage Example

```python
from pyminioadmin import MinioAdminClient

# Initialize the MinIO Admin Client
client = MinioAdminClient('host:3000', 'access-key', 'secret-key')

# Example: Create a new user
client.create_user('new-access-key', 'new-secret-key')
```

## Source Code

The source code for this project is available on GitHub:

[GitHub Repository](https://github.com/dreazz97/minio-admin-client-lib)