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

def generate_auditable_hash(public_block: AuditableBlock, commited_message: str):
    hash_args: HashArgs = {
        'previousHash': public_block['previousHash'],
        'counter': public_block['counter'],
        'commitedMessage': commited_message
    }
    serialized_data = json.dumps(hash_args, ensure_ascii=False, separators=(',', ':'))
    hash =  sha256(serialized_data.encode('utf-8')).hexdigest()

    return hash

def generate_commited_message(private_block: PrivateBlock):
    message_content: MessageContent = {
        'content': private_block['content'],
        'author': private_block['author']
    }
    commit_message_args: CommitArgs = {
        'commitedKey': private_block['commitedKey'],
        'message': message_content
    }
    commited_message = commit_function(commit_message_args)

    return commited_message

def commit_function(args: CommitArgs):
    processed_message_content = json.dumps(args['message'], ensure_ascii=False, separators=(',', ':'))
    commit_args: CommitArgsProcessed = {
        'commitedKey': args['commitedKey'],
        'message': processed_message_content
    }
    serialized_data = json.dumps(commit_args, ensure_ascii=False, separators=(',', ':'))
    return sha256(serialized_data.encode('utf-8')).hexdigest()

def verify_private_blocks(public_blocks: List[AuditableBlock], private_blocks: List[PrivateBlock]):
    if (len(private_blocks) == 0):
        print("No blocks in private file, returning.")
        return

    initial_counter = private_blocks[0]['counter']

    for private_block in private_blocks:
        counter = private_block['counter']
        public_block = public_blocks[counter-1]
        commited_message = generate_commited_message(private_block)
        generated_hash = generate_auditable_hash(public_block, commited_message)

        if (len(private_blocks) > counter-initial_counter+1):
            next_previous_hash = public_blocks[counter]["previousHash"]
            if (generated_hash != next_previous_hash):
                print('New hash does not match previousHash from next block.')
                print(f'Generated hash: {generated_hash}')
                print(f'Next block previous hash: {public_blocks[counter]["previousHash"]}')
                assert (generated_hash == next_previous_hash)
                return

        if (generated_hash != public_block['hash']):
            print('Private Block hash did not match the one from Public Block.')
            print(f'Public Block hash: {public_block["hash"]}')
            print(f'Private Block hash: {generated_hash}')
            assert (generated_hash == public_block['hash'])
            return

def verify_public_blocks(public_blocks: List[AuditableBlock]):
    if (len(public_blocks) == 0):
        print("No blocks in public file, returning.")
        return

    for public_block in public_blocks:
        counter = public_block['counter']
        public_block = public_blocks[counter-1]
        generated_hash = generate_auditable_hash(public_block, public_block['commitedMessage'])

        if (len(public_blocks) > counter):
            next_previous_hash = public_blocks[counter]["previousHash"]
            if (generated_hash != next_previous_hash):
                print('New hash does not match previousHash from next block.')
                print(f'Generated hash: {generated_hash}')
                print(f'Next block previous hash: {public_blocks[counter]["previousHash"]}')
                assert (generated_hash == next_previous_hash)
                return

        if (generated_hash != public_block['hash']):
            print('Public Block hash did not match the one from Public Block.')
            print(f'Public Block hash: {public_block["hash"]}')
            print(f'Public Block hash: {generated_hash}')
            assert (generated_hash == public_block['hash'])
            return


def main(public_filepath: str, private_filepath: str):
    public_content = file_reader(public_filepath)
    initial_block: AuditableBlock = public_content['initialBlock']
    public_blocks: List[AuditableBlock] = public_content['logMessages']

    private_content = file_reader(private_filepath)
    initial_commited_key: str = private_content['initialCommitedKey']
    private_blocks: List[PrivateBlock] = private_content['logMessages']

    print(f'Starting audition on public blocks.')
    print(f'Reference file: {public_filepath}')

    verify_public_blocks(public_blocks)

    print("Audition completed.")

    print(f'Starting audition on private blocks listed in {private_filepath}')
    print(f'Reference file: {public_filepath}')

    verify_private_blocks(public_blocks, private_blocks)

    print("Audition completed.")

