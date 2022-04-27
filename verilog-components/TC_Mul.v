module TC_Mul (in0, in1, out0, out1);
    parameter size = 1;
    input [size-1:0] in0;
    input [size-1:0] in1;
    output [size-1:0] out0;
    output [size-1:0] out1;

    assign {out1, out0} = in0 * in1;
endmodule

