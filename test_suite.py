from typing import List, TypedDict
import os
import main

class TestArgs(TypedDict):
    public_filepath: str
    private_filepath: str

def collect_test_cases(root_path: str = "tests") -> List[TestArgs]:
    test_args_list: List[TestArgs] = []
    case_types = ["sucess_cases", "fail_cases"]

    for case_type in case_types:
        case_dir = os.path.join(root_path, case_type)
        if not os.path.isdir(case_dir):
            continue

        for test_case in os.listdir(case_dir):
            test_case_path = os.path.join(case_dir, test_case)
            if not os.path.isdir(test_case_path):
                continue

            public_file = None
            private_file = None

            for file in os.listdir(test_case_path):
                if file.startswith("public"):
                    public_file = os.path.join(test_case_path, file)
                elif file.startswith("private"):
                    private_file = os.path.join(test_case_path, file)

            if public_file and private_file:
                test_args_list.append(TestArgs(
                    public_filepath=public_file,
                    private_filepath=private_file
                ))

    return test_args_list

def test():
    cases = collect_test_cases()
    for case in cases:
        result = main.main(case['public_filepath'], case['private_filepath'])

test()
