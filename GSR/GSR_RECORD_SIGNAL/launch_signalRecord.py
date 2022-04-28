import GSR_rec.GSR_RECORD_SIGNAL.signalRecord as sigrec
def startGSR(path, sec):
    sample_rate = 384000  # using the highest sampling frequency
    myrec = sigrec.Record(sample_rate, sec)
    val = myrec.mysignal()
    myrec.savefile(path, val)
