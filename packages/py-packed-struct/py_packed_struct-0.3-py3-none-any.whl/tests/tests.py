"""Implements some unit tests"""
from test_utils import *
from packed_struct import *

class TypesTest:

    @test
    def test_unsigned_int_correct():
        # correct case
        bits = 3
        data = c_unsigned_int(bits)
        
        non_blocking_assert(data.fmt == f"u{bits}", f"uint format not correct, expected u{bits}, current {data.fmt}")
        non_blocking_assert(data.size == bits, f"uint size not correct, expected {bits}, current {data.size}")

    @test
    def test_unsigned_int_negative_bits():
        # wrong case
        bits = -4
        try:
            # this should fail
            data = c_unsigned_int(bits)
            # if it reach this point, it's not failed
            raise TestException()
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "uint allows for negative integer size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer", f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")
    
    @test
    def test_unsigned_int_null_bits():
        # wrong case
        bits = 0
        try:
            # this should fail
            data = c_unsigned_int(bits)
            # if it reach this point, it's not failed
            raise TestException()
        
        except Exception as e:
            if isinstance(e, TestException):
                non_blocking_assert(False, "uint allows for 0 size")
            else:
                non_blocking_assert(str(e) == "Number of bits shall be a positive integer", f"wrong exception (expected: Number of bits shall be a positive integer, current {str(e)})")

    
    @test
    def test_signed_int():
        pass


    @test
    def unpack_test_correct():
        pass


################
# 
#     RUN
#
################
if __name__ == "__main__":
    run()