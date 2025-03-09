from rtp import RTP
from rtp import PayloadType


class DTMF:
    EVENT_NUMBERS = {
        # {Signal name: RFC2833 event}
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "*": 10,
        "#": 11,
        "A": 12,
        "B": 13,
        "C": 14,
        "D": 15,
        "Flash": 16,
    }

    @classmethod
    def make_numbers_packets(
            cls,
            numbers: str,
            payload_type: PayloadType = PayloadType.DYNAMIC_101,
            tone_packets_count: int = 10
    ) -> list[bytes]:
        if tone_packets_count < 6:
            raise RuntimeError('Too few packets.')

        res_packets = []
        timestamp = 1
        sequence = None
        ssrc = None
        for number in numbers:
            packets = []

            number = cls.EVENT_NUMBERS[number].to_bytes(length=1, byteorder="big")

            for p in range(1, tone_packets_count):
                event_duration = p * 160
                if p > tone_packets_count-3:  # end event
                    dtmf_payload = (
                        number
                        + (0b10001010).to_bytes(length=1, byteorder="big")
                        + event_duration.to_bytes(length=2, byteorder="big")
                    )
                else:
                    dtmf_payload = (
                        number
                        + (0b00001010).to_bytes(length=1, byteorder="big")
                        + event_duration.to_bytes(length=2, byteorder="big")
                    )

                if p == 1:
                    pack = RTP(
                        marker=True,
                        payloadType=payload_type,
                        timestamp=timestamp,
                        payload=bytearray(dtmf_payload),
                    )
                    sequence = pack.sequenceNumber if not sequence else sequence + 1
                    ssrc = pack.ssrc if not ssrc else ssrc
                    pack.sequenceNumber = sequence
                    pack.ssrc = ssrc
                else:
                    sequence += 1
                    pack = RTP(
                        marker=False,
                        payloadType=payload_type,
                        timestamp=timestamp,
                        payload=bytearray(dtmf_payload),
                        sequenceNumber=sequence,
                        ssrc=ssrc,
                    )
                packets.append(pack.toBytes())
            timestamp += 160
            res_packets.extend(packets)
        return res_packets
