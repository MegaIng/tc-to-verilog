module TC_Neg16 (in, out);
    input [15:0] in;
    output [15:0] out;

    assign out = 16'b0000_0000_0000_0000 - in;
endmodule

