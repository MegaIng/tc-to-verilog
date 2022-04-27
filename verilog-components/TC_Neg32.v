module TC_Neg32 (in, out);
    input [31:0] in;
    output [31:0] out;

    assign out = 32'b0000_0000_0000_0000_0000_0000_0000_0000 - in;
endmodule

