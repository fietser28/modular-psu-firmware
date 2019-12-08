from utime import ticks_ms, ticks_add, ticks_diff, sleep_ms
from eez import scpi

U_STEP = 0.1
U_MAX = 40.0
TIME_STEP_MS = 4
MEASURE_DELAY_MS = 2
I_SET = 4.0
TRACE_FILE = "/diode-tester.dlog"

try:
    scpi("OUTP 0")
    scpi("INST ch1")
    I_MAX = float(scpi("CURR? MAX"))
    scpi("VOLT 0")
    scpi("CURR " + str(I_SET))

    scpi("SENS:DLOG:TRAC:X:UNIT VOLT")
    scpi("SENS:DLOG:TRAC:X:STEP " + str(U_STEP))
    scpi("SENS:DLOG:TRAC:X:RANG:MAX " + str(U_MAX))
    scpi("SENS:DLOG:TRAC:Y1:UNIT AMPER")
    scpi("SENS:DLOG:TRAC:Y1:RANG:MAX " + str(I_MAX))

    # FILE_NAME_MAX_CHARS = 20
    # fileName = scpi('query text, "Diode model", ' % FILE_NAME_MAX_CHARS)

    scpi("INIT:DLOG:TRACE \"" + TRACE_FILE + "\"");

    scpi("OUTP 1")

    scpi("DISP:WINDOW:DLOG")

    t = ticks_ms()
    i = 0
    while True:
        u_set = i * U_STEP
        if u_set > U_MAX:
            break

        scpi("VOLT " + str(u_set))

        t = ticks_add(t, MEASURE_DELAY_MS)
        sleep_ms(ticks_diff(t, ticks_ms()))

        mode = scpi("OUTP:MODE?")
        #if mode.startswith("CC"):
        #    break

        scpi("DLOG:TRACE:DATA " + scpi("MEAS:CURR?"))

        i = i + 1

        t = ticks_add(t, TIME_STEP_MS - MEASURE_DELAY_MS)
        sleep_ms(ticks_diff(t, ticks_ms()))
finally:
    scpi("ABOR:DLOG")
    scpi("OUTP 0")
