import sys

def writeJumpCase(file, line, holeCount, offset, clockwise = -1):
    index = offset

    for time in range(holeCount - 2):
        text = ','.join([str(elem) for elem in line])
        index = index + 1

        if clockwise == -1: 
            text = text[::-1]
            
        file.write("{} Jump({},{})\n".format(index, text, time + 1))
    
    return index


def writePegCase(file, holeCount, offset):
    index = offset

    for peg in range(holeCount):
        for time in range(holeCount - 1):
            index = index + 1
            file.write("{} Peg({},{})\n".format(index, peg + 1, time + 1))


def writeCausal(file, line, holeCount, offset, offset2Peg):
    index = offset

    for time in range(holeCount - 2):
        index = index + 1
        pegIdx = 0
        a = -1

        for peg in line:
            if pegIdx > 1: a = 1
            file.write("{} {}\n".format(-index, a * (offset2Peg + (peg - 1) * (holeCount - 1) + time + 2)))
            pegIdx = pegIdx + 1
        
    return index


def writePrecondition(file, line, holeCount, offset, offset2Peg):
    index = offset

    for time in range(holeCount - 2):
        index = index + 1
        pegIdx = 0
        a = 1

        for peg in line:
            if pegIdx > 1: a = -1
            file.write("{} {}\n".format(-index, a * (offset2Peg + (peg - 1) * (holeCount - 1) + time + 1)))
            pegIdx = pegIdx + 1
        
    return index


def writeFrameA(file, triples, holeCount, offset):
    index = offset + 1

    for line in triples:
        line.reverse()

    for peg in range(holeCount):
        for time in range(holeCount - 2):
            array = []
            jmpIdx = 0

            for line in triples:
                if line[0] == peg + 1 or line[1] == peg + 1:
                    array.append(jmpIdx * (holeCount - 2) * 2 + time + 1)
                
                if line[2] == peg + 1 or line[1] == peg + 1:
                    array.append((jmpIdx * 2 + 1) * (holeCount - 2) + time + 1)

                jmpIdx = jmpIdx + 1

            file.write("{} {} {}\n".format(-index, index + 1, ' '.join([str(elem) for elem in array])))
            index = index + 1
        
        index = index + 1


def writeFrameB(file, triples, holeCount, offset):
    index = offset + 1

    for peg in range(holeCount):
        for time in range(holeCount - 2):
            array = []
            jmpIdx = 0

            for line in triples:
                if line[0] == peg + 1:
                    array.append((jmpIdx * 2 + 1) * (holeCount - 2) + time + 1)

                if line[2] == peg + 1:
                    array.append(jmpIdx * 2 * (holeCount - 2) + time + 1)

                jmpIdx = jmpIdx + 1

            file.write("{} {} {}\n".format(index, -index - 1, ' '.join([str(elem) for elem in array])))
            index = index + 1
        
        index = index + 1


def writeOneAction(file, holeCount, offset2Peg):
    for jmpIdx in range(offset2Peg):
        jmpIdxTmp = jmpIdx + holeCount - 2

        while True:
            if jmpIdxTmp >= offset2Peg:
                break

            file.write("{} {}\n".format(-jmpIdx - 1, -jmpIdxTmp - 1))
            jmpIdxTmp = jmpIdxTmp + holeCount - 2


def writeStarting(file, startIdx, holeCount, offset2Peg):
    for pegIdx in range(holeCount):
        a = 1

        if pegIdx == startIdx - 1:
            a = -1

        file.write("{}\n".format(a * (offset2Peg + 1 + (holeCount - 1) * pegIdx)))


def writeEndingA(file, holeCount, offset2Peg):
    for pegIdx in range(holeCount):
        file.write("{} ".format(offset2Peg  + (holeCount - 1) * (pegIdx + 1)))

    file.write("\n")

def writeEndingB(file, holeCount, offset2Peg):
    for pegIdx in range(holeCount):
        hIdx = offset2Peg  + (holeCount - 1) * (pegIdx + 1)
        pegIdxTmp = pegIdx + 1

        while True:
            if pegIdxTmp > holeCount - 1:
                break

            jIdx = offset2Peg  + (holeCount - 1) * (pegIdxTmp + 1)
            pegIdxTmp = pegIdxTmp + 1

            file.write("{} {}\n".format(-hIdx, -jIdx))


def main(argv):
    with open('input.txt') as f1, open('propositions.txt', 'w') as f2, open('output.txt', 'w') as f3:
        holeCount, startIdx = [int(x) for x in next(f1).split()]
        triples = [[int(x) for x in line.split()] for line in f1]
        index = 0

        # Write JumpCase
        for line in triples:
            index = writeJumpCase(f2, line, holeCount, index, 1)
            index = writeJumpCase(f2, line, holeCount, index)

        # Write PegCase
        writePegCase(f2, holeCount, index)
        
        # Precondition Axioms
        offset2Peg = len(triples) * (holeCount - 2) * 2
        index = 0

        for line in triples:
            index = writePrecondition(f3, line, holeCount, index, offset2Peg)

            line.reverse()
            index = writePrecondition(f3, line, holeCount, index, offset2Peg)

        # Causal Axioms
        index = 0
        for line in triples:
            line.reverse()
            index = writeCausal(f3, line, holeCount, index, offset2Peg)

            line.reverse()  
            index = writeCausal(f3, line, holeCount, index, offset2Peg)

        # Frame Axioms (a)
        writeFrameA(f3, triples, holeCount, index)

        # Frame Axioms (b)
        writeFrameB(f3, triples, holeCount, index)

        # Frame Axioms (b)
        writeOneAction(f3, holeCount, offset2Peg)

        # Starting State
        writeStarting(f3, startIdx, holeCount, offset2Peg)

        # Ending State (a)
        writeEndingA(f3, holeCount, offset2Peg)

        # Ending State (b)
        writeEndingB(f3, holeCount, offset2Peg)

        f1.close()
        f2.close()
        f3.close()


if __name__ == "__main__":
    main(sys.argv)