import os

def convert_to_header(origin, destination):
    os.system('rm cache/ASM_CODE.o')
    os.system(f'gcc -c {origin} -o cache/ASM_CODE.o')
    os.system(f'gcc -E -P -o {destination} cache/ASM_CODE.o')

def convert_to_script(origin, destination):
    os.system('rm cache/ASM_CODE.o')
    os.system(f'gcc -c {origin} -o cache/ASM_CODE.o')
    os.system(f'objdump -d cache/ASM_CODE.o | gcc -S -xc - -o {destination}')