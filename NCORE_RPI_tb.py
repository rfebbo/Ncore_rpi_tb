from machine import Pin
from machine import Timer

main_clk = False

def flip_clk(t):
    global main_clk
    main_clk = not main_clk


def update_state(t):
    print(dir(state_timer))


if __name__ == '__main__':


    main_timer = Timer()
    state_timer = Timer()


    

    # periodic at 1kHz
    #try:
    main_timer.init(mode=Timer.PERIODIC, freq=1000, callback=flip_clk)
    state_timer.init(mode=Timer.PERIODIC, freq=100, callback=update_state)
    #except:
     #   main_timer.deinit()
          #  state_timer.deinit()

