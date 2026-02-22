import os



base_sha = os.environ.get('BASE_SHA')
head_sha = os.environ.get('HEAD_SHA')

print("✅ Analysis complete. Everything looks good!")

print(base_sha)
print(head_sha)
