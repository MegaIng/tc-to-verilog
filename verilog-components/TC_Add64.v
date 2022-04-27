module TC_Add64 (in0, in1, ci, out, co);
    input [63:0] in0;
    input [63:0] in1;
    input ci;
    output [63:0] out;
    output co;

    assign {co, out} = in0 + in1 + ci;
endmodule

