
The corresponding components should be in a file ``<Component name>.v`` in [``verilog-components``](verilog-components) and define a module of the same name.
The module should have a port signature ``(clock, reset, inputs..., outputs...)`` where the pins are in the order they are in TC top to bottom.
The names of the ports need be in sync with [``tc2verilog/tc_components.py``](tc2verilog/tc_components.py)


| Component name         | Verilog needed | Verilog created |
|------------------------|----------------|-----------------|
| Error                  |                |                 |
| Off                    | yes            |                 |
| On                     | yes            |                 |
| Buffer1                |                |                 |
| Not                    | yes            |                 |
| And                    | yes            |                 |
| And3                   | yes            |                 |
| Nand                   | yes            |                 |
| Or                     | yes            |                 |
| Or3                    | yes            |                 |
| Nor                    | yes            |                 |
| Xor                    | yes            |                 |
| Xnor                   | yes            |                 |
| ByteCounter            | yes            |                 |
| VirtualByteCounter     |                |                 |
| QwordCounter           | yes            |                 |
| VirtualQwordCounter    |                |                 |
| Ram                    | yes            |                 |
| VirtualRam             |                |                 |
| QwordRam               | yes            |                 |
| VirtualQwordRam        |                |                 |
| Stack                  | yes            |                 |
| VirtualStack           |                |                 |
| Register               | yes            |                 |
| VirtualRegister        |                |                 |
| RegisterRed            |                |                 |
| VirtualRegisterRed     |                |                 |
| RegisterRedPlus        |                |                 |
| VirtualRegisterRedPlus |                |                 |
| QwordRegister          | yes            |                 |
| VirtualQwordRegister   |                |                 |
| ByteSwitch             | yes            |                 |
| ByteMux                | yes            |                 |
| Decoder1               | yes            |                 |
| Decoder3               | yes            |                 |
| ByteConstant           | yes            |                 |
| ByteNot                | yes            |                 |
| ByteOr                 | yes            |                 |
| ByteAnd                | yes            |                 |
| ByteXor                | yes            |                 |
| ByteEqual              | yes            |                 |
| ByteLessUOld           |                |                 |
| ByteLessIOld           |                |                 |
| ByteNeg                | yes            |                 |
| ByteAdd                | yes            |                 |
| ByteMul                | yes            |                 |
| ByteSplitter           | (maybe)        |                 |
| ByteMaker              | (maybe)        |                 |
| QwordSplitter          | (maybe)        |                 |
| QwordMaker             | (maybe)        |                 |
| FullAdder              | yes            |                 |
| BitMemory              | yes            |                 |
| VirtualBitMemory       |                |                 |
| SRLatch                | yes            |                 |
| DELETED_0              |                |                 |
| Clock                  | (later)        |                 |
| WaveformGenerator      | (later)        |                 |
| HttpClient             |                |                 |
| DELETED_1              |                |                 |
| Keypad                 |                |                 |
| FileRom                |                |                 |
| Halt                   | (maybe)        |                 |
| WireCluster            | (maybe)        |                 |
| Screen                 | (later)        |                 |
| Program1               | (later)        |                 |
| Program1Red            |                |                 |
| DELETED_2              |                |                 |
| DELETED_3              |                |                 |
| Program4               | (later)        |                 |
| LevelGate              |                |                 |
| Input1                 |                |                 |
| Input2Pin              |                |                 |
| Input3Pin              |                |                 |
| Input4Pin              |                |                 |
| InputConditions        |                |                 |
| Input8                 |                |                 |
| Input64                |                |                 |
| InputCode              |                |                 |
| Input1_1B              |                |                 |
| Output1                |                |                 |
| Output1Sum             |                |                 |
| Output1Car             |                |                 |
| Output1Aval            |                |                 |
| Output1Bval            |                |                 |
| Output2Pin             |                |                 |
| Output3Pin             |                |                 |
| Output4Pin             |                |                 |
| Output8                |                |                 |
| Output64               |                |                 |
| Output1_1B             |                |                 |
| OutputCounter          |                |                 |
| InputOutput            |                |                 |
| Custom                 |                |                 |
| VirtualCustom          |                |                 |
| QwordProgram           | (later)        |                 |
| DelayLine              | yes            |                 |
| VirtualDelayLine       |                |                 |
| Console                | (later)        |                 |
| ByteShl                | yes            |                 |
| ByteShr                | yes            |                 |
| QwordConstant          | yes            |                 |
| QwordNot               | yes            |                 |
| QwordOr                | yes            |                 |
| QwordAnd               | yes            |                 |
| QwordXor               | yes            |                 |
| QwordNeg               | yes            |                 |
| QwordAdd               | yes            |                 |
| QwordMul               | yes            |                 |
| QwordEqual             | yes            |                 |
| QwordLessU             | yes            |                 |
| QwordLessI             | yes            |                 |
| QwordShl               | yes            |                 |
| QwordShr               | yes            |                 |
| QwordMux               | yes            |                 |
| QwordSwitch            | yes            |                 |
| ProbeComponentBit      |                |                 |
| ProbeComponentWord     |                |                 |
| AndOrLatch             | yes            |                 |
| NandNandLatch          | yes            |                 |
| NorNorLatch            | yes            |                 |
| ByteLessU              | yes            |                 |
| ByteLessI              | yes            |                 |
| DotMatrixDisplay       | (later)        |                 |
| SegmentDisplay         | (later)        |                 |
| Input16                |                |                 |
| Input32                |                |                 |
| Output16               |                |                 |
| Output32               |                |                 |
| Bidirectional1         |                |                 |
| Bidirectional8         |                |                 |
| Bidirectional16        |                |                 |
| Bidirectional32        |                |                 |
| Bidirectional64        |                |                 |
| Buffer8                |                |                 |
| Buffer16               |                |                 |
| Buffer32               |                |                 |
| Buffer64               |                |                 |
| ProbeWireBit           |                |                 |
| ProbeWireWord          |                |                 |