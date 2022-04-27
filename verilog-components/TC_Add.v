module TC_Add (in0, in1, ci, out, co);
    parameter size = 1;
    input [size-1:0] in0;
    input [size-1:0] in1;
    input ci;
    output [size-1:0] out;
    output co;

    assign {co, out} = in0 + in1 + ci;
endmodule

