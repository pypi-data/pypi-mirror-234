from machine import Pin, PWM, ADC
from time import sleep, sleep_ms, sleep_us

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
        self._pwm.duty_u16(int(64 * i))
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
    
    def __init__(self, pin):
        self._pin = Pin(pin)
        self._pwm = PWM(self._pin)
        self._pwm.freq(50)
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
        newDuty = minDuty + (maxDuty - minDuty) * (a + 90) / 180
        
        self._pwm.duty_u16(int(newDuty))
        self._angle = a

class Button:
    
    def __init__(self, pin = 13):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def value(self):
        return self._pin.value()

    def pressed(self):
        return self.value() == 0
    
    def waitPressed(self):
        while not self.pressed():
            pass
            
        sleep_ms(10)

    def waitReleased(self):
        while self.pressed():
            pass
            
        sleep_ms(10)

    def waitClicked(self):
        self.waitPressed()
        self.waitReleased()

class Rotary:

    def __init__(self, pin = 28):
        self._adc = ADC(Pin(pin))
        
    def raw_value(self):
        return self._adc.read_u16()

    def value(self):
        return self._adc.read_u16() / 65536

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

def test():
    right_red = LED(16)
    right_green = LED(17)
    right_blue = LED(18)
    
    left_red = LED(19)
    left_green = LED(20)
    left_blue = LED(21)

    right_leg = Servo(6)
    right_foot = Servo(7)
    left_leg = Servo(8)
    left_foot = Servo(9)

    speaker = Speaker()
    button = Button()
    rotary = Rotary()
    
    index = 0
    
    components = [right_red, right_green, right_blue, left_red, left_green,
                  left_blue, right_leg, right_foot, left_leg, left_foot, speaker]
    
    while button.pressed():
        sleep_ms(20)
        
    while index < len(components):
        what = components[index]
        print(what)
        
        while not button.pressed():
            value = rotary.raw_value()
            
            print(value)
            
            if isinstance(what, LED):
                what.intensity(value // 256)
            elif isinstance(what, Servo):
                what.angle(transform(value, 0, 65536, -60, 61))
            elif isinstance(what, Speaker):
                what.tone(transform(value, 0, 65536, 10, 10001))
            
            sleep_ms(20)
                       
        while button.pressed():
            sleep_ms(20)

        if isinstance(what, LED):
            what.off()
        elif isinstance(what, Servo):
            what.angle(0)
        elif isinstance(what, Speaker):
            what.no_tone()

        index = index + 1

right_eye = RGB(19)
left_eye = RGB(16)

right_leg = Servo(6)
right_foot = Servo(7)

left_leg = Servo(8)
left_foot = Servo(9)

speaker = Speaker()

button = Button()
rotary = Rotary()

def reset():
    right_eye.off()
    left_eye.off()
    
    for s in (right_leg, right_foot, left_leg, left_foot):
        s.angle(0)
        
    speaker.no_tone()

