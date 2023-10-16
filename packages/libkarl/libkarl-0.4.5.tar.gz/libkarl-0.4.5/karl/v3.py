from machine import Pin, PWM, ADC
from time import sleep, sleep_ms, sleep_us, ticks_ms
from json import load, dump
from os import listdir

class LED:

    def __init__(self, pin):
        self._pin = Pin(pin)
        self._pwm = PWM(self._pin)
        self.off()

    def intensity(self, i = None):
        if i == None:
            return self._intensity
        elif i < 0:
            i = 0
        elif i > 255:
            i = 255
        
        self._pwm.freq(1000)
        self._pwm.duty_u16(64 * i) # 256 is too bright
        self._intensity = i

    def off(self):
        self.intensity(0)

    def on(self):
        self.intensity(255)

    def toggle(self):
        if self._intensity == 0:
            self.on()
        else:
            self.off()            

class RGB:

    def __init__(self, pin_red, pin_green = None, pin_blue = None):
        if pin_green == None:
            pin_green = pin_red + 1
            
        if pin_blue == None:
            pin_blue = pin_red + 2
        
        self.red = LED(pin_red)
        self.green = LED(pin_green)
        self.blue = LED(pin_blue)

    def intensity(self, i = None):
        if i == None:
            return self.red.intensity()
        
        self.red.intensity(i)
        self.green.intensity(i)
        self.blue.intensity(i)

    def off(self):
        self.intensity(0)

    def on(self):
        self.intensity(255)

    def toggle(self):
        if self.intensity() == 0:
            self.on()
        else:
            self.off()

class Servo:
    
    def __init__(self, pin, offset = 0):
        self._pin = Pin(pin)
        self._pwm = PWM(self._pin)
        self._pwm.freq(50)
        self._offset = offset
        self.angle(0)
        
    def angle(self, a = None):
        if a == None:
            return self._angle
        elif a < -60:
            a = -60
        elif a > 60:
            a = 60
            
        maxDuty = 9000
        minDuty = 1000
        newDuty = minDuty + (maxDuty - minDuty) * (a + 90 + self._offset) / 180
        
        self._pwm.duty_u16(int(newDuty))
        self._angle = a

class Button:
    
    def __init__(self, pin = 22):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._pin.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING, handler=self.callback)
        self._count = 0
        self._last = 0
        self.interrupt = None

    def callback(self, pin):
        if ticks_ms() - self._last < 100:
            return

        self._last = ticks_ms()

        if pin.value() == 1:
            return

        self._count = self._count + 1

        try:
            if self.interrupt != None:
                self.interrupt(self)
        except:
            print("Invalid interrupt handler.")

    def hasBeenPressed(self):
        if self._count > 0:
            self._count = 0
            return True
        else:
            return False

    def value(self):
        return 1 - self._pin.value()

    def pressed(self):
        return self.value() != 0
    
    def wait(self, b = None):
        if b == None:
          while not self.pressed():
              pass
          while self.pressed():
              pass
        elif b:
          while not self.pressed():
              pass
        else:
          while self.pressed():
              pass

class Rotary:

    def __init__(self, pin = 28):
        self._adc = ADC(Pin(pin))
        
    def value(self, min = None, max = None):
        v = (self._adc.read_u16() - 536)

        if v < 0:
            v = 0
            
        return v / 65000

    def range(self, min, max = None):
        v = (self._adc.read_u16() - 536)
        if v < 0:
            v = 0
        
        if max == None:
            return transform(v, 0, 65000, 0, min)
        else:
            return transform(v, 0, 65000, min, max)

class Speaker:

    def __init__(self, pin = 10):
        self._pin = Pin(pin)
        self._duty = 32767
        self._pwm = PWM(self._pin)
        self.no_tone()

    def duty(self, value = None):
        if value == None:
            return self._duty
        
        self._duty = value

    def tone(self, freq):
        self._pwm.freq(int(freq))
        self._pwm.duty_u16(self._duty)

    def no_tone(self):
        self._pwm.deinit()
        
    def beep(self, length, pitch = 0):
        self.tone(self.get_frequency(pitch + 60))
        sleep(length)
        self.no_tone()

    def get_frequency(self, pitch):
        a = 440
        return (a / 32) * (2 ** ((pitch - 9) / 12))

