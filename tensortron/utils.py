import imageio
import struct
import zlib
import numpy

class Data(object):
    def __init__(self):
        filename = '/Users/bzztbomb/projects/mame/snap/bob.avi'
        self._vid = imageio.get_reader(filename, 'ffmpeg')
        self._videocount = 0
        for _ in self._vid:
            self._videocount += 1

        inp_file = '/Users/bzztbomb/projects/mame/inp/inputs4'
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
            self._moves.append((port0_value, port1_value))
        self._epochs_completed = 0
        self._index_in_epoch = 0
        if (totalMoves < self._videocount):
            self._num_examples = totalMoves
        else:
            self._num_examples = self._videocount

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
