module TC_Shl34 (in, shift, out);
    input [31:0] in;
    input [4:0] shift;
    output [31:0] out;

    assign out = in << shift;
endmodule

