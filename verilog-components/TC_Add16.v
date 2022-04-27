module TC_Add16 (in0, in1, ci, out, co);
    input [15:0] in0;
    input [15:0] in1;
    input ci;
    output [15:0] out;
    output co;

    assign {co, out} = in0 + in1 + ci;
endmodule

