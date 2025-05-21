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
    counter: int

class MessageContent(TypedDict):
    content: str
    author: str

class CommitArgs(TypedDict):
    commitedKey: str
    message: MessageContent

class CommitArgsProcessed(TypedDict):
    commitedKey: str
    message: str

class HashArgs(TypedDict):
    previousHash: str
    counter: int
    commitedMessage: str

def file_reader(filepath: str):
    with open(filepath) as f:
        json_object = json.load(f)

    return json_object

def generate_auditable_hash(public_block: AuditableBlock, private_block: PrivateBlock):
    message_content: MessageContent = {
        'content': private_block['content'],
        'author': private_block['author']
    }
    commit_message_args: CommitArgs = {
        'commitedKey': private_block['commitedKey'],
        'message': message_content
    }
    commited_message = commit_function(commit_message_args)

    hash_args: HashArgs = {
        'previousHash': public_block['previousHash'],
        'counter': public_block['counter'],
        'commitedMessage': commited_message
    }
    serialized_data = json.dumps(hash_args, ensure_ascii=False, separators=(',', ':'))
    hash =  sha256(serialized_data.encode('utf-8')).hexdigest()

    return hash

def commit_function(args: CommitArgs):
    processed_message_content = json.dumps(args['message'], ensure_ascii=False, separators=(',', ':'))
    commit_args: CommitArgsProcessed = {
        'commitedKey': args['commitedKey'],
        'message': processed_message_content
    }
    serialized_data = json.dumps(commit_args, ensure_ascii=False, separators=(',', ':'))
    return sha256(serialized_data.encode('utf-8')).hexdigest()

def main(public_filepath: str, private_filepath: str):
    public_content = file_reader(public_filepath)
    initial_block: AuditableBlock = public_content['initialBlock']
    hashchain: List[AuditableBlock] = public_content['logMessages']

    private_content = file_reader(private_filepath)
    initial_commited_key: str = private_content['initialCommitedKey']
    chat_content: List[PrivateBlock] = private_content['logMessages']

    print(f'Starting audition on block listed in {private_filepath}')
    print(f'Reference file: {public_filepath}')

    if (len(chat_content) == 0):
        print("No blocks in private file, returning.")
        return

    initial_counter = chat_content[0]['counter']

    for private_block in chat_content:
        counter = private_block['counter']
        public_block = hashchain[counter-1]
        generated_hash = generate_auditable_hash(public_block, private_block)

        if (len(chat_content) > counter-initial_counter+1):
            next_previous_hash = hashchain[counter]["previousHash"]
            if (generated_hash != next_previous_hash):
                print('New hash does not match previousHash from next block.')
                print(f'Generated hash: {generated_hash}')
                print(f'Next block previous hash: {hashchain[counter]["previousHash"]}')
                return

        if (generated_hash != public_block['hash']):
            print('Private Block hash did not match the one from Public Block.')
            print(f'Public Block hash: {public_block["hash"]}')
            print(f'Private Block hash: {generated_hash}')
            return

    print("Audition completed.")

public_filepath = "./test_files/partial_conversation/public_logs_2025-05-21.json"
private_filepath = "./test_files/partial_conversation/private_logs_2025-05-21.json"
main(public_filepath, private_filepath)
