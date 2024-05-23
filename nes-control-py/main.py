from nes_serial import NesBroker

def main():
    with NesBroker("COM6") as broker:
        while 1:
            inp = input("Enter command\n")
            
            if inp == 'Q' or inp == 'q':
                break
            if inp == 'exit-safe-mode':
                broker.exit_safe_mode()
            if inp == 'enter-safe-mode':
                broker.enter_safe_mode()
            if inp == 'reset-control-state':
                broker.set_control_state(0)
            if inp == 'q-mode':
                print(broker.state)



if __name__ == "__main__":
    main()


