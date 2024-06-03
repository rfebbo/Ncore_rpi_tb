from machine import Pin
from machine import Timer

from micropython import const




main_clk = False
check_clk = False

scan_data = '01010101'

def flip_clk(t):
    global main_clk, check_clk
    if check_clk == False:
        main_clk = not main_clk
        check_clk = True
    


if __name__ == '__main__':

    
    main_timer = Timer()
    state_timer = Timer()
    
    main_timer.init(mode=Timer.PERIODIC, freq=500, callback=flip_clk)

    p0 = Pin(2, Pin.OUT)
    p0.value(0)
    
    
    p1 = Pin(1, Pin.OUT)
    p1.value(0)
    
    
    current_bit = 0
    prev_clk_state = main_clk
    run = True
    
    p0_value = 0
    
    
    while run:
        if check_clk:
            check_clk = False
            if main_clk == False and prev_clk_state == True:
                
                print(scan_data[current_bit])
            
                if scan_data[current_bit] == '0':
                    p0_value = 0
                elif scan_data[current_bit] == '1':
                    p0_value = 1
                
                current_bit += 1
                
                if current_bit >= len(scan_data):
                    run = False
                
                
        p1.value(main_clk)
        p0.value(p0_value)
        prev_clk_state = main_clk
        
        
