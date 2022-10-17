from zlib import decompress,compress
from struct import unpack

def convert(img_bytes: bytes) -> bytes:
        '''
        This is for turning apple cgbi png to standard png
        :param img_bytes: bytes: apple png
        :param error: bool: raise error if not CgBI
        :return: bytes: image;
        '''
        # 8 byte signature header which allows computer to know that it's a png
        signature_header = img_bytes[:8]
        # Everything other than signature header
        rest_of_png = img_bytes[8::]
        # Create a new png starting with the signature header (https://www.w3.org/TR/PNG-Rationale.html#R.PNG-file-signature)
        new_PNG = signature_header
        # The index of byte reading
        current_byte = 8

        # Have CgBI?
        cgbi=False
        idat_cgbi_data = b''
        IDAT_chunk_type = b''
        img_width = 0
        img_height = 0
        # Going through every chunk in png
        while current_byte < len(img_bytes):
            # Chunk Length:     4 bytes
            # Chunk Type  :     4 bytes ASCII letters
            # Chunk Data  :     defined in 'Chunk Length' field
            # CRC         :     4 bytes
            # Reading length field (chunk length is the length of data, not the whole chunk)
            chunk_length_raw = img_bytes[current_byte:current_byte + 4]
            # Turning bytes into integer
            chunk_length = int.from_bytes(chunk_length_raw, 'big')
            current_byte = current_byte + 4
            # Reading type field
            chunk_type_raw = img_bytes[current_byte:current_byte + 4]
            # Turning bytes into string
            chunk_type = str(chunk_type_raw, encoding='ASCII')
            current_byte = current_byte + 4
            # Extracting chunk_data
            chunk_data = img_bytes[current_byte:current_byte + chunk_length]
            # Reading CRC field
            chunk_CRC = img_bytes[current_byte + chunk_length:current_byte + chunk_length + 4]
            # Removing CgBI chunk
            if chunk_type == 'CgBI':
                current_byte = current_byte + chunk_length + 4
                cgbi=True
                continue
            # Reading img width and height
            elif chunk_type == 'IHDR':
                if cgbi:
                    # img_width = int.from_bytes(chunk_data[0:4], 'big')
                    # img_height = int.from_bytes(chunk_data[4:8], 'big')
                    img_width, img_height, bitd, colort, compm, filterm, interlacem = unpack('>IIBBBBB', chunk_data)
                    if compm != 0:
                        raise Exception('invalid compression method')
                    if filterm != 0:
                        raise Exception('invalid filter method')
                    if colort != 6:
                        raise Exception('we only support truecolor with alpha')
                    if bitd != 8:
                        raise Exception('we only support a bit depth of 8')
                    if interlacem != 0:
                        raise Exception('we only support no interlacing')
                else:
                    raise ValueError("CgBI chunk not found, mey be a normal PNG!")
                    raise
            elif chunk_type == 'IDAT':
                # Add all chunk data.keek data complete
                IDAT_chunk_type = chunk_type_raw
                idat_cgbi_data = idat_cgbi_data + chunk_data
                current_byte = current_byte + chunk_length + 4
                continue
            # Turning BGRA into RGBA
            elif chunk_type == 'IEND':
                
                # [B,G,R,A] -> [R,G,B,A]
                # 0 -> 2
                # 1 -> 1
                # 2 -> 0
                # 3 -> 3
                # Decompressing, see more https://iphonedev.wiki/index.php/CgBI_file_format#Differences_from_PNG
                try:
                    buffer_size = img_width * img_height * 4 + img_height
                    chunk_idat_data = zlib.decompress(idat_cgbi_data, wbits=-8, bufsize=buffer_size)
                except Exception as e:
                    raise ArithmeticError('Error resolving IDAT chunk!\n' + str(e))
                # Creating bytes like new data
                new_data = b''
                for y in range(img_height):
                    # index of current position
                    position = len(new_data)
                    # Separator
                    new_data = new_data + bytes([chunk_idat_data[position]])
                    for x in range(img_width):
                        # index of current pixes
                        pixel = len(new_data)
                        # Red
                        new_data = new_data + bytes([chunk_idat_data[pixel + 2]])
                        # Green
                        new_data = new_data + bytes([chunk_idat_data[pixel + 1]])
                        # Blue
                        new_data = new_data + bytes([chunk_idat_data[pixel + 0]])
                        # Alpha
                        new_data = new_data + bytes([chunk_idat_data[pixel + 3]])
                chunk_idat_data = new_data
                chunk_idat_data = zlib.compress(chunk_idat_data)
                chunk_length_raw = len(chunk_idat_data).to_bytes(4, 'big')
                # cal new crc
                new_CRC = zlib.crc32(IDAT_chunk_type)
                new_CRC = zlib.crc32(chunk_idat_data, new_CRC)
                new_CRC = (new_CRC + 0x100000000) % 0x100000000
                new_PNG = new_PNG + chunk_length_raw + IDAT_chunk_type + chunk_idat_data + new_CRC.to_bytes(4, 'big')

            new_CRC = zlib.crc32(chunk_type_raw)
            new_CRC = zlib.crc32(chunk_data, new_CRC)
            new_CRC = (new_CRC + 0x100000000) % 0x100000000
            new_PNG = new_PNG + chunk_length_raw + chunk_type_raw + chunk_data + new_CRC.to_bytes(4, 'big')
            current_byte = current_byte + chunk_length + 4
        return new_PNG


