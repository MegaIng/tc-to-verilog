module TC_Add32 (in0, in1, ci, out, co);
    input [31:0] in0;
    input [31:0] in1;
    input ci;
    output [31:0] out;
    output co;

    assign {co, out} = in0 + in1 + ci;
endmodule

