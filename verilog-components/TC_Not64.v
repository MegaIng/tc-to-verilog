module TC_Not64(in, out);
    input [63:0] in;
    output [63:0] out;
    
    assign out = ~in;
endmodule

