
The corresponding components should be in a file ``<Component name>.v`` in [``verilog-components``](verilog-components) and define a module of the same name.
The module should have a port signature ``(clock, reset, inputs..., outputs...)`` where the pins are in the order they are in TC top to bottom.
The names of the ports need be in sync with [``tc2verilog/tc_components.py``](tc2verilog/tc_components.py)

---

logxen> almost everything now has a size parameter to control its bit width. exceptions include Decoders, FullAdder, latches, splitters and makers. Shl and Shr are also not parameterized yet because the shift width is log2(size) and I haven't figured out what to do about that yet. ><

  *1 synchronous devices ... these need clock and reset so I'm skipping them for the moment to complete the easy ones

  *2 latches ... latches are considered Bad Things in the fpga and asic world as they difficult to implement and can lead to poor timing results. we are supposed to stick to synchronous clocked memory stuff.

  *3 hardware peripherals ... these things are likely not portable and will have to be targetted to specific hardware platforms. as memory mapped devices they will also need clock and reset.

---



| Component name          | Verilog needed | Verilog created | in py |
|-------------------------|----------------|-----------------|-------|
| Error                   |                | ?               |       |
| Off                     | via Constant   | yes             | yes   |
| On                      | via Constant   | yes             | yes   |
| Buffer1                 |                | yes             | yes   |
| Not                     | yes            | yes             | yes   |
| And                     | yes            | yes             | yes   |
| And3                    | yes            | yes             | yes   |
| Nand                    | yes            | yes             | yes   |
| Or                      | yes            | yes             | yes   |
| Or3                     | yes            | yes             | yes   |
| Nor                     | yes            | yes             | yes   |
| Xor                     | yes            | yes             | yes   |
| Xnor                    | yes            | yes             | yes   |
| Counter8                | yes            | yes             | yes   |
| VirtualCounter8         |                |                 |       |
| Counter64               | yes            | yes             | yes   |
| VirtualCounter64        |                |                 |       |
| Ram                     | (later)        | yes             | yes   |
| VirtualRam              |                |                 |       |
| DELETED_0               |                |                 |       |
| DELETED_1               |                |                 |       |
| Stack                   | (later)        | *1            * |       |
| VirtualStack            |                |                 |       |
| Register8               | yes            | yes             | yes   |
| VirtualRegister8        |                |                 |       |
| Register8Red            |                |                 |       |
| VirtualRegister8Red     |                |                 |       |
| Register8RedPlus        |                |                 |       |
| VirtualRegister8RedPlus |                |                 |       |
| Register64              | yes            | yes             | yes   |
| VirtualRegister64       |                |                 |       |
| Switch8                 | yes            | yes             | yes   |
| Mux8                    | yes            | yes             | yes   |
| Decoder1                | yes            | yes             | yes   |
| Decoder3                | yes            | yes             | yes   |
| Constant8               | yes            | yes             | yes   |
| Not8                    | yes            | yes             | yes   |
| Or8                     | yes            | yes             | yes   |
| And8                    | yes            | yes             | yes   |
| Xor8                    | yes            | yes             | yes   |
| Equal8                  | yes            | yes             | yes   |
| DELETED_2               |                |                 |       |
| DELETED_3               |                |                 |       |
| Neg8                    | yes            | yes             | yes   |
| Add8                    | yes            | yes             | yes   |
| Mul8                    | yes            | yes             | yes   |
| Splitter8               | (maybe)        | yes             | yes   |
| Maker8                  | (maybe)        | yes             | yes   |
| Splitter64              | (maybe)        | yes             | yes   |
| Maker64                 | (maybe)        | yes             | yes   |
| FullAdder               | yes            | yes             | yes   |
| BitMemory               | yes            |                 |       |
| VirtualBitMemory        |                |                 |       |
| SRLatch                 | yes            | yes *2          |       |
| Decoder2                | yes            | yes             | yes   |
| Clock                   | (later)        | *3              |       |
| WaveformGenerator       | (later)        | *3              |       |
| DELETED_4               |                |                 |       |
| DELETED_5               |                |                 |       |
| Keypad                  |                |                 |       |
| FileRom                 |                | *1            * |       |
| Halt                    | (maybe)        | ?               |       |
| WireCluster             | (maybe)        | ?               |       |
| Screen                  | (later)        |                 |       |
| Program8_1              | (later)        | yes             | yes   |
| Program8_1Red           |                |                 |       |
| DONT_REUSE_0            |                |                 |       |
| DONT_REUSE_1            |                |                 |       |
| Program8_4              | (later)        | yes             | yes   |
| LevelGate               |                |                 |       |
| Input1                  |                |                 | yes   |
| Input2Pin               |                |                 | yes   |
| Input3Pin               |                |                 | yes   |
| Input4Pin               |                |                 | yes   |
| InputConditions         |                |                 |       |
| Input8                  |                |                 | yes   |
| Input64                 |                |                 | yes   |
| InputCode               |                |                 |       |
| Input1_1B               |                |                 | yes   |
| Output1                 |                |                 | yes   |
| Output1Sum              |                |                 | yes   |
| Output1Car              |                |                 | yes   |
| Output1Aval             |                |                 |       |
| Output1Bval             |                |                 |       |
| Output2Pin              |                |                 | yes   |
| Output3Pin              |                |                 | yes   |
| Output4Pin              |                |                 | yes   |
| Output8                 |                |                 | yes   |
| Output64                |                |                 | yes   |
| Output1_1B              |                |                 | yes   |
| OutputCounter           |                |                 |       |
| InputOutput             |                |                 |       |
| Custom                  |                |                 |       |
| VirtualCustom           |                |                 |       |
| ProgramWord             | (later)        | yes             |       |
| DelayLine1              | yes            | yes             | yes   |
| VirtualDelayLine1       |                |                 |       |
| Console                 | (later)        | *3              |       |
| Shl8                    | yes            | yes             | yes   |
| Shr8                    | yes            | yes             | yes   |
| Constant64              | yes            | yes             | yes   |
| Not64                   | yes            | yes             | yes   |
| Or64                    | yes            | yes             | yes   |
| And64                   | yes            | yes             | yes   |
| Xor64                   | yes            | yes             | yes   |
| Neg64                   | yes            | yes             | yes   |
| Add64                   | yes            | yes             | yes   |
| Mul64                   | yes            | yes             | yes   |
| Equal64                 | yes            | yes             | yes   |
| LessU64                 | yes            | yes             | yes   |
| LessI64                 | yes            | yes             | yes   |
| Shl64                   | yes            | yes             | yes   |
| Shr64                   | yes            | yes             | yes   |
| Mux64                   | yes            | yes             | yes   |
| Switch64                | yes            | yes             | yes   |
| ProbeComponentBit       |                |                 |       |
| ProbeComponentWord      |                |                 |       |
| AndOrLatch              | yes            | *2              |       |
| NandNandLatch           | yes            | yes *2          |       |
| NorNorLatch             | yes            | yes *2          |       |
| LessU8                  | yes            | yes             | yes   |
| LessI8                  | yes            | yes             | yes   |
| DotMatrixDisplay        | (later)        | *3              |       |
| SegmentDisplay          | (later)        | *3              |       |
| Input16                 |                |                 | yes   |
| Input32                 |                |                 | yes   |
| Output16                |                |                 | yes   |
| Output32                |                |                 | yes   |
| Bidirectional1          |                |                 |       |
| Bidirectional8          |                |                 |       |
| Bidirectional16         |                |                 |       |
| Bidirectional32         |                |                 |       |
| Bidirectional64         |                |                 |       |
| Buffer8                 | yes            | yes             | yes   |
| Buffer16                | yes            | yes             | yes   |
| Buffer32                | yes            | yes             | yes   |
| Buffer64                | yes            | yes             | yes   |
| ProbeWireBit            |                |                 |       |
| ProbeWireWord           |                |                 |       |
| Switch1                 | yes            | yes             | yes   |
| Output1z                |                |                 |       |
| Output8z                |                |                 |       |
| Output16z               |                |                 |       |
| Output32z               |                |                 |       |
| Output64z               |                |                 |       |
| Constant16              | yes            | yes             | yes   |
| Not16                   | yes            | yes             | yes   |
| Or16                    | yes            | yes             | yes   |
| And16                   | yes            | yes             | yes   |
| Xor16                   | yes            | yes             | yes   |
| Neg16                   | yes            | yes             | yes   |
| Add16                   | yes            | yes             | yes   |
| Mul16                   | yes            | yes             | yes   |
| Equal16                 | yes            | yes             | yes   |
| LessU16                 | yes            | yes             | yes   |
| LessI16                 | yes            | yes             | yes   |
| Shl16                   | yes            | yes             | yes   |
| Shr16                   | yes            | yes             | yes   |
| Mux16                   | yes            | yes             | yes   |
| Switch16                | yes            | yes             | yes   |
| Splitter16              | (maybe)        | yes             | yes   |
| Maker16                 | (maybe)        | yes             | yes   |
| Register16              | yes            | yes             | yes   |
| VirtualRegister16       |                |                 |       |
| Counter16               | yes            | yes             | yes   |
| VirtualCounter16        |                |                 |       |
| Constant32              | yes            | yes             | yes   |
| Not32                   | yes            | yes             | yes   |
| Or32                    | yes            | yes             | yes   |
| And32                   | yes            | yes             | yes   |
| Xor32                   | yes            | yes             | yes   |
| Neg32                   | yes            | yes             | yes   |
| Add32                   | yes            | yes             | yes   |
| Mul32                   | yes            | yes             | yes   |
| Equal32                 | yes            | yes             | yes   |
| LessU32                 | yes            | yes             | yes   |
| LessI32                 | yes            | yes             | yes   |
| Shl32                   | yes            | yes             | yes   |
| Shr32                   | yes            | yes             | yes   |
| Mux32                   | yes            | yes             | yes   |
| Switch32                | yes            | yes             | yes   |
| Splitter32              | yes            | yes             | yes   |
| Maker32                 | yes            | yes             | yes   |
| Register32              | yes            | yes             | yes   |
| VirtualRegister32       |                |                 |       |
| Counter32               | yes            | yes             | yes   |
| VirtualCounter32        |                |                 |       |
| Output8zLevel           |                |                 |       |
| Nand8                   | yes            | yes             | yes   |
| Nor8                    | yes            | yes             | yes   |
| Xnor8                   | yes            | yes             | yes   |
| Nand16                  | yes            | yes             | yes   |
| Nor16                   | yes            | yes             | yes   |
| Xnor16                  | yes            | yes             | yes   |
| Nand32                  | yes            | yes             | yes   |
| Nor32                   | yes            | yes             | yes   |
| Xnor32                  | yes            | yes             | yes   |
| Nand64                  | yes            | yes             | yes   |
| Nor64                   | yes            | yes             | yes   |
| Xnor64                  | yes            | yes             | yes   |
| CheapRam                | (later)        | *               |       |
| VirtualCheapRam         |                |                 |       |
| CheapRamLat             | (later)        | *               |       |
| VirtualCheapRamLat      |                |                 |       |
| FastRam                 | (later)        | *               |       |
| VirtualFastRam          |                |                 |       |
| Rom                     | (later)        | *               |       |
| VirtualRom              |                |                 |       |
| SolutionRom             |                |                 |       |
| VirtualSolutionRom      |                |                 |       |
| DelayLine8              | yes            | yes             | yes   |
| VirtualDelayLine8       |                |                 |       |
| DelayLine16             | yes            | yes             | yes   |
| VirtualDelayLine16      |                |                 |       |
| DelayLine32             | yes            | yes             | yes   |
| VirtualDelayLine32      |                |                 |       |
| DelayLine64             | yes            | yes             | yes   |
| VirtualDelayLine64      |                |                 |       |
| DualLoadRam             | (later)        | *1              |       |
| VirtualDualLoadRam      |                |                 |       |
| Hdd                     | (later)        | *1              |       |
| VirtualHdd              |                |                 |       |
