from machine import Pin
from machine import Timer
import time

main_clk = False
check_clk = False

scan_data = '00000000000010000100001001010100'

def flip_clk(t):
    global main_clk, check_clk
    if not check_clk:
        main_clk = not main_clk
        check_clk = True

if __name__ == '__main__':
    main_timer = Timer()

    main_timer.init(mode=Timer.PERIODIC, freq=500, callback=flip_clk)

    scan_in = Pin(2, Pin.OUT)
    scan_in.value(0)

    clk = Pin(1, Pin.OUT)
    clk.value(0)
    
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
                    

                    if clk_count >= 20:
                        #scan_enable_value = 1
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

                    if current_bit > len(scan_data):
                        clk_count = 0
                        current_bit = 0
                        data_count += 1
                        if data_count >= 40:
                            run = False
                        #state = 'read'
                        scan_enable_value = False   #added 3 lines to update scan_enable_value before exiting while loop
                    #else:
                        #scan_enable_value = True
                elif state == 'read':
                    if clk_count >= 1000:
                        run = False
                    
                        
                        
                
                clk_count += 1
                
                    
            scan_in.value(scan_in_value)
            clk.value(main_clk)
            scan_enable.value(1)
            rna_clk.value(main_clk and rna_clk_enable)  #added rna clk
            prev_main_clk_state = main_clk

  
