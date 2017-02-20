import imageio
import struct
import zlib
import numpy

class Data(object):
    def __init__(self):
        filename = '/Users/bzztbomb/projects/mame/snap/movie.avi'
        self._vid = imageio.get_reader(filename, 'ffmpeg')
        self._videocount = 0
        for _ in self._vid:
            self._videocount += 1

        inp_file = '/Users/bzztbomb/projects/mame/inp/moves'
        data = open(inp_file, "rb").read()
        magic = struct.Struct('q').unpack(b'MAMEINP\x00')[0]
        header_struct = struct.Struct('=qqbbH12s32s')
        (header, basetime, version_major, version_minor, reserved, sysname, appdesc) = header_struct.unpack(data[:64])

        moves = zlib.decompress(data[64:])
        record_struct = struct.Struct('=iqIIIIIII')
        # robotron has three input ports
        moveSize = 40
        totalMoves = len(moves) // moveSize

        begin = 0
        self._moves = []
        for i in range(totalMoves):
            (seconds, attoseconds, machine_speed, port0_def, port0_value, port1_def, port1_value, port2_def, port2_value) = record_struct.unpack(moves[begin:begin+moveSize])
            begin = begin + moveSize

            move_updown = self.port_to_axis(port0_value, 0x2, 0x1)
            move_leftright = self.port_to_axis(port0_value, 0x4, 0x8)
            fire_updown = self.port_to_axis(port0_value, 0x80, 0x40)
            fire_leftright = self.port_to_axis(port1_value, 0x1, 0x2)
            start = self.port_to_axis(port0_value, 0x100000, 0x10)

            self._moves.append((move_updown, move_leftright, fire_updown, fire_leftright, start))
        self._epochs_completed = 0
        self._index_in_epoch = 0
        print ("INP moves: " + str(totalMoves))
        print ("VIDEO frames: " + str(self._videocount))
        if (totalMoves < self._videocount):
            self._num_examples = totalMoves
        else:
            self._num_examples = self._videocount

    def port_to_axis(self, portval, low, high):
        if (portval & low):
            return -1
        if (portval & high):
            return 1
        return 0

    @property
    def num_examples(self):
        return self._num_examples

    def next_batch(self, batch_size):
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch

        X = []
        for i in range(start, end):
            X.append(self._vid.get_data(i))

        return numpy.array(X), numpy.array(self._moves[start:end])
