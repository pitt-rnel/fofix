#!/usr/bin/python
import PyRTMA2 as RTMA
import climber_config as RTMA_types

MID_LISTENER = 11

if __name__ == "__main__":
    mod = RTMA.RTMA_Module(MID_LISTENER, 0)
    mod.ConnectToMMM("localhost:7111")
    mod.Subscribe(RTMA_types.MT_FOFIX_PROMPT)
    mod.Subscribe(RTMA_types.MT_FOFIX_INPUT)
    mod.Subscribe(RTMA_types.MT_FOFIX_MISSED)

    print("Listener running...\n")
    print("Message definitions header file: {}".format(RTMA_types.__file__))

    while True: 
        try:
            msg_in = RTMA.CMessage()
            rm_ret = mod.ReadMessage(msg_in, 1)
            
            if msg_in.GetHeader().msg_type == RTMA_types.MT_FOFIX_PROMPT:
                msg_data = RTMA_types.MDF_FOFIX_PROMPT()
                RTMA.copy_from_msg(msg_data, msg_in)
                print('PROMPT - note: {}, target_time: {}, game_time: {}'.format(msg_data.note, msg_data.target_time, msg_data.game_time))
            elif msg_in.GetHeader().msg_type == RTMA_types.MT_FOFIX_INPUT:
                msg_data = RTMA_types.MDF_FOFIX_INPUT()
                RTMA.copy_from_msg(msg_data, msg_in)
                print('INPUT - notes_strummed: {}, game_time: {}, hit_note: {}'.format(msg_data.notes_strummed[0:5], msg_data.game_time, msg_data.hit_note))
            elif msg_in.GetHeader().msg_type == RTMA_types.MT_FOFIX_MISSED:
                msg_data = RTMA_types.MDF_FOFIX_MISSED()
                RTMA.copy_from_msg(msg_data, msg_in)
                print('MISSED - note: {}, target_time: {}, game_time: {}'.format(msg_data.note, msg_data.target_time, msg_data.game_time))
            elif not bool(rm_ret):
                pass
            else:
                print('Received Unhandled Message: {}'.format(msg_in.GetHeader().msg_type))
        except KeyboardInterrupt:
            break

mod.DisconnectFromMMM()