def transform(x, i_m, i_M, o_m, o_M):
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

def get_config_str(section, key, default = ""):
    s = config.get(section)
    if s == None:
        return default
    return s.get(key, default)

def get_config_int(section, key, default = 0):
    s = config.get(section)
    if s == None:
        return default
    return int(s.get(key, default))

def set_config_int(section, key, value):
    s = config.get(section)
    if s == None:
        config[section] = {}
        s = config.get(section)
    s[key] = value

def reset():
    global config, right_eye, left_eye, right_leg, left_leg, right_foot, left_foot, speaker, button, rotary

    if 'karl.json' in listdir():
        try:
            stream = open("/karl.json", "r")
            config = load(stream)
        except:
            print("Error loading config from 'karl.json'")
            config = {}
    else:
        print("No 'karl.json' found. Assuming defaults.")
        config = {}        
        
    revision = get_config_str("board", "revision", "unknown")

    right_eye = RGB(19)
    left_eye = RGB(16)

    right_leg = Servo(6, get_config_int("offsets", "right_leg", 0))
    right_foot = Servo(7, get_config_int("offsets", "right_foot", 0))

    left_leg = Servo(8, get_config_int("offsets", "left_leg", 0))
    left_foot = Servo(9, get_config_int("offsets", "left_foot", 0))

    speaker = Speaker()

    button = Button(13 if revision < "4e" else 22)
    rotary = Rotary()
    
    right_eye.off()
    left_eye.off()
    
    for s in (right_leg, right_foot, left_leg, left_foot):
        s.angle(0)
        
    speaker.no_tone()

def test():
    right_red = LED(16)
    right_green = LED(17)
    right_blue = LED(18)
    
    left_red = LED(19)
    left_green = LED(20)
    left_blue = LED(21)
    
    index = 0
    
    ext_pins = (Pin(0, Pin.OUT), Pin(1, Pin.OUT), Pin(2, Pin.OUT), Pin(3, Pin.OUT),
                Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(26, Pin.OUT), Pin(27, Pin.OUT))

    components = [ right_red, right_green, right_blue,
                   left_red,  left_green,  left_blue,
                   speaker,
                   right_leg, right_foot, left_leg, left_foot, ext_pins]
    
    last_pin = None

    while button.pressed():
        sleep_ms(20)
        
    while index < len(components):
        what = components[index]
        print("Now testing ", what)
        
        while not button.pressed():
            if isinstance(what, LED):
                what.intensity(rotary.range(0, 256))
            elif isinstance(what, Servo):
                what.angle(rotary.range(-60, 61))
            elif isinstance(what, Speaker):
                what.tone(rotary.range(10, 10001))
            elif what == ext_pins:
                pin = ext_pins[rotary.range(8)]
                if pin != last_pin:
                    if last_pin != None:
                        last_pin.off()
                    pin.on()
                    last_pin = pin
            
            sleep_ms(20)
                       
        while button.pressed():
            sleep_ms(20)

        if isinstance(what, LED):
            what.off()
        elif isinstance(what, Servo):
            what.angle(0)
        elif isinstance(what, Speaker):
            what.no_tone()
        elif what == ext_pins:
            last_pin.off()

        index = index + 1

def tune():
    right_leg._offset = 0
    right_foot._offset = 0
    
    left_leg._offset = 0
    left_foot._offset = 0
    
    index = 0
    
    components = [ right_leg, right_foot, left_leg, left_foot ]
    
    while button.pressed():
        sleep_ms(20)
        
    while index < len(components):
        what = components[index]
        print("Now tuning ", what)
        
        while not button.pressed():
            what.angle(rotary.range(-15, 16))
            sleep_ms(20)
                       
        while button.pressed():
            sleep_ms(20)

        index = index + 1

    set_config_int("offsets", "right_leg", right_leg._angle);
    set_config_int("offsets", "right_foot", right_foot._angle);
    set_config_int("offsets", "left_leg", left_leg._angle);
    set_config_int("offsets", "left_foot", left_foot._angle);

    stream = open("/karl.json", "w")
    dump(config, stream)
    stream.close()
    
    reset()

reset()
