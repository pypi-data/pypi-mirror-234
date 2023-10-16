import maxwell.protocol.maxwell_protocol_pb2 as maxwell_protocol_pb2


def encode_msg(msg):
    if msg.__class__ == maxwell_protocol_pb2.auth_rep_t:
        return (42).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.auth_req_t:
        return (41).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.error2_rep_t:
        return (32).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.error_rep_t:
        return (30).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.get_routes_rep_t:
        return (76).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.get_routes_req_t:
        return (75).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.get_route_dist_checksum_rep_t:
        return (80).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.get_route_dist_checksum_req_t:
        return (79).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.get_topic_dist_checksum_rep_t:
        return (78).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.get_topic_dist_checksum_req_t:
        return (77).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.locate_topic_rep_t:
        return (86).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.locate_topic_req_t:
        return (85).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.ok2_rep_t:
        return (31).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.ok_rep_t:
        return (29).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.pick_frontends_rep_t:
        return (84).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.pick_frontends_req_t:
        return (83).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.pick_frontend_rep_t:
        return (82).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.pick_frontend_req_t:
        return (81).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.ping_rep_t:
        return (2).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.ping_req_t:
        return (1).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.pull_rep_t:
        return (36).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.pull_req_t:
        return (35).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.push_rep_t:
        return (34).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.push_req_t:
        return (33).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.register_backend_rep_t:
        return (68).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.register_backend_req_t:
        return (67).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.register_frontend_rep_t:
        return (66).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.register_frontend_req_t:
        return (65).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.register_service_rep_t:
        return (70).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.register_service_req_t:
        return (69).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.req_rep_t:
        return (40).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.req_req_t:
        return (39).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.resolve_ip_rep_t:
        return (122).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.resolve_ip_req_t:
        return (121).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.set_routes_rep_t:
        return (72).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    elif msg.__class__ == maxwell_protocol_pb2.set_routes_req_t:
        return (71).to_bytes(1, 'little', signed=False) + msg.SerializeToString()
    else:
      raise TypeError(f"Unknown msg type: {msg.__class__}")


def decode_msg(encoded_msg):
    msg_type_uint32 = int.from_bytes(encoded_msg[:1], byteorder='little')
    if msg_type_uint32 == 42:
        msg = maxwell_protocol_pb2.auth_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 41:
        msg = maxwell_protocol_pb2.auth_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 32:
        msg = maxwell_protocol_pb2.error2_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 30:
        msg = maxwell_protocol_pb2.error_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 76:
        msg = maxwell_protocol_pb2.get_routes_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 75:
        msg = maxwell_protocol_pb2.get_routes_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 80:
        msg = maxwell_protocol_pb2.get_route_dist_checksum_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 79:
        msg = maxwell_protocol_pb2.get_route_dist_checksum_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 78:
        msg = maxwell_protocol_pb2.get_topic_dist_checksum_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 77:
        msg = maxwell_protocol_pb2.get_topic_dist_checksum_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 86:
        msg = maxwell_protocol_pb2.locate_topic_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 85:
        msg = maxwell_protocol_pb2.locate_topic_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 31:
        msg = maxwell_protocol_pb2.ok2_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 29:
        msg = maxwell_protocol_pb2.ok_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 84:
        msg = maxwell_protocol_pb2.pick_frontends_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 83:
        msg = maxwell_protocol_pb2.pick_frontends_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 82:
        msg = maxwell_protocol_pb2.pick_frontend_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 81:
        msg = maxwell_protocol_pb2.pick_frontend_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 2:
        msg = maxwell_protocol_pb2.ping_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 1:
        msg = maxwell_protocol_pb2.ping_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 36:
        msg = maxwell_protocol_pb2.pull_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 35:
        msg = maxwell_protocol_pb2.pull_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 34:
        msg = maxwell_protocol_pb2.push_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 33:
        msg = maxwell_protocol_pb2.push_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 68:
        msg = maxwell_protocol_pb2.register_backend_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 67:
        msg = maxwell_protocol_pb2.register_backend_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 66:
        msg = maxwell_protocol_pb2.register_frontend_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 65:
        msg = maxwell_protocol_pb2.register_frontend_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 70:
        msg = maxwell_protocol_pb2.register_service_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 69:
        msg = maxwell_protocol_pb2.register_service_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 40:
        msg = maxwell_protocol_pb2.req_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 39:
        msg = maxwell_protocol_pb2.req_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 122:
        msg = maxwell_protocol_pb2.resolve_ip_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 121:
        msg = maxwell_protocol_pb2.resolve_ip_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 72:
        msg = maxwell_protocol_pb2.set_routes_rep_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    elif msg_type_uint32 == 71:
        msg = maxwell_protocol_pb2.set_routes_req_t()
        msg.ParseFromString(encoded_msg[1:])
        return msg
    else:
      raise TypeError(f"Unknown msg type: {msg_type_uint32}")
