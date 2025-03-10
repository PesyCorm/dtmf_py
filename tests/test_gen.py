from rtp import RTP, PayloadType

from dtmf_py import DTMF


def test_gen():
    packets = DTMF.make_numbers_packets('1', payload_type=PayloadType.DYNAMIC_101)
    for i, pack in enumerate(packets):
        decoded_pack = RTP().fromBytes(pack)
        if i == 0:
            assert decoded_pack.marker == True, 'First packet must have Marker = True'
        assert decoded_pack.payloadType == PayloadType.DYNAMIC_101, 'Packet must have expected payload type'
        assert decoded_pack.version == 2, 'Packet must have version == 2'
