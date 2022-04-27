module TC_Neg64 (in, out);
    input [63:0] in;
    output [63:0] out;

    assign out = 64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 - in;
endmodule

