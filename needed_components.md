
The corresponding components should be in a file ``<Component name>.v`` in [``verilog-components``](verilog-components) and define a module of the same name.
The module should have a port signature ``(clock, reset, inputs..., outputs...)`` where the pins are in the order they are in TC top to bottom.
The names of the ports need be in sync with [``tc2verilog/tc_components.py``](tc2verilog/tc_components.py)

---

logxen> a number of these component names (such as on, not, and, or, etc...) are reserved words in verilog and so are not valid module names. I have prepended "TC_" to the module names for now.

I went ahead and implemented the Buffer1 because you might need a buffer to connect two wires with different names.

  *1 synchronous devices ... these need clock and reset so I'm skipping them for the moment to complete the easy ones

  *2 latches ... latches are considered Bad Things in the fpga and asic world as they difficult to implement and can lead to poor timing results. we are supposed to stick to synchronous clocked memory stuff.

  *3 hardware peripherals ... these things are likely not portable and will have to be targetted to specific hardware platforms. as memory mapped devices they will also need clock and reset.
  
  *4 I have collapsed things to busses. it is very easy to select wires from busses and build new busses from them in verilog. they work a lot like arrays. so I think these parts probably do not need to be implemented as modules.

---



| Component name         | Verilog needed | Verilog created |
|------------------------|----------------|-----------------|
| Error                  |                | ?               |
| Off                    | yes            | yes             |
| On                     | yes            | yes             |
| Buffer1                |                | yes             |
| Not                    | yes            | yes             |
| And                    | yes            | yes             |
| And3                   | yes            | yes             |
| Nand                   | yes            | yes             |
| Or                     | yes            | yes             |
| Or3                    | yes            | yes             |
| Nor                    | yes            | yes             |
| Xor                    | yes            | yes             |
| Xnor                   | yes            | yes             |
| ByteCounter            | yes            | *1              |
| VirtualByteCounter     |                |                 |
| QwordCounter           | yes            | *1              |
| VirtualQwordCounter    |                |                 |
| Ram                    | (later)        | *1              |
| VirtualRam             |                |                 |
| QwordRam               | (later)        | *1              |
| VirtualQwordRam        |                |                 |
| Stack                  | (later)        | *1              |
| VirtualStack           |                |                 |
| Register               | yes            | *1              |
| VirtualRegister        |                |                 |
| RegisterRed            |                |                 |
| VirtualRegisterRed     |                |                 |
| RegisterRedPlus        |                |                 |
| VirtualRegisterRedPlus |                |                 |
| QwordRegister          | yes            | *1              |
| VirtualQwordRegister   |                |                 |
| ByteSwitch             | yes            | yes             |
| ByteMux                | yes            | yes             |
| Decoder1               | yes            | yes             |
| Decoder2               |                | yes             |
| Decoder3               | yes            | yes             |
| ByteConstant           | yes            | yes             |
| ByteNot                | yes            | yes             |
| ByteOr                 | yes            | yes             |
| ByteAnd                | yes            | yes             |
| ByteXor                | yes            | yes             |
| ByteEqual              | yes            | yes             |
| ByteLessUOld           |                |                 |
| ByteLessIOld           |                |                 |
| ByteNeg                | yes            | yes             |
| ByteAdd                | yes            | yes             |
| ByteMul                | yes            | yes             |
| ByteSplitter           | (maybe)        | *4              |
| ByteMaker              | (maybe)        | *4              |
| QwordSplitter          | (maybe)        | *4              |
| QwordMaker             | (maybe)        | *4              |
| FullAdder              | yes            | yes             |
| BitMemory              | yes            | *1              |
| VirtualBitMemory       |                |                 |
| SRLatch                | yes            | yes *2          |
| DELETED_0              |                |                 |
| Clock                  | (later)        | *3              |
| WaveformGenerator      | (later)        | *3              |
| HttpClient             |                | *3              |
| DELETED_1              |                |                 |
| Keypad                 |                |                 |
| FileRom                |                | *3              |
| Halt                   | (maybe)        | ?               |
| WireCluster            | (maybe)        | ?               |
| Screen                 | (later)        | *3              |
| Program1               | (later)        | *1              |
| Program1Red            |                |                 |
| DELETED_2              |                |                 |
| DELETED_3              |                |                 |
| Program4               | (later)        | *1              |
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
| QwordProgram           | (later)        | *1              |
| DelayLine              | yes            | *1              |
| VirtualDelayLine       |                |                 |
| Console                | (later)        | *3              |
| ByteShl                | yes            | yes             |
| ByteShr                | yes            | yes             |
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
| AndOrLatch             | yes            | *2              |
| NandNandLatch          | yes            | yes *2          |
| NorNorLatch            | yes            | yes *2          |
| ByteLessU              | yes            | yes             |
| ByteLessI              | yes            | yes             |
| DotMatrixDisplay       | (later)        | *3              |
| SegmentDisplay         | (later)        | *3              |
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
