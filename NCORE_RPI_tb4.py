from machine import Pin
from machine import Timer
import time

main_clk = False
check_clk = False

scan_data = '00000000000010000100001001010100'


def flip_clk(t):
    global main_clk, check_clk
    main_clk = not main_clk  #same logic just no if statement
    check_clk = True

sc_in = []

if __name__ == '__main__':
    main_timer = Timer()

    main_timer.init(mode=Timer.PERIODIC, freq=200, callback=flip_clk)



    clk = Pin(1, Pin.OUT)
    clk.value(0)
    
    scan_in = Pin(2, Pin.OUT)
    scan_in.value(0)
    
    scan_enable = Pin(3, Pin.OUT)
    scan_enable.value(0)
    
    reset_n = Pin(4, Pin.OUT)
    reset_n.value(0)
    
    rna_clk = Pin(5, Pin.OUT)
    rna_clk.value(0)
    
    
    
    
    current_bit = 0
    prev_main_clk_state = main_clk
    run = True

    scan_in_value = 0
    scan_enable_value = 0
    
    state = 'reset'
    clk_count = 0
    data_count = 0
    rna_clk_enable = True
    
    
    

    while run:
        if check_clk:
            check_clk = False

            if not main_clk and prev_main_clk_state:
                
                if state == 'reset':
                    rna_clk_enable = True
                    reset_n.value(0)
                    scan_in.value(0)
                    scan_enable.value(0)
                    
                    if clk_count >= 40:
                        reset_n.value(1) 
                        clk_count = 0
                        state = 'program'
                        rna_clk_enable = False
                elif state == 'program':
                    if current_bit < len(scan_data):
                        print(f"Current bit: {scan_data[current_bit]}")
                        if scan_data[current_bit] == '0':
                            scan_in_value = 0
                        elif scan_data[current_bit] == '1':
                            scan_in_value = 1

                    current_bit += 1

                    if current_bit >= len(scan_data):  #should just be < ?
                        clk_count = 0
                        current_bit = 0
                        data_count += 1
                        if data_count >= 40:
                            run = False
                        scan_enable_value = 0  #changed from boolean
                    else:
                        scan_enable_value = 1  

                elif state == 'read':
                    if clk_count >= 1000:
                        run = False
                
                clk_count += 1
                
            sc_in.append(scan_in_value)

            scan_in.value(scan_in_value)
            clk.value(main_clk)
            scan_enable.value(scan_enable_value)  #changed from 1 to read in scan enable value
            rna_clk.value(rna_clk_enable and main_clk) 
            prev_main_clk_state = main_clk
            
    print(sc_in)
