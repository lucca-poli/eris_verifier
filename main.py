import json
from typing import List, TypedDict
from hashlib import sha256

class AuditableBlock(TypedDict):
    commitedMessage: str
    counter: int
    hash: str
    previousHash: str

class PrivateBlock(TypedDict):
    content: str
    author: str
    commitedKey: str

class MessageContent(TypedDict):
    content: str
    author: str

class CommitArgs(TypedDict):
    commitedKey: str
    message: str

def file_reader(filepath: str):
    with open(filepath) as f:
        json_object = json.load(f)

    return json_object

def main(public_filepath: str, private_filepath: str):
    public_content = file_reader(public_filepath)
    initial_block: AuditableBlock = public_content['initialBlock']
    hashchain: List[AuditableBlock] = public_content['logMessages']

    private_content = file_reader(private_filepath)
    initial_commited_key: str = private_content['initialCommitedKey']
    chat_content: List[PrivateBlock] = private_content['logMessages']

    print("chat_content is: ", chat_content[1])

    test_message: MessageContent = {
        "content": chat_content[1]["content"],
        "author": chat_content[1]["author"]
    }
    print("commit object: ", {
        "commitedKey": chat_content[1]["commitedKey"],
        "message": json.dumps(test_message, ensure_ascii=False, separators=(',', ':'))
    })
    first_commit = commit_function({
        "commitedKey": chat_content[1]["commitedKey"],
        "message": json.dumps(test_message, ensure_ascii=False, separators=(',', ':'))
    })
    print(first_commit)

def commit_function(args: CommitArgs):
    serialized_data = json.dumps(args, ensure_ascii=False, separators=(',', ':'))
    return sha256(serialized_data.encode('utf-8')).hexdigest()

public_filepath = "./test_files/total_conversation/public_logs_2025-05-21.json"
private_filepath = "./test_files/total_conversation/private_logs_2025-05-21.json"
main(public_filepath, private_filepath)
