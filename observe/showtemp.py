from sense_hat import SenseHat
sense = SenseHat()

while True:
    t = sense.get_temperature()
    h = sense.get_humidity()

    t = round(t, 1)
    h = round(h, 1)

    msg = "T={0},H={1}".format(t,h)

    sense.show_message(msg, scroll_speed=0.05)
