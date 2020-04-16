section .data
    I8 a 2
    I16 b 4
section .main
    mul @a @b
    call #64
    call #128