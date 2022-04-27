module TC_Not32(in, out);
    input [31:0] in;
    output [31:0] out;
    
    assign out = ~in;
endmodule

