module TC_ByteNot(in, out);
    input [7:0] in;
    output [7:0] out;
    
    assign out = ~in;
endmodule

