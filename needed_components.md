
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



| Component name          | Verilog needed | Verilog created |
|-------------------------|----------------|-----------------|
| Error                   |                | ?               |
| Off                     | yes            | yes             |
| On                      | yes            | yes             |
| Buffer1                 |                | yes             |
| Not                     | yes            | yes             |
| And                     | yes            | yes             |
| And3                    | yes            | yes             |
| Nand                    | yes            | yes             |
| Or                      | yes            | yes             |
| Or3                     | yes            | yes             |
| Nor                     | yes            | yes             |
| Xor                     | yes            | yes             |
| Xnor                    | yes            | yes             |
| Counter8                | yes            | *1              |
| VirtualCounter8         |                |                 |
| Counter64               | yes            | *1              |
| VirtualCounter64        |                |                 |
| Ram                     | (later)        | *1              |
| VirtualRam              |                |                 |
| DELETED_0               |                |                 |
| DELETED_1               |                |                 |
| Stack                   | (later)        | *1              |
| VirtualStack            |                |                 |
| Register8               | yes            | *1              |
| VirtualRegister8        |                |                 |
| Register8Red            |                |                 |
| VirtualRegister8Red     |                |                 |
| Register8RedPlus        |                |                 |
| VirtualRegister8RedPlus |                |                 |
| Register64              | yes            | *1              |
| VirtualRegister64       |                |                 |
| Switch8                 | yes            | yes             |
| Mux8                    | yes            | yes             |
| Decoder1                | yes            | yes             |
| Decoder3                | yes            | yes             |
| Constant8               | yes            | yes             |
| Not8                    | yes            | yes             |
| Or8                     | yes            | yes             |
| And8                    | yes            | yes             |
| Xor8                    | yes            | yes             |
| Equal8                  | yes            | yes             |
| DELETED_2               |                |                 |
| DELETED_3               |                |                 |
| Neg8                    | yes            | yes             |
| Add8                    | yes            | yes             |
| Mul8                    | yes            | yes             |
| Splitter8               | (maybe)        | *4              |
| Maker8                  | (maybe)        | *4              |
| Splitter64              | (maybe)        | *4              |
| Maker64                 | (maybe)        | *4              |
| FullAdder               | yes            | yes             |
| BitMemory               | yes            | *1              |
| VirtualBitMemory        |                |                 |
| SRLatch                 | yes            | yes *2          |
| Decoder2                | yes            | yes             |
| Clock                   | (later)        | *3              |
| WaveformGenerator       | (later)        | *3              |
| DELETED_4               |                |                 |
| DELETED_5               |                |                 |
| Keypad                  |                |                 |
| FileRom                 |                | *3              |
| Halt                    | (maybe)        | ?               |
| WireCluster             | (maybe)        | ?               |
| Screen                  | (later)        | *3              |
| Program8_1              | (later)        | *1              |
| Program8_1Red           |                |                 |
| DONT_REUSE_0            |                |                 |
| DONT_REUSE_1            |                |                 |
| Program8_4              | (later)        | *1              |
| LevelGate               |                |                 |
| Input1                  |                |                 |
| Input2Pin               |                |                 |
| Input3Pin               |                |                 |
| Input4Pin               |                |                 |
| InputConditions         |                |                 |
| Input8                  |                |                 |
| Input64                 |                |                 |
| InputCode               |                |                 |
| Input1_1B               |                |                 |
| Output1                 |                |                 |
| Output1Sum              |                |                 |
| Output1Car              |                |                 |
| Output1Aval             |                |                 |
| Output1Bval             |                |                 |
| Output2Pin              |                |                 |
| Output3Pin              |                |                 |
| Output4Pin              |                |                 |
| Output8                 |                |                 |
| Output64                |                |                 |
| Output1_1B              |                |                 |
| OutputCounter           |                |                 |
| InputOutput             |                |                 |
| Custom                  |                |                 |
| VirtualCustom           |                |                 |
| ProgramWord             | (later)        | *1              |
| DelayLine1              | yes            | *1              |
| VirtualDelayLine1       |                |                 |
| Console                 | (later)        | *3              |
| Shl8                    | yes            | yes             |
| Shr8                    | yes            | yes             |
| Constant64              | yes            |                 |
| Not64                   | yes            |                 |
| Or64                    | yes            |                 |
| And64                   | yes            |                 |
| Xor64                   | yes            |                 |
| Neg64                   | yes            |                 |
| Add64                   | yes            |                 |
| Mul64                   | yes            |                 |
| Equal64                 | yes            |                 |
| LessU64                 | yes            |                 |
| LessI64                 | yes            |                 |
| Shl64                   | yes            |                 |
| Shr64                   | yes            |                 |
| Mux64                   | yes            |                 |
| Switch64                | yes            |                 |
| ProbeComponentBit       |                |                 |
| ProbeComponentWord      |                |                 |
| AndOrLatch              | yes            | *2              |
| NandNandLatch           | yes            | yes *2          |
| NorNorLatch             | yes            | yes *2          |
| LessU8                  | yes            | yes             |
| LessI8                  | yes            | yes             |
| DotMatrixDisplay        | (later)        | *3              |
| SegmentDisplay          | (later)        | *3              |
| Input16                 |                |                 |
| Input32                 |                |                 |
| Output16                |                |                 |
| Output32                |                |                 |
| Bidirectional1          |                |                 |
| Bidirectional8          |                |                 |
| Bidirectional16         |                |                 |
| Bidirectional32         |                |                 |
| Bidirectional64         |                |                 |
| Buffer8                 | yes            |                 |
| Buffer16                | yes            |                 |
| Buffer32                | yes            |                 |
| Buffer64                | yes            |                 |
| ProbeWireBit            |                |                 |
| ProbeWireWord           |                |                 |
| Switch1                 | yes            |                 |
 | Output1z                |                |                 |
 | Output8z                |                |                 |
 | Output16z               |                |                 |
 | Output32z               |                |                 |
 | Output64z               |                |                 |
 | Constant16              |                |                 |
 | Not16                   | yes            |                 |
 | Or16                    | yes            |                 |
 | And16                   | yes            |                 |
 | Xor16                   | yes            |                 |
 | Neg16                   | yes            |                 |
 | Add16                   | yes            |                 |
 | Mul16                   | yes            |                 |
 | Equal16                 | yes            |                 |
 | LessU16                 | yes            |                 |
 | LessI16                 | yes            |                 |
 | Shl16                   | yes            |                 |
 | Shr16                   | yes            |                 |
 | Mux16                   | yes            |                 |
 | Switch16                | yes            |                 |
 | Splitter16              | (maybe)        |                 |
 | Maker16                 | (maybe)        |                 |
 | Register16              | yes            |                 |
 | VirtualRegister16       |                |                 |
 | Counter16               | yes            |                 |
 | VirtualCounter16        |                |                 |
 | Constant32              | yes            |                 |
 | Not32                   | yes            |                 |
 | Or32                    | yes            |                 |
 | And32                   | yes            |                 |
 | Xor32                   | yes            |                 |
 | Neg32                   | yes            |                 |
 | Add32                   | yes            |                 |
 | Mul32                   | yes            |                 |
 | Equal32                 | yes            |                 |
 | LessU32                 | yes            |                 |
 | LessI32                 | yes            |                 |
 | Shl32                   | yes            |                 |
 | Shr32                   | yes            |                 |
 | Mux32                   | yes            |                 |
 | Switch32                | yes            |                 |
 | Splitter32              | yes            |                 |
 | Maker32                 | yes            |                 |
 | Register32              | yes            |                 |
 | VirtualRegister32       | yes            |                 |
 | Counter32               | yes            |                 |
 | VirtualCounter32        |                |                 |
 | Output8zLevel           |                |                 |
 | Nand8                   | yes            |                 |
 | Nor8                    | yes            |                 |
 | Xnor8                   | yes            |                 |
 | Nand16                  | yes            |                 |
 | Nor16                   | yes            |                 |
 | Xnor16                  | yes            |                 |
 | Nand32                  | yes            |                 |
 | Nor32                   | yes            |                 |
 | Xnor32                  | yes            |                 |
 | Nand64                  | yes            |                 |
 | Nor64                   | yes            |                 |
 | Xnor64                  | yes            |                 |
 | CheapRam                | (later)        |                 |
 | VirtualCheapRam         |                |                 |
 | CheapRamLat             | (later)        |                 |
 | VirtualCheapRamLat      |                |                 |
 | FastRam                 | (later)        |                 |
 | VirtualFastRam          |                |                 |
 | Rom                     | (later)        |                 |
 | VirtualRom              |                |                 |
 | SolutionRom             | ?              |                 |
 | VirtualSolutionRom      |                |                 |
 | DelayLine8              | yes            |                 |
 | VirtualDelayLine8       |                |                 |
 | DelayLine16             | yes            |                 |
 | VirtualDelayLine16      |                |                 |
 | DelayLine32             | yes            |                 |
 | VirtualDelayLine32      |                |                 |
 | DelayLine64             | yes            |                 |
 | VirtualDelayLine64      |                |                 |
 | DualLoadRam             | (later)        |                 |
 | VirtualDualLoadRam      |                |                 |
 | Hdd                     | (later)        |                 |
 | VirtualHdd              |                |                 |