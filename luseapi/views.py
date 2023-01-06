import simplefix

message = simplefix.FixMessage()
message.append_pair(8, "FIXT.1.1")
message.append_pair(35, 0)
message.append_pair(49, "Pangaea")
message.append_pair(56, "STT")
message.append_pair(112, "TR0003692")
message.append_pair(34, 4684, header=True)
message.append_time(52, header=True)


message
