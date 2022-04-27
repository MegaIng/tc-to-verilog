module TC_Mul64 (in0, in1, out);
    input [63:0] in0;
    input [63:0] in1;
    output [15:0] out;

    assign out = in0 * in1;
endmodule

