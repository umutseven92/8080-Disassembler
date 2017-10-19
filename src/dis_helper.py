# Helper methods go here

# Get the two chars next to instruction opcodes, which are memory registers
def get_dest(offset, hexed, addt, x):
	dest = ""

	for i in range(1, offset+1):
		offset_byte = hexed[(x * 2) + i * 2] + hexed[(x*2) + i*2 +1]
		dest = offset_byte + dest

	dest = addt + dest
	return dest

