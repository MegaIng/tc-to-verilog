module TC_Add8 (in0, in1, ci, out, co);
    input [7:0] in0;
    input [7:0] in1;
    input ci;
    output [7:0] out;
    output co;

    assign {co, out} = in0 + in1 + ci;
endmodule

