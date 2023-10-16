from beni.bbyte import BytesWriter, BytesReader


def test():
    endian = '>'
    writer = BytesWriter(endian)
    writer.writeInt(123)
    writer.writeListStr(['a', 'b', 'c'])
    writer.writeDouble(3.14)

    reader = BytesReader(endian, writer.toBytes())
    assert reader.readInt() == 123
    assert reader.readListStr() == ['a', 'b', 'c']
    assert reader.readDouble() == 3.14
