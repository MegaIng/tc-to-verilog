module TC_Mul (in0, in1, out0, out1);
    parameter BIT_WIDTH = 1;
    input [BIT_WIDTH-1:0] in0;
    input [BIT_WIDTH-1:0] in1;
    output [BIT_WIDTH-1:0] out0;
    output [BIT_WIDTH-1:0] out1;

    assign {out1, out0} = in0 * in1;
endmodule

