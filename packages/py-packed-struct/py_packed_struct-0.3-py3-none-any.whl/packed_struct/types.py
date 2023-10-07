"""This module wraps the `bitstruct` package to implement a C like packed struct (https://bitstruct.readthedocs.io/en/latest/index.html)"""
import bitstruct as bstruct


BYTE_ENDIANNESS = {
    "=": "",
    "big": ">",
    "small": "<",
}


class Type:
    """Generic type

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        if bits <= 0 or type(bits) != int:
            raise Exception("Number of bits shall be a positive integer")
        self.fmt = None
        self.value = None
        self.size = None

    def __repr__(self) -> str:
        return str(self.value)


class c_unsigned_int(Type):
    """`u` stands for unsigned integer, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"u{bits}"
        self.size = bits


class c_signed_int(Type):
    """`s` stands for signed integer, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"s{bits}"
        self.size = bits


class c_float(Type):
    """`f` stands for float (16, 32, 64 bits), according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        if bits not in (16, 32, 64):
            raise Exception(
                f"Float must be of 16, 32 or 64 bits (requested: {bits}). See https://bitstruct.readthedocs.io/en/latest/#performance."
            )

        self.fmt: str = f"f{bits}"
        self.size = bits


class c_bool(Type):
    """`b` stands for boolean, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"b{bits}"
        self.size = bits


class c_char(Type):
    """`c` stands for char in C language, `t` according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)

    Nota bene: a char is always contained in at least 8 bits.
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        if bits % 8 != 0:
            raise UserWarning(
                "char must be contained in multiples of 8 bits (see https://bitstruct.readthedocs.io/en/latest/#performance)"
            )
        self.fmt: str = f"t{bits}"
        self.size = bits


class c_raw_bytes(Type):
    """`r` stands for raw, for raw bytes, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"r{bits}"
        self.size = bits


class c_padding(Type):
    """`p` stands for padding, according to bitstruct [doc](https://bitstruct.readthedocs.io/en/latest/index.html#functions)

    Argument:
        `bits`: number of bits (`int`)
    """

    def __init__(self, bits: int) -> None:
        super().__init__(bits)
        self.fmt: str = f"u{bits}"
        self.size = bits
        self.value = 0


class Struct:
    """Definition of a C-like packed struct

    Argument:
        `data_dict`: dictionary of data to be included in the packed struct (key: name, item: data type)

    Nota bene:
        Data types can only be of type `Type` or of type `Struct`, for nested structures

    Example:
        1) simple struct
        ```python
        person = Struct({"name": c_char(10*8), "age": c_unsigned_int(8), "weight": c_float(32)})
        # person in C would be:
        # struct{
        #    char[10] name;
        #    uint8_t age;
        #    float weight;
        # } person;
        ```

        2) nested structs
        ```python
        person = Struct(
            {
                "name": c_char(10*8),
                "age": c_unsigned_int(8),
                "weight": c_float(32),
                "dresses": Struct(
                    {
                        "tshirt": c_char(10*8),
                        "shorts": c_char(10*8)
                    }
                )
            }
        )
        person["dresses"].set_data(tshirt="nike", shorts="adidas")
        person.set_data(name="Maria", age=26, weight=76.8)
        print(person.size)
        print(person.pack())
        ```
    """

    def __init__(self, data_dict: dict) -> None:
        if not data_dict:
            raise Exception("Empty structure cannot be created")

        # check on types of data
        for key, item in data_dict.items():
            if not (isinstance(item, Type) or isinstance(item, Struct)):
                raise Exception(
                    f"Data {key} shall be of type Type or Struct. Current type: {type(item)}"
                )

        # if all checks are passed, initialize attributes
        self._data = data_dict
        self._fmt = None

    def __getitem__(self, data):
        return self._data[data]

    def __getattr__(self, data):
        try:
            return self._data[data]
        except:
            raise AttributeError

    def __repr__(self) -> str:
        representation = {}
        for key, item in self._data.items():
            representation[key] = item
        return str(representation)

    """Properties"""

    @property
    def size(self) -> int:
        """Return the size of the struct"""
        bitsize = 0
        for _, item in self._data.items():
            bitsize += item.size
        return bitsize

    @property
    def fmt(self) -> str:
        """Return the composed format of a struct, i.e. data types packed together.
        If already computed, returns directly it (to save time), if not compute it.
        """
        if not self._fmt:
            self._fmt = "".join([item.fmt for _, item in self._data.items()])

        return self._fmt

    @property
    def value(self) -> list:
        """Return the list of values of all data"""
        # this can be managed in a more pythonic way maybe with list comprehension,
        # but a comprehension creates a list of lists when multiple Structs are nested
        values = []
        for _, item in self._data.items():
            val = item.value
            if type(val) is list:
                values += val
            else:
                values.append(val)
        return values

    """Public methods"""

    def get_data(self) -> dict:
        """Return a dict containing all data in the struct."""
        return self._data

    def pack(self, byte_endianness: str = "=") -> bytes:
        """Return a `bytes` object containing the packed string with the requested `byte_endianness`
        according to specified format

        Argument:
            `byte_endianness`: shall be "big", "small" or "=" (default: "=", i.e. native)
        """

        check_array = [True if x is not None else False for x in self.value]
        if not byte_endianness in BYTE_ENDIANNESS.keys():
            raise Exception("Byte endianness shall be 'small', 'big' or '='")
        if not all(check_array):
            raise Exception("You have to initialize all data.")

        # set byte endianness
        B_endianness = BYTE_ENDIANNESS[byte_endianness]

        fmt = f"{self.fmt}{B_endianness}"
        args = self.value

        return bstruct.pack(fmt, *args)

    def set_data(self, **kwargs):
        """Set data in the struct.

        Examples of usage:
            ```python
            person = Struct({"name": c_char(10*8), "age": c_unsigned_int(8), "weight": c_float(32)})
            person.set_data(name="Mario", age=25, weight=75.8)
            ```
        """
        if not kwargs:
            raise Exception("Give me some data: see examples")

        for key, item in kwargs.items():
            if not key in self._data.keys():
                raise AttributeError(
                    f"Data {key} not found! Current data are: {self._data.keys()}"
                )
            # if the key exists, we can set the value
            self._data[key].value = item

    def unpack(self, byte_string: bytes, byte_endianness: str = "=") -> dict:
        """Unpack `byte_string: bytes` according to the format of the struct.
        Return a dict containing data.

        Arguments:
            * `byte_string`: the byte string you want to unpack

            * `byte_endianness`: shall be "big", "small" or "=" (default: "=", i.e. native)
        """
        if not byte_endianness in BYTE_ENDIANNESS.keys():
            raise Exception("Byte endianness shall be 'small', 'big' or '='")

        # set byte endianness
        B_endianness = BYTE_ENDIANNESS[byte_endianness]
        # set unpack format
        fmt = f"{self.fmt}{B_endianness}"

        unpacked = bstruct.unpack(fmt, byte_string)
        i = 0

        def recursive_set(dict_item, idx: int):
            for _, item in dict_item.items():
                if isinstance(item, Struct):
                    idx = recursive_set(item._data, idx)
                else:
                    item.value = unpacked[idx]
                    idx += 1
            return idx

        recursive_set(self._data, i)

        return self._data
