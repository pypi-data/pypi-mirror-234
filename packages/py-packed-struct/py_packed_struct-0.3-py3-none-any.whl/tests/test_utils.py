import logging

logging.basicConfig(
    level=logging.INFO,
    format='| %(levelname)-8s | %(message)s \n ----------------------------------------------------------------------'
)

required_tests = []
errors = False


def test(f):
    required_tests.append(f)
    return f

def non_blocking_assert(condition: bool, message: str):
    try:
        assert condition, message
    except AssertionError as e:
        global errors 
        errors = True

        logging.error(e)
        
 
def run():
    global errors
    for test in required_tests:
        try:
            logging.info(f"Running test: {test.__name__}")
            test()
        except AssertionError as e:
            logging.error(e)
            errors = True
        except Exception as e:
            errors = True
            raise e
    
    if errors: 
        raise TestException("Something failed")
        

class TestException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)