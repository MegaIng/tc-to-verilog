module TC_ByteAnd(a, b, out);
    input [7:0] a;
    input [7:0] b;
    output [7:0] out;
    
    assign out = a & b;
endmodule

