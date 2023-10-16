from sys import argv
import os

def main():
    iso_path = argv[1]
    pyscript = argv[2]
    pyscript_folder = argv[3]
    pyscript_name = argv[4]
    os.system('rm cache/*')
    os.system(f'cythonize -i {pyscript}')
    os.system(f'objdump -d {pyscript_folder}/{pyscript_name}.so > cache/subkernel.asm')
    os.system('cp kernel/kernel.asm cache')
    os.system('nasm -f elf cache/kernel.asm -o cache/kernel.o')
    os.system('nasm -f elf cache/subkernel.asm -o cache/subkernel.o')
    os.system('ld -m elf_i386 -o cache/kernel.bin cache/kernel.o cache/subkernel.o')
    os.system(f'genisoimage -o {iso_path} bootloader/mbr.bin bootloader/bootmngr.bin cache/kernel.bin')