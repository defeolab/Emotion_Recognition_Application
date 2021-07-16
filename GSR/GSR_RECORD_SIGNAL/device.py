import sounddevice as sd

print(sd.query_devices())
print(sd.default.device)
print(f"INPUT DEVICE:  {sd.default.device['input']}")
print(f"OUTPUT DEVICE:  {sd.default.device['output']}")
