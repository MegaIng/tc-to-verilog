module TC_Shl (in, shift, out);
    parameter size = 1;
    input [size-1:0] in;
    input [7:0] shift;
    output [size-1:0] out;

    assign out = in << shift;
endmodule